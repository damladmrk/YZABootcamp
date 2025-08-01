from fastapi import APIRouter, HTTPException
import numpy as np
from datetime import datetime
from app.core.model_loader import model_loader
from app.core.preprocessor import preprocessor
from app.services.gemini_service import gemini_service
from app.schemas.analysis import AnalysisResult, HealthResponse
from app.schemas.test import TestSubmission
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__, settings.LOG_LEVEL)

router = APIRouter(prefix=settings.API_PREFIX)

def get_risk_level(prediction: str, suicidal: int) -> str:
    """Risk seviyesini belirler"""
    if suicidal == 1:
        return "Çok Yüksek Risk"
    
    risk_map = {
        "Normal": "Düşük Risk",
        "Depression": "Orta Risk",
        "Bipolar Type-1": "Yüksek Risk",
        "Bipolar Type-2": "Orta-Yüksek Risk"
    }
    return risk_map.get(prediction, "Orta Risk")

@router.post("/analyze-test", response_model=AnalysisResult)
async def analyze_test(test_data: TestSubmission):
    """Test sonuçlarını analiz eder"""
    try:
        logger.info(f"📥 Analiz isteği alındı: {len(test_data.answers)} cevap")
        
        # Frontend verisini dönüştür
        frontend_data = {answer.category: answer.answer for answer in test_data.answers}
        
        # Tanı ve faktörler için varsayılan değerler
        diagnosis = "Normal"
        confidence = 0.0
        important_factors = {}
        risk_level = "Düşük Risk"
        professional_help = False
        
        # Model yüklüyse tahmin yap
        if model_loader.loaded:
            # Veriyi ön işle
            processed_data = preprocessor.preprocess(frontend_data)
            
            # Tahmin yap
            diagnosis = model_loader.model.predict(processed_data)[0]
            proba = model_loader.model.predict_proba(processed_data)[0]
            confidence = np.max(proba)
            
            # SHAP analizi
            shap_values = model_loader.explainer.shap_values(processed_data)
            important_factors = {
                col: float(abs(val)) 
                for col, val in zip(processed_data.columns, shap_values[0])
            }
            
            # Risk değerlendirmesi
            suicidal = 1 if frontend_data.get("Suicidal_thoughts") == "YES" else 0
            risk_level = get_risk_level(diagnosis, suicidal)
            professional_help = risk_level in ["Yüksek Risk", "Çok Yüksek Risk"]
        
        # Gemini ile analiz oluştur
        llm_response = gemini_service.generate_analysis(
            prediction=diagnosis,
            confidence=confidence,
            risk_level=risk_level,
            factors=important_factors
        )
        
        # Yanıtı hazırla
        return {
            "analysis_id": f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now(),
            "total_score": test_data.totalScore,
            "max_score": test_data.maxScore,
            "score_percentage": test_data.scorePercentage,
            "ai_analysis": llm_response.get("analysis", ""),
            "category_analysis": {},  # Frontend uyumluluğu için
            "recommendations": llm_response.get("recommendations", []),
            "risk_level": risk_level,
            "professional_help_needed": professional_help,
            "diagnosis": diagnosis,
            "confidence": confidence
        }
        
    except Exception as e:
        logger.error(f"🔴 Analiz hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Sistem sağlık durumunu kontrol eder"""
    return {
        "status": "healthy",
        "model_loaded": model_loader.loaded,
        "gemini_available": gemini_service.model is not None,
        "timestamp": datetime.now()
    }