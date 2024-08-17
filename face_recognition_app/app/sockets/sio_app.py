import socketio
import cv2
import numpy as np
from ..utils.face_utils import verify_face_encoding

def register_handlers(sio):
    @sio.event
    async def connect(sid, environ):
        print(f"Client connected: {sid}")

    @sio.event
    async def disconnect(sid):
        print(f"Client disconnected: {sid}")

    @sio.event
    async def verify_face_realtime(sid, data):
        img_data = data['image']
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        client_id = verify_face_encoding(img)
        if client_id:
            await sio.emit('face_verified', {'client_id': client_id}, room=sid)
        else:
            await sio.emit('face_not_recognized', room=sid)