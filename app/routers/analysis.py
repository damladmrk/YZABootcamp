
from fastapi import APIRouter
from app.services.llm_service import analyze_text

router = APIRouter(prefix="/analysis")

@router.get("/run")
def run_analysis(text: str):
    return {"analysis": analyze_text(text)}
