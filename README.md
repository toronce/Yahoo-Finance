# Alpha Vantage 재무제표 분석기

실제 기업의 재무 데이터를 Alpha Vantage API를 통해 분석하는 웹 애플리케이션입니다.

## 주요 기능

- Alpha Vantage API를 사용한 실시간 재무 데이터 분석
- 회사 개요, 손익계산서, 재무상태표 데이터 제공
- 연도별 매출 및 이익 추이 차트
- 6개의 인기 기업(Apple, Microsoft, Google, Tesla, Amazon, NVIDIA) 빠른 분석

## 사용 방법

1. 사이트에 접속합니다: [https://your-username.github.io/financial-statements/](https://your-username.github.io/financial-statements/)
2. [Alpha Vantage](https://www.alphavantage.co/support/#api-key)에서 무료 API 키를 받습니다.
3. 받은 API 키를 입력합니다.
4. 분석하고 싶은 기업의 티커 심볼(예: AAPL, MSFT)을 입력하여 분석합니다.

또는 URL에 API 키를 직접 포함시킬 수 있습니다:
```
https://your-username.github.io/financial-statements/?apikey=YOUR_API_KEY
```

## 기술 스택

- HTML/CSS/JavaScript
- Tailwind CSS
- Chart.js
- Font Awesome

## 알려진 문제점

- CORS 정책으로 인해 일부 브라우저에서 API 호출이 차단될 수 있습니다.
- Alpha Vantage의 무료 API는 분당 5회, 일일 500회의 호출 제한이 있습니다.

## 라이선스

MIT 