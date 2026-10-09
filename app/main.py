from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import datasets
from app.api import investigations
from app.api import remediation

app = FastAPI(
    title="DataTrust Agent API",
    description="An AI-powered data-quality investigation and remediation assistant",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(datasets.router, prefix="/api/datasets", tags=["datasets"])
app.include_router(investigations.router, prefix="/api", tags=["investigations"])
app.include_router(remediation.router, prefix="/api", tags=["remediation"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}
