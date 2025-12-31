const path = require('path');
const f = require('./jcap_20201228.js'); // 确保路径正确

// 监听标准输入
const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});

f.onRuntimeInitialized = () => {
    // 告知 Python：我已经准备好了
    console.log("READY");

    rl.on('line', (line) => {
        try {
            const args = JSON.parse(line);
            var result // 假设传过来的是 JSON [arg0, arg1]
            if (args[0]==='getEncryptData'){
                result = f.getEncryptData(args[1], args[2]);
            } else {
                result = f.getCaptchaAuth(args[1])
            }
            console.log(JSON.stringify({status: "success", data: result}));
        } catch (e) {
            console.log(JSON.stringify({status: "error", message: e.message}));
        }
    });
};