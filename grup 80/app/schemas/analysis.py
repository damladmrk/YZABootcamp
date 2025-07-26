from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List

class AnalysisResult(BaseModel):
    analysis_id: str
    timestamp: datetime
    total_score: int
    max_score: int
    score_percentage: float
    ai_analysis: str
    category_analysis: Dict[str, Dict]
    recommendations: List[str]
    risk_level: str
    professional_help_needed: bool
    diagnosis: str
    confidence: float

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    gemini_available: bool
    timestamp: datetime