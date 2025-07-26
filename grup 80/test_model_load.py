import joblib

# Model dosyasının yolunu doğru yazdığından emin ol
model_path = "models/mental_health_xgboost_v1.pkl"

try:
    model = joblib.load(model_path)
    print("✅ Model başarıyla yüklendi!")
    print("Model tipi:", type(model))
except Exception as e:
    print("❌ Model yüklenemedi!")
    print("Hata mesajı:", str(e))