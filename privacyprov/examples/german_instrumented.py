from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

from privacyprov import OperatorType, WorkflowContext
from privacyprov.examples.common import finalise_privacyprov_run, load_dataset_or_sample, print_artifact_privacy


GERMAN_COLUMNS = [
    "checking", "duration", "credit_history", "purpose", "amount", "savings", "employment",
    "installment_rate", "personal_status", "other_debtors", "residence_since", "property",
    "age", "other_inst", "housing", "existing_credits", "job", "people_liable",
    "phone", "foreigner", "label",
]


def sample_german() -> pd.DataFrame:
    return pd.DataFrame({
        "checking": ["A11", "A12", "A14", "A13", "A11", "A14"],
        "duration": [6, 48, 12, 42, 24, 36],
        "credit_history": ["A34", "A32", "A34", "A33", "A31", "A32"],
        "purpose": ["A43", "A40", "A42", "A41", "A49", "A46"],
        "amount": [1169, 5951, 2096, 7882, 4870, 9055],
        "savings": ["A65", "A61", "A61", "A61", "A61", "A65"],
        "employment": ["A75", "A73", "A74", "A74", "A73", "A72"],
        "installment_rate": [4, 2, 2, 2, 3, 2],
        "personal_status": ["A93", "A92", "A93", "A93", "A92", "A95"],
        "other_debtors": ["A101", "A101", "A101", "A103", "A101", "A101"],
        "residence_since": [4, 2, 3, 4, 4, 4],
        "property": ["A121", "A121", "A121", "A122", "A124", "A123"],
        "age": [67, 22, 49, 45, 53, 35],
        "other_inst": ["A143", "A143", "A143", "A143", "A143", "A143"],
        "housing": ["A152", "A152", "A152", "A153", "A153", "A153"],
        "existing_credits": [2, 1, 1, 1, 2, 1],
        "job": ["A173", "A173", "A172", "A173", "A173", "A172"],
        "people_liable": [1, 1, 2, 2, 2, 2],
        "phone": ["A192", "A191", "A191", "A191", "A191", "A192"],
        "foreigner": ["A201", "A201", "A201", "A201", "A201", "A202"],
        "label": [1, 2, 1, 1, 2, 1],
    })


def load_german(dataset: str | None) -> pd.DataFrame:
    if dataset and Path(dataset).exists():
        df = pd.read_csv(dataset, sep=r"\s+", header=None)
        if df.shape[1] == len(GERMAN_COLUMNS):
            df.columns = GERMAN_COLUMNS
        return df
    return sample_german()


def run_pipeline(dataset: str | None = None, frac: float = 1.0, out_dir: str | Path = "outputs/german"):
    config_dir = Path(__file__).resolve().parents[1] / "config" / "German"
    ctx = WorkflowContext("german_credit_pipeline", purpose="credit_risk_research", materialize_cells=True)

    df0 = load_german(dataset)
    if 0 < frac < 1:
        df0 = df0.sample(frac=frac, random_state=42).reset_index(drop=True)
    ctx.register_dataframe("D0_GermanRaw", df0, role="raw_german_credit")

    @ctx.step(
        name="A0_value_translation",
        op=OperatorType.TR,
        inputs=["D0_GermanRaw"],
        outputs=["D1_GermanTranslated"],
        phase="DataPreparation",
        policy_id="A0_value_translation_policy",
    )
    def value_translation(df: pd.DataFrame) -> pd.DataFrame:
        return df.replace({
            "checking": {"A11": "check_low", "A12": "check_mid", "A13": "check_high", "A14": "check_none"},
            "credit_history": {"A30": "debt_none", "A31": "debt_noneBank", "A32": "debt_onSchedule", "A33": "debt_delay", "A34": "debt_critical"},
            "purpose": {"A40": "pur_newCar", "A41": "pur_usedCar", "A42": "pur_furniture", "A43": "pur_tv", "A44": "pur_appliance", "A45": "pur_repairs", "A46": "pur_education", "A47": "pur_vacation", "A48": "pur_retraining", "A49": "pur_business", "A410": "pur_other"},
            "savings": {"A61": "sav_small", "A62": "sav_medium", "A63": "sav_large", "A64": "sav_xlarge", "A65": "sav_none"},
            "employment": {"A71": "emp_unemployed", "A72": "emp_lessOne", "A73": "emp_lessFour", "A74": "emp_lessSeven", "A75": "emp_moreSeven"},
            "other_debtors": {"A101": "debtor_none", "A102": "debtor_coApp", "A103": "debtor_guarantor"},
            "property": {"A121": "prop_realEstate", "A122": "prop_agreement", "A123": "prop_car", "A124": "prop_none"},
            "other_inst": {"A141": "oi_bank", "A142": "oi_stores", "A143": "oi_none"},
            "housing": {"A151": "hous_rent", "A152": "hous_own", "A153": "hous_free"},
            "job": {"A171": "job_unskilledNR", "A172": "job_unskilledR", "A173": "job_skilled", "A174": "job_highSkill"},
            "phone": {"A191": 0, "A192": 1},
            "foreigner": {"A201": 1, "A202": 0},
            "label": {2: 0},
        })

    @ctx.step(
        name="A1_derive_status_gender",
        op=OperatorType.TR,
        inputs=["D1_GermanTranslated"],
        outputs=["D2_GermanStatusGender"],
        phase="FeatureEngineering",
        policy_id="A1_derive_status_gender_policy",
    )
    def derive_status_gender(df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out["status"] = np.where(
            out.personal_status.isin(["A91", "A92"]), "divorced",
            np.where(out.personal_status.isin(["A93", "A95"]), "single", "married"),
        )
        out["gender"] = np.where(out.personal_status.isin(["A92", "A95"]), 0, 1)
        return out

    @ctx.step(
        name="A2_drop_personal_status",
        op=OperatorType.RED,
        inputs=["D2_GermanStatusGender"],
        outputs=["D3_GermanNoPersonalStatus"],
        phase="FeatureSelection",
        policy_id="A2_drop_personal_status_policy",
    )
    def drop_personal_status(df: pd.DataFrame) -> pd.DataFrame:
        return df.drop(columns=["personal_status"])

    @ctx.step(
        name="A3_one_hot_encode",
        op=OperatorType.TR,
        inputs=["D3_GermanNoPersonalStatus"],
        outputs=["D4_GermanEncoded"],
        phase="FeatureEngineering",
        policy_id="A3_one_hot_encode_policy",
    )
    def one_hot_encode(df: pd.DataFrame) -> pd.DataFrame:
        cols = ["checking", "credit_history", "purpose", "savings", "employment", "other_debtors", "property", "other_inst", "housing", "job", "status"]
        return pd.get_dummies(df, columns=cols, prefix=cols)

    @ctx.step(
        name="A4_split_train_test",
        op=OperatorType.RED,
        inputs=["D4_GermanEncoded"],
        outputs=["D5_GermanTrainDataset", "D6_GermanTestDataset"],
        phase="LearningPreparation",
        policy_id="A4_split_train_test_policy",
    )
    def split_train_test(df: pd.DataFrame):
        mid = max(1, int(len(df) * 0.67))
        return df.iloc[:mid].copy(), df.iloc[mid:].copy()

    @ctx.step(
        name="A5_train_classifier",
        op=OperatorType.LEARN,
        inputs=["D5_GermanTrainDataset"],
        outputs=["M1_GermanCreditClassifier"],
        phase="Learning",
        policy_id="A5_train_classifier_policy",
    )
    def train_classifier(df: pd.DataFrame):
        X = df.drop(columns=["label"]).select_dtypes(include=["number", "bool"]).astype(float)
        y = df["label"].astype(int)
        return DecisionTreeClassifier(random_state=13).fit(X, y)

    @ctx.step(
        name="A6_evaluate_classifier",
        op=OperatorType.EVAL,
        inputs=["M1_GermanCreditClassifier", "D6_GermanTestDataset"],
        outputs=["E1_GermanAccuracy"],
        phase="Evaluation",
        policy_id="A6_evaluate_classifier_policy",
    )
    def evaluate_classifier(model, test_df: pd.DataFrame):
        if len(test_df) == 0:
            return 0.0
        X = test_df.drop(columns=["label"]).select_dtypes(include=["number", "bool"]).astype(float)
        y = test_df["label"].astype(int)
        return accuracy_score(y, model.predict(X))

    d1 = value_translation(df0)
    d2 = derive_status_gender(d1)
    d3 = drop_personal_status(d2)
    d4 = one_hot_encode(d3)
    d5, d6 = split_train_test(d4)
    m1 = train_classifier(d5)
    _ = evaluate_classifier(m1, d6)

    summary = finalise_privacyprov_run(
        ctx,
        privacy_config_path=config_dir / "german_privacy_annotations.json",
        operation_policy_path=config_dir / "german_operation_policies.json",
        out_dir=out_dir,
        prefix="german",
    )
    print("German Credit summary:", summary)
    print_artifact_privacy(ctx, ["D4_GermanEncoded", "M1_GermanCreditClassifier", "E1_GermanAccuracy"])
    return ctx, summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--frac", type=float, default=1.0)
    parser.add_argument("--out-dir", default="outputs/german")
    args = parser.parse_args()
    run_pipeline(args.dataset, args.frac, args.out_dir)
