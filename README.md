# Face Recognition Application

![Project Banner](image/schoolLogo.png)

## Coal City University

**Supervisor:** Dr. Michael Edeh, Ph.D  
**Student:** Ojinta Chukwumdiebube

---

## Table of Contents

1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Installation and Setup](#installation-and-setup)
4. [Running the Application](#running-the-application)
5. [API Endpoints](#api-endpoints)
   - [Handle Image (Socket Event)](#handle-image-socket-event)
   - [Add Face (POST /add_face)](#add-face
   - [Handle Image (Socket Event)](#handle-image-socket-event)
   - [Add Face (POST /add_face)](#add-face-post-add_face)
6. [Image Processing](#image-processing)
7. [Firebase Integration](#firebase-integration)
8. [Testing](#testing)
9. [Docker](#docker)
   - [Dockerfile](#dockerfile)
   - [Building and Running the Docker Container](#building-and-running-the-docker-container)
10. [Dependencies](#dependencies)
11. [Future Enhancements](#future-enhancements)
12. [Acknowledgements](#acknowledgements)
13. [Tags](#tags)

---

## Introduction

Welcome to the Face Recognition Application, a comprehensive project developed as part of my final year at Coal City University under the supervision of Dr. Michael Edeh, Ph.D. This application leverages advanced face recognition technology to detect and identify faces from images in real-time. Built with FastAPI, Firebase, and face recognition libraries, this application is designed to be efficient, scalable, and easy to use.

---

## Project Structure

````plaintext
face_recognition_app/
│
├── face_recognition_app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── firebase_utils.py
│   ├── image_processing.py
│   ├── face_recognition_utils.py
│   ├── routes.py
│   ├── run_server.py
│   ├── settings.py
├── image
├── tests/
│   ├── __init__.py
│   ├── test_routes.py
├── training
│   ├── Images
│   │   ├── images
│   ├── Resources
│   │   ├── modes
│   ├── EncodeFile.p
│   ├── EncodeGenerator.py
│   ├── firebaseDatabase.py
│   ├── main.py
├── pyproject.toml
├── poetry.lock
└── README.md

## Installation and Setup

To get started with the Face Recognition Application, follow these steps:

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/git
    cd face_recognition_app
    ```

2. **Install Poetry:**

    Follow the instructions on the [official Poetry website](https://python-poetry.org/docs/#installation) to install Poetry.

3. **Install Dependencies:**

    ```bash
    poetry install
    ```

4. **Firebase Setup:**

    - Place your Firebase `firebase_key.json` file in the project root.
    - Update the Firebase configuration in `config.py` with your Firebase project's storage bucket and database URL.

---

## Running the Application

To run the application, execute the following command:

```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

## Running the Application

To run the application, execute the following command:

\`\`\`bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
\`\`\`

This command starts the FastAPI server, binding it to \`0.0.0.0\` (all network interfaces) on port \`8000\`. The \`--reload\` option enables auto-reloading of the server when code changes are detected, which is useful during development.

Ensure that all dependencies are installed and configured correctly as per the previous setup instructions before running the command.

### Accessing the Application

Once the server is running, you can access the API and interact with the endpoints using tools like \`curl\`, Postman, or directly from your web browser. The base URL for the API will be \`http://localhost:8000\`.

---

## API Endpoints

### Handle Image (Socket Event)

- **Event Name:** \`image\`
- **Description:** Handles the incoming image data, processes it for face recognition, and returns detected face details.
- **Usage:**

    \`\`\`python
    socket_manager.emit('image', {'image': '<base64-encoded-image>'})
    \`\`\`

### Add Face (POST /add_face)

- **Endpoint:** \`/add_face\`
- **Method:** \`POST\`
- **Description:** Adds a new face to the database and uploads the face encoding and image to Firebase.
- **Request Body:**

    \`\`\`json
    {
        "image": "data:image/jpeg;base64,<base64-encoded-image>",
        "name": "John Doe",
        "type": "Visitor",
        "invited_by": "Jane Smith"
    }
    \`\`\`

- **Response:**

    \`\`\`json
    {
        "message": "Face added successfully",
        "face_details": {
            "name": "John Doe",
            "type": "Visitor",
            "ref_no": "ABC123",
            "invited_by": "Jane Smith",
            "registered": "2023-07-15T14:28:23.382748",
            "latest": "2023-07-15T14:28:23.382748",
            "image_url": "https://your-firebase-storage-url/faces/XYZ789.jpg"
        }
    }
    \`\`\`

---

## Image Processing

The image processing module handles tasks such as cropping, converting images between formats, and extracting face encodings. The key functions include:

- **\`crop_image(image, size)\`**: Crops an image to the specified size.
- **\`handle_image(sid, data)\`**: Processes the image received from the socket event, performs face recognition, and returns the results.

---

## Firebase Integration

Firebase is used for storing face images and face encodings, as well as for real-time database interactions. The Firebase utilities module provides functions to interact with Firebase services:

- **\`generate_random_key(length)\`**: Generates a random key for unique identification.
- **\`upload_image_to_firebase(image, path)\`**: Uploads an image to Firebase Storage and returns the URL.
- **\`load_known_faces(face_encoding_dir)\`**: Loads known face encodings and details from Firebase.

---

## Testing

Tests are written using \`pytest\` and are located in the \`tests/\` directory. To run the tests, execute:

\`\`\`bash
poetry run pytest
\`\`\`

### Example Test: \`test_routes.py\`

\`\`\`python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_add_face():
    response = client.post('/add_face', json={
        "image": "data:image/jpeg;base64,<base64-encoded-image>",
        "name": "Test Name",
        "type": "Visitor",
        "invited_by": "Test Inviter"
    })
    assert response.status_code == 200
    assert response.json()['message'] == 'Face added successfully'
\`\`\`

---

## Docker

### Dockerfile

To containerize the Face Recognition Application, use the following Dockerfile:

\`\`\`dockerfile
# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables to avoid Python buffering issues
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \\
    apt-get install -y build-essential libopencv-dev && \\
    apt-get clean && \\
    rm -rf /var/lib/apt/lists/*

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install --no-cache-dir poetry

# Install the project dependencies
RUN poetry config virtualenvs.create false && \\
    poetry install --no-interaction --no-ansi

# Copy the entire project to the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
\`\`\`

### Building and Running the Docker Container

1. **Build the Docker Image:**

    \`\`\`bash
    docker build -t face_recognition_app .
    \`\`\`

2. **Run the Docker Container:**

    \`\`\`bash
    docker run -p 8000:8000 --name face_recognition_app_container face_recognition_app
    \`\`\`

---

## Dependencies

- **FastAPI:** A modern, fast (high-performance), web framework for building APIs with Python 3.6+.
- **Uvicorn:** A lightning-fast ASGI server implementation, using \`uvloop\` and \`httptools\`.
- **face_recognition:** The world's simplest facial recognition API for Python and the command line.
- **opencv-python-headless:** OpenCV without GUI functionality.
- **numpy:** The fundamental package for scientific computing with Python.
- **Pillow:** The Python Imaging Library adds image processing capabilities to your Python interpreter.
- **firebase-admin:** Firebase Admin SDK enables access to Firebase services from privileged environments.

---

## Future Enhancements

- **Real-time Face Recognition:** Enhance the system to support real-time face recognition from video streams.
- **Enhanced Security:** Implement advanced security measures to protect sensitive data.
- **User Interface:** Develop a user-friendly interface for easier interaction with the system.
- **Scalability:** Optimize the system to handle a larger database of faces and higher traffic.

---

## Acknowledgements

I would like to thank my supervisor, Dr. Michael Edeh, Ph.D., for his invaluable guidance and support throughout this project. Special thanks to Coal City University for providing the resources and environment conducive to learning and innovation.

---

## Tags

**#FaceRecognition** **#FastAPI** **#Firebase** **#Python** **#FinalYearProject** **#CoalCityUniversity** **#ComputerVision** **#AI** **#MachineLearning**

---

This comprehensive README provides detailed information about the project, guiding users through installation, setup, usage, Docker containerization, and future enhancements. It also acknowledges contributions and provides tags for easy categorization.
````
