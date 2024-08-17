import cv2
import face_recognition
import pickle
import os

# Importing images
folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
clientIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    clientIds.append(os.path.splitext(path)[0])

    # fileName = f'{folderPath}/{path}'
    # bucket = storage.bucket()
    # blob = bucket.blob(fileName)
    # blob.upload_from_filename(fileName)


    # print(path)
    # print(os.path.splitext(path)[0])
print(clientIds)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

        # print(encodeList)
    return encodeList


print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, clientIds]
print("Encoding Complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")