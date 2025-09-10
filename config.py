import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

# 環境変数からDATABASE_URLを取得
DATABASE_URL = os.getenv("DATABASE_URL")
