import base64


class RC4:
    def __init__(self, key):
        self.key = key
        self.s_box = self.init_box(key)

    # 密钥调度算法(KSA)
    # 用来初始化S盒(0-255):先填充S后混洗
    def init_box(self, key):
        s_box = list(range(256))  # 初始S盒是0到255的整数列表
        j = 0
        key_length = len(key)

        for i in range(256):
            j = (j + s_box[i] + ord(key[i % key_length])) % 256
            s_box[i], s_box[j] = s_box[j], s_box[i]  # 交换S盒中的元素
        return s_box

    # 伪随机字节生成算法(PRGA)
    # 每次调用时返回一个伪随机字节,随机选择S的元素并修改排列组合
    def prga(self):
        i = 0
        j = 0
        while True:
            i = (i + 1) % 256
            j = (j + self.s_box[i]) % 256
            self.s_box[i], self.s_box[j] = self.s_box[j], self.s_box[i]  # 交换S盒中的元素
            t = (self.s_box[i] + self.s_box[j]) % 256
            k = self.s_box[t]
            yield k
            # 使用类似return的生成器yield返回伪随机字节
            # 使得函数每次执行时可以逐步生成一个伪随机值并暂停执行，等待下一次请求

    def encrypt_decrypt(self, data, mode='encrypt'):
        # 通过PRGA生成的伪随机流与输入数据进行异或操作
        prga_generate = self.prga()  # 获取密钥流生成器
        result = []

        for char in data:
            key_stream_byte = next(prga_generate)  # 用next()调用生成器并获取一个伪随机字节
            result.append(chr(ord(char) ^ key_stream_byte))  # 与数据进行异或

        return ''.join(result)

    # 将数据编码为Base64格式
    def base64_encode(self, data):
        return base64.b64encode(data.encode('utf-8')).decode('utf-8')

    # 将Base64编码的密文解码
    def base64_decode(self, data):
        return base64.b64decode(data).decode('utf-8')

    def process_input(self, mode, data):
        if mode == 'encrypt':
            # 先加密，再进行Base64编码
            encrypted = self.encrypt_decrypt(data, mode='encrypt')
            return self.base64_encode(encrypted)  # 返回Base64编码的加密数据
        elif mode == 'decrypt':
            # 先Base64解码，再解密
            decoded_data = self.base64_decode(data)
            return self.encrypt_decrypt(decoded_data, mode='decrypt')
        else:
            raise ValueError("Invalid mode: choose 'encrypt' or 'decrypt'")

