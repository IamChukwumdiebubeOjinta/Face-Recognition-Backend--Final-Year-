from typing import Annotated
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from datetime import datetime
from ..utils.firebase_utils import add_to_firebase, get_from_firebase, bucket, update_in_firebase, delete_from_firebase, get_all_users
from ..utils.face_utils import add_face_encoding, verify_face_encoding

router = APIRouter()

@router.post("/add_face")
async def add_face(
    client_id: Annotated[str, Form()],
    name: Annotated[str, Form()],
    dept: Annotated[str, Form()] | None = None,
    invited_by: Annotated[str, Form()] | None = None,
    user_type: Annotated[str, Form()] = "Visitor",
    file: UploadFile = File(...),
) -> JSONResponse:
    print(client_id, name)
    if not client_id or not name:
        raise HTTPException(status_code=400, detail="Client ID, name, and department are required")
    
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Invalid image")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image format")

    face_encoding = add_face_encoding(img, client_id)
    if face_encoding is None:
        raise HTTPException(status_code=400, detail="No face detected in the image")

    img_path = f"faces/{client_id}.jpg"
    blob = bucket.blob(img_path)
    try:
        blob.upload_from_string(contents, content_type='image/jpeg')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

    image_url = blob.public_url

    data = {
        "name": name,
        "department": dept,
        "type": user_type,
        "recorded_time": datetime.utcnow().isoformat(),
        "image_url": image_url
    }

    if user_type.lower() == "visitor" and invited_by:
        data["invited_by"] = invited_by
    
    try:
        add_to_firebase(client_id, data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add data to Firebase: {str(e)}")

    return JSONResponse(content={"message": "Face added successfully"}, status_code=201)


@router.post("/verify_face")
async def verify_face(file: UploadFile = File(...)) -> JSONResponse:
    import datetime
    contents: bytes = await file.read()
    nparr: np.ndarray = np.frombuffer(contents, np.uint8)
    img: np.ndarray = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    client_id: str | None = verify_face_encoding(img)
    
    if client_id:
        client_data = get_from_firebase(client_id)
        
        # Generate signed URL
        blob = bucket.blob(f"faces/{client_id}.jpg")
        signed_url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=15),
            method="GET"
        )
        
        # Add signed URL to client data
        client_data['image_url'] = signed_url
        
        return JSONResponse(content={"message": "Face verified", "client_id": client_id, "client_data": client_data}, status_code=200)
    else:
        return JSONResponse(content={"message": "Face not recognized"}, status_code=404)

@router.patch("/update_face")
async def update_face(client_id: str, name: str = None, dept: str = None, user_type: str = None, invited_by: str = None):
    if not client_id:
        raise HTTPException(status_code=400, detail="Client ID is required")

    client_data = get_from_firebase(client_id)
    if not client_data:
        raise HTTPException(status_code=404, detail="Client not found")

    if name:
        client_data['name'] = name
    if dept:
        client_data['department'] = dept
    if user_type:
        client_data['type'] = user_type
    
    if user_type and user_type.lower() == "visitor" and invited_by:
        client_data['invited_by'] = invited_by
    elif user_type and user_type.lower() != "visitor" and "invited_by" in client_data:
        del client_data['invited_by']

    update_in_firebase(client_id, client_data)
    return JSONResponse(content={"message": "Client information updated successfully"}, status_code=200)

@router.delete("/delete_face")
async def delete_face(client_id: str):
    if not client_id:
        raise HTTPException(status_code=400, detail="Client ID is required")

    client_data = get_from_firebase(client_id)
    if not client_data:
        raise HTTPException(status_code=404, detail="Client not found")

    img_path = f"faces/{client_id}.jpg"
    blob = bucket.blob(img_path)
    if blob.exists():
        blob.delete()
    
    delete_from_firebase(client_id)
    return JSONResponse(content={"message": "Client data deleted successfully"}, status_code=200)

@router.get("/get_users")
async def get_users():
    users = get_all_users()
    if not users:
        return JSONResponse(content={"message": "No users found"}, status_code=404)
    return JSONResponse(content={"users": users}, status_code=200)
