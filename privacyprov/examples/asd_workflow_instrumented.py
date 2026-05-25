from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

from privacyprov import (
    WorkflowContext,
    OperatorType,
    PrivacyConfigLoader,
    InitialPrivacyAnnotator,
    OperationPolicyConfigLoader,
    OperationPolicyMaterializer,
    PrivacyPropagationEngine,
)


def main() -> None:
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)

    ctx = WorkflowContext(
        pipeline_name="ASD_privacy_walkthrough",
        run_id="asd_run_001",
        purpose="clinical_research",
        materialize_records=True,
        materialize_cells=True,
    )

    # Input artifact for this implementation phase. In the full pipeline, this
    # is the output of the previous fusion/context-enrichment operation.
    raw = pd.DataFrame({
        "Id": ["C001", "C001", "C002", "C002"],
        "window_start": ["09:00:00", "09:00:30", "09:00:00", "09:00:30"],
        "HR_res": [119.6, 124.0, 86.0, 87.0],
        "EDA_res": [3.8, 4.1, 1.3, 1.4],
        "ACC_res": [0.52, 0.70, 0.34, 0.36],
        "chall_behav": ["yes", "no", "no", "yes"],
        "sev": [4, 0, 0, 3],
        "age_grp": ["6-8", "6-8", "9-11", "9-11"],
        "sex": ["M", "M", "F", "F"],
        "clinic_site": ["SiteA", "SiteA", "SiteB", "SiteB"],
        "diag": ["ASD", "ASD", "ASD", "ASD"],
    })
    ctx.register_dataframe("D6_EnrichedEpisodeData", raw, role="enriched", record_id_col=None)

    @ctx.step(
        name="S5_normalise",
        op=OperatorType.TR,
        inputs=["D6_EnrichedEpisodeData"],
        outputs=["D7_NormalizedEpisodeData"],
        phase="LearningPreparation",
        policy_id="S5_normalise_policy",
        output_roles={"D7_NormalizedEpisodeData": "normalised"},
    )
    def normalise(df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        for src, dst in [("HR_res", "HR_norm"), ("EDA_res", "EDA_norm"), ("ACC_res", "ACC_norm")]:
            min_v = out[src].min()
            max_v = out[src].max()
            out[dst] = (out[src] - min_v) / (max_v - min_v)
        return out[[
            "Id", "window_start", "HR_norm", "EDA_norm", "ACC_norm",
            "chall_behav", "sev", "age_grp", "sex", "clinic_site", "diag"
        ]]

    @ctx.step(
        name="S6_select_modelling_features",
        op=OperatorType.RED,
        inputs=["D7_NormalizedEpisodeData"],
        outputs=["D8_ModellingDataset"],
        phase="LearningPreparation",
        policy_id="S6_select_modelling_features_policy",
        output_roles={"D8_ModellingDataset": "modelling"},
    )
    def select_features(df: pd.DataFrame) -> pd.DataFrame:
        return df[["HR_norm", "EDA_norm", "ACC_norm", "chall_behav", "sev", "age_grp", "sex"]].copy()

    @ctx.step(
        name="S7_split_train_test",
        op=OperatorType.RED,
        inputs=["D8_ModellingDataset"],
        outputs=["D9_TrainDataset", "D10_TestDataset"],
        phase="LearningPreparation",
        policy_id="S7_split_train_test_policy",
        output_roles={"D9_TrainDataset": "train", "D10_TestDataset": "test"},
    )
    def split_train_test(df: pd.DataFrame):
        # Subject-aware toy split: first two records train, last two records test.
        return df.iloc[:2].copy(), df.iloc[2:].copy()

    @ctx.step(
        name="S8_train_classifier",
        op=OperatorType.LEARN,
        inputs=["D9_TrainDataset"],
        outputs=["M1_ChallengingBehaviourClassifier"],
        phase="Learning",
        policy_id="S8_train_classifier_policy",
    )
    def train_classifier(df: pd.DataFrame):
        X = pd.get_dummies(df[["HR_norm", "EDA_norm", "ACC_norm", "age_grp", "sex"]])
        y = (df["chall_behav"] == "yes").astype(int)
        model = DecisionTreeClassifier(random_state=7)
        return model.fit(X, y)

    d7 = normalise(raw)
    d8 = select_features(d7)
    train_df, test_df = split_train_test(d8)
    model = train_classifier(train_df)

    # Register a metric explicitly to show how evaluation can be added later.
    X_test = pd.get_dummies(test_df[["HR_norm", "EDA_norm", "ACC_norm", "age_grp", "sex"]])
    X_train_cols = pd.get_dummies(train_df[["HR_norm", "EDA_norm", "ACC_norm", "age_grp", "sex"]]).columns
    X_test = X_test.reindex(columns=X_train_cols, fill_value=0)
    y_test = (test_df["chall_behav"] == "yes").astype(int)
    acc = accuracy_score(y_test, model.predict(X_test))
    ctx.register_metric("E1_accuracy", "accuracy", acc, split="test")

    # Component 2: load and materialise the initial privacy ontology + manual annotations.
    config_dir = Path(__file__).resolve().parents[1] / "config"
    config_path = config_dir / "asd_privacy_annotations.json"
    privacy_config = PrivacyConfigLoader.load(config_path)
    annotation_summary = InitialPrivacyAnnotator(ctx.graph, privacy_config).apply()

    # Component 3: load and materialise operation policies. These policies
    # describe how each Step should propagate, rewrite, mint, or remove privacy
    # annotations. The next component will consume them during propagation.
    policy_path = config_dir / "asd_operation_policies.json"
    operation_policy_config = OperationPolicyConfigLoader.load(policy_path)
    policy_summary = OperationPolicyMaterializer(ctx.graph, operation_policy_config).apply()

    # Component 4: run operator-aware privacy propagation. This consumes the
    # seeded privacy annotations, the operation policy dictionary, and the
    # retrospective provenance graph to infer annotations for derived artifacts.
    propagation_engine = PrivacyPropagationEngine(ctx.graph, privacy_config, operation_policy_config)
    propagation_summary = propagation_engine.apply()

    propagated_artifacts = [
        "D7_NormalizedEpisodeData",
        "D8_ModellingDataset",
        "D9_TrainDataset",
        "D10_TestDataset",
        "M1_ChallengingBehaviourClassifier",
    ]
    privacy_report = propagation_engine.artifact_privacy_summary(propagated_artifacts)

    import json
    with (out_dir / "asd_propagation_summary.json").open("w", encoding="utf-8") as f:
        json.dump({
            "propagation_summary": propagation_summary,
            "artifact_privacy_summary": privacy_report,
        }, f, indent=2, ensure_ascii=False)

    ctx.export_json(out_dir / "asd_propagated_graph.json")
    ctx.export_neo4j_csv(out_dir / "asd_propagated_nodes.csv", out_dir / "asd_propagated_relationships.csv")
    print("Provenance summary:", ctx.summary())
    print("Privacy seed summary:", annotation_summary)
    print("Operation policy summary:", policy_summary)
    print("Propagation summary:", propagation_summary)
    print("Propagated artifact privacy summary:", privacy_report)


if __name__ == "__main__":
    main()
