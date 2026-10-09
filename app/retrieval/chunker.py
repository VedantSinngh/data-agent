import os
import yaml
from typing import List, Dict, Any
from pydantic import BaseModel

class DocumentChunk(BaseModel):
    chunk_id: str
    text: str
    metadata: Dict[str, Any]

def parse_markdown_with_frontmatter(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                metadata = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError:
                metadata = {}
            body = parts[2].strip()
            return {"metadata": metadata, "body": body}
            
    return {"metadata": {}, "body": content}

def chunk_document(file_path: str) -> List[DocumentChunk]:
    # For a small knowledge base, we'll use document-level or heading-aware chunking.
    # Here, we'll keep it simple and treat the whole doc as one chunk since they are small,
    # or split by headings if needed. Let's return one chunk per file for simplicity.
    
    parsed = parse_markdown_with_frontmatter(file_path)
    metadata = parsed["metadata"]
    body = parsed["body"]
    doc_id = metadata.get("document_id", os.path.basename(file_path))
    
    # Very basic chunking by headers
    sections = body.split("\n## ")
    
    chunks = []
    for i, section in enumerate(sections):
        section_text = section if i == 0 else f"## {section}"
        chunk = DocumentChunk(
            chunk_id=f"{doc_id}_chunk_{i}",
            text=section_text.strip(),
            metadata=metadata
        )
        chunks.append(chunk)
        
    return chunks

def load_all_chunks(kb_dir: str) -> List[DocumentChunk]:
    all_chunks = []
    if not os.path.exists(kb_dir):
        return all_chunks
        
    for filename in os.listdir(kb_dir):
        if filename.endswith(".md"):
            file_path = os.path.join(kb_dir, filename)
            all_chunks.extend(chunk_document(file_path))
            
    return all_chunks
