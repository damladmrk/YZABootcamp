
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/test")

class TestRequest(BaseModel):
    user_id: str

@router.post("/start")
def start_test(req: TestRequest):
    # Fake test logic
    return {"result": "Test başarıyla tamamlandı. Analiz yapılıyor."}
