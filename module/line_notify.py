import mimetypes, socket
import os
import subprocess
import sys
import requests

url = 'https://notify-api.line.me/api/notify'
# linetoken = 'VhcjD0lfUq7slvV4Mahf8eaa9zKIBK4trCTnEsUigLQ'
# linetoken = '0Fr41lAuwYniaDzHQaUpXo32vx38KmRuB6nSWqce2Oj'

class LineNotify:
    def __init__(self, linetoken, file_path):
        self.linetoken = linetoken
        self.file_path = file_path

def check_internet_connection():
    remote_server = "www.google.com"
    port = 80
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        sock.connect((remote_server, port))
        return True
    except socket.error:
        return False
    finally:
        sock.close()

def get_file_type(file_path):
    mime_type, encoding = mimetypes.guess_type(file_path)
    return mime_type

def send_notify(file_path, msg):
    if not msg:
        msg = "No specific message."
    linetoken = os.environ.get("line_token")
    header = {'Authorization': 'Bearer ' + linetoken}
    payload = {'message':msg}
    if file_path:
        image = {'imageFile': open(file_path, 'rb')}
        res = requests.post(url, headers=header, files=image, data=payload)
    else:
        res = requests.post(url, headers=header, data=payload)
    print(res)
    return res.status_code

if __name__ == '__main__':

    if len(sys.argv) == 3:
        msg = sys.argv[1]
        file_path = sys.argv[2]
    elif len(sys.argv) == 2:
        msg = sys.argv[1]
        file_path = ""
    else:
        msg = ""
        file_path = ""
    send_notify(file_path, msg)