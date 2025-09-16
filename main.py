import os
import json
import pandas as pd
from io import BytesIO
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
from db import init_db, save_to_db  # save_to_dbをsave_recordsに変更
from mask import mask_company   # 企業名マスク処理

# Google Drive設定
SERVICE_ACCOUNT_FILE = os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
FILE_ID = "1TmBvByxQNEbuh-FdSCn2XsA2TDIFdTOM"  # Google DriveのCSVファイルID

creds_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])

def download_csv_from_drive():
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    service = build("drive", "v3", credentials=creds)
    request = service.files().get_media(fileId=FILE_ID)
    fh = BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%")
    fh.seek(0)
    df = pd.read_csv(fh)
    return df

def load_csv_and_process():
    df = download_csv_from_drive()
    records = []
    for _, row in df.iterrows():
        summary = mask_company(str(row["テキスト要約"]))
        content = mask_company(str(row["通話テキスト"]))
        records.append({"summary": summary, "content": content})
    return records

def main():
    print("DB初期化...")
    init_db()
    print("CSV読み込み...")
    records = load_csv_and_process()
    print("DB保存...")
    save_to_db(records)
    print("完了！")

if __name__ == "__main__":
    main()
