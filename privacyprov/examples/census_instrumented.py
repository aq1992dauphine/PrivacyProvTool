from __future__ import annotations

import argparse
from pathlib import Path
import sys

# Allow running this file directly as: python privacyprov/examples/census_instrumented.py
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

from privacyprov import OperatorType, WorkflowContext
from privacyprov.examples.common import finalise_privacyprov_run, load_dataset_or_sample, print_artifact_privacy


CENSUS_NAMES = [
    "age", "workclass", "fnlwgt", "education", "education-num", "marital-status",
    "occupation", "relationship", "race", "sex", "capital-gain", "capital-loss",
    "hours-per-week", "native-country", "label",
]


def sample_census() -> pd.DataFrame:
    return pd.DataFrame([
        [39, " State-gov ", 77516, " Bachelors ", 13, " Never-married ", " Adm-clerical ", " Not-in-family ", " White ", " Male ", 2174, 0, 40, " United-States ", "<=50K"],
        [50, " Self-emp-not-inc ", 83311, " Bachelors ", 13, " Married-civ-spouse ", " Exec-managerial ", " Husband ", " White ", " Male ", 0, 0, 13, " United-States ", "<=50K"],
        [38, " Private ", 215646, " HS-grad ", 9, " Divorced ", " Handlers-cleaners ", " Not-in-family ", " White ", " Male ", 0, 0, 40, " United-States ", "<=50K"],
        [53, " Private ", 234721, " 11th ", 7, " Married-civ-spouse ", " Handlers-cleaners ", " Husband ", " Black ", " Male ", 0, 0, 40, " United-States ", "<=50K"],
        [28, " Private ", 338409, " Bachelors ", 13, " Married-civ-spouse ", " Prof-specialty ", " Wife ", " Black ", " Female ", 0, 0, 40, " Cuba ", ">50K"],
        [37, " Private ", 284582, " Masters ", 14, " Married-civ-spouse ", " Exec-managerial ", " Wife ", " White ", " Female ", 0, 0, 40, " United-States ", ">50K"],
    ], columns=CENSUS_NAMES)


def load_census(dataset: str | None, frac: float) -> pd.DataFrame:
    if dataset and Path(dataset).exists():
        df = pd.read_csv(dataset, header=None)
        if df.shape[1] == len(CENSUS_NAMES):
            df.columns = CENSUS_NAMES
    else:
        df = sample_census()
    if 0 < frac < 1:
        df = df.sample(frac=frac, random_state=42)
    return df.reset_index(drop=True)


def run_pipeline(dataset: str | None = None, frac: float = 1.0, out_dir: str | Path = "outputs/census"):
    config_dir = Path(__file__).resolve().parents[1] / "config" / "Census"
    ctx = WorkflowContext("census_income_pipeline", purpose="income_model_development", materialize_cells=True)

    d0 = load_census(dataset, frac)
    ctx.register_dataframe("D0_CensusRaw", d0, role="raw_census")

    @ctx.step(
        name="C0_strip_whitespace",
        op=OperatorType.TR,
        inputs=["D0_CensusRaw"],
        outputs=["D1_CensusStripped"],
        phase="DataPreparation",
        policy_id="C0_strip_whitespace_policy",
    )
    def strip_whitespace(df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        cols = ["workclass", "education", "marital-status", "occupation", "relationship", "race", "sex", "native-country", "label"]
        for c in cols:
            out[c] = out[c].astype(str).str.strip()
        return out

    @ctx.step(
        name="C1_replace_missing",
        op=OperatorType.TR,
        inputs=["D1_CensusStripped"],
        outputs=["D2_CensusMissingReplaced"],
        phase="DataPreparation",
        policy_id="C1_replace_missing_policy",
    )
    def replace_missing(df: pd.DataFrame) -> pd.DataFrame:
        return df.replace("?", pd.NA)

    @ctx.step(
        name="C2_one_hot_encode",
        op=OperatorType.TR,
        inputs=["D2_CensusMissingReplaced"],
        outputs=["D3_CensusEncoded"],
        phase="FeatureEngineering",
        policy_id="C2_one_hot_encode_policy",
    )
    def one_hot_encode(df: pd.DataFrame) -> pd.DataFrame:
        cols = ["workclass", "education", "marital-status", "occupation", "relationship", "race", "native-country"]
        return pd.get_dummies(df, columns=cols, prefix=cols)

    @ctx.step(
        name="C3_binary_transform",
        op=OperatorType.TR,
        inputs=["D3_CensusEncoded"],
        outputs=["D4_CensusBinary"],
        phase="FeatureEngineering",
        policy_id="C3_binary_transform_policy",
    )
    def binary_transform(df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out["sex"] = out["sex"].replace({"Male": 1, "Female": 0}).astype(int)
        out["label"] = out["label"].replace({"<=50K": 0, ">50K": 1}).astype(int)
        return out

    @ctx.step(
        name="C4_drop_weight",
        op=OperatorType.RED,
        inputs=["D4_CensusBinary"],
        outputs=["D5_CensusModellingDataset"],
        phase="FeatureSelection",
        policy_id="C4_drop_weight_policy",
    )
    def drop_weight(df: pd.DataFrame) -> pd.DataFrame:
        return df.drop(columns=["fnlwgt"])

    @ctx.step(
        name="C5_split_train_test",
        op=OperatorType.RED,
        inputs=["D5_CensusModellingDataset"],
        outputs=["D6_CensusTrainDataset", "D7_CensusTestDataset"],
        phase="LearningPreparation",
        policy_id="C5_split_train_test_policy",
    )
    def split_train_test(df: pd.DataFrame):
        mid = max(1, int(len(df) * 0.67))
        return df.iloc[:mid].copy(), df.iloc[mid:].copy()

    @ctx.step(
        name="C6_train_classifier",
        op=OperatorType.LEARN,
        inputs=["D6_CensusTrainDataset"],
        outputs=["M1_CensusIncomeClassifier"],
        phase="Learning",
        policy_id="C6_train_classifier_policy",
    )
    def train_classifier(df: pd.DataFrame):
        X = df.drop(columns=["label"]).select_dtypes(include=["number", "bool"]).astype(float)
        y = df["label"].astype(int)
        return DecisionTreeClassifier(random_state=11).fit(X, y)

    @ctx.step(
        name="C7_evaluate_classifier",
        op=OperatorType.EVAL,
        inputs=["M1_CensusIncomeClassifier", "D7_CensusTestDataset"],
        outputs=["E1_CensusAccuracy"],
        phase="Evaluation",
        policy_id="C7_evaluate_classifier_policy",
    )
    def evaluate_classifier(model, test_df: pd.DataFrame):
        if len(test_df) == 0:
            return 0.0
        X = test_df.drop(columns=["label"]).select_dtypes(include=["number", "bool"]).astype(float)
        y = test_df["label"].astype(int)
        return accuracy_score(y, model.predict(X))

    d1 = strip_whitespace(d0)
    d2 = replace_missing(d1)
    d3 = one_hot_encode(d2)
    d4 = binary_transform(d3)
    d5 = drop_weight(d4)
    d6, d7 = split_train_test(d5)
    m1 = train_classifier(d6)
    _ = evaluate_classifier(m1, d7)

    summary = finalise_privacyprov_run(
        ctx,
        privacy_config_path=config_dir / "census_privacy_annotations.json",
        operation_policy_path=config_dir / "census_operation_policies.json",
        out_dir=out_dir,
        prefix="census",
    )
    print("Census summary:", summary)
    print_artifact_privacy(ctx, ["D5_CensusModellingDataset", "M1_CensusIncomeClassifier", "E1_CensusAccuracy"])
    return ctx, summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--frac", type=float, default=1.0)
    parser.add_argument("--out-dir", default="outputs/census")
    args = parser.parse_args()
    run_pipeline(args.dataset, args.frac, args.out_dir)
