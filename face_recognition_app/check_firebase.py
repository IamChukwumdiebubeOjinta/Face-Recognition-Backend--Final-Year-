from firebase_admin import credentials, initialize_app, storage
import firebase_admin
from app.utils.setting import settings
import os

service_account_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'serviceAccountKey.json')

print("service_account_path >> ",service_account_path)
print("service_account_settings >> ",settings)

# Initialize Firebase
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': settings.storageBucket,
    'databaseURL': settings.databaseURL
})

# Access bucket and list files
bucket = storage.bucket()
blobs = bucket.list_blobs()

for blob in blobs:
    print(blob.name)
