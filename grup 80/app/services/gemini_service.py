import google.generativeai as genai
import json
import logging
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__, settings.LOG_LEVEL)

class GeminiService:
    def __init__(self):
        self.client = None
        self.model = None
        self.initialize()
    
    def initialize(self):
        try:
            if not settings.GEMINI_API_KEY:
                logger.warning("❌ GEMINI_API_KEY ayarlanmamış, Gemini servisi devre dışı")
                return
            
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMINI_MODEL_NAME)
            logger.info("✅ Gemini servisi başlatıldı")
        except Exception as e:
            logger.error(f"❌ Gemini başlatma hatası: {str(e)}")
    
    def generate_analysis(self, prediction: str, confidence: float, 
                        risk_level: str, factors: dict) -> dict:
        """Gemini API ile analiz oluşturur"""
        try:
            if not self.model:
                return self.get_fallback_analysis(prediction)
            
            # En önemli 3 faktörü al
            top_factors = sorted(factors.items(), key=lambda x: x[1], reverse=True)[:3]
            factors_str = "\n".join([f"- {k}: {v:.2f}" for k, v in top_factors])
            
            prompt = f"""
            **Tanı**: {prediction} (Güven: %{confidence*100:.1f})
            **Risk Seviyesi**: {risk_level}
            
            **Etkili Faktörler**:
            {factors_str}

            **Talimatlar**:
            1. Tanıyı basit bir dille açıkla
            2. Risk seviyesini yorumla
            3. En etkili 3 faktörü açıkla
            4. 3-5 kişiselleştirilmiş öneri ver
            5. Profesyonel yardım gerekip gerekmediğini belirt
            6. Umut verici ve destekleyici bir ton kullan

            **Çıktı Formatı**:
            {{
                "analysis": "Analiz metni...",
                "recommendations": ["Öneri 1", "Öneri 2"]
            }}
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # JSON'dan önce ve sonraki gereksiz kısımları temizle
            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
            
            return json.loads(response_text)
        except Exception as e:
            logger.error(f"❌ Gemini analiz hatası: {str(e)}")
            return self.get_fallback_analysis(prediction)
    
    def get_fallback_analysis(self, prediction: str) -> dict:
        """Gemini kullanılamadığında fallback analiz"""
        return {
            "analysis": f"Model tanısı: {prediction}. AI analizi şu anda kullanılamıyor.",
            "recommendations": [
                "Düzenli egzersiz yapın",
                "Sağlıklı beslenmeye özen gösterin",
                "Uyku düzeninizi koruyun"
            ]
        }

# Global Gemini service instance
gemini_service = GeminiService()