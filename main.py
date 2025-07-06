
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import test, analysis

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(test.router)
app.include_router(analysis.router)
