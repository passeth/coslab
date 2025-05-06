import pandas as pd
from openpyxl import load_workbook
from typing import Dict

# 엑셀 파일 경로
file_path = "docsample/제품표준서_EVCO1097_(KBOW001)-키스바이 로즈마인 프래그런스 오일워시- 글래머 센슈얼리티.xls"

# 모든 시트 이름 확인
xls = pd.ExcelFile(file_path)
print(xls.sheet_names)

# 각 시트별로 데이터프레임으로 읽기
for sheet in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet)
    print(f"시트명: {sheet}")
    print(df.head(20))  # 상위 20행만 출력

def parse_excel_file(filepath: str) -> Dict[str, pd.DataFrame]:
    wb = load_workbook(filepath, data_only=True)
    ws = wb[SHEET_INPUT]
    # 1. 제품 정보 robust 추출
    product_info = robust_parse_product_info(ws)
    # ... 이하 동일
