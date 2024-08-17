from socketio import AsyncServer

class SocketManager:
    def __init__(self, sio: AsyncServer):
        self.sio = sio

    async def emit_face_verified(self, client_id: str):
        await self.sio.emit('face_verified', {'client_id': client_id})