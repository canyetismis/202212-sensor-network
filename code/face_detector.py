import face_recognition
import cv2
import numpy as np
import os
import serial

class FaceDetector:

    def __init__(self, video_device: int = 0, faces_uri: str=os.getcwd() + '/faces/', com: str='COM6'):
        self.__video_capture = cv2.VideoCapture(video_device)
        self.__existing_faces = self.__get_faces(faces_uri)
        self.__ser = serial.Serial(com, 9600, timeout = 1, write_timeout = 1) 

    def __get_faces(self, uri: str):
        face_list = os.listdir(uri)
        return_list = []
        for face in face_list:
            #extract the name from file name
            name = face.split('.')
            name = name[0]

            #Load the image and get the encoding
            image = face_recognition.load_image_file(uri + face)
            encoding = face_recognition.face_encodings(image)[0]
            return_list.append(
                {
                    'name': name,
                    'encoding': encoding
                }
            )

        return return_list
    
    def detect_faces(self):
        process_frame = True
        face_locations = []
        face_encodings = []

        existing_face_encodings = []
        
        for face in self.__existing_faces:
            existing_face_encodings.append(face['encoding'])
        
        self.__ser.write(b'0')
        
        while self.__video_capture.isOpened():
            
            ret, frame = self.__video_capture.read()

            if process_frame:
                #resize the frame and convert colours
                resize_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                resize_frame = resize_frame[:, :, ::-1]

                #find all the face locations:
                face_locations = face_recognition.face_locations(resize_frame)
                face_encodings = face_recognition.face_encodings(resize_frame, face_locations)
                
                face_names = []
                for encoding in face_encodings:
                    matches = face_recognition.compare_faces(existing_face_encodings, encoding)
                    face_name = "Unknown"

                    face_distances = face_recognition.face_distance(existing_face_encodings, encoding)
                    best_index = np.argmin(face_distances)
                    if matches[best_index]:
                        face_name = self.__existing_faces[best_index]['name']
                    
                    face_names.append(face_name)
            
            process_frame = not process_frame
            self.__ser.write(b'0')
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                if name == "Unknown":
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                    self.__ser.write(b'1')
                    print(self.__ser.readline().decode('ascii'))
                else:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)
        
            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
    
    def __del__(self):
        self.__video_capture.release()