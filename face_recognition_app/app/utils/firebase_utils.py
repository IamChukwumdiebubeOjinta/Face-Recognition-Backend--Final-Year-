import firebase_admin
from firebase_admin import credentials, db, storage
from .setting import settings
import os

service_account_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'serviceAccountKey.json')

# Initialize Firebase Admin
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': settings.storageBucket,
    'databaseURL': settings.databaseURL
})

bucket = storage.bucket()
ref = db.reference('facial-r-users')

def add_to_firebase(client_id, data):
    ref.child(client_id).set(data)

def get_from_firebase(client_id):
    return ref.child(client_id).get()

def update_in_firebase(client_id, data):
    ref.child(client_id).update(data)

def delete_from_firebase(client_id):
    ref.child(client_id).delete()

def get_all_users():
    return ref.get()
