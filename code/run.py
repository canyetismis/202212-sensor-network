
from face_detector import FaceDetector
from ftpclient import FTPClient

client = FTPClient()
client.retrieve_images()

fd = FaceDetector(com="COM6")
fd.detect_faces()
