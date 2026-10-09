from pydantic import BaseModel
from typing import Literal, List, Dict, Any

class DataQualityFinding(BaseModel):
    finding_id: str
    rule_id: str
    column: str
    issue_type: str
    severity: Literal["low", "medium", "high", "critical"]
    affected_rows: int
    evidence: Dict[str, Any]
    recommended_action: str
    auto_fix_allowed: bool

class DatasetProfileResponse(BaseModel):
    num_rows: int
    num_columns: int
    columns: Dict[str, Any]

class ChecksResponse(BaseModel):
    summary: str
    findings: List[DataQualityFinding]

class InvestigationReportFinding(BaseModel):
    finding_id: str
    severity: Literal["low", "medium", "high", "critical"]
    explanation: str
    business_impact: str
    recommended_action: str
    evidence_ids: List[str]
    requires_human_review: bool

class InvestigationReport(BaseModel):
    summary: str
    findings: List[InvestigationReportFinding]
    limitations: List[str]
    abstained: bool
