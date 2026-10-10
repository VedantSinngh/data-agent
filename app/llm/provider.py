import os
import json
from groq import Groq
from pydantic import BaseModel
from typing import List, Literal
from app.schemas.responses import InvestigationReport, InvestigationReportFinding

class LLMProvider:
    """Interface for LLM inference using Groq Cloud."""
    
    def __init__(self):
        # Initialize Groq client. It will automatically look for the GROQ_API_KEY environment variable.
        self.client = Groq()
        # Llama 3 8B or 70B are great for this on Groq
        self.model = "llama-3.1-8b-instant" 
        
    def generate_structured_response(self, prompt: str) -> InvestigationReport:
        """
        Calls Groq API to generate a structured Data Quality Investigation Report.
        """
        
        # We inject the JSON schema requirements into the system prompt to guarantee the output structure
        system_instruction = (
            "You are a strict JSON data-quality AI. You must respond ONLY with valid JSON matching this structure: \n"
            "{\n"
            '  "summary": "string",\n'
            '  "findings": [\n'
            '    {\n'
            '      "finding_id": "string",\n'
            '      "severity": "low|medium|high|critical",\n'
            '      "explanation": "string",\n'
            '      "business_impact": "string",\n'
            '      "recommended_action": "string",\n'
            '      "evidence_ids": ["string"],\n'
            '      "requires_human_review": boolean\n'
            '    }\n'
            '  ],\n'
            '  "limitations": ["string"],\n'
            '  "abstained": boolean\n'
            "}\n"
            "Do not include markdown blocks, do not include explanations outside the JSON."
        )

        try:
            print(f"[LLMProvider] Sending prompt to Groq ({self.model})...")
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_instruction,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                response_format={"type": "json_object"},
                temperature=0.1, # Keep it deterministic
            )
            
            # Parse the JSON response
            response_content = chat_completion.choices[0].message.content
            data = json.loads(response_content)
            
            # Validate and return using Pydantic
            return InvestigationReport(**data)
            
        except Exception as e:
            print(f"[LLMProvider] Groq API Error: {e}")
            # Fallback to a safe error report if the API fails or hallucinates non-JSON
            return InvestigationReport(
                summary=f"Error communicating with Groq LLM: {str(e)}",
                findings=[],
                limitations=["LLM Generation Failed"],
                abstained=True
            )
