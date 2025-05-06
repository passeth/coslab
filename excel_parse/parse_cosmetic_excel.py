import pandas as pd
import os

def get_engine(filename):
    if filename.lower().endswith('.xls'):
        return 'xlrd'
    else:
        return 'openpyxl'

def extract_product_info_by_cell(df_input):
    info = {}
    mapping = {
        'product_name_kor': ['국문제품명', '제품명', '이름'],
        'product_name_eng': ['영문제품명', '영문이름'],
        'doc_no': ['관리번호'],
        'issued_date': ['작성일자'],
        'product_code': ['제품코드', '코드'],
        'type': ['성상'],
        'capacity': ['포장단위'],
        'recorded': ['작성자'],
        'usage_instructions': ['사용법', '용법'],
    }
    for idx, row in df_input.iterrows():
        key = str(row[0]).strip() if not pd.isna(row[0]) else ""
        for col, keywords in mapping.items():
            if key in keywords:
                info[col] = str(row[1]).strip() if not pd.isna(row[1]) else ""
    return info

def parse_excel_file(filepath: str):
    engine = get_engine(filepath)
    xls = pd.ExcelFile(filepath, engine=engine)
    # 입력란 시트 읽기
    df_input = pd.read_excel(xls, sheet_name='입력란', engine=engine)
    # 셀 위치 기반으로 제품 정보 추출
    product_info = extract_product_info_by_cell(df_input)
    product_info['source_file'] = os.path.basename(filepath)  # 원본 파일명도 기록
    return product_info

# === 메인 실행부 ===
EXCEL_DIR = r"D:\(주)에바스코스메틱 Dropbox\팀's shared workspace\EVAS COSMETIC\Project_RISE\100_QC DB\04_제품 표준서"
all_products = []

for fname in os.listdir(EXCEL_DIR):
    if fname.endswith('.xls') or fname.endswith('.xlsx'):
        fpath = os.path.join(EXCEL_DIR, fname)
        try:
            info = parse_excel_file(fpath)
            all_products.append(info)
            print(f"Parsed: {fname}")
        except Exception as e:
            print(f"Error parsing {fname}: {e}")

# DataFrame으로 통합
if all_products:
    df_all = pd.DataFrame(all_products)
    df_all.to_csv("all_products_info.csv", index=False, encoding='utf-8-sig')
    print("모든 제품 정보가 all_products_info.csv 파일로 저장되었습니다.")
else:
    print("추출된 제품 정보가 없습니다.")