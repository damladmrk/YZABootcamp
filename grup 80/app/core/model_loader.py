import joblib
import os
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__, settings.LOG_LEVEL)

class ModelLoader:
    def __init__(self):
        self.model = None
        self.explainer = None
        self.loaded = False

    def load_model(self):
        try:
            # Model dosya yolunu mutlak yola çevir
            model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", settings.MODEL_PATH))
            logger.info(f"Model yükleniyor: {model_path}")

            # Dosyanın varlığını kontrol et
            if not os.path.exists(model_path):
                logger.error(f"Model dosyası bulunamadı: {model_path}")
                raise FileNotFoundError(f"Model dosyası bulunamadı: {model_path}")

            # Modeli yükle
            self.model = joblib.load(model_path)
            logger.info("✅ Model başarıyla yüklendi")

            # SHAP explainer oluştur
            try:
                import shap
                self.explainer = shap.TreeExplainer(self.model)
                logger.info("✅ SHAP explainer başlatıldı")
            except ImportError as e:
                logger.error(f"SHAP kütüphanesi yüklü değil: {str(e)}")
                raise ImportError("SHAP kütüphanesi yüklü değil. Lütfen 'pip install shap' komutunu çalıştırın.")
            except Exception as e:
                logger.error(f"SHAP explainer oluşturma hatası: {str(e)}")
                raise

            self.loaded = True
            return True
        except FileNotFoundError as e:
            logger.error(f"❌ Model yükleme başarısız - Dosya bulunamadı: {str(e)}")
            self.loaded = False
            return False
        except Exception as e:
            logger.error(f"❌ Model yükleme başarısız: {str(e)}")
            self.loaded = False
            return False

# Global model loader instance
model_loader = ModelLoader()