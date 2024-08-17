import cv2
import face_recognition
import pickle
import os
import numpy as np

# Load the encoding file
encode_file_path = 'face_recognition_app/app/EncodeFile.p'
if os.path.exists(encode_file_path):
    with open(encode_file_path, 'rb') as file:
        encodeListKnownWithIds = pickle.load(file)
else:
    encodeListKnownWithIds = ([], [])
encodeListKnown, clientIds = encodeListKnownWithIds

print("encoding loaded", clientIds)

def add_face_encoding(img, client_id):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(img_rgb)
    
    if not face_locations:
        return None
    
    face_encoding = face_recognition.face_encodings(img_rgb, face_locations)[0]
    
    # Add new encoding and client ID to the lists
    encodeListKnown.append(face_encoding)
    clientIds.append(client_id)
    
    # Save updated encodings
    with open(encode_file_path, 'wb') as file:
        pickle.dump([encodeListKnown, clientIds], file)
    
    # Save image
    img_directory = 'face_recognition_app/app/Images/'
    os.makedirs(img_directory, exist_ok=True)
    img_path = os.path.join(img_directory, f"{client_id}.jpg")
    cv2.imwrite(img_path, img)
    
    return face_encoding

def verify_face_encoding(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(img_rgb)
    
    if not face_locations:
        print("No face detected")
        return None
    
    face_encoding = face_recognition.face_encodings(img_rgb, face_locations)[0]
    print(f"Generated face encoding: {face_encoding}")
    
    matches = face_recognition.compare_faces(encodeListKnown, face_encoding, tolerance=0.6)
    face_distances = face_recognition.face_distance(encodeListKnown, face_encoding)
    
    print(f"Matches: {matches}")
    print(f"Face distances: {face_distances}")
    
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        return clientIds[best_match_index]
    else:
        return None

