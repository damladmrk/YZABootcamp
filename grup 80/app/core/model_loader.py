from pathlib import Path
import xgboost as xgb  # XGBoost kütüphanesi eklenmeli
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
            base_dir = Path(__file__).resolve().parent.parent.parent
            model_path = base_dir / settings.MODEL_PATH
            logger.info(f"Model yükleniyor: {model_path}")

            if not model_path.exists():
                logger.error(f"❌ Model dosyası bulunamadı: {model_path}")
                raise FileNotFoundError(f"Model dosyası bulunamadı: {model_path}")

            # DÜZELTME: joblib yerine xgboost ile yükle
            self.model = xgb.Booster()
            self.model.load_model(model_path)
            logger.info("✅ Model başarıyla yüklendi (xgboost format)")

            # SHAP explainer için düzeltme
            try:
                import shap
                # DÜZELTME: TreeExplainer'a model doğrudan verilmeli
                self.explainer = shap.TreeExplainer(self.model)
                logger.info("✅ SHAP explainer başlatıldı")
            except ImportError as e:
                logger.error(f"SHAP kütüphanesi yüklü değil: {str(e)}")
                raise
            except Exception as e:
                logger.error(f"SHAP explainer oluşturma hatası: {str(e)}")
                raise

            self.loaded = True
            return True

        except Exception as e:
            logger.error(f"❌ Model yükleme başarısız: {str(e)}", exc_info=True)
            self.loaded = False
            return False

# Global model loader instance
model_loader = ModelLoader()