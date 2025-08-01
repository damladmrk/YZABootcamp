import os
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel
from typing import List
import numpy as np

from app.config import settings
from app.core.model_loader import model_loader
from app.utils.logger import setup_logger

# Logger kurulumu
logger = setup_logger(__name__, settings.LOG_LEVEL)

# Kök ve statik dizin tanımları
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

# FastAPI uygulaması
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI destekli psikolojik test platformu",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Statik dosyaları mount et
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Model yükleme
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Uygulama başlatılıyor...")
    try:
        model_loader.load_model()
        if model_loader.loaded:
            logger.info("✅ Model başarıyla yüklendi")
        else:
            logger.warning("⚠️ Model yüklenemedi, bazı özellikler çalışmayabilir")
    except Exception as e:
        logger.error(f"❌ Model yükleme hatası: {str(e)}")
        logger.warning("⚠️ Model yüklenemedi, bazı özellikler çalışmayabilir")
    logger.info("✅ Başlangıç işlemleri tamamlandı")

# API ANALIZ ENDPOINT
class TestData(BaseModel):
    answers: List[float]

@app.post("/api/analyze-test")
async def analyze_test(data: TestData):
    if not model_loader.loaded:
        raise HTTPException(status_code=503, detail="Model yüklenemedi")

    try:
        test_array = np.array(data.answers).reshape(1, -1)
        score = model_loader.model.predict(test_array)[0]

        # Yorum
        if score >= 80:
            interpretation = "Ruh sağlığınız çok iyi durumda."
        elif score >= 60:
            interpretation = "Ruh sağlığınız iyi durumda."
        elif score >= 40:
            interpretation = "Orta düzeyde stres olabilir."
        else:
            interpretation = "Yüksek stres belirtileri var."

        return {
            "score": int(score),
            "interpretation": interpretation,
            "analysis": "AI modeline göre ruhsal sağlığınız değerlendirilmiştir.",
            "recommendations": [
                "Düzenli egzersiz yapın.",
                "Uykunuza dikkat edin.",
                "Sosyal bağlar kurun.",
                "Gerekirse bir uzmana danışın."
            ]
        }

    except Exception as e:
        logger.error(f"Analiz hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analiz sırasında hata oluştu: {str(e)}")

# HTML SAYFALARI SUNUMU
@app.get("/")
async def serve_index():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/test.html")
async def serve_test():
    return FileResponse(STATIC_DIR / "test.html")

@app.get("/results.html")
async def serve_results():
    return FileResponse(STATIC_DIR / "results.html")

@app.get("/developers.html")
async def serve_developers():
    return FileResponse(STATIC_DIR / "developers.html")

@app.get("/how-it-works.html")
async def serve_how_it_works():
    return FileResponse(STATIC_DIR / "how-it-works.html")

# SAĞLIK KONTROLÜ
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "model_loaded": model_loader.loaded,
        "version": settings.VERSION
    }
