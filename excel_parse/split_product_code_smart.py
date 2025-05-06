import pandas as pd
import os
import re

# === 설정 ===
RESULT_DIR = r"C:\Users\passe\.cursor\excel_parse_result"

# === 함수 정의 ===
def expand_code_range(code):
    """
    MLPF001~005 → [MLPF001, MLPF002, ..., MLPF005]
    """
    m = re.match(r'^([A-Za-z]+)(\d+)\s*~\s*(\d+)$', code)
    if m:
        prefix, start, end = m.group(1), m.group(2), m.group(3)
        width = len(start)
        start_num = int(start)
        end_num = int(end)
        return [f"{prefix}{str(i).zfill(width)}" for i in range(start_num, end_num+1)]
    return [code]

def split_product_codes(row):
    # 쉼표, 슬래시, 탭, 줄바꿈 등 다양한 구분자 지원
    codes = re.split(r'[,/\t\r\n]+', str(row['product_code']))
    codes = [c.strip() for c in codes if c.strip()]
    if not codes:
        return []
    result = []
    prefix_match = re.match(r'^([A-Za-z]+)', codes[0])
    prefix = prefix_match.group(1) if prefix_match else ''
    for idx, code in enumerate(codes):
        code = code.strip()
        # 범위 표기 처리 (MLPF001~005)
        expanded = expand_code_range(code)
        for ex_code in expanded:
            # 두 번째 이후 값이 숫자(혹은 숫자+문자)로 시작하면 prefix 붙이기
            if idx > 0 and prefix and re.match(r'^[0-9]+[A-Za-z0-9]*$', ex_code):
                ex_code = prefix + ex_code
            new_row = row.copy()
            new_row['product_code'] = ex_code
            result.append(new_row)
    return result

# === 메인 실행부 ===
for fname in os.listdir(RESULT_DIR):
    if fname.endswith('.csv'):
        fpath = os.path.join(RESULT_DIR, fname)
        df = pd.read_csv(fpath, dtype=str)
        new_rows = []
        for _, row in df.iterrows():
            new_rows.extend(split_product_codes(row))
        df_new = pd.DataFrame(new_rows)
        df_new.to_csv(fpath, index=False, encoding='utf-8-sig')
        print(f"Updated: {fname}")

print("모든 파일의 product_code 중첩이 분리되어 저장되었습니다.") 