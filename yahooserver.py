from flask import Flask, request, jsonify
import yfinance as yf
import numpy as np
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# 네이버 금융 재무제표 크롤러 함수
# 종목코드(6자리, 예: 005930) 입력 시 dict 반환

def get_naver_financials(code):
    url = f"https://finance.naver.com/item/main.nhn?code={code}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    # 연간 재무제표 테이블
    table = soup.select_one('div.section.cop_analysis div.sub_section tbody')
    if not table:
        return {}
    rows = table.find_all('tr')
    # 연도 추출
    years = [th.get_text(strip=True) for th in rows[0].find_all('th')][1:]
    # 주요 항목 추출
    result = {}
    for row in rows[1:]:
        tds = row.find_all(['th', 'td'])
        if not tds: continue
        name = tds[0].get_text(strip=True)
        values = [td.get_text(strip=True).replace(',', '').replace('N/A', '') for td in tds[1:]]
        # 항목명 매핑
        if name in ['매출액', '영업이익', '당기순이익', 'EPS(원)']:
            key = {'매출액': 'Total Revenue', '영업이익': 'Operating Income', '당기순이익': 'Net Income', 'EPS(원)': 'Basic EPS'}[name]
            for i, y in enumerate(years):
                if y not in result:
                    result[y] = {}
                try:
                    val = float(values[i]) if values[i] else None
                except:
                    val = None
                result[y][key] = val
    return result

@app.route('/stock', methods=['GET'])
def get_stock():
    symbol = request.args.get('symbol')
    history_flag = request.args.get('history')
    if not symbol:
        return jsonify({'error': 'symbol 파라미터가 필요합니다.'}), 400
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        financials = ticker.financials
        balance_sheet = ticker.balance_sheet
        # 인덱스/컬럼 문자열 변환
        if not financials.empty:
            fin_dict = financials.T.copy()
            fin_dict.index = fin_dict.index.map(str)
            fin_dict.columns = fin_dict.columns.map(str)
            fin_json = fin_dict.to_dict(orient="index")
        else:
            fin_json = {}
        if not balance_sheet.empty:
            bal_dict = balance_sheet.T.copy()
            bal_dict.index = bal_dict.index.map(str)
            bal_dict.columns = bal_dict.columns.map(str)
            bal_json = bal_dict.to_dict(orient="index")
        else:
            bal_json = {}
        # 한국 종목이면 네이버 금융에서 재무제표 보완
        if symbol.endswith('.KS') or symbol.endswith('.KQ'):
            code = symbol.split('.')[0]
            naver_fin = get_naver_financials(code)
            # 네이버 연도별 데이터가 있으면 financials에 병합(덮어쓰기)
            for y, vals in naver_fin.items():
                if y not in fin_json:
                    fin_json[y] = {}
                fin_json[y].update(vals)
        # NaN, inf, -inf를 None으로 변환
        def clean_nan(obj):
            if isinstance(obj, dict):
                return {k: clean_nan(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [clean_nan(v) for v in obj]
            elif isinstance(obj, float):
                if np.isnan(obj) or np.isinf(obj):
                    return None
                else:
                    return obj
            else:
                return obj
        fin_json = clean_nan(fin_json)
        bal_json = clean_nan(bal_json)
        # 시세 차트 데이터
        hist_json = {}
        if history_flag:
            try:
                hist = ticker.history(period="1y")
                if not hist.empty and 'Close' in hist.columns:
                    hist_json = {str(k): v for k, v in hist['Close'].to_dict().items()}
                else:
                    hist_json = {}
            except Exception as e:
                hist_json = {}
        return jsonify({
            'info': info,
            'financials': fin_json,
            'balance_sheet': bal_json,
            'history': hist_json
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("[INFO] Flask 서버가 http://localhost:5000 에서 실행됩니다.")
    app.run(host='0.0.0.0', port=5000, debug=True)