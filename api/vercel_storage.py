import os
import json
from vercel_storage import blob

class VercelStorage:
    @staticmethod
    def save_data(key: str, data):
        """حفظ البيانات في Vercel Storage"""
        blob.put(
            key=key,
            body=json.dumps(data),
            options={'addRandomSuffix': False}
        )

    @staticmethod
    def load_data(key: str):
        """تحميل البيانات من Vercel Storage"""
        try:
            data = blob.get(key=key).json()
            return json.loads(data)
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
