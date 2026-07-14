# 🎁 선물멘토 (Gift Mentor)

받는 사람의 정보만 입력하면 AI가 딱 맞는 선물 3가지를 추천해주는 웹 서비스입니다.

**배포 URL**: https://gift-recommender-navy.vercel.app

---

## 📌 서비스 소개

선물을 고를 때 무엇을 사야 할지 고민되는 순간, AI에게 물어보세요.
받는 사람과의 관계, 나이, 성별, 예산, 취향/관심사를 입력하면 Google Gemini API가 조건에 맞는 선물 3가지와 추천 이유를 제안해줍니다.

### 주요 기능
- 🏠 홈 (서비스 소개)
- 🎯 AI 선물 추천 (입력 → AI 분석 → 결과 출력)
- 📖 이용 방법 안내
- ❓ FAQ

---

## 🛠 기술 스택

| 구분 | 기술 |
|---|---|
| 프론트엔드 | HTML5, CSS3, Vanilla JavaScript |
| 백엔드 | Python (Vercel Serverless Functions) |
| AI API | Google Gemini API (`gemini-flash-latest`) |
| 배포 | Vercel |
| 버전 관리 | Git / GitHub |

---

## 📁 프로젝트 구조

```
gift_recommender/
├── index.html          # 메인 페이지 (홈/추천/이용방법/FAQ)
├── css/
│   └── style.css       # 스타일시트 (반응형 포함)
├── js/
│   └── script.js       # 프론트엔드 로직 (폼 처리, fetch 요청)
├── api/
│   └── recommend.py    # AI 선물 추천 API (Vercel Serverless Function)
├── requirements.txt     # Python 패키지 의존성
├── vercel.json          # Vercel 배포 설정 (정적 파일 + API 라우팅)
└── README.md
```

---

## 🤖 AI 기능 설계

| 항목 | 내용 |
|---|---|
| **입력** | 받는 사람과의 관계, 나이, 성별, 예산(원), 취향/관심사 |
| **출력** | 선물 추천 3가지 (이름 + 추천 이유) |
| **처리 흐름** | 사용자 입력 → JS가 `/api/recommend`로 POST 요청 → 서버에서 프롬프트 생성 → Gemini API 호출 → JSON 파싱 후 결과 반환 → 화면에 카드 형태로 표시 |

### 실패 처리 기준

| 상황 | 처리 방식 |
|---|---|
| 필수값(관계/나이/예산) 누락 | 400 응답, "필수값을 입력하세요" 안내 |
| 요청 형식 오류 | 400 응답, "요청 형식이 올바르지 않습니다" |
| API 키 미설정 | 500 응답, 서버 설정 오류 안내 |
| AI 응답 없음/파싱 실패 | 502 응답, "AI가 응답을 생성하지 못했습니다" |
| 응답 지연(타임아웃) | 프론트에서 25초 초과 시 "응답이 지연되고 있습니다" 안내 |

---

## 🚀 로컬 실행 방법

### 1. 저장소 클론
```bash
git clone https://github.com/gayun32/gift_recommender.git
cd gift_recommender
```

### 2. Python 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정 (아래 "환경 변수 설정" 참고)

### 4. 로컬 프론트엔드 확인
`index.html`을 브라우저로 직접 열면 화면 구성은 확인할 수 있지만, AI 추천 기능(`/api/recommend`)은 Vercel 서버리스 환경에서만 동작하므로 로컬에서는 정상 호출되지 않습니다.
API 기능까지 로컬에서 테스트하려면 [Vercel CLI](https://vercel.com/docs/cli)를 설치한 뒤 아래 명령어를 사용하세요.
```bash
npm i -g vercel
vercel dev
```

---

## ☁️ 배포 방법 (Vercel)

1. [Vercel](https://vercel.com)에 GitHub 계정으로 로그인
2. **Add New → Project** 클릭 후 이 저장소(`gift_recommender`) Import
3. Framework Preset: **Other**
4. **Environment Variables**에 `GEMINI_API_KEY` 등록 (아래 참고)
5. **Deploy** 클릭
6. 이후 코드 수정 시 `main` 브랜치에 push하면 자동으로 재배포됩니다.

---

## 🔑 환경 변수 설정

이 프로젝트는 Google Gemini API 키를 환경 변수로 관리합니다. **API 키는 절대 코드에 하드코딩하거나 저장소에 커밋하지 않습니다.**

| 변수명 | 설명 |
|---|---|
| `GEMINI_API_KEY` | Google AI Studio에서 발급받은 Gemini API 키 |

### 로컬 개발 시
프로젝트 루트에 `.env` 파일을 만들고 아래와 같이 작성하세요 (`.env`는 `.gitignore`에 등록되어 있어 커밋되지 않습니다).
```dotenv
GEMINI_API_KEY=발급받은_실제_API_키
```
키 발급은 [Google AI Studio](https://aistudio.google.com/apikey)에서 받을 수 있습니다.

### Vercel 배포 시
Vercel 대시보드 → 프로젝트 → **Settings → Environment Variables**에서 동일한 이름(`GEMINI_API_KEY`)으로 등록합니다. (Production/Preview/Development 환경 모두 체크)

---

## 📱 반응형 지원

`css/style.css`에 아래 두 가지 화면 크기 기준 미디어 쿼리가 적용되어 있습니다.
- 태블릿 이하 (max-width: 768px)
- 모바일 (max-width: 480px)

---

## 📄 라이선스
개인 학습 프로젝트로 제작되었습니다.
