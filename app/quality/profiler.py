import pandas as pd
from typing import Dict, Any

def profile_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate schema and column statistics."""
    profile = {
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "columns": {}
    }
    
    for col in df.columns:
        col_type = str(df[col].dtype)
        num_missing = int(df[col].isna().sum())
        missing_percentage = (num_missing / len(df)) * 100
        num_unique = int(df[col].nunique())
        
        col_stats = {
            "type": col_type,
            "missing_count": num_missing,
            "missing_percentage": missing_percentage,
            "unique_count": num_unique
        }
        
        if pd.api.types.is_numeric_dtype(df[col]):
            col_stats["min"] = float(df[col].min()) if not pd.isna(df[col].min()) else None
            col_stats["max"] = float(df[col].max()) if not pd.isna(df[col].max()) else None
            col_stats["mean"] = float(df[col].mean()) if not pd.isna(df[col].mean()) else None
            
        profile["columns"][col] = col_stats
        
    return profile
