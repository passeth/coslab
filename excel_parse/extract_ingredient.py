import pandas as pd
import os

def get_engine(filename):
    if filename.lower().endswith('.xls'):
        return 'xlrd'
    else:
        return 'openpyxl'

def extract_ingredient(df_input, product_code, issued_date):
    # B14-B53: material_code (index 13~52), C14-C53: ratio (index 13~52)
    rows = []
    for i in range(13, 53):  # 14~53행
        material_code = df_input.iloc[i, 1] if not pd.isna(df_input.iloc[i, 1]) else ""
        ratio = df_input.iloc[i, 2] if not pd.isna(df_input.iloc[i, 2]) else ""
        if material_code:  # 코드가 비어있지 않으면
            rows.append({
                "product_code": product_code,
                "issued_date": issued_date,
                "material_code": str(material_code).strip(),
                "ratio": str(ratio).strip(),
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
    # ingredient 추출
    ingredient_rows = extract_ingredient(df_input, product_code, issued_date)
    for row in ingredient_rows:
        row['source_file'] = os.path.basename(filepath)
    return ingredient_rows

# === 메인 실행부 ===
EXCEL_DIR = r"D:\(주)에바스코스메틱 Dropbox\팀's shared workspace\EVAS COSMETIC\Project_RISE\100_QC DB\04_제품 표준서"
all_ingredient = []

for fname in os.listdir(EXCEL_DIR):
    if fname.endswith('.xls') or fname.endswith('.xlsx'):
        fpath = os.path.join(EXCEL_DIR, fname)
        try:
            rows = parse_excel_file(fpath)
            all_ingredient.extend(rows)
            print(f"Parsed: {fname}")
        except Exception as e:
            print(f"Error parsing {fname}: {e}")

# DataFrame으로 통합
if all_ingredient:
    df_all = pd.DataFrame(all_ingredient)
    df_all.to_csv("all_ingredient.csv", index=False, encoding='utf-8-sig')
    print("모든 ingredient 정보가 all_ingredient.csv 파일로 저장되었습니다.")
else:
    print("추출된 ingredient 정보가 없습니다.") 