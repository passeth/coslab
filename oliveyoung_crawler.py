from playwright.sync_api import sync_playwright

url = "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000188240"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(2000)  # 2초 대기
    # 상세페이지 이미지가 들어있는 부분의 셀렉터를 정확히 지정
    image_elements = page.query_selector_all('.iPrdViewimg img')
    image_urls = []
    for img in image_elements:
        src = img.get_attribute('data-src') or img.get_attribute('src')
        if src and src.startswith('http'):
            image_urls.append(src)
    browser.close()

print("상세페이지 이미지 URL 목록:")
for img_url in image_urls:
    print(img_url) 