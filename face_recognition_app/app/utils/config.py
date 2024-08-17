import os
import firebase_admin
from ..utils.setting import settings
from firebase_admin import credentials, storage, db

import logging

logging.basicConfig(level=logging.INFO)

service_account_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'serviceAccountKey.json')

# Initialize Firebase Admin
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': settings.storageBucket,
    'databaseURL': settings.databaseURL
})

bucket = storage.bucket()

logging.info(f"Service account path: {service_account_path}")
logging.info(f"Storage bucket: {settings.storageBucket}")
logging.info(f"Database URL: {settings.databaseURL}")
