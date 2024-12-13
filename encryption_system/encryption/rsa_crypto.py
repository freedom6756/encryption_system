import random


class RSA:
    def __init__(self, key_size=2048):
        self.key_size = key_size
        self.public_key = None
        self.private_key = None
        self.p = None
        self.q = None
        self.n = None
        self.e = None
        self.d = None

    def generate_large_prime(self):
        """ 使用Miller-Rabin素性测试生成一个大素数 """
        while True:
            num = random.getrandbits(self.key_size // 2) | 1  # 随机生成一个奇数
            if self.miller_rabin(num):
                return num

    def miller_rabin(self, n, k=40):
        """ Miller-Rabin素性测试算法 """
        if n == 2 or n == 3:
            return True
        if n < 2 or n % 2 == 0:
            return False

        # 写成n-1 = 2^r * d的形式
        d = n - 1
        r = 0
        while d % 2 == 0:
            d //= 2
            r += 1

        # 进行k次试验
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = self.fast_exponentiation(a, d, n)  # 使用快速幂算法
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = self.fast_exponentiation(x, 2, n)  # 使用快速幂算法
                if x == n - 1:
                    break
            else:
                return False
        return True

    def mod_inverse(self, a, m):
        """ 计算a关于m的模逆，使用扩展欧几里得算法 """
        t, new_t = 0, 1
        r, new_r = m, a
        while new_r != 0:
            quotient = r // new_r
            t, new_t = new_t, t - quotient * new_t
            r, new_r = new_r, r - quotient * new_r
        if r > 1:
            return None  # 无法求模逆
        if t < 0:
            t = t + m
        return t

    def generate_random_e(self, phi_n):
        """ 随机生成一个符合条件的e，要求e与φ(n)互质且1 < e < φ(n) """
        while True:
            e = random.randrange(2, phi_n)
            # 检查e与φ(n)是否互质
            if self.gcd(e, phi_n) == 1:
                return e

    def gcd(self, a, b):
        """ 计算a和b的最大公约数 """
        while b != 0:
            a, b = b, a % b
        return a

    def generate_keypair(self):
        """ 生成RSA密钥对 """
        # 生成两个大素数p, q
        self.p = self.generate_large_prime()
        self.q = self.generate_large_prime()
        self.n = self.p * self.q

        # 计算欧拉函数φ(n)
        phi_n = (self.p - 1) * (self.q - 1)

        # 随机选择公钥e（要求e与φ(n)互质）
        self.e = self.generate_random_e(phi_n)

        # 计算私钥d，满足d * e ≡ 1 (mod φ(n))
        self.d = self.mod_inverse(self.e, phi_n)

        # 公钥和私钥
        self.public_key = (self.e, self.n)
        self.private_key = (self.d, self.n)

    def fast_exponentiation(self, base, exp, mod):
        """ 实现快速幂算法 """
        result = 1
        while exp > 0:
            if exp % 2 == 1:  # 如果 exp 是奇数
                result = (result * base) % mod
            base = (base * base) % mod  # 将 base 自乘（即指数的二分）
            exp //= 2  # 将指数减半
        return result

    def encrypt(self, plaintext, public_key=None):
        """ 使用公钥加密消息，同时返回密文和私钥部分 """
        # 如果没有传入公钥，则使用类的默认公钥
        if public_key is None:
            public_key = self.public_key

        e, n = public_key
        plaintext_bytes = plaintext.encode('utf-8')
        plaintext_int = int.from_bytes(plaintext_bytes, byteorder='big')

        # 检查明文是否超过了n的大小
        if plaintext_int >= n:
            raise ValueError("明文太大，无法直接加密，考虑分块加密")

        ciphertext_int = self.fast_exponentiation(plaintext_int, e, n)  # 使用快速幂

        # 返回密文和私钥的相关部分（d, n）
        return ciphertext_int, self.private_key

    def encrypt_in_blocks(self, plaintext, public_key=None, block_size=None):
        """ 分块加密消息 """
        if public_key is None:
            public_key = self.public_key

        e, n = public_key
        if block_size is None:
            block_size = (n.bit_length() - 1) // 8  # 适应n大小的块大小

        # 将明文分成块
        plaintext_bytes = plaintext.encode('utf-8')
        blocks = [plaintext_bytes[i:i + block_size] for i in range(0, len(plaintext_bytes), block_size)]

        ciphertext_blocks = []
        for block in blocks:
            block_int = int.from_bytes(block, byteorder='big')
            if block_int >= n:
                raise ValueError("块太大，无法加密")
            ciphertext_int = self.fast_exponentiation(block_int, e, n)
            ciphertext_blocks.append(ciphertext_int)

        # 返回密文和私钥的相关部分（d, n）
        return ciphertext_blocks, self.private_key

    def decrypt(self, ciphertext, private_key=None):
        """ 使用私钥解密消息 """
        # 如果没有传入私钥，则使用类的默认私钥
        if private_key is None:
            private_key = self.private_key

        d, n = private_key
        decrypted_int = self.fast_exponentiation(ciphertext, d, n)  # 使用快速幂
        decrypted_bytes = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, byteorder='big')
        return decrypted_bytes.decode('utf-8')

    def decrypt_in_blocks(self, ciphertext_blocks, private_key=None):
        """ 分块解密消息 """
        if private_key is None:
            private_key = self.private_key

        d, n = private_key
        decrypted_bytes = b""
        for ciphertext_int in ciphertext_blocks:
            decrypted_int = self.fast_exponentiation(ciphertext_int, d, n)
            block_bytes = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, byteorder='big')
            decrypted_bytes += block_bytes

        return decrypted_bytes.decode('utf-8')

    @staticmethod
    def parse_key(key_str):
        """将公钥或私钥字符串解析成元组 (e, n) 或 (d, n)"""
        if not key_str:
            return None
        # 去掉圆括号
        key_str = key_str.strip("()")
        try:
            return tuple(map(int, key_str.split(',')))
        except ValueError:
            return None

'''
rsa = RSA()
rsa.generate_keypair()

# 明文
plaintext = 'hello'
# 使用公钥加密
ciphertext_blocks, private_key = rsa.encrypt_in_blocks(plaintext)
print(ciphertext_blocks)

# 使用私钥解密
decrypted_message = rsa.decrypt_in_blocks(ciphertext_blocks)
print(f"解密后的消息: {decrypted_message}")
'''