"""
Pydantic models for the Psychological Test API
Defines data structures for requests and responses
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class TestCategory(str, Enum):
    """Test categories enum"""
    MOOD = "Mood"
    SLEEP = "Sleep"
    ANXIETY = "Anxiety"
    SOCIAL = "Social"
    CONCENTRATION = "Concentration"
    ENERGY = "Energy"
    STRESS = "Stress"
    RELATIONSHIPS = "Relationships"
    SELF_ESTEEM = "Self-esteem"
    FUTURE = "Future"

class RiskLevel(str, Enum):
    """Risk level enum"""
    LOW = "Düşük Risk"
    LOW_MEDIUM = "Düşük-Orta Risk"
    MEDIUM = "Orta Risk"
    HIGH = "Yüksek Risk"
    VERY_HIGH = "Çok Yüksek Risk"

class TestAnswer(BaseModel):
    """Individual test answer model"""
    question_id: int = Field(..., description="Question ID")
    category: TestCategory = Field(..., description="Question category")
    question: str = Field(..., description="Question text")
    answer: str = Field(..., description="Selected answer text")
    value: int = Field(..., ge=1, le=5, description="Answer value (1-5)")
    
    class Config:
        schema_extra = {
            "example": {
                "question_id": 1,
                "category": "Mood",
                "question": "Son iki hafta içinde kendinizi nasıl hissettiniz?",
                "answer": "Genel olarak iyi",
                "value": 4
            }
        }

class TestResults(BaseModel):
    """Complete test results model"""
    answers: List[TestAnswer] = Field(..., description="List of all answers")
    total_score: int = Field(..., description="Total score")
    max_score: int = Field(..., description="Maximum possible score")
    score_percentage: float = Field(..., ge=0, le=100, description="Score as percentage")
    duration: float = Field(..., description="Test duration in seconds")
    completed_at: datetime = Field(..., description="Test completion timestamp")
    
    @validator('answers')
    def validate_answers_count(cls, v):
        if len(v) < 10:
            raise ValueError('Test must have at least 10 answers')
        return v
    
    @validator('score_percentage')
    def validate_score_percentage(cls, v, values):
        if 'total_score' in values and 'max_score' in values:
            expected_percentage = (values['total_score'] / values['max_score']) * 100
            if abs(v - expected_percentage) > 0.1:
                raise ValueError('Score percentage does not match total score')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "answers": [
                    {
                        "question_id": 1,
                        "category": "Mood",
                        "question": "Son iki hafta içinde kendinizi nasıl hissettiniz?",
                        "answer": "Genel olarak iyi",
                        "value": 4
                    }
                ],
                "total_score": 35,
                "max_score": 50,
                "score_percentage": 70.0,
                "duration": 300.5,
                "completed_at": "2024-01-15T14:30:00"
            }
        }

class CategoryAnalysis(BaseModel):
    """Category-specific analysis model"""
    total_score: int = Field(..., description="Total score for category")
    question_count: int = Field(..., description="Number of questions in category")
    average_score: float = Field(..., description="Average score for category")
    percentage: float = Field(..., ge=0, le=100, description="Category score as percentage")
    interpretation: str = Field(..., description="Category interpretation")
    answers: List[TestAnswer] = Field(..., description="Answers in this category")
    
    class Config:
        schema_extra = {
            "example": {
                "total_score": 8,
                "question_count": 2,
                "average_score": 4.0,
                "percentage": 80.0,
                "interpretation": "Mükemmel",
                "answers": []
            }
        }

class AnalysisResult(BaseModel):
    """Complete analysis result model"""
    analysis_id: str = Field(..., description="Unique analysis ID")
    timestamp: datetime = Field(..., description="Analysis timestamp")
    total_score: int = Field(..., description="Total test score")
    max_score: int = Field(..., description="Maximum possible score")
    score_percentage: float = Field(..., ge=0, le=100, description="Score as percentage")
    ai_analysis: str = Field(..., description="AI-generated analysis text")
    category_analysis: Dict[str, CategoryAnalysis] = Field(..., description="Category-specific analysis")
    recommendations: List[str] = Field(..., description="Personalized recommendations")
    risk_level: RiskLevel = Field(..., description="Assessed risk level")
    professional_help_needed: bool = Field(..., description="Whether professional help is recommended")
    
    class Config:
        schema_extra = {
            "example": {
                "analysis_id": "analysis_20240115_143000",
                "timestamp": "2024-01-15T14:30:00",
                "total_score": 35,
                "max_score": 50,
                "score_percentage": 70.0,
                "ai_analysis": "Test sonuçlarınız genel olarak olumlu...",
                "category_analysis": {},
                "recommendations": ["Düzenli egzersiz yapın", "Kaliteli uyku alın"],
                "risk_level": "Düşük-Orta Risk",
                "professional_help_needed": False
            }
        }

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "error": "Validation Error",
                "detail": "Test answers are required",
                "timestamp": "2024-01-15T14:30:00"
            }
        }

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Health check timestamp")
    version: str = Field(default="1.0.0", description="API version")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-15T14:30:00",
                "version": "1.0.0"
            }
        }

class StatisticsResponse(BaseModel):
    """Statistics response model"""
    total_tests: int = Field(..., description="Total number of tests taken")
    average_score: float = Field(..., description="Average score across all tests")
    most_common_category: str = Field(..., description="Most problematic category")
    completion_rate: float = Field(..., description="Test completion rate")
    
    class Config:
        schema_extra = {
            "example": {
                "total_tests": 1000,
                "average_score": 65.5,
                "most_common_category": "Mood",
                "completion_rate": 89.5
            }
        }

class TestQuestion(BaseModel):
    """Test question model"""
    id: int = Field(..., description="Question ID")
    category: TestCategory = Field(..., description="Question category")
    question: str = Field(..., description="Question text")
    options: List[Dict[str, Any]] = Field(..., description="Answer options")
    
    @validator('options')
    def validate_options(cls, v):
        if len(v) != 5:
            raise ValueError('Each question must have exactly 5 options')
        
        for option in v:
            if 'text' not in option or 'value' not in option:
                raise ValueError('Each option must have text and value')
            if not isinstance(option['value'], int) or option['value'] < 1 or option['value'] > 5:
                raise ValueError('Option values must be integers between 1 and 5')
        
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "category": "Mood",
                "question": "Son iki hafta içinde kendinizi nasıl hissettiniz?",
                "options": [
                    {"text": "Çok iyi ve enerjik", "value": 5},
                    {"text": "Genel olarak iyi", "value": 4},
                    {"text": "Normal/kararsız", "value": 3},
                    {"text": "Biraz kötü", "value": 2},
                    {"text": "Çok kötü ve umutsuz", "value": 1}
                ]
            }
        }

class SaveResultsRequest(BaseModel):
    """Request model for saving test results"""
    test_results: TestResults = Field(..., description="Test results to save")
    user_id: Optional[str] = Field(None, description="Optional user ID")
    anonymous: bool = Field(default=True, description="Whether to save anonymously")
    
    class Config:
        schema_extra = {
            "example": {
                "test_results": {
                    "answers": [],
                    "total_score": 35,
                    "max_score": 50,
                    "score_percentage": 70.0,
                    "duration": 300.5,
                    "completed_at": "2024-01-15T14:30:00"
                },
                "user_id": None,
                "anonymous": True
            }
        }

class SaveResultsResponse(BaseModel):
    """Response model for saving test results"""
    message: str = Field(..., description="Success message")
    result_id: str = Field(..., description="Saved result ID")
    timestamp: datetime = Field(..., description="Save timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Results saved successfully",
                "result_id": "result_20240115_143000",
                "timestamp": "2024-01-15T14:30:00"
            }
        }
