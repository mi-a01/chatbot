# DB更新処理
python main.py || true

# APIサーバー起動
uvicorn api:app --host 0.0.0.0 --port $PORT
