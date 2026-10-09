from fastapi import APIRouter, HTTPException
import pandas as pd
import os
from typing import Dict, Any
from app.schemas.requests import RemediationPreviewRequest

router = APIRouter()
DATASETS_DIR = "data/samples"

def get_dataset_path(dataset_id: str) -> str:
    path = os.path.join(DATASETS_DIR, f"{dataset_id}.csv")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Dataset not found")
    return path

@router.post("/datasets/{dataset_id}/remediation/preview")
def preview_remediation(dataset_id: str, request: RemediationPreviewRequest) -> Dict[str, Any]:
    """
    Preview the effect of a proposed transformation. 
    Does not modify the original data.
    """
    path = get_dataset_path(dataset_id)
    df = pd.read_csv(path)
    initial_rows = len(df)
    
    # Mocking remediation logic based on finding_id
    # In reality, the LLM maps proposed_action to explicit dataframe operations.
    if "DUPLICATE" in request.finding_id.upper():
        # Action: Remove exact duplicates
        df_clean = df.drop_duplicates()
        action_taken = "Removed exact duplicate rows."
    elif "MISSING" in request.finding_id.upper():
        # Action: Drop rows with missing critical fields (for demo purposes)
        df_clean = df.dropna()
        action_taken = "Removed rows with missing values."
    else:
        df_clean = df
        action_taken = "No safe automatic remediation supported for this finding."
        
    final_rows = len(df_clean)
    
    return {
        "dataset_id": dataset_id,
        "finding_id": request.finding_id,
        "action_simulated": action_taken,
        "metrics_before": {"num_rows": initial_rows},
        "metrics_after": {"num_rows": final_rows},
        "rows_affected": initial_rows - final_rows,
        "safe_to_apply": True if initial_rows != final_rows else False
    }
