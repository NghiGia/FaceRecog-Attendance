import cv2
import numpy as np
import face_recognition

imgElon= face_recognition.load_image_file('ImageBasic/Elon Musk.jpeg')
imgElon= cv2.cvtColor(imgElon,cv2.COLOR_BGR2RGB)
imgTest= face_recognition.load_image_file('ImageBasic/Elon Test.jpeg')
imgTest= cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)

facLoc=face_recognition.face_locations(imgElon)[0]
encodeElon=face_recognition.face_encodings(imgElon)[0]
cv2.rectangle(imgElon,(facLoc[3],facLoc[0]),(facLoc[1],facLoc[2]),(255,0,255),2)

facLocTest=face_recognition.face_locations(imgTest)[0]
encodeElonTest=face_recognition.face_encodings(imgTest)[0]
cv2.rectangle(imgTest,(facLoc[3],facLoc[0]),(facLoc[1],facLoc[2]),(255,0,255),2)

results=face_recognition.compare_faces([encodeElon],encodeElonTest)
faceDis=face_recognition.face_distance([encodeElon],encodeElonTest)
print(results,faceDis)

cv2.imshow('Elon Musk',imgElon)
cv2.imshow('Test',imgTest)
cv2.waitKey(0)

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import json
#
# scopes = [
# 'https://www.googleapis.com/auth/spreadsheets',
# 'https://www.googleapis.com/auth/drive'
# ]
# credentials = ServiceAccountCredentials.from_json_keyfile_name("ggsheet-proskill-212-49b358d8dd86.json", scopes) #access the json key you downloaded earlier
# file = gspread.authorize(credentials) # authenticate the JSON key with gspread
# sheet = file.open("Attendance_sheet")  #open sheet
# sheet = sheet.sheet1 #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1
#
# all_cells = sheet.range('A1:C6')
# print(all_cells)
#
# sheet.update_cell(2, 3, 'Change') #updates row 2 on column 3