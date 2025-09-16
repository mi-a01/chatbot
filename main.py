import os
import json
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from db import init_db, save_to_db
from mask import mask_company

# Google Sheets 設定
SERVICE_ACCOUNT_FILE = os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SPREADSHEET_ID = "1zCusDmPY_2ovuw_8x-ltEltIIi2mXUiNR27Pj2_0vMU"
RANGE_NAME = "A:Z"  # 必要な範囲を指定。Q列・R列が含まれるように

creds_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])

def download_sheet():
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get("values", [])

    if not values:
        print("スプレッドシートにデータがありません")
        return pd.DataFrame()

    # ヘッダー行を DataFrame の列名にする
    df = pd.DataFrame(values[1:], columns=values[0])
    return df

def load_sheet_and_process():
    df = download_sheet()
    if df.empty:
        return []

    # NaN 埋め
    df["テキスト要約"] = df.get("テキスト要約", pd.Series([""]*len(df))).fillna("")
    df["通話テキスト"] = df.get("通話テキスト", pd.Series([""]*len(df))).fillna("")

    records = []
    for _, row in df.iterrows():
        summary = mask_company(str(row["テキスト要約"]))
        content = mask_company(str(row["通話テキスト"]))
        records.append({"summary": summary, "content": content})
    return records

def main():
    print("DB初期化...")
    init_db()
    print("スプレッドシート読み込み...")
    records = load_sheet_and_process()
    print("DB保存...")
    save_to_db(records)
    print("完了！")

if __name__ == "__main__":
    main()
