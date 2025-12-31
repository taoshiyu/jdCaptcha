
// window.Module = {
//     onRuntimeInitialized: function() {
//         console.log("Wasm 模块初始化成功！");
//
//         if (window.Module.f.getEncryptData) {
//             // 导出到你自己的全局命名空间下
//             window.MyCrypto = {
//                 encrypt: window.Module.f.getEncryptData
//             };
//             console.log("getEncryptData 已成功导出到 window.MyCrypto.encrypt");
//         }
//     }
// };
const f = require("./jcap_20201228.js");
console.log('i am here')
setTimeout(()=>{
    global.getEncryptData = f.getEncryptData
    },
)


