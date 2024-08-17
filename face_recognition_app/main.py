from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
import socketio
from fastapi.middleware.cors import CORSMiddleware
from socketio import ASGIApp
from app.routes import face_router
from app.sockets import sio_app

app = FastAPI(
    title="Face Recognition App",
    description="API for face recognition app",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a Socket.IO server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# Create an ASGI app wrapping the Socket.IO server and the FastAPI app
socket_app = socketio.ASGIApp(sio, app)

# Include Socket.IO event handlers
sio_app.register_handlers(sio)

# Include router
app.include_router(
    face_router.router, 
    prefix="/api/v1"
)

@app.get('/', include_in_schema=False, response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
def index():
    return "/docs"