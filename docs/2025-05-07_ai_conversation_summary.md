# 2025-05-07 AI 대화/설계 요약

## 📅 작업 일정표

| 날짜           | 작업 항목       | 예상 소요 시간 |
|----------------|----------------|---------------|
| 2025-05-07 오후 | UI 세팅        | 2시간          |
| 2025-05-07 오후 | Supabase 연결  | 2시간          |

---

## ✅ To Do List

1. 원료 데이타 파일 업데이트
2. 원료 MSDS 및 성분비 자료 pdf 파싱 도전

---

## 🛠️ n8n Batch PDF 파싱 & Supabase 업데이트 워크플로우

### 1. Dropbox 폴더 파일 리스트
- Dropbox Node: 지정 폴더 내 모든 PDF 파일 리스트 가져오기

### 2. 파일 다운로드
- Dropbox Download Node: 각 파일을 임시 경로로 다운로드

### 3. AI 모듈로 PDF 파싱
- Function Node 또는 HTTP Request Node:
  - Python/Node.js로 만든 AI 파싱 서버 호출 (예: FastAPI, Flask, Express, OpenAI API 등)
  - PDF 파일을 base64 또는 바이너리로 전송
  - 파싱 결과(JSON/CSV 등) 반환

### 4. Supabase 테이블에 데이터 업데이트
- HTTP Request Node (Supabase REST API 사용)
  - 파싱 결과를 Supabase 테이블에 insert/upsert

### 5. 파싱 실패 파일 관리
- IF Node: 파싱 결과가 실패/에러일 경우 분기
- Dropbox Move Node: 실패한 파일을 "/실패폴더"로 이동

### 6. 로깅/알림(선택)
- Slack/Email Node: 성공/실패 결과 알림

---

### 🗂️ 워크플로우 구조 예시

```
[Dropbox List Files]
        ↓
[For Each File]
        ↓
[Dropbox Download File]
        ↓
[AI 파싱 HTTP Request]
        ↓
[IF 파싱 성공?] ── No ──> [Dropbox Move to 실패폴더]
        │
       Yes
        ↓
[Supabase HTTP Request (Insert/Upsert)]
        ↓
[Slack/Email 알림 (선택)]
```

---

### 📝 각 단계별 상세 설정 팁

1. Dropbox List Files: 폴더 경로 지정, 파일 확장자 필터링(.pdf)
2. Dropbox Download File: 각 파일의 경로로 다운로드
3. AI 파싱 HTTP Request: AI 서버 엔드포인트 /parse-pdf, PDF 파일(base64), 파일명 등 전달, 파싱 결과(JSON)
4. Supabase HTTP Request: Supabase REST API 엔드포인트, 인증(anon key), Body: 파싱 결과(JSON)
5. IF/Move Node: 파싱 실패 시 Dropbox의 "실패폴더"로 파일 이동

---

### 🧩 AI 파싱 서버 예시 (Python FastAPI)

```python
from fastapi import FastAPI, File, UploadFile
import pdfplumber, pandas as pd

app = FastAPI()

@app.post("/parse-pdf")
async def parse_pdf(file: UploadFile = File(...)):
    # PDF 파싱 로직
    # 실패 시 {"success": False, "reason": "..."}
    # 성공 시 {"success": True, "data": {...}}
```

---

### 🚦 실행/운영 팁
- n8n 워크플로우는 "수동 실행" 또는 "스케줄러"로 돌릴 수 있음
- 파싱 실패 파일은 별도 폴더로 관리해 재처리/검수 가능
- Supabase에 중복 데이터 방지 위해 upsert(중복시 갱신) 추천

---

## 📈 문서 자동화 단계별 전략

### 🚀 1. MVP 단계
- **Bubble + PDF 플러그인**
  - Bubble UI에서 문서 미리보기/조회
  - PDF Conjurer, SelectPDF 등 플러그인으로 PDF 생성/다운로드
  - 빠른 프로토타입, 비개발자도 운영 가능

### 🔄 2. 확장 단계
- **n8n 트리거 + 외부 PDF 생성**
  - Bubble에서 "고급 PDF 생성" 버튼 → n8n Webhook 호출
  - n8n에서 Python/Node.js 등 외부 PDF 생성 엔진 실행
  - 복잡한 레이아웃, 대량 자동화, 이메일 발송, S3 업로드 등 확장
  - Bubble로 PDF 파일 URL 반환, 다운로드/이메일 등 후처리

### 🌐 3. 고도화 단계
- **React/Next.js 등으로 웹앱 개발**
  - 완전한 커스터마이징, 고급 UX, 대량 서비스, 실시간 협업 등 구현
  - Supabase, n8n, 외부 PDF 엔진 등과 자유롭게 연동
  - 모바일/PC 반응형, 고급 보안, 다양한 서비스 확장

---

## 📝 정리
- **MVP:** Bubble + PDF 플러그인 → 빠른 적용, 쉬운 유지보수
- **확장:** n8n + 외부 PDF 엔진 → 복잡한 문서, 대량 자동화, 고품질 PDF
- **고도화:** React 등 웹앱 → 완전한 커스터마이징, 다양한 서비스, 고급 UX

---

## 🔗 전체 워크플로우
1. **Bubble UI**
   - 품목코드(제품코드) 선택 (드롭다운, 검색 등)
   - "문서 조회" 트리거 버튼 클릭
2. **Bubble → Supabase Edge Function 호출**
   - API Connector 등으로 Supabase Edge Function(서버리스 함수) 호출
   - 품목코드 등 파라미터 전달
3. **Supabase Edge Function**
   - Supabase DB에서 해당 품목/제품의 모든 관련 데이터(성적서, 성분, 표준서 등) 추출
   - 필요한 데이터만 Bubble에 JSON 형태로 반환
4. **Bubble UI**
   - 반환받은 데이터를 화면에 문서 미리보기/조회 형태로 렌더링
   - 표, 텍스트, 이미지 등 실시간으로 확인/수정 가능
   - 필요시 PDF 출력 (PDF 플러그인으로 현재 화면을 PDF로 익스포트)
5. **확장/고도화 시**
   - "고급 PDF 생성" 버튼 → n8n Webhook 호출 → 외부 Python/Node.js에서 고품질 PDF 생성
   - Bubble에 PDF 파일 URL 반환, 다운로드/이메일 발송 등

---

## 🛠️ Bubble UI 구축 지원 가능 항목
1. **Bubble API Connector 설정**
   - Supabase Edge Function 연동 API Connector 플러그인 설정법
   - 엔드포인트, 메서드(POST), 헤더(anon key), 바디(JSON) 입력 예시
   - API 테스트 및 응답 데이터 구조 확인
   - API 호출 결과를 Bubble 데이터로 바인딩하는 방법
2. **Bubble UI 컴포넌트 설계**
   - 품목코드 선택 드롭다운/검색창, "문서 조회" 버튼, 트리거 워크플로우
   - 반복그룹(Repeating Group): 표, 리스트, 성분 등 동적 데이터 표시
   - 텍스트, 이미지, 표 등 미리보기 레이아웃 설계
   - 상태 관리(로딩, 에러, 결과 없음 등)
3. **PDF 플러그인 활용법**
   - PDF Conjurer, SelectPDF 등 플러그인 설치/설정법
   - Bubble UI와 동일하게 PDF로 익스포트하는 방법
   - PDF 생성 워크플로우(버튼 클릭 → PDF 다운로드/이메일 발송 등)
   - 동적 데이터 PDF에 반영하는 팁
4. **실제 워크플로우 예시/샘플**
   - 품목코드 선택 → API 호출 → 데이터 미리보기 → PDF 출력 전체 워크플로우 예시
   - Bubble 워크플로우(Workflow) 설정: 버튼 클릭 시 API 호출, 결과 저장, PDF 생성 트리거
5. **고급 팁/문제 해결**
   - API 인증(anon key) 헤더 추가 방법
   - API 응답 데이터 구조에 따라 Bubble 데이터 구조 설계
   - 반복그룹 내 동적 데이터 PDF 변환 시 주의점
   - Bubble에서 조건부 표시, 필터, 정렬 등 고급 UI/UX 구현
6. **추가 지원 가능**
   - Bubble 앱 구조 설계(페이지, 팝업, 네비게이션 등)
   - 디자인/UX 개선(모바일 대응, 반응형 등)
   - 테스트/디버깅 지원
   - n8n, 외부 API, Supabase 등과의 연동 고도화

---

## 📅 오늘의 작업 요약
- 연구 문서를 데이터화하여 Supabase에 업로드하는 자동화 파이프라인을 구축함
- lab_*.csv 파일 구조에 맞춰 Supabase 테이블을 자동 생성
- Python 스크립트로 데이터 일괄 업로드
- 이후 이 데이터를 활용해 문서 자동화(제품표준서, 성적서 등) 기획 시작
- Bubble, n8n, Supabase, 외부 PDF 엔진 등 단계별 확장 전략 수립 