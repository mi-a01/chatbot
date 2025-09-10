import csv
from db import init_db, save_to_db
from config import CSV_PATH

def load_csv_and_process():
    records = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            summary = row["テキスト要約"]   # Q列
            content = row["通話テキスト"]   # R列
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
