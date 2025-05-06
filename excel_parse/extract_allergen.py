import pandas as pd
import os

def get_engine(filename):
    if filename.lower().endswith('.xls'):
        return 'xlrd'
    else:
        return 'openpyxl'

def extract_allergen(df_input, product_code, issued_date):
    # F43: KR (index 42), F48: EN (index 47)
    rows = []
    for idx, (row_idx, typ) in enumerate([(42, 'KR'), (47, 'EN')]):
        val = df_input.iloc[row_idx, 5] if row_idx < len(df_input) and not pd.isna(df_input.iloc[row_idx, 5]) else None
        if val:
            allergens = [a.strip() for a in str(val).split(',') if a.strip()]
            for allergen in allergens:
                rows.append({
                    "product_code": product_code,
                    "issued_date": issued_date,
                    "type": typ,
                    "allergen": allergen,
                })
        else:
            rows.append({
                "product_code": product_code,
                "issued_date": issued_date,
                "type": typ,
                "allergen": None,
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
    # allergen 추출
    allergen_rows = extract_allergen(df_input, product_code, issued_date)
    for row in allergen_rows:
        row['source_file'] = os.path.basename(filepath)
    return allergen_rows

# === 메인 실행부 ===
EXCEL_DIR = r"D:\(주)에바스코스메틱 Dropbox\팀's shared workspace\EVAS COSMETIC\Project_RISE\100_QC DB\04_제품 표준서"
all_allergen = []

for fname in os.listdir(EXCEL_DIR):
    if fname.endswith('.xls') or fname.endswith('.xlsx'):
        fpath = os.path.join(EXCEL_DIR, fname)
        try:
            rows = parse_excel_file(fpath)
            all_allergen.extend(rows)
            print(f"Parsed: {fname}")
        except Exception as e:
            print(f"Error parsing {fname}: {e}")

# DataFrame으로 통합
if all_allergen:
    df_all = pd.DataFrame(all_allergen)
    df_all.to_csv("all_allergen.csv", index=False, encoding='utf-8-sig')
    print("모든 allergen 정보가 all_allergen.csv 파일로 저장되었습니다.")
else:
    print("추출된 allergen 정보가 없습니다.") 