import pandas as pd
import os

def get_engine(filename):
    if filename.lower().endswith('.xls'):
        return 'xlrd'
    else:
        return 'openpyxl'

def extract_test_result_en(df_input, product_code, issued_date):
    # K4-K28: test_item, L4-L28: result, M4-M28: note
    # pandas는 0-index이므로 3~27행, K=10, L=11, M=12
    rows = []
    for i in range(3, 28):  # 4~28행
        test_item = df_input.iloc[i, 10] if not pd.isna(df_input.iloc[i, 10]) else ""
        result = df_input.iloc[i, 11] if not pd.isna(df_input.iloc[i, 11]) else ""
        note = df_input.iloc[i, 12] if not pd.isna(df_input.iloc[i, 12]) else ""
        if test_item:  # 시험항목이 비어있지 않으면
            rows.append({
                "product_code": product_code,
                "issued_date": issued_date,
                "test_item": str(test_item).strip(),
                "result": str(result).strip(),
                "note": str(note).strip(),
            })
    return rows

def parse_excel_file(filepath: str):
    engine = get_engine(filepath)
    xls = pd.ExcelFile(filepath, engine=engine)
    df_input = pd.read_excel(xls, sheet_name='입력란', engine=engine)
    # 제품코드, 작성일자 추출
    product_code = ""
    issued_date = ""
    for idx, row in df_input.iterrows():
        key = str(row[0]).strip() if not pd.isna(row[0]) else ""
        if key in ['제품코드', '코드']:
            product_code = str(row[1]).strip()
        if key in ['작성일자']:
            issued_date = str(row[1]).strip()
    # test_result_en 추출
    test_result_en_rows = extract_test_result_en(df_input, product_code, issued_date)
    for row in test_result_en_rows:
        row['source_file'] = os.path.basename(filepath)
    return test_result_en_rows

# === 메인 실행부 ===
EXCEL_DIR = r"D:\(주)에바스코스메틱 Dropbox\팀's shared workspace\EVAS COSMETIC\Project_RISE\100_QC DB\04_제품 표준서"
all_test_result_en = []

for fname in os.listdir(EXCEL_DIR):
    if fname.endswith('.xls') or fname.endswith('.xlsx'):
        fpath = os.path.join(EXCEL_DIR, fname)
        try:
            rows = parse_excel_file(fpath)
            all_test_result_en.extend(rows)
            print(f"Parsed: {fname}")
        except Exception as e:
            print(f"Error parsing {fname}: {e}")

# DataFrame으로 통합
if all_test_result_en:
    df_all = pd.DataFrame(all_test_result_en)
    df_all.to_csv("all_test_result_en.csv", index=False, encoding='utf-8-sig')
    print("모든 test_result_en 정보가 all_test_result_en.csv 파일로 저장되었습니다.")
else:
    print("추출된 test_result_en 정보가 없습니다.") 