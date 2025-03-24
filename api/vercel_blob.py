import os
import json
from vercel_blob import put, head

class VercelStorage:
    @staticmethod
    def save_data(data):
        """حفظ البيانات في Vercel Blob Storage"""
        put(
            name='library.json',
            body=json.dumps(data),
            options={
                'addRandomSuffix': False,
                'token': os.getenv('BLOB_READ_WRITE_TOKEN')
            }
        )

    @staticmethod
    def load_data():
        """جلب البيانات من Vercel Blob Storage"""
        try:
            response = head(
                'library.json',
                options={
                    'token': os.getenv('BLOB_READ_WRITE_TOKEN')
                }
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Error loading data: {e}")
            return []
