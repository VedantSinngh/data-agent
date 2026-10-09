from fastapi import APIRouter, HTTPException
import pandas as pd
import os
from app.schemas.requests import InvestigationRequest
from app.schemas.responses import InvestigationReport
from app.agent.tools import AgentTools
from app.llm.provider import LLMProvider
from app.agent.orchestrator import AgentOrchestrator
from app.retrieval.hybrid_search import HybridRetriever
from app.retrieval.chunker import load_all_chunks

router = APIRouter()

# Global initialization (In a real app, use Dependency Injection or Lifespan handlers)
DATASETS_DIR = "data/samples"
KB_DIR = "data/knowledge_base"

# Initialize RAG
retriever = HybridRetriever()
chunks = load_all_chunks(KB_DIR)
if chunks:
    retriever.index_documents(chunks)

# Initialize Agent
tools = AgentTools(retriever)
llm = LLMProvider()
orchestrator = AgentOrchestrator(tools, llm)

def get_dataset_path(dataset_id: str) -> str:
    path = os.path.join(DATASETS_DIR, f"{dataset_id}.csv")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Dataset not found")
    return path

@router.post("/datasets/{dataset_id}/investigate", response_model=InvestigationReport)
def investigate_dataset(dataset_id: str, request: InvestigationRequest):
    path = get_dataset_path(dataset_id)
    df = pd.read_csv(path)
    
    report = orchestrator.investigate(df, request.question)
    return report
