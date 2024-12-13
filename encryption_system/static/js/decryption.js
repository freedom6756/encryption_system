window.onload = function () {
    console.log('页面已完全加载');

    // 绑定加密端与解密端按钮事件
    document.getElementById('start-socket-btn').addEventListener('click', startSocketService);
    document.getElementById('refresh-btn').addEventListener('click', refreshFileList);


    // 启动 Socket 服务
    function startSocketService() {
        fetch('/start_socket_service', {
            method: 'POST',
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Socket 服务已启动！');
                    // 启动后显示解密端私钥输入框
                    document.getElementById('decryption-private-key-section').style.display = 'block';
                } else {
                    alert('启动 Socket 服务失败：' + data.message);
                }
            })
            .catch(error => {
                console.error('Error starting socket service:', error);
                alert('启动 Socket 服务失败！');
            });
    }

    // 刷新文件列表
    function refreshFileList() {
        const fileListUl = document.getElementById('file-list-ul');
        fileListUl.innerHTML = '';  // 清空当前列表

        // 请求后端获取文件列表
        fetch('/get-file-list')
            .then(response => response.json())
            .then(files => {
                files.forEach(file => {
                    const li = document.createElement('li');
                    // 创建下载链接
                    const downloadLink = document.createElement('a');
                    downloadLink.href = `/download/${file}`;  // 设置文件下载链接
                    downloadLink.textContent = file;
                    li.appendChild(downloadLink);
                    fileListUl.appendChild(li);
                });
            })
            .catch(error => {
                console.error('Error fetching file list:', error);
            });
    }

};


// 解密按钮事件
document.getElementById('decrypt-button').addEventListener('click', function () {
    sharedKey = document.getElementById('shared_key').value;
    const algorithm = document.getElementById('decryption-algorithm').value;
    const ciphertext = document.getElementById('ciphertext-input').value;
    let dataToDecrypt = ciphertext;
    decryptData(sharedKey, algorithm, dataToDecrypt);
});

// 解密数据并显示在密文框中
function decryptData(sharedKey, algorithm, dataToDecrypt) {
    let decryptedData;

    // 使用不同的解密算法解密数据
    if (algorithm === 'AES') {
        decryptWithAES(sharedKey, dataToDecrypt);  // 注意这里传递的是 dataToDecrypt（即密文）
    } else if (algorithm === 'RSA') {
        listenForSharedKey();
        shared_key=localStorage.getItem('sharedKey');
        decryptWithRSA(shared_key, dataToDecrypt);  // 请确保你已经实现了 RSA 解密函数
    } else if (algorithm === 'RC4') {
        decryptWithRC4(sharedKey, dataToDecrypt);  // 请确保你已经实现了 RC4 解密函数
    }
}

// AES 解密函数
function decryptWithAES(sharedKey, dataToDecrypt) {
    fetch('/decrypt_with_aes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            sharedKey: sharedKey,  // 共享密钥
            ciphertext: dataToDecrypt  // 密文
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 将解密后的数据填充到输出框
                document.getElementById('output').value = data.decryptedData;
            } else {
                alert('解密失败：' + data.message);
            }
        })
        .catch(error => {
            console.error('解密请求失败:', error);
            alert('解密请求失败');
        });
}

function decryptWithRC4(sharedKey, dataToDecrypt) {
    fetch('/decrypt_with_rc4', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            sharedKey: sharedKey,  // 共享密钥
            ciphertext: dataToDecrypt  // 密文
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.status === 'success') {
                // 将解密后的数据填充到输出框
                document.getElementById('output').value = data.decryptedData;
            } else {
                alert('解密失败：' + data.message);
            }
        })
        .catch(error => {
            console.error('解密请求失败:', error);
            alert('解密请求失败');
        });
}

function decryptWithRSA(sharedKey, dataToDecrypt) {
    fetch('/decrypt_with_rsa', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            sharedKey: sharedKey,  // 共享密钥
            ciphertext: dataToDecrypt  // 密文
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 将解密后的数据填充到输出框
                document.getElementById('output').value = data.decryptedData;
            } else {
                alert('解密失败：' + data.message);
            }
        })
        .catch(error => {
            console.error('解密请求失败:', error);
            alert('解密请求失败');
        });
}



document.getElementById('save-file-btn').addEventListener('click', function () {
    const ciphertext = document.getElementById('output').value.trim();

    if (!ciphertext) {
        alert("请先解密密文");
        return;
    }

    const binaryData = atob(ciphertext);
    const byteArray = new Uint8Array(binaryData.length);

    for (let i = 0; i < binaryData.length; i++) {
        byteArray[i] = binaryData.charCodeAt(i);
    }

    // 创建一个FormData对象，用于上传数据
    const formData = new FormData();
    const fileBlob = new Blob([byteArray], { type: getMimeTypeFromHeader(byteArray) });

    // 获取当前时间戳
    const timestamp = Date.now();
    // 生成文件名，添加时间戳
    const fileName = 'decrypted_file_' + timestamp + getFileExtensionFromMimeType(fileBlob.type);
    formData.append('file', fileBlob, fileName);

    // 发送到后端保存
    fetch('/save-file', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              alert("文件保存成功！");
          } else {
              alert("文件保存失败！");
          }
      }).catch(error => {
          console.error("文件上传失败:", error);
      });
});



function getMimeTypeFromHeader(byteArray) {
    // 获取前 4 个字节并转换为十六进制字符串
    const hex = Array.from(byteArray.slice(0, 4)) // 获取前4个字节
                     .map(b => b.toString(16).padStart(2, '0')) // 转换为16进制
                     .join(''); // 合并为一个字符串

    console.log("File header (hex):", hex);  // 打印实际的文件头

    // 根据文件的Hex头判断文件类型
    if (hex.startsWith('8950')) {
        return 'image/png';
    } else if (hex.startsWith('ffd8')) {
        return 'image/jpeg';
    } else if (hex.startsWith('2550')) {
        return 'application/pdf';
    } else if (hex.startsWith('504b')) {
        return 'application/zip';
    } else {
        return 'application/octet-stream';  // 默认处理为通用二进制文件
    }
}



// 根据MIME类型确定文件扩展名
function getFileExtensionFromMimeType(mimeType) {
    switch (mimeType) {
        case 'image/png':
            return '.png';
        case 'image/jpeg':
            return '.jpg';
        case 'application/pdf':
            return '.pdf';
        case 'application/zip':
            return '.zip';
        default:
            return '.bin';
    }
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

document.getElementById('submit-private-key').addEventListener('click', submitPrivateKey);

function submitPrivateKey() {
    var decryptionPrivateKey = document.getElementById('decryption-private-key').value;

    if (!decryptionPrivateKey) {
        alert('请提供解密端私钥');
        return;
    }

    fetch('/submit_decryption_private_key', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ decryptionPrivateKey: decryptionPrivateKey })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('解密端私钥提交成功');

            // 清空 localStorage 中的 sharedKey
            localStorage.removeItem('sharedKey');

            // 提交成功后开始监听 sharedKey 的变化
            listenForSharedKey();
        } else {
            alert('提交失败：' + data.message);
        }
    })
    .catch(error => {
        console.error('Error submitting decryption private key:', error);
        alert('提交失败');
    });
}

function listenForSharedKey() {
    // 设置定时器，每500毫秒检查一次 sharedKey 是否存在
    const interval = setInterval(function() {
        sharedKey = localStorage.getItem('sharedKey');

        if (sharedKey) {
            // 一旦获取到 sharedKey，将其填充到输入框
            document.getElementById('shared_key').value = sharedKey;


            // 停止监听，因为已经获取到了共享密钥
            clearInterval(interval);
        }
    }, 500);  // 每500毫秒检查一次
}
