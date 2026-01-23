const express = require('express');
const bodyParser = require('body-parser');
const f = require('./jcap_20201228.js');

const app = express();
app.use(bodyParser.json({ limit: '1mb' }));

let ready = false;
let queue = [];
let working = false;

// WASM 初始化
f.onRuntimeInitialized = () => {
    ready = true;
    console.log('WASM READY');
};

function runNext() {
    if (working || queue.length === 0 || !ready) return;

    working = true;
    const { req, res } = queue.shift();

    try {
        let result;
        if (req.type === 'getEncryptData') {
            result = f.getEncryptData(req.a, req.b);
        } else {
            result = f.getCaptchaAuth(req.a);
        }
        res.json({ code: 0, data: result });

    } catch (e) {
        res.status(500).json({ code: -1, msg: e.message });

    } finally {
        working = false;
        setImmediate(runNext); // 继续处理队列
    }
}

app.post('/encrypt', (req, res) => {
    if (!ready) {
        return res.status(503).json({ msg: 'WASM not ready' });
    }
    queue.push({ req: req.body, res });
    runNext();
});

app.post('/captchaAuth', (req, res) => {
    if (!ready) {
        return res.status(503).json({ msg: 'WASM not ready' });
    }
    queue.push({ req: req.body, res });
    runNext();
});

app.get('/health', (_, res) => {
    res.send('OK');
});

app.listen(3000, () => {
    console.log('Encrypt service listening on 3000');
});
