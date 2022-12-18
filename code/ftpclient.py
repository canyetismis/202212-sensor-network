import ftplib
import os

class FTPClient:
    def __init__(self, hostname: str = "10.50.202.242", username: str="user08", password: str="user08"):
        self.__ftp_server = ftplib.FTP(hostname, username, password)
    
    def retrieve_images(self, uri: str = os.getcwd() + '/faces/'):
        files = []

        try:
            files = self.__ftp_server.nlst()
        except ftplib.error_perm as resp:
            if str(resp) == "550 No files found":
                print("No files in this directory")
            else:
                raise

        for f in files:
            handle = open(uri + f, 'wb')
            self.__ftp_server.retrbinary("RETR " + f, handle.write)
    
    def __del__(self):
        self.__ftp_server.close()