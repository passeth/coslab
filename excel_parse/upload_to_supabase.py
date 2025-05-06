import os
import pandas as pd
from supabase import create_client, Client

# Supabase 연결 정보
url = "https://usvjbuudnofwhmclwhfl.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzdmpidXVkbm9md2htY2x3aGZsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU0MTc5NDgsImV4cCI6MjA2MDk5Mzk0OH0.DkUXLZMnZljFs1Pti7xnHvsYzO1lTyhovdzMFerbvq4"
supabase: Client = create_client(url, key)

# CSV 파일이 있는 폴더
CSV_DIR = r"C:\Users\passe\.cursor\excel_parse_result"

# lab_*.csv 파일을 모두 찾아서 업로드
for fname in os.listdir(CSV_DIR):
    if fname.startswith("lab_") and fname.endswith(".csv"):
        table_name = fname.replace(".csv", "")
        fpath = os.path.join(CSV_DIR, fname)
        df = pd.read_csv(fpath, dtype=str)
        print(f"Uploading {fname} → {table_name} ({len(df)} rows)")
        # 100건씩 배치 업로드
        for i in range(0, len(df), 100):
            # NaN을 None으로 변환 (JSON 직렬화 오류 방지)
            batch_df = df.iloc[i:i+100].where(pd.notnull(df.iloc[i:i+100]), None)
            batch = batch_df.to_dict(orient="records")
            supabase.table(table_name).insert(batch).execute()
        print(f"Done: {fname}")

print("모든 lab_ 테이블 업로드 완료!") 