import pandas as pd
from app.schemas.responses import InvestigationReport
from app.llm.provider import LLMProvider
from app.llm.prompts import build_investigation_prompt
from app.agent.tools import AgentTools

class AgentOrchestrator:
    def __init__(self, tools: AgentTools, llm: LLMProvider):
        self.tools = tools
        self.llm = llm
        
    def investigate(self, df: pd.DataFrame, question: str) -> InvestigationReport:
        # Step 1: Run quality checks
        findings = self.tools.run_quality_checks_tool(df)
        
        # Step 2: Retrieve relevant quality rules based on the question
        rules = self.tools.retrieve_quality_rules_tool(question)
        
        # Step 3: Build the prompt
        prompt = build_investigation_prompt(question, findings, rules)
        
        # Step 4: Call the LLM
        report = self.llm.generate_structured_response(prompt)
        
        # Step 5: (Optional) Validate that report evidence_ids exist in retrieved rules
        # In a full implementation, we'd enforce this explicitly.
        return report
