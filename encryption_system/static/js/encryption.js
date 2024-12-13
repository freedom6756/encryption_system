window.onload = function () {
    console.log('页面已完全加载');

    // 绑定加密端与解密端按钮事件
    document.getElementById('connect-button').addEventListener('click', connectToDecrypt);
    document.getElementById('exchange-key-btn').addEventListener('click', exchangeKey);

    // 监听选择传输内容的变化
    document.getElementById('file-or-text').addEventListener('change', toggleFileUploadSection);

    // 初始化页面时判断选择框的值
    toggleFileUploadSection();

    function connectToDecrypt() {
        // 发送请求到后端，不传递密钥，只发起连接请求
        fetch('/connect_to_decrypt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({})  // 第一次连接时不传递密钥
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('已连接到解密端！');
                    // 显示密钥输入框
                    document.getElementById('key-exchange-section').style.display = 'block';
                } else {
                    alert('连接失败：' + data.message);
                }
            })
            .catch(error => {
                console.error('Error connecting to decrypt:', error);
                alert('连接失败！');
            });
    }


    // 交换密钥操作
    function exchangeKey() {
        var a = document.getElementById('encryption-private-key').value;  // 加密端私钥

        if (!a) {
            alert('请提供加密端私钥');
            return;
        }

        // 获取解密端私钥
        fetch('/get_decryption_private_key')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    var b = data.decryptionPrivateKey;  // 解密端私钥

                    // 发送请求到后端进行 Diffie-Hellman 密钥交换
                    fetch('/exchange_keys', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({a: a, b: b})
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.status === 'success') {
                                alert('密钥交换成功');
                                console.log(data.result);
                                const sharedKey = data.result.shared_secret_A;
                                document.getElementById('shared-key').value = sharedKey;
                                console.log('共享密钥:', sharedKey);

                                // 将共享密钥存储到 localStorage
                                localStorage.setItem('sharedKey', sharedKey);



                            } else {
                                alert('密钥交换失败：' + data.message);
                            }
                        })
                        .catch(error => {
                            console.error('Error during key exchange:', error);
                            alert('密钥交换失败');
                        });
                } else {
                    alert('获取解密端私钥失败：' + data.message);
                }
            })
            .catch(error => {
                console.error('Error fetching decryption private key:', error);
                alert('获取解密端私钥失败');
            });
    }


    // 控制文件上传表单的显示与隐藏
    function toggleFileUploadSection() {
        const fileOrTextSelect = document.getElementById('file-or-text');
        const fileUploadSection = document.getElementById('file-upload-section');

        if (fileOrTextSelect.value === 'file') {
            fileUploadSection.style.display = 'block';
        } else {
            fileUploadSection.style.display = 'none';
        }
    }
};

// 加密按钮事件
document.getElementById('encrypt-button').addEventListener('click', function () {
    const sharedKey = document.getElementById('shared-key').value;
    const algorithm = document.getElementById('encryption-algorithm').value;
    const message = document.getElementById('message').value;
    const fileOrText = document.getElementById('file-or-text').value;
    let dataToEncrypt = message;  // 默认加密消息内容
    encryptData(sharedKey, algorithm, dataToEncrypt);

});

// 加密数据并显示在密文框中
function encryptData(sharedKey, algorithm, dataToEncrypt) {
    //let encryptedData;

    // 使用不同的加密算法加密数据
    if (algorithm === 'AES') {
        encryptWithAES(sharedKey, dataToEncrypt);
    } else if (algorithm === 'RSA') {
        encryptWithRSA(sharedKey, dataToEncrypt);
    } else if (algorithm === 'RC4') {
        encryptWithRC4(sharedKey, dataToEncrypt);
    }

    // 将加密后的密文填入密文框
    // document.getElementById('ciphertext').value = encryptedData;

    // 保存加密后的数据到全局变量
    // window.encryptedData = encryptedData;  // 用于后续发送
}

document.getElementById('send-button').addEventListener('click', function () {
    // 获取加密后的数据
    const ciphertext = document.getElementById('ciphertext').value;

    // 检查加密数据是否为空
    if (!ciphertext) {
        alert('请先加密数据');
        return;
    }

    // 将加密数据保存为txt文件
    const encryptedBlob = new Blob([ciphertext], {type: 'text/plain'});
    const file = new File([encryptedBlob], 'encrypted_data.txt', {type: 'text/plain'});

    // 创建 FormData 对象，上传文件
    const formData = new FormData();
    formData.append('file', file);

    // 发送加密文件到后端
    sendEncryptedFile(formData);
});

// 发送加密文件到后端
function sendEncryptedFile(formData) {
    fetch('/send_encrypted_file', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('数据已发送');
            } else {
                alert('发送失败：' + data.message);
            }
        })
        .catch(error => {
            console.error('Error sending encrypted data:', error);
            alert('发送失败');
        });
}


function encryptWithAES(sharedKey, message) {
    fetch('/encrypt_with_aes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            sharedKey: sharedKey,
            message: message
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 将加密后的数据填充到密文框
                document.getElementById('ciphertext').value = data.encryptedData;
            } else {
                alert('加密失败：' + data.message);
            }
        })
        .catch(error => {
            console.error('加密请求失败:', error);
            alert('加密请求失败');
        });
}

function encryptWithRC4(sharedKey, message) {
    fetch('/encrypt_with_rc4', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            sharedKey: sharedKey,
            message: message
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 将加密后的数据填充到密文框
                document.getElementById('ciphertext').value = data.encryptedData;
            } else {
                alert('加密失败：' + data.message);
            }
        })
        .catch(error => {
            console.error('加密请求失败:', error);
            alert('加密请求失败');
        });
}

function encryptWithRSA(sharedKey, message) {
    fetch('/encrypt_with_rsa', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            sharedKey: sharedKey,
            message: message
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 将加密后的数据填充到密文框

                document.getElementById('shared-key').value = data.private_key;
                console.log(data.encryptedData.toString())
                localStorage.setItem('sharedKey', data.private_key);
                document.getElementById('ciphertext').value = data.encryptedData.toString();
            } else {
                alert('加密失败：' + data.message);
            }
        })
        .catch(error => {
            console.error('加密请求失败:', error);
            alert('加密请求失败');
        });
}

function handleFileUpload(event) {
    const file = event.target.files[0];  // 获取选择的文件
    if (file) {
        const reader = new FileReader();

        // 读取文件为文本内容
        reader.onload = function (e) {
            const fileContent = e.target.result;  // 文件内容
            document.getElementById('ciphertext-input').value = fileContent;  // 将内容填充到密文框
        };

        // 读取文件内容
        reader.readAsText(file);  // 如果你需要以其他格式处理，可以使用readAsDataURL等方法
    }
}

// 监听文件上传事件
document.getElementById('file-upload').addEventListener('change', function (event) {
    const file = event.target.files[0];  // 获取上传的文件
    if (file) {
        const reader = new FileReader();

        // 文件读取完成后的回调函数
        reader.onload = function (e) {
            // 将文件内容转换为Base64并填入明文框
            const base64Content = e.target.result.split(',')[1];  // 获取Base64部分
            document.getElementById('message').value = base64Content;  // 将Base64填入明文框
        };

        // 读取文件为Data URL（Base64）
        reader.readAsDataURL(file);
    }
});

document.getElementById("back-home-btn").onclick = function() {
    window.location.href = "/";  // 返回主页面，假设主页面为根路径
};
