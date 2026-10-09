from fastapi import APIRouter, HTTPException
import pandas as pd
import os
from app.schemas.responses import DatasetProfileResponse, ChecksResponse
from app.quality.profiler import profile_dataset
from app.quality.rules import run_all_checks

router = APIRouter()

# For demonstration, we'll assume a single sample dataset is mapped to an ID.
DATASETS_DIR = "data/samples"

def get_dataset_path(dataset_id: str) -> str:
    path = os.path.join(DATASETS_DIR, f"{dataset_id}.csv")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Dataset not found")
    return path

@router.get("/{dataset_id}/profile", response_model=DatasetProfileResponse)
def get_dataset_profile(dataset_id: str):
    path = get_dataset_path(dataset_id)
    df = pd.read_csv(path)
    profile = profile_dataset(df)
    return profile

@router.post("/{dataset_id}/checks", response_model=ChecksResponse)
def run_dataset_checks(dataset_id: str):
    path = get_dataset_path(dataset_id)
    df = pd.read_csv(path)
    findings = run_all_checks(df)
    
    return {
        "summary": f"Executed data quality checks and found {len(findings)} issues.",
        "findings": findings
    }
