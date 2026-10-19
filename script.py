import os
import time
from ftplib import FTP

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FTP_HOST = "://example.com"
FTP_USER = "your_username"
FTP_PASS = "your_password"
REMOTE_DIR = "/public_html/files"
LOCAL_DIR = os.path.join(BASE_DIR, "dump")
CHECK_INTERVAL = 10

def log(text):
    print(f"[{time.strftime('%d.%m.%Y %H:%M:%S')}] {text}")

def connect():
    ftp = FTP()
    ftp.connect(FTP_HOST, 21, timeout=30)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.set_pasv(True)
    if REMOTE_DIR:
        ftp.cwd(REMOTE_DIR)
    log("FTP CONNECTED")
    return ftp

def download_and_delete(ftp, name):
    local_path = os.path.join(LOCAL_DIR, name)
    with open(local_path, "wb") as f:
        ftp.retrbinary(f"RETR {name}", f.write)
    ftp.delete(name)
    log(f"DOWNLOADED AND DELETED {name}")

os.makedirs(LOCAL_DIR, exist_ok=True)
ftp = None
log("START")
while True:
    if ftp is None:
        try:
            ftp = connect()
        except Exception as e:
            log(f"FTP ERROR: {e}")
            time.sleep(5)
            continue
    try:
        items = ftp.nlst()
        for name in items:
            try:
                ftp.size(name)
                is_file = True
            except:
                is_file = False
            if not is_file:
                continue
            download_and_delete(ftp, name)
    except Exception as e:
        log(f"ERROR: {e}")
        try:
            ftp.quit()
        except:
            pass
        ftp = None
    time.sleep(CHECK_INTERVAL)