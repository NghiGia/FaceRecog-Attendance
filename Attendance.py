import cv2
import numpy as np
import face_recognition
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import serial
import serial.tools.list_ports
from datetime import datetime

# scopes = [
#     'https://www.googleapis.com/auth/spreadsheets',
#     'https://www.googleapis.com/auth/drive'
# ]
# credentials = ServiceAccountCredentials.from_json_keyfile_name("ggsheet-proskill-212-49b358d8dd86.json",
#                                                                scopes)  # access the json key you downloaded earlier
# file = gspread.authorize(credentials)  # authenticate the JSON key with gspread
# sheet = file.open("Attendance_sheet")  # open sheet
# sheet = sheet.sheet1  # replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1
#

path = 'ImageBasic'
images = []
clasNames = []
myList = os.listdir(path)
for cls in myList:
    currentImg = cv2.imread(f'{path}/{cls}')
    images.append(currentImg)
    clasNames.append(os.path.splitext(cls)[0])
print("Class")
print(clasNames)


def findEncoding(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        print(encode)
        encodeList.append(encode)
    return encodeList


encodeListKnow = findEncoding(images)
print(len(encodeListKnow))

cap = cv2.VideoCapture(0)

def openCam():
    counter = 2
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faceCurrent = face_recognition.face_locations(imgS)
        encodeCurrent = face_recognition.face_encodings(imgS, faceCurrent)

        for encodeFace, faceLoc in zip(encodeCurrent, faceCurrent):
            matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = clasNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                with open('Attendance.csv', 'r+') as f:
                    myDataList = f.readlines()
                    NameList = []
                    for line in myDataList:
                        entry = line.split(',')
                        NameList.append(entry[0])
                    if name not in NameList:
                        now = datetime.now()
                        dtString = now.strftime('%H:%M:%S')
                        f.writelines(f'\n{name},{dtString}')

                        # # updata to sheet
                        # sheet.update_cell(counter, 1, f'{name}')  # updates row 2 on column 3
                        # sheet.update_cell(counter, 2, f'{dtString}')  # updates row 2 on column 3
                        counter += 1

                print(name)
        cv2.imshow('Webcam cua Nghi', img)
        cv2.waitKey(1)


# while True:
#     # readSerial()
#     openCam()
