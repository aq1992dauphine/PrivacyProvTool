from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

from privacyprov import OperatorType, WorkflowContext
from privacyprov.examples.common import finalise_privacyprov_run, load_dataset_or_sample, print_artifact_privacy


def sample_compas() -> pd.DataFrame:
    return pd.DataFrame({
        "age": [25, 34, 45, 22, 51, 29],
        "c_charge_degree": ["F", "M", "F", "M", "F", "M"],
        "race": ["African-American", "Caucasian", "Hispanic", "Caucasian", "African-American", "Other"],
        "sex": ["Male", "Female", "Male", "Male", "Female", "Male"],
        "priors_count": [2, 0, 5, 1, 3, 0],
        "days_b_screening_arrest": [-1, 0, 2, None, -3, 1],
        "two_year_recid": [1, 0, 1, 0, 1, 0],
        "c_jail_in": ["2013-01-01", "2013-02-01", "2013-03-05", "2013-04-10", "2013-05-01", "2013-06-15"],
        "c_jail_out": ["2013-01-10", "2013-02-02", "2013-03-20", "2013-04-12", "2013-05-20", "2013-06-17"],
        "irrelevant_col": ["x", "y", "z", "q", "r", "s"],
    })


def run_pipeline(dataset: str | None = None, frac: float = 1.0, out_dir: str | Path = "outputs/compas"):
    config_dir = Path(__file__).resolve().parent
    ctx = WorkflowContext("compas_recidivism_pipeline", purpose="criminal_justice_research", materialize_cells=True)

    df0 = load_dataset_or_sample(dataset, sample_compas)
    if 0 < frac < 1:
        df0 = df0.sample(frac=frac, random_state=42).reset_index(drop=True)
    ctx.register_dataframe("D0_COMPASRaw", df0, role="raw_compas")

    @ctx.step(
        name="B0_select_columns",
        op=OperatorType.RED,
        inputs=["D0_COMPASRaw"],
        outputs=["D1_COMPASSelected"],
        phase="DataPreparation",
        policy_id="B0_select_columns_policy",
    )
    def select_columns(df: pd.DataFrame) -> pd.DataFrame:
        columns = ["age", "c_charge_degree", "race", "sex", "priors_count", "days_b_screening_arrest", "two_year_recid", "c_jail_in", "c_jail_out"]
        return df[columns].copy()

    @ctx.step(
        name="B1_drop_missing",
        op=OperatorType.RED,
        inputs=["D1_COMPASSelected"],
        outputs=["D2_COMPASNoMissing"],
        phase="DataPreparation",
        policy_id="B1_drop_missing_policy",
    )
    def drop_missing(df: pd.DataFrame) -> pd.DataFrame:
        return df.dropna().copy()

    @ctx.step(
        name="B2_binary_race",
        op=OperatorType.TR,
        inputs=["D2_COMPASNoMissing"],
        outputs=["D3_COMPASRaceBinary"],
        phase="FeatureEngineering",
        policy_id="B2_binary_race_policy",
    )
    def binary_race(df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out["race"] = [1 if r == "Caucasian" else 0 for r in out["race"]]
        return out

    @ctx.step(
        name="B3_label_transform",
        op=OperatorType.TR,
        inputs=["D3_COMPASRaceBinary"],
        outputs=["D4_COMPASLabelTransformed"],
        phase="FeatureEngineering",
        policy_id="B3_label_transform_policy",
    )
    def label_transform(df: pd.DataFrame) -> pd.DataFrame:
        out = df.rename({"two_year_recid": "label"}, axis=1)
        out["label"] = [0 if l == 1 else 1 for l in out["label"]]
        return out

    @ctx.step(
        name="B4_create_jailtime",
        op=OperatorType.TR,
        inputs=["D4_COMPASLabelTransformed"],
        outputs=["D5_COMPASJailtime"],
        phase="FeatureEngineering",
        policy_id="B4_create_jailtime_policy",
    )
    def create_jailtime(df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out["jailtime"] = (pd.to_datetime(out["c_jail_out"]) - pd.to_datetime(out["c_jail_in"])).dt.days
        return out

    @ctx.step(
        name="B5_drop_jail_dates",
        op=OperatorType.RED,
        inputs=["D5_COMPASJailtime"],
        outputs=["D6_COMPASNoJailDates"],
        phase="FeatureSelection",
        policy_id="B5_drop_jail_dates_policy",
    )
    def drop_jail_dates(df: pd.DataFrame) -> pd.DataFrame:
        return df.drop(columns=["c_jail_in", "c_jail_out"])

    @ctx.step(
        name="B6_charge_degree_binary",
        op=OperatorType.TR,
        inputs=["D6_COMPASNoJailDates"],
        outputs=["D7_COMPASFinal"],
        phase="FeatureEngineering",
        policy_id="B6_charge_degree_binary_policy",
    )
    def charge_degree_binary(df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out["c_charge_degree"] = [0 if s == "M" else 1 for s in out["c_charge_degree"]]
        out["sex"] = [1 if s == "Male" else 0 for s in out["sex"]]
        return out

    @ctx.step(
        name="B7_split_train_test",
        op=OperatorType.RED,
        inputs=["D7_COMPASFinal"],
        outputs=["D8_COMPASTrainDataset", "D9_COMPASTestDataset"],
        phase="LearningPreparation",
        policy_id="B7_split_train_test_policy",
    )
    def split_train_test(df: pd.DataFrame):
        mid = max(1, int(len(df) * 0.67))
        return df.iloc[:mid].copy(), df.iloc[mid:].copy()

    @ctx.step(
        name="B8_train_classifier",
        op=OperatorType.LEARN,
        inputs=["D8_COMPASTrainDataset"],
        outputs=["M1_COMPASRecidivismClassifier"],
        phase="Learning",
        policy_id="B8_train_classifier_policy",
    )
    def train_classifier(df: pd.DataFrame):
        X = df.drop(columns=["label"]).select_dtypes(include=["number", "bool"]).astype(float)
        y = df["label"].astype(int)
        return DecisionTreeClassifier(random_state=12).fit(X, y)

    @ctx.step(
        name="B9_evaluate_classifier",
        op=OperatorType.EVAL,
        inputs=["M1_COMPASRecidivismClassifier", "D9_COMPASTestDataset"],
        outputs=["E1_COMPASAccuracy"],
        phase="Evaluation",
        policy_id="B9_evaluate_classifier_policy",
    )
    def evaluate_classifier(model, test_df: pd.DataFrame):
        if len(test_df) == 0:
            return 0.0
        X = test_df.drop(columns=["label"]).select_dtypes(include=["number", "bool"]).astype(float)
        y = test_df["label"].astype(int)
        return accuracy_score(y, model.predict(X))

    d1 = select_columns(df0)
    d2 = drop_missing(d1)
    d3 = binary_race(d2)
    d4 = label_transform(d3)
    d5 = create_jailtime(d4)
    d6 = drop_jail_dates(d5)
    d7 = charge_degree_binary(d6)
    d8, d9 = split_train_test(d7)
    m1 = train_classifier(d8)
    _ = evaluate_classifier(m1, d9)

    summary = finalise_privacyprov_run(
        ctx,
        privacy_config_path=config_dir / "compas_privacy_annotations.json",
        operation_policy_path=config_dir / "compas_operation_policies.json",
        out_dir=out_dir,
        prefix="compas",
    )
    print("COMPAS summary:", summary)
    print_artifact_privacy(ctx, ["D7_COMPASFinal", "M1_COMPASRecidivismClassifier", "E1_COMPASAccuracy"])
    return ctx, summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--frac", type=float, default=1.0)
    parser.add_argument("--out-dir", default="outputs/compas")
    args = parser.parse_args()
    run_pipeline(args.dataset, args.frac, args.out_dir)
