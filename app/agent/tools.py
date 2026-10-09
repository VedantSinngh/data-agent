import pandas as pd
from typing import List, Dict, Any
from app.quality.profiler import profile_dataset
from app.quality.rules import run_all_checks
from app.retrieval.hybrid_search import HybridRetriever

class AgentTools:
    def __init__(self, retriever: HybridRetriever):
        self.retriever = retriever

    def run_quality_checks_tool(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        return run_all_checks(df)
        
    def retrieve_quality_rules_tool(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        return self.retriever.search(query, k=k)
        
    def profile_dataset_tool(self, df: pd.DataFrame) -> Dict[str, Any]:
        return profile_dataset(df)
