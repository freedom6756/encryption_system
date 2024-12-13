from flask import Flask, render_template, request, jsonify, send_from_directory
from encryption.caesar_crypto import Caesar
from encryption.aes_crypto import AES
from encryption.md5_crypto import MD5
from encryption.md5_static import MD5_Static
from encryption.rsa_crypto import RSA
from encryption.keyword_crypto import KeywordCipher
from encryption.vigenere_crypto import VigenereCipher
from encryption.autokey_plaintext_crypto import Autokey_Plaintext
from encryption.playfair_crypto import PlayfairCipher
from encryption.permutation_crypto import PermutationCipher
from encryption.column_permutation_crypto import ColumnPermutationCipher
from encryption.rc4_crypto import RC4
from encryption.affine_crypto import AffineCipher
from encryption.multiliteral_crypto import MultiliteralCipher
from encryption.autokey_ciphertext_crypto import Autokey_Ciphertext
from encryption.ecc_crypto import ECC
from encryption.double_playfair_crypto import DoublePlayfairCipher
from encryption.double_transposition_crypto import DoubleTranspositionCipher
from encryption.ca_crypto import CellularAutomatonCryptography
from encryption.dh_crypto import DiffieHellman
from encryption.ecdh_crypto import ECDH
import random
import socket
import threading
import os
import stat
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encryption')
def encryption():
    return render_template('encryption.html')


@app.route('/decryption')
def decryption():
    return render_template('decryption.html')


@app.route('/single_encryption')
def single_encryption():
    return render_template('single_encryption.html')


@app.route('/dual_encryption')
def dual_encryption():
    return render_template('dual_encryption.html')


@app.route('/encryption/caesar_crypto', methods=['POST'])
def caesar_route():
    message = request.form['message']
    shift = int(request.form['shift'])
    action = request.form['action']  # 新增一个 action 字段来标识加密或解密

    # 创建 Caesar 类的实例
    caesar = Caesar(shift)

    if action == 'encrypt':
        # 调用 encrypt 方法进行加密
        result = caesar.encrypt(message)
    elif action == 'decrypt':
        # 调用 decrypt 方法进行解密
        result = caesar.decrypt(message)
    else:
        result = "Invalid action"

    return result


@app.route('/encryption/keyword_crypto', methods=['POST'])
def keyword_route():
    message = request.form['message']

    action = request.form['action']  # 新增一个 action 字段来标识加密或解密
    keyword = request.form['keyword']

    # 创建 Caesar 类的实例
    keyword_cipher = KeywordCipher(keyword=keyword)

    if action == 'encrypt':
        # 调用 encrypt 方法进行加密
        result = keyword_cipher.encrypt(message)
    elif action == 'decrypt':
        # 调用 decrypt 方法进行解密
        result = keyword_cipher.decrypt(message)
    else:
        result = "Invalid action"

    return result


@app.route('/encryption/affine_crypto', methods=['POST'])
def affine_route():
    message = request.form['message']

    action = request.form['action']  # 新增一个 action 字段来标识加密或解密
    key1 = int(request.form['key1'])
    key = int(request.form['key'])

    # 创建 Caesar 类的实例
    affine = AffineCipher(a=key, b=key1)
    if affine.check_a_coprime_with_26(key):
        if action == 'encrypt':
            # 调用 encrypt 方法进行加密
            result = affine.encrypt(message)
        elif action == 'decrypt':
            # 调用 decrypt 方法进行解密
            result = affine.decrypt(message)
        else:
            result = "Invalid action"

    else:
        result = f"你输入的密钥A与26不互素,请重新输入"

    return result


@app.route('/encryption/multiliteral_crypto', methods=['POST'])
def multiliteral_route():
    message = request.form['message']

    action = request.form['action']  # 新增一个 action 字段来标识加密或解密
    key = request.form['key']

    multiliteral = MultiliteralCipher(key=key)

    if action == 'encrypt':
        # 调用 encrypt 方法进行加密
        result = multiliteral.encrypt(message)
    elif action == 'decrypt':
        # 调用 decrypt 方法进行解密
        result = multiliteral.decrypt(message)
    else:
        result = "Invalid action"

    return result


@app.route('/encryption/vigenere_crypto', methods=['POST'])
def vigenere_route():
    message = request.form['message']

    action = request.form['action']  # 新增一个 action 字段来标识加密或解密
    key = request.form['key']

    # 创建 Caesar 类的实例
    vigenere = VigenereCipher(key=key)

    if action == 'encrypt':
        # 调用 encrypt 方法进行加密
        result = vigenere.encrypt(message)
    elif action == 'decrypt':
        # 调用 decrypt 方法进行解密
        result = vigenere.decrypt(message)
    else:
        result = "Invalid action"

    return result


@app.route('/encryption/autokey_plaintext_crypto', methods=['POST'])
def autokey_plaintext_route():
    message = request.form['message']

    action = request.form['action']  # 新增一个 action 字段来标识加密或解密
    key = request.form['key']

    # 创建 Caesar 类的实例
    autokey_plaintext = Autokey_Plaintext(key=key)

    if action == 'encrypt':
        # 调用 encrypt 方法进行加密
        result = autokey_plaintext.encrypt(message)
    elif action == 'decrypt':
        # 调用 decrypt 方法进行解密
        result = autokey_plaintext.decrypt(message)
    else:
        result = "Invalid action"

    return result


@app.route('/encryption/autokey_ciphertext_crypto', methods=['POST'])
def autokey_ciphertext_route():
    message = request.form['message']

    action = request.form['action']  # 新增一个 action 字段来标识加密或解密
    key = request.form['key']

    # 创建 Caesar 类的实例
    autokey_ciphertext = Autokey_Ciphertext(key=key)

    if action == 'encrypt':
        # 调用 encrypt 方法进行加密
        result = autokey_ciphertext.encrypt(message)
    elif action == 'decrypt':
        # 调用 decrypt 方法进行解密
        result = autokey_ciphertext.decrypt(message)
    else:
        result = "Invalid action"

    return result


@app.route('/encryption/playfair_crypto', methods=['POST'])
def playfair_route():
    message = request.form['message']

    action = request.form['action']  # 新增一个 action 字段来标识加密或解密
    key = request.form['key']

    # 创建 Caesar 类的实例
    playfair = PlayfairCipher(key=key)

    if action == 'encrypt':
        # 调用 encrypt 方法进行加密
        result = playfair.encrypt(message)
    elif action == 'decrypt':
        # 调用 decrypt 方法进行解密
        result = playfair.decrypt(message)
    else:
        result = "Invalid action"

    return result


@app.route('/encryption/double_playfair_crypto', methods=['POST'])
def double_playfair_route():
    message = request.form['message']

    action = request.form['action']  # 新增一个 action 字段来标识加密或解密
    key = request.form['key']
    key1 = request.form['key1']

    # 创建 Caesar 类的实例
    double_playfair = DoublePlayfairCipher(key1=key, key2=key1)

    if action == 'encrypt':
        # 调用 encrypt 方法进行加密
        result = double_playfair.encrypt(message)
    elif action == 'decrypt':
        # 调用 decrypt 方法进行解密
        result = double_playfair.decrypt(message)
    else:
        result = "Invalid action"

    return result


@app.route('/encryption/permutation_crypto', methods=['POST'])
def permutation_route():
    message = request.form['message']

    action = request.form['action']  # 新增一个 action 字段来标识加密或解密
    key = request.form['key']

    # 创建 Caesar 类的实例
    permutation = PermutationCipher(key=key)

    if action == 'encrypt':
        # 调用 encrypt 方法进行加密
        result = permutation.encrypt(message)
    elif action == 'decrypt':
        # 调用 decrypt 方法进行解密
        result = permutation.decrypt(message)
    else:
        result = "Invalid action"

    return result


@app.route('/encryption/column_permutation_crypto', methods=['POST'])
def column_permutation_route():
    message = request.form['message']

    action = request.form['action']  # 新增一个 action 字段来标识加密或解密
    keyword = request.form['keyword']

    column_permutation = ColumnPermutationCipher(keyword=keyword)

    if action == 'encrypt':
        # 调用 encrypt 方法进行加密
        result = column_permutation.encrypt(message)
    elif action == 'decrypt':
        # 调用 decrypt 方法进行解密
        result = column_permutation.decrypt(message)
    else:
        result = "Invalid action"

    return result


@app.route('/encryption/double_transposition_crypto', methods=['POST'])
def double_transposition_route():
    message = request.form['message']

    action = request.form['action']  # 新增一个 action 字段来标识加密或解密
    key = request.form['key']
    key1 = request.form['key1']

    # 创建 Caesar 类的实例
    double_transposition = DoubleTranspositionCipher(first_keyword=key, second_keyword=key1)

    if action == 'encrypt':
        # 调用 encrypt 方法进行加密
        result = double_transposition.encrypt(message)
    elif action == 'decrypt':
        # 调用 decrypt 方法进行解密
        result = double_transposition.decrypt(message)
    else:
        result = "Invalid action"

    return result


@app.route('/encryption/rc4_crypto', methods=['POST'])
def rc4_route():
    message = request.form['message']

    action = request.form['action']  # 新增一个 action 字段来标识加密或解密
    key = request.form['key']

    rc4 = RC4(key=key)

    if action == 'encrypt':
        # 调用 encrypt 方法进行加密
        result = rc4.process_input('encrypt', message)
    elif action == 'decrypt':
        # 调用 decrypt 方法进行解密
        result = rc4.process_input('decrypt', message)
    else:
        result = "Invalid action"

    return result


@app.route('/encryption/ca_crypto', methods=['POST'])
def ca_route():
    message = request.form['message']

    action = request.form['action']  # 新增一个 action 字段来标识加密或解密
    key = int(request.form['key'])
    key1 = request.form['key1']

    ca = CellularAutomatonCryptography(rule_number=key, length=256)

    if action == 'encrypt':
        # 调用 encrypt 方法进行加密
        result = ca.encrypt(message, key=key1)
    elif action == 'decrypt':
        # 调用 decrypt 方法进行解密
        result = ca.decrypt(message, key=key1)
    else:
        result = "Invalid action"

    return result


@app.route('/encryption/aes_crypto', methods=['POST'])
def aes_route():
    # 从请求中获取参数
    message = int(request.form['message'], 16)
    key = int(request.form['key'], 16)  # 传入的 key 作为整数
    action = request.form['action']  # 加密或解密操作

    # 创建 AES 类的实例
    aes = AES()
    RoundKeys = aes.round_key_generator(key)
    # 将消息转换为字节
    message_bytes = aes.num_2_16bytes(message)

    if action == 'encrypt':
        # 调用 aes_encrypt 方法进行加密
        ciphertext = aes.aes_encrypt(message_bytes, RoundKeys)
        result = hex(aes._16bytes2num(ciphertext))  # 将字节转换回字符
    elif action == 'decrypt':
        # 调用 aes_decrypt 方法进行解密
        plaintext = aes.aes_decrypt(message_bytes, RoundKeys)
        result = hex(aes._16bytes2num(plaintext))  # 将字节转换回字符
    else:
        result = "Invalid action"

    return result


@app.route('/encryption/aes_ecb_crypto', methods=['POST'])
def aes_ecb_route():
    # 从请求中获取参数
    message = request.form['message']  # 明文消息（字符串）
    key = int(request.form['key'], 16)  # 密钥（16进制字符串转为整数）
    action = request.form['action']  # 操作类型：'encrypt' 或 'decrypt'

    # 创建 AES 类的实例
    aes = AES()
    RoundKeys = aes.round_key_generator(key)

    if action == 'encrypt':
        # 将 message 转换为字节串
        message_bytes = message.encode('utf-8')
        message_list = list(message_bytes)  # 将字节串转换为整数列表
        ciphertext = aes.aes_ecb_encrypt(message_list, RoundKeys)
        result = hex(aes._16bytes2num(ciphertext))  # 将字节转换为16字节的整数并转换为十六进制字符串
    elif action == 'decrypt':
        if message.startswith('0x'):
            message = message[2:]  # 去掉 0x 前缀
        message_bytes = bytes.fromhex(message)  # 从十六进制字符串转换为字节串
        decrypted_plaintext = aes.aes_ecb_decrypt(message_bytes, RoundKeys)
        result = bytes(decrypted_plaintext).decode('utf-8', errors='ignore')  # 解密后转回字符串
    else:
        result = "Invalid action"  # 非法的操作类型

    # 返回加密或解密后的结果
    return result


@app.route('/encryption/md5_crypto', methods=['POST'])
def md5_route():
    action = request.form['action']  # 加密还是解密
    message = request.form['message']

    # 创建 MD5 类的实例
    md5 = MD5()

    if action == 'encrypt':
        # 调用 hash 方法进行加密
        result = md5.check_and_insert(message)
    elif action == 'decrypt':
        # 调用 decrypt 方法进行“解密”
        result = md5.decrypt(message)
    else:
        result = "Invalid action"
    md5.close()

    return result


@app.route('/encryption/rsa_crypto', methods=['POST'])
def rsa_crypto():
    # 从请求中获取参数
    message = request.form.get('message')  # 消息
    key_size = request.form.get('key_size', None)  # 获取 key_size，默认 None
    action = request.form.get('action')  # 加密或解密操作
    public_key = request.form.get('public_key')  # 公钥（可选）
    private_key = request.form.get('private_key')  # 私钥

    # 检查必要的参数
    if not message or not action:
        return jsonify({'error': 'Message and action are required'}), 400

    # 如果 key_size 为空字符串，则使用默认值 2048
    if key_size is None or key_size == '':
        key_size = 2048
    else:
        try:
            key_size = int(key_size)
            if key_size <= 0:
                raise ValueError("Key size must be a positive integer.")
        except ValueError as e:
            return jsonify({'error': f'Invalid key size: {e}'}), 400

    # 创建 RSA 类的实例
    rsa = RSA(key_size=key_size)

    if action == 'encrypt':
        # 如果提供了公钥，则使用提供的公钥进行加密
        if public_key:
            public_key = rsa.parse_key(public_key)
            if public_key is None:
                return jsonify({'error': 'Invalid public key format'}), 400
            ciphertext_blocks, private_key_part = rsa.encrypt_in_blocks(message, public_key=public_key)
        else:
            rsa.generate_keypair()
            ciphertext_blocks, private_key_part = rsa.encrypt_in_blocks(message)

        # 返回加密后的密文块（数字形式），以及私钥部分（d, n）
        return jsonify({
            'ciphertext': [str(block) for block in ciphertext_blocks],  # 返回密文块列表
            'private_key': f'({private_key_part[0]},{private_key_part[1]})'  # 返回私钥 (d, n) 形式
        })

    elif action == 'decrypt':
        # 如果没有提供私钥，则返回错误
        if not private_key:
            return jsonify({'error': 'Private key is required for decryption'}), 400

        # 解析私钥
        private_key = rsa.parse_key(private_key)
        if private_key is None:
            return jsonify({'error': 'Invalid private key format'}), 400

        try:
            # 将密文从字符串转换为整数（支持单个整数或多个密文块）
            if ',' in message:
                ciphertext_blocks = [int(c) for c in message.split(',')]
            else:
                ciphertext_blocks = [int(message)]
        except ValueError:
            return jsonify({'error': 'Invalid ciphertext format'}), 400

        # 逐个解密密文块
        decrypted_message = ''
        for ciphertext in ciphertext_blocks:
            decrypted_message += rsa.decrypt(ciphertext, private_key=private_key)

        return jsonify({'decrypted_message': decrypted_message})

    else:
        return jsonify({'error': 'Invalid action. Must be "encrypt" or "decrypt".'}), 400


@app.route('/encryption/ecc_crypto', methods=['POST'])
def ecc_crypto():
    # 从请求中获取参数
    message = request.form.get('message')  # 消息
    action = request.form.get('action')  # 加密或解密操作
    private_key = int(request.form['private_key'])  # 私钥
    c1 = request.form['c1']
    c2 = request.form['c2']
    ecc = ECC()
    q = ecc.point_mul(ecc.G, private_key)
    if action == 'encrypt':
        k = random.randint(1, ecc.n - 1)  # 生成随机数 k
        c1, c2 = ecc.encrypt(message, q, k)
        c2_str = ECC.format_C2_output(c2)
        return jsonify({
            'Q': f'{q}',
            'C1': f'{c1}',
            'C2_Str': f'{c2_str}'
        })

    elif action == 'decrypt':
        c1_x, c1_y = ecc.parse_C1_input(c1)
        c1 = (c1_x, c1_y)
        c2 = ECC.parse_C2_input(c2)
        points = ecc.decrypt(c1, c2, private_key)
        result = ecc.map_points_to_message(points)
        return jsonify({
            'result': f"{result}"
        })

    else:
        return jsonify({'error': 'Invalid action. Must be "encrypt" or "decrypt".'}), 400


@app.route('/encryption/dh_crypto', methods=['POST'])
def dh_crypto():
    a = int(request.form['key'])
    b = int(request.form['key1'])
    bit = int(request.form['bit']) if 'bit' in request.form and request.form['bit'] else 512
    dh = DiffieHellman(bits=bit)
    result = dh.calculate_key_exchange(a, b)
    return jsonify({
        'p': f"{result['p']}",
        'g': f"{result['g']}",
        'A': f"{result['A']}",
        'B': f"{result['B']}",
        'shared_secret_A': f"{result['shared_secret_A']}",
        'shared_secret_B': f"{result['shared_secret_B']}",
    })


@app.route('/encryption/ecdh_crypto', methods=['POST'])
def ecdh_crypto():
    a = int(request.form['key'])
    b = int(request.form['key1'])
    bit = int(request.form['bit']) if 'bit' in request.form and request.form['bit'] else 512
    ecdh = ECDH()
    result = ecdh.run_diffie_hellman(a, b, bits=bit)
    return jsonify({
        'p': f"{result['p']}",
        'g': f"{result['g']}",
        'A': f"{result['A']}",
        'B': f"{result['B']}",
        'shared_secret_A': f"{result['shared_secret_A']}",
        'shared_secret_B': f"{result['shared_secret_B']}",
    })


@app.route('/connect_to_decrypt', methods=['POST'])
def connect_to_decrypt():
    try:
        # 获取前端传来的密钥，第一次连接时可以没有密钥
        data = request.get_json()
        key = data.get('key')

        # 不需要密钥即可进行连接
        if key:
            print(f"Received key: {key}")
        else:
            print("No key provided, proceeding without key.")

        # 解密端服务器的配置
        host = '127.0.0.1'  # 解密端服务器地址
        port = 12345  # 解密端服务器监听端口

        print(f"尝试连接到 {host}:{port}")

        # 创建 TCP socket 连接到解密端服务器
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))  # 连接到解密端服务器
            print("已连接到解密端服务器。")

            # 如果提供了密钥，发送给解密端
            if key:
                s.sendall(key.encode())
                print(f"密钥 {key} 已发送到解密端。")

            # 接收解密端返回的响应
            response = s.recv(1024).decode('utf-8')  # 解码为 UTF-8
            print(f"接收到响应: {response}")

        return jsonify({"status": "success", "message": response})

    except Exception as e:
        print(f"连接解密端时出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})


# 设定保存接收文件的文件夹路径
FILE_SAVE_PATH = 'E:/Python code/encryption_system/socket_connect/encryption/'
os.chmod(FILE_SAVE_PATH, stat.S_IRWXU)
FILE_SAVE_DIR = 'E:/Python code/encryption_system/socket_connect/decryption/'
os.chmod(FILE_SAVE_DIR, stat.S_IRWXU)

# 确保文件夹存在
if not os.path.exists(FILE_SAVE_PATH):
    os.makedirs(FILE_SAVE_PATH)


def handle_client(conn, addr):
    try:
        print(f"接收到来自 {addr} 的连接")
        conn.sendall("服务已启动，连接成功".encode('utf-8'))  # 发送连接成功消息
        print("消息已发送给客户端")

        # 设置接收超时
        conn.settimeout(10)  # 10秒超时设置

        # 临时存储文件内容
        temp_file_data = bytearray()  # 使用bytearray来临时存储接收到的文件数据

        while True:
            file_data = conn.recv(1024)

            if not file_data:
                print("没有更多数据，连接已关闭或超时")
                break  # 如果接收到空字节串，表示连接关闭，跳出循环

            if b'EOF' in file_data:  # 如果接收到EOF标志，去掉EOF并结束
                print("接收到EOF标志，文件传输结束")
                file_data = file_data.replace(b'EOF', b'')  # 移除EOF标志
                temp_file_data.extend(file_data)  # 将最后一部分数据添加到临时数据中
                break  # 停止接收文件

            # 确保文件内容不包括EOF标志
            print(f"接收到的数据: {file_data}")
            temp_file_data.extend(file_data)

        if temp_file_data:  # 只有当接收到的数据不为空时才创建文件
            # 生成唯一文件名
            timestamp = str(int(time.time() * 1000))  # 使用当前时间戳作为文件名
            file_path = os.path.join(FILE_SAVE_DIR, f"decrypted_data_{timestamp}.txt")

            # 保存文件到磁盘
            with open(file_path, 'wb') as f:
                f.write(temp_file_data)

            print(f"文件已保存到 {file_path}")
            conn.sendall(f"文件接收并保存成功，文件名: {os.path.basename(file_path)}".encode('utf-8'))

    except Exception as e:
        print(f"与客户端 {addr} 通信时出错: {e}")
        conn.sendall(f"文件传输失败: {e}".encode('utf-8'))

    finally:
        try:
            conn.close()
        except Exception as close_error:
            print(f"关闭连接时出错: {close_error}")


@app.route('/send_encrypted_file', methods=['POST'])
def send_encrypted_file():
    try:
        # 获取上传的加密文件
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "没有文件上传"})

        file = request.files['file']
        file_content = file.read()
        print(f"收到文件: {file.filename}, 内容长度: {len(file_content)}")

        # 生成一个唯一的文件名（例如基于时间戳）
        timestamp = str(int(time.time() * 1000))  # 使用当前时间戳作为文件名
        file_path = os.path.join(FILE_SAVE_PATH, f"encrypted_data_{timestamp}.txt")

        # 保存文件到本地（可以作为备份）
        with open(file_path, 'wb') as f:
            f.write(file_content)
        print(f"文件已保存: {file_path}")

        # 在 Socket 中发送加密数据
        host = '127.0.0.1'  # 解密端服务器的IP地址
        port = 12345  # 解密端监听的端口

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))  # 连接到解密端服务器
            print("已连接到解密端，开始发送文件")

            # 分块发送文件内容
            chunk_size = 1024  # 发送数据的块大小
            for i in range(0, len(file_content), chunk_size):
                chunk = file_content[i:i + chunk_size]
                s.sendall(chunk)
                print(f"已发送 {i + len(chunk)}/{len(file_content)} 字节")

            # 发送结束标志
            s.sendall(b'EOF')  # 发送一个特殊标志，表示文件传输结束
            print("文件发送完毕，等待解密端确认接收")

            # 等待解密端确认接收
            response = s.recv(1024).decode('utf-8')
            print(f"解密端响应: {response}")

        return jsonify({"status": "success", "message": "加密文件已发送"})

    except Exception as e:
        print(f"发送加密文件时出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})


def start_tcp_service():
    try:
        host = '127.0.0.1'
        port = 12345

        # 创建一个 TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))  # 绑定地址和端口
            s.listen(2)  # 最大连接数设置为2
            print(f"服务已启动，等待连接... {host}:{port}")

            while True:
                conn, addr = s.accept()  # 等待客户端连接
                # 启动一个新线程来处理每个客户端连接
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

    except Exception as e:
        print(f"启动服务失败: {e}")


@app.route('/start_socket_service', methods=['POST'])
def start_socket_service_route():
    try:
        # 在后台线程启动 TCP 服务
        threading.Thread(target=start_tcp_service, daemon=True).start()

        return jsonify({"status": "success", "message": "Socket 服务已启动"})

    except Exception as e:
        print(f"启动 Socket 服务时出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})


dh = DiffieHellman(bits=512)


@app.route('/exchange_keys', methods=['POST'])
def exchange_keys():
    try:
        # 获取前端传入的加解密端私钥
        data = request.get_json()
        a_private_key = int(data['a'])  # 加密端私钥
        b_private_key = int(data['b'])  # 解密端私钥

        # 使用 DiffieHellman 类计算密钥交换
        result = dh.calculate_key_exchange(a_private_key, b_private_key)

        # 返回计算结果，包括共享密钥
        shared_key = str(result['shared_secret_A'])  # 共享密钥

        return jsonify({
            'status': 'success',
            'result': {
                'shared_secret_A': shared_key,  # 返回共享密钥
                'shared_secret_B': shared_key  # 解密端也使用相同的共享密钥
            }
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


# AES 加密函数
@app.route('/encrypt_with_aes', methods=['POST'])
def encrypt_with_aes():
    try:
        # 从请求中获取 JSON 数据
        data = request.get_json()
        shared_key = data.get('sharedKey')  # 获取共享密钥
        message = data.get('message')  # 获取要加密的消息

        # 验证共享密钥和消息是否存在
        if not shared_key or not message:
            return jsonify({"status": "error", "message": "共享密钥和消息不能为空"})

        # 将共享密钥转换为 256 位 AES 密钥（通过 MD5 处理）
        md5_static = MD5_Static()
        key = md5_static.hash(shared_key)  # 使用 MD5 处理共享密钥
        key_hex = '0x' + key  # 生成十六进制字符串（带有 '0x' 前缀）
        key_int = int(key_hex, 16)  # 将十六进制字符串转换为整数

        # 使用自定义的 AES 类和 aes_ecb_encrypt 方法进行加密
        aes = AES()

        # 生成轮密钥
        round_keys = aes.round_key_generator(key_int)

        # 使用 ECB 模式进行加密
        data_bytes = message.encode('utf-8')  # 将数据编码为字节
        data_list = list(data_bytes)  # 转换为整数列表
        encrypted_data = aes.aes_ecb_encrypt(data_list, round_keys)  # 加密数据

        # 将加密后的数据转换为十六进制字符串
        result = hex(aes._16bytes2num(encrypted_data))

        # 返回加密后的数据
        return jsonify({"status": "success", "encryptedData": result})

    except Exception as e:
        # 错误处理
        print(f"加密时出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})


@app.route('/decrypt_with_aes', methods=['POST'])
def decrypt_with_aes():
    try:
        # 从请求中获取 JSON 数据
        data = request.get_json()
        shared_key = data.get('sharedKey')  # 获取共享密钥
        ciphertext = data.get('ciphertext')  # 获取要加密的消息
        print(shared_key)
        print(ciphertext)

        # 验证共享密钥和消息是否存在
        if not shared_key or not ciphertext:
            return jsonify({"status": "error", "message": "共享密钥和消息不能为空"})

        # 将共享密钥转换为 256 位 AES 密钥（通过 MD5 处理）
        md5_static = MD5_Static()
        key = md5_static.hash(shared_key)  # 使用 MD5 处理共享密钥
        key_hex = '0x' + key  # 生成十六进制字符串（带有 '0x' 前缀）
        key_int = int(key_hex, 16)  # 将十六进制字符串转换为整数

        # 使用自定义的 AES 类和 aes_ecb_encrypt 方法进行加密
        aes = AES()

        # 生成轮密钥
        round_keys = aes.round_key_generator(key_int)

        if ciphertext.startswith('0x'):
            cipher = ciphertext[2:]  # 去掉 0x 前缀
        message_bytes = bytes.fromhex(cipher)  # 从十六进制字符串转换为字节串
        decrypted_plaintext = aes.aes_ecb_decrypt(message_bytes, round_keys)
        result = bytes(decrypted_plaintext).decode('utf-8', errors='ignore')  # 解密后转回字符串

        # 返回加密后的数据
        return jsonify({"status": "success", "decryptedData": result})

    except Exception as e:
        # 错误处理
        print(f"加密时出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})


@app.route('/encrypt_with_rc4', methods=['POST'])
def encrypt_with_rc4():
    try:
        # 从请求中获取 JSON 数据
        data = request.get_json()
        shared_key = data.get('sharedKey')  # 获取共享密钥
        message = data.get('message')  # 获取要加密的消息

        # 验证共享密钥和消息是否存在
        if not shared_key or not message:
            return jsonify({"status": "error", "message": "共享密钥和消息不能为空"})

        rc4 = RC4(key=shared_key)
        result = rc4.process_input('encrypt', message)

        # 返回加密后的数据
        return jsonify({"status": "success", "encryptedData": result})

    except Exception as e:
        # 错误处理
        print(f"加密时出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})


@app.route('/decrypt_with_rc4', methods=['POST'])
def decrypt_with_rc4():
    try:
        # 从请求中获取 JSON 数据
        data = request.get_json()
        shared_key = data.get('sharedKey')  # 获取共享密钥
        ciphertext = data.get('ciphertext')  # 获取要加密的消息

        # 验证共享密钥和消息是否存在
        if not shared_key or not ciphertext:
            return jsonify({"status": "error", "message": "共享密钥和消息不能为空"})

        rc4 = RC4(key=shared_key)
        result = rc4.process_input('decrypt', ciphertext)

        # 返回加密后的数据
        return jsonify({"status": "success", "decryptedData": result})

    except Exception as e:
        # 错误处理
        print(f"加密时出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})


@app.route('/encrypt_with_rsa', methods=['POST'])
def encrypt_with_rsa():
    try:
        # 从请求中获取 JSON 数据
        data = request.get_json()
        message = data.get('message')  # 获取要加密的消息
        key_size = data.get('key_size', None)
        if key_size is None or key_size == '':
            key_size = 2048
        else:
            try:
                key_size = int(key_size)
                if key_size <= 0:
                    raise ValueError("Key size must be a positive integer.")
            except ValueError as e:
                return jsonify({'error': f'Invalid key size: {e}'}), 400
        rsa = RSA(key_size=key_size)

        rsa.generate_keypair()
        ciphertext_blocks, private_key_part = rsa.encrypt_in_blocks(message)
        print(ciphertext_blocks)
        print(private_key_part)
        # 返回加密后的数据
        return jsonify({"status": "success",
                        "encryptedData": str(ciphertext_blocks),
                        "private_key": f'({private_key_part[0]},{private_key_part[1]})'
                        })

    except Exception as e:
        # 错误处理
        print(f"加密时出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})


@app.route('/decrypt_with_rsa', methods=['POST'])
def decrypt_with_rsa():
    try:
        # 从请求中获取 JSON 数据
        data = request.get_json()
        print(data)
        private_key = data.get('sharedKey')  # 获取共享密钥
        ciphertext = data.get('ciphertext')  # 获取要加密的消息
        print(private_key)
        print(ciphertext)
        key_size = data.get('key_size', None)
        if key_size is None or key_size == '':
            key_size = 2048
        else:
            try:
                key_size = int(key_size)
                if key_size <= 0:
                    raise ValueError("Key size must be a positive integer.")
            except ValueError as e:
                return jsonify({'error': f'Invalid key size: {e}'}), 400
        rsa = RSA(key_size=key_size)
        if not private_key:
            return jsonify({'error': 'Private key is required for decryption'}), 400
        private_key = rsa.parse_key(private_key)
        if private_key is None:
            return jsonify({'error': 'Invalid private key format'}), 400

        try:
            # 将密文从字符串转换为整数（支持单个整数或多个密文块）
            ciphertext = ciphertext.strip('[]')
            if ',' in ciphertext:
                ciphertext_blocks = [int(c) for c in ciphertext.split(',')]
            else:
                ciphertext_blocks = [int(ciphertext)]
        except ValueError:
            return jsonify({'error': 'Invalid ciphertext format'}), 400

            # 逐个解密密文块
        decrypted_message = ''
        print("ok")
        for ciphertext in ciphertext_blocks:
            decrypted_message += rsa.decrypt(ciphertext, private_key=private_key)
            print(decrypted_message)
        return jsonify({"status": "success",
                        "decryptedData": decrypted_message,
                        })

    except Exception as e:
        # 错误处理
        print(f"加密时出错: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})


# 设置文件存储目录
UPLOAD_FOLDER = 'E:/Python code/encryption_system/socket_connect/decryption/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/get-file-list', methods=['GET'])
def get_file_list():
    try:
        # 获取文件列表
        file_list = os.listdir(app.config['UPLOAD_FOLDER'])
        return jsonify(file_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        # 从存储目录发送文件
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/save-file', methods=['POST'])
def save_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400

    # 保存文件
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    return jsonify({'success': True})


decryption_private_key = None


@app.route('/submit_decryption_private_key', methods=['POST'])
def submit_decryption_private_key():
    global decryption_private_key

    # 从请求体获取解密端私钥
    data = request.get_json()
    decryption_private_key = data.get('decryptionPrivateKey')

    if not decryption_private_key:
        return jsonify({'status': 'error', 'message': '解密端私钥不能为空'}), 400

    return jsonify({'status': 'success', 'message': '解密端私钥提交成功'})


@app.route('/get_decryption_private_key', methods=['GET'])
def get_decryption_private_key():
    print(decryption_private_key)
    if decryption_private_key:
        return jsonify({'status': 'success', 'decryptionPrivateKey': decryption_private_key})
    else:
        return jsonify({'status': 'error', 'message': '解密端私钥未设置'}), 404


if __name__ == "__main__":
    app.run(debug=True)
