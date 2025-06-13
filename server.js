const express = require('express');
const cors = require('cors');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

const app = express();
app.use(cors());

app.get('/av', async (req, res) => {
    // 모든 쿼리 파라미터를 Alpha Vantage로 전달
    const params = new URLSearchParams(req.query).toString();
    const url = `https://www.alphavantage.co/query?${params}`;
    try {
        const response = await fetch(url);
        const data = await response.json();
        res.json(data);
    } catch (err) {
        res.status(500).json({ error: 'Proxy fetch failed', detail: err.message });
    }
});

app.get('/stock', async (req, res) => {
    // 모든 쿼리 파라미터를 Flask 서버로 전달
    const params = new URLSearchParams(req.query).toString();
    const url = `http://localhost:5000/stock?${params}`;
    try {
        const response = await fetch(url);
        const text = await response.text();
        try {
            const data = JSON.parse(text);
            if (data.error) {
                console.error('[Flask Error]', data.error, data.detail || '');
                res.status(500).json({ error: data.error, detail: data.detail || '' });
            } else {
                res.json(data);
            }
        } catch (jsonErr) {
            console.error('[Proxy JSON Parse Error]', jsonErr, '\nRaw response:', text);
            res.status(500).json({ error: 'Flask 서버 응답 파싱 실패', detail: jsonErr.message, raw: text });
        }
    } catch (err) {
        console.error('[Proxy Fetch Error]', err);
        res.status(500).json({ error: 'Flask proxy fetch failed', detail: err.message });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Alpha Vantage Proxy running on port ${PORT}`);
});