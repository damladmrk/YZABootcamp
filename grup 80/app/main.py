from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.endpoints import router as api_router
from app.core.model_loader import model_loader
from app.utils.logger import setup_logger
from fastapi.responses import FileResponse

# Logger ayarları
logger = setup_logger(__name__, settings.LOG_LEVEL)

# FastAPI uygulamasını oluştur
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

# API router'ını ekle
app.include_router(api_router)

# Statik dosyaları sun
app.mount("/static", StaticFiles(directory="static"), name="static")

# Uygulama başlangıcında modeli yükle
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Uygulama başlatılıyor...")
    model_loader.load_model()
    logger.info("✅ Başlangıç işlemleri tamamlandı")

# HTML sayfalarını sun
@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

@app.get("/test.html")
async def serve_test():
    return FileResponse("static/test.html")

@app.get("/results.html")
async def serve_results():
    return FileResponse("static/results.html")

@app.get("/developers.html")
async def serve_developers():
    return FileResponse("static/developers.html")

@app.get("/how-it-works.html")
async def serve_how_it_works():
    return FileResponse("static/how-it-works.html")

# Sağlık kontrolü endpoint'i
@app.get("/health")
async def health_check():
    return {"status": "ok", "model_loaded": model_loader.loaded}