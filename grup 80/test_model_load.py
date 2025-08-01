from pathlib import Path
import joblib

model_path = Path("C:/Users/busra/OneDrive/Masaüstü/grup 80/models/mental_health_xgboost_v1.pkl")

try:
    model = joblib.load(model_path)
    print("✅ Model başarıyla yüklendi.")
except Exception as e:
    print("❌ Model yüklenemedi:")
    print(e)
