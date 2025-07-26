import pandas as pd
import logging
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__, settings.LOG_LEVEL)

class DataPreprocessor:
    def __init__(self):
        self.ordinal_map = {
            "Seldom": 0, 
            "Sometimes": 1, 
            "Usually": 2, 
            "Most-Often": 3
        }
        self.binary_cols = [
            'Mood_Swing', 'Suicidal_thoughts', 'Anorxia', 'Authority_Respect',
            'Try_Explanation', 'Aggressive_Response', 'Ignore_Move_On',
            'Nervous_Break_down', 'Admit_Mistakes', 'Overthinking'
        ]
    
    def preprocess(self, data: dict) -> pd.DataFrame:
        """Frontend verisini model formatına dönüştürür"""
        try:
            # Ordinal encoding
            for col in ['Sadness', 'Euphoric', 'Exhausted', 'Sleep_dissorder']:
                if col in data:
                    data[col] = self.ordinal_map.get(data[col], 1)
            
            # Binary encoding
            for col in self.binary_cols:
                if col in data:
                    data[col] = 1 if data.get(col, "NO") == "YES" else 0
            
            # Numeric conversion
            for col in ['Sexual_Activity', 'Concentration', 'Optimisim']:
                if col in data:
                    value = data[col]
                    if "From" in value:
                        data[col] = int(value.split()[0])
                    else:
                        data[col] = 5  # Default value
            
            # Özellik mühendisliği
            data['Mood_Suicidal_Interaction'] = data.get('Mood_Swing', 0) * data.get('Suicidal_thoughts', 0)
            data['Exhaustion_Sleep'] = data.get('Exhausted', 0) * data.get('Sleep_dissorder', 0)
            data['Total_Symptom_Score'] = sum(data.get(k, 0) for k in ['Sadness', 'Exhausted', 'Sleep_dissorder'])
            
            return pd.DataFrame([data])
        except Exception as e:
            logger.error(f"❌ Veri ön işleme hatası: {str(e)}")
            raise ValueError(f"Veri ön işleme hatası: {str(e)}")

# Global preprocessor instance
preprocessor = DataPreprocessor()

print(pd.__version__)