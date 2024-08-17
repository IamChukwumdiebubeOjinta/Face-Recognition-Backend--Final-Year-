from face_recognition_app.app.services.face_service import FaceService
from face_recognition_app.app.services.db_service import DBService
from face_recognition_app.app.socket_manager import SocketManager
from socketio import AsyncServer

db_service = DBService()
face_service = FaceService(db_service)
socket_manager = SocketManager(AsyncServer())

def get_face_service():
    return face_service

def get_db_service():
    return db_service

def get_socket_manager():
    return socket_manager