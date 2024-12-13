// Filter algorithms based on search
function filterAlgorithms() {
    const query = document.getElementById('search').value.toLowerCase();
    const categories = document.querySelectorAll('#algorithm-list .category');

    categories.forEach(category => {
        const sublist = category.nextElementSibling; // 获取分类下的子列表

        // 先检查分类项自身是否匹配
        const categoryText = category.textContent.toLowerCase();
        const categoryMatch = categoryText.includes(query);

        let sublistVisible = false;

        // 检查子列表中的每个子项
        const subItems = sublist ? sublist.querySelectorAll('li') : [];
        subItems.forEach(subItem => {
            const subItemText = subItem.textContent.toLowerCase();
            if (subItemText.includes(query)) {
                subItem.style.display = 'block';
                sublistVisible = true;
            } else {
                subItem.style.display = 'none';
            }
        });

        // 如果分类项或其子项匹配搜索内容，则显示该分类，并展开子列表
        if (categoryMatch || sublistVisible) {
            category.style.display = 'block';
            if (sublist) {
                sublist.style.display = 'block'; // 展开子列表
            }
        } else {
            category.style.display = 'none';
            if (sublist) {
                sublist.style.display = 'none'; // 隐藏子列表
            }
        }
    });
}


// Toggle category list visibility and change arrow direction
function toggleCategory(categoryId) {
    const category = document.getElementById(categoryId);
    const arrow = category.previousElementSibling.querySelector('.arrow');

    // Toggle the sublist visibility
    if (category.style.display === 'none' || category.style.display === '') {
        category.style.display = 'block';
        arrow.textContent = '▼';  // Change arrow to down
    } else {
        category.style.display = 'none';
        arrow.textContent = '►';  // Change arrow to right
    }
}

// Change the form dynamically based on selected algorithm
$(document).ready(function() {
    // Add event listener for clicking on algorithms
    $("#algorithm-list li[data-algorithm]").click(function(event) {
        // Prevent category toggle from triggering
        event.stopPropagation();

        const algorithm = $(this).data('algorithm');
        loadAlgorithmForm(algorithm);
    });
});

function loadAlgorithmForm(algorithm) {
    let formUrl = ''; // 初始化表单URL
    let algorithmName = '';  // 用来存储算法名称

    // 根据算法名称选择对应的表单文件
    switch(algorithm) {
        case 'caesar_crypto':
            formUrl = '/static/forms/caesar_form.html';
            algorithmName = 'Caesar Cipher';
            break;
        case 'keyword_crypto':
            formUrl = '/static/forms/keyword_form.html';
            algorithmName = 'Keyword Cipher';
            break;
        case 'affine_crypto':
            formUrl = '/static/forms/affine_form.html';
            algorithmName = 'Affine Cipher';
            break;
        case 'multiliteral_crypto':
            formUrl = '/static/forms/multiliteral_form.html';
            algorithmName = 'Multiliteral Cipher';
            break;
        case 'vigenere_crypto':
            formUrl = '/static/forms/vigenere_form.html';
            algorithmName = 'Vigenere Cipher';
            break;
        case 'autokey_plaintext_crypto':
            formUrl = '/static/forms/autokey_plaintext_form.html';
            algorithmName = 'Autokey Plaintext Cipher';
            break;
        case 'autokey_ciphertext_crypto':
            formUrl = '/static/forms/autokey_ciphertext_form.html';
            algorithmName = 'Autokey Ciphertext Cipher';
            break;
        case 'playfair_crypto':
            formUrl = '/static/forms/playfair_form.html';
            algorithmName = 'Playfair Cipher';
            break;
        case 'double_playfair_crypto':
            formUrl = '/static/forms/double_playfair_form.html';
            algorithmName = 'Double Playfair Cipher';
            break;
        case 'permutation_crypto':
            formUrl = '/static/forms/permutation_form.html'
            algorithmName = 'Permutation Cipher'
            break;
        case 'column_permutation_crypto':
            formUrl = '/static/forms/column_permutation_form.html'
            algorithmName = 'Column Permutation Cipher'
            break;
        case 'double_transposition_crypto':
            formUrl = '/static/forms/double_transposition_form.html'
            algorithmName = 'Double Transposition Cipher'
            break;
        case 'rc4_crypto':
            formUrl = '/static/forms/rc4_form.html'
            algorithmName = 'RC4 Cipher(Base64)'
            break;
        case 'ca_crypto':
            formUrl = '/static/forms/ca_form.html'
            algorithmName = 'CA Cipher(Base64)'
            break;
        case 'aes_crypto':
            formUrl = '/static/forms/aes_form.html';
            algorithmName = 'AES Cipher';
            break;
        case 'aes_ecb_crypto':
            formUrl = '/static/forms/aes_ecb_form.html';
            algorithmName = 'AES ECB Cipher';
            break;
        case 'rsa_crypto':
            formUrl = '/static/forms/rsa_form.html';
            algorithmName = 'RSA Cipher';
            break;
        case 'ecc_crypto':
            formUrl = '/static/forms/ecc_form.html';
            algorithmName = 'ECC Cipher';
            break;
        case 'md5_crypto':
            formUrl = '/static/forms/md5_form.html';
            algorithmName = 'MD5 Hash';
            break;
        case 'dh_crypto':
            formUrl = '/static/forms/dh_form.html';
            algorithmName = 'DH Exchange';
            break;
        case 'ecdh_crypto':
            formUrl = '/static/forms/ecdh_form.html';
            algorithmName = 'ECDH Exchange';
            break;
        default:
            console.error('Unknown algorithm:', algorithm);
            return;  // 如果找不到匹配的算法，则不执行
    }
    // 确认是否正确构建了表单 URL
    console.log('Loading form from URL:', formUrl);
    document.querySelector("#operation-area h2").textContent = `${algorithmName} `;

    // 使用 Fetch API 加载对应的表单文件
    fetch(formUrl)
        .then(response => {
            // 如果响应不是 OK 状态，则抛出错误
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            // 返回响应文本
            return response.text();
        })
        .then(html => {
            console.log('Form HTML successfully loaded:', html);  // 输出加载的 HTML
            // 将 HTML 内容插入到页面
            document.getElementById('algorithm-form').innerHTML = html;
            // 清空输出区域
            document.getElementById('output-area').innerHTML = '';
        })
        .catch(error => {
            // 捕获并输出错误
            console.error('Error loading the form:', error);
            alert('无法加载表单，请稍后再试。');
        });
}


function submitForm(algorithm, action) {
    const formData = {
        message: document.getElementById("message") ? document.getElementById("message").value : undefined,
        shift: document.getElementById("shift") ? document.getElementById("shift").value : undefined,
        keyword: document.getElementById("keyword") ? document.getElementById("keyword").value : undefined,
        a: document.getElementById("a") ? document.getElementById("a").value : undefined,
        b: document.getElementById("b") ? document.getElementById("b").value : undefined,
        bit: document.getElementById("bit") ? document.getElementById("bit").value : undefined,
        c1: document.getElementById("c1") ? document.getElementById("c1").value : undefined,
        c2: document.getElementById("c2") ? document.getElementById("c2").value : undefined,
        key: document.getElementById("key") ? document.getElementById("key").value : undefined,
        key1: document.getElementById("key1") ? document.getElementById("key1").value : undefined,
        key_size: document.getElementById("key_size") ? document.getElementById("key_size").value : undefined,
        public_key: document.getElementById("public_key") ? document.getElementById("public_key").value : undefined,
        private_key: document.getElementById("private_key") ? document.getElementById("private_key").value : undefined,
        action: action
    };

    $.ajax({
    url: `/encryption/${algorithm}`,  // 路径只需要到算法部分
    method: 'POST',
    data: formData,
    success: function(response) {
        let outputContent = '';

        // 判断当前使用的算法
        if (algorithm === 'rsa_crypto') {
            // 只有当算法是RSA时，才按照RSA的返回格式处理
            if (response.ciphertext) {
                outputContent = `<h2>加密结果:</h2><p>密文: ${response.ciphertext}</p>`;
                if (response.private_key) {
                    outputContent += `<p>私钥 (d, n): ${response.private_key}</p>`;
                }
            } else if (response.decrypted_message) {
                outputContent = `<h2>解密结果:</h2><p>明文: ${response.decrypted_message}</p>`;
            } else {
                outputContent = `<h2>结果:</h2><p>${response.error || '未知错误'}</p>`;
            }
        } else if (algorithm === 'ecc_crypto') {
            if (response.Q) {
                outputContent = `<h2>加密结果:</h2><p>生成的公钥: <br>${response.Q}</p>`;
                if (response.C1 && response.C2_Str) {
                    outputContent += `<p>密文: <br>C1=${response.C1}<br>C2=${response.C2_Str}</p>`;
                }
            } else if (response.result) {
                outputContent = `<h2>解密结果:</h2><p>明文: ${response.result}</p>`;
            } else {
                outputContent = `<h2>结果:</h2><p>${response.error || '未知错误'}</p>`;
            }
        } else if (algorithm === 'dh_crypto' || algorithm === 'ecdh_crypto') {
            outputContent = `<h2>结果:</h2><p>素数 p:<br>${response.p}<br>生成元 g:${response.g}<br>A 的公钥:${response.A}<br>B 的公钥:${response.B}<br>A 计算的共享密钥:${response.shared_secret_A}<br>B 计算的共享密钥:${response.shared_secret_B}</p>`
            document.getElementById("output-area").innerHTML = outputContent;
            setTimeout(function() {
                if (response.shared_secret_A === response.shared_secret_B) {
                    alert("共享密钥匹配，安全交换成功！");
                } else {
                    alert("共享密钥不匹配");
                }
            }, 100);  // 设置延迟为 0 毫秒，意味着页面更新后立刻弹窗
        } else {
            // 如果是其他算法（如AES等），按不同方式处理
            outputContent = `<h2>结果:</h2><p>${response}</p>`;
        }

        // 将内容插入到结果区域
        document.getElementById("output-area").innerHTML = outputContent;
    },
    error: function(xhr, status, error) {
        // 错误处理
        document.getElementById("output-area").innerHTML = `<h2>错误:</h2><p>${error}</p>`;
    }
});
}


// Optional: Function to close all categories on page load
window.onload = function() {
  // 处理分类列表
  const categories = document.querySelectorAll('.category');
  categories.forEach(function(category) {
    const sublist = category.querySelector('.sub-list');
    const arrow = category.querySelector('.arrow');
    sublist.style.display = 'none'; // 默认隐藏所有子列表
    arrow.textContent = '►'; // 设置箭头指向右
  });
};

window.onload = function() {
  // 处理分类列表
  const categories = document.querySelectorAll('.category');
  categories.forEach(function(category) {
    const sublist = category.querySelector('.sub-list');
    const arrow = category.querySelector('.arrow');
    sublist.style.display = 'none'; // 默认隐藏所有子列表
    arrow.textContent = '►'; // 设置箭头指向右
  });
};

// 定义读取文件内容的函数
function handleFileUpload(fileInputId, targetInputId) {
  const fileInput = document.getElementById(fileInputId);
  const targetInput = document.getElementById(targetInputId);

  if (fileInput && targetInput) {
    const file = fileInput.files[0];
    if (file) {
      const reader = new FileReader();

      reader.onload = function(e) {
        targetInput.value = e.target.result; // 将文件内容赋值到目标输入框
      };

      reader.onerror = function(e) {
        console.error("Error reading file:", e); // 如果读取文件时发生错误，输出错误信息
      };

      reader.readAsText(file); // 读取文件内容
    } else {
      console.log("No file selected"); // 如果没有选择文件
    }
  } else {
    console.error("文件输入框或目标输入框不存在！");
  }
}


// 生成随机AES密钥并填入输入框，始终使用128位密钥
function generateRandomAESKeyAndFill() {
    const keyInput = document.getElementById('key');  // 获取密钥输入框元素

    const keyLength = "128";  // 固定为128位

    // 设置字节长度为16（128位）
    const byteLength = 16;  // 128位密钥（16字节）

    // 生成密钥并填充输入框
    const randomKey = generateRandomAESKey(byteLength);
    keyInput.value = randomKey;  // 将生成的密钥填入输入框
}

// 生成随机AES密钥（128位，16字节）并加上0x前缀
function generateRandomAESKey(byteLength) {
    const array = new Uint8Array(byteLength);  // 根据字节长度生成数组
    window.crypto.getRandomValues(array);  // 获取强随机数

    // 转换为十六进制字符串，并加上0x前缀
    const hexKey = Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
    console.log(hexKey);  // 调试：输出生成的密钥（没有0x前缀）
    return '0x' + hexKey;  // 返回带有0x前缀的密钥
}

// 清空所有输入框内容的函数
function clearInputs() {
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.value = ''; // 清空每个input的值
    });
}

