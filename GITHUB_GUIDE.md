# GitHub 업로드 및 배포 가이드

이 가이드는 재무제표 분석기를 GitHub에 업로드하고 GitHub Pages를 통해 배포하는 방법을 안내합니다.

## 1. GitHub 저장소 생성

1. [GitHub](https://github.com/)에 로그인합니다.
2. 우측 상단의 '+' 버튼을 클릭하고 'New repository'를 선택합니다.
3. 저장소 이름을 'financial-statements'로 입력합니다 (다른 이름도 가능).
4. 저장소 설명을 추가하고 'Public'으로 설정합니다.
5. 'Create repository' 버튼을 클릭합니다.

## 2. 저장소에 파일 업로드

### 방법 1: GitHub 웹 인터페이스 사용

1. 생성된 저장소 페이지에서 'uploading an existing file' 링크를 클릭합니다.
2. 다음 파일들을 끌어다 놓거나 '파일 선택' 버튼을 클릭하여 업로드합니다:
   - `index.html`
   - `README.md`
   - `.nojekyll`
3. 'Commit changes' 버튼을 클릭합니다.

### 방법 2: Git 명령어 사용

1. Git이 설치되어 있지 않다면 [Git 다운로드](https://git-scm.com/downloads)에서 설치합니다.
2. 명령 프롬프트(CMD) 또는 PowerShell을 열고 작업 폴더로 이동합니다:
   ```bash
   cd C:\Users\toron\Desktop\cursor AI2
   ```
3. 다음 명령어를 순서대로 실행합니다:
   ```bash
   git init
   git add index.html README.md .nojekyll
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/your-username/financial-statements.git
   git push -u origin main
   ```
   (`your-username`을 실제 GitHub 사용자 이름으로 바꾸세요)

## 3. GitHub Pages 활성화

1. GitHub 저장소 페이지에서 'Settings' 탭을 클릭합니다.
2. 좌측 메뉴에서 'Pages'를 클릭합니다.
3. 'Source' 섹션에서 'Branch'를 'main'으로 설정하고 폴더를 '/(root)'로 설정합니다.
4. 'Save' 버튼을 클릭합니다.
5. 페이지가 배포되기까지 몇 분 정도 기다립니다.
6. 배포가 완료되면 페이지 상단에 사이트 URL이 표시됩니다:
   `https://your-username.github.io/financial-statements/`

## 4. 사용 방법

1. 배포된 사이트에 접속합니다:
   `https://your-username.github.io/financial-statements/`
2. Alpha Vantage API 키를 입력하고 기업 분석을 시작합니다.
3. 또는 URL에 API 키를 직접 포함시킬 수 있습니다:
   `https://your-username.github.io/financial-statements/?apikey=YOUR_API_KEY`

## 5. 문제 해결

### CORS 오류

CORS 정책으로 API 호출이 실패할 경우:

1. [CORS Anywhere 데모 페이지](https://cors-anywhere.herokuapp.com/corsdemo)에 접속합니다.
2. 'Request temporary access to the demo server' 버튼을 클릭합니다.
3. 페이지를 새로고침하고 다시 시도합니다.

### API 키 오류

1. API 키가 올바른지 확인합니다.
2. [Alpha Vantage](https://www.alphavantage.co/support/#api-key)에서 새 API 키를 발급받습니다.
3. API 사용량 제한(분당 5회, 일일 500회)을 초과했는지 확인합니다.

### 기타 문제

브라우저의 개발자 도구(F12)의 콘솔 탭에서 오류 메시지를 확인하세요. 