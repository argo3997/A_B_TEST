# 🧪 A/B 테스트 프로젝트: 새 결제 페이지 UI 테스트

## 📋 프로젝트 개요

이커머스 플랫폼의 결제 페이지 UI 개선 효과를 검증하기 위한 A/B 테스트 분석 프로젝트입니다.

### 실험 설계
- **실험 기간**: 2024년 5월 1일 ~ 5월 31일 (1개월)
- **실험 대상**: 결제 페이지 진입 고객 20,000명
- **Control (A)**: 기존 결제 UI
- **Treatment (B)**: 새 결제 UI (간소화된 폼, 진행 단계 표시, 간편결제 강조)

### 핵심 결과
| 지표 | Control | Treatment | 변화 |
|------|---------|-----------|------|
| 전환율 | 12.96% | 17.90% | **+38.1%** |
| 객단가 | 80,422원 | 88,147원 | **+9.6%** |
| 결제시간 | 181초 | 121초 | **-33%** |

---

## 📁 폴더 구조

```
AB_Test_Checkout_UI/
├── data/
│   ├── raw/              # 원본 데이터
│   └── processed/        # 가공 데이터
├── notebooks/            # Jupyter 노트북
├── scripts/              # Python 스크립트
├── outputs/
│   ├── figures/          # 시각화
│   └── reports/          # 분석 결과
├── tableau/              # 태블로 대시보드
└── docs/                 # 문서
```

---

## 🚀 시작하기

### 1. 환경 설정

```bash
# 가상환경 생성 (선택)
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# 라이브러리 설치
pip install -r requirements.txt
```

### 2. 데이터 생성

```bash
# 베이스 데이터 생성
python scripts/01_generate_base_data.py

# A/B 테스트 데이터 생성
python scripts/02_generate_ab_test_data.py
```

### 3. 분석 실행

```bash
# Jupyter Notebook 실행
jupyter notebook notebooks/AB_Test_Analysis.ipynb

# 또는 스크립트 실행
python scripts/03_analysis.py
```

---

## 📊 주요 분석 내용

### 1. 전환율 분석
- 그룹별 전환율 비교
- 통계적 유의성 검정 (Chi-square, Z-test)
- 95% 신뢰구간

### 2. 세그먼트 분석
- 디바이스별 (모바일/데스크톱/태블릿)
- 연령대별 (20대~60대 이상)
- 지역별

### 3. 추가 지표 분석
- 객단가 (AOV)
- 결제 소요 시간
- 결제 수단 변화

### 4. 시계열 분석
- 일별 전환율 추이
- 누적 전환율 (수렴 확인)
- 요일별 패턴

---

## 💡 핵심 인사이트

1. **모바일 최적화 효과**: 모바일에서 전환율 개선 폭이 가장 큼 (+5.68%p)
2. **젊은 층 적응**: 20~30대에서 새 UI 효과가 극대화 (+6%p 이상)
3. **간편결제 증가**: 카카오페이, 네이버페이 비중 상승
4. **결제 경험 개선**: 결제 소요 시간 33% 단축

---

## ✅ 결론 및 권고

**권고사항**: 새 결제 UI 전체 적용

**예상 비즈니스 임팩트**:
- 전환율 상승 효과: +38%
- 객단가 상승 효과: +9.6%
- **복합 효과: 월 매출 약 52% 증가 예상**

---

## 🛠 기술 스택

- **데이터 분석**: Python, Pandas, NumPy, SciPy
- **시각화**: Matplotlib, Seaborn, Tableau
- **통계 검정**: Chi-square, Z-test, 신뢰구간

---

## 📧 Contact

- **작성자**: 이창규
- **이메일**: argo3997@gmail.com
- **LinkedIn**: [LinkedIn URL]
- **GitHub**: [GitHub URL]

---

*이 프로젝트는 포트폴리오 목적으로 시뮬레이션 데이터를 사용하여 제작되었습니다.*
