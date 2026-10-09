from pydantic import BaseModel
from typing import Optional, List

class InvestigationRequest(BaseModel):
    dataset_id: str
    question: str
    
class RemediationPreviewRequest(BaseModel):
    dataset_id: str
    finding_id: str
    proposed_action: str
