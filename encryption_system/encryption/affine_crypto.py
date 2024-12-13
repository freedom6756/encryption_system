class AffineCipher:
    def __init__(self, a, b, m=26):
        # 初始化密钥a、b和字母表大小m
        self.a = a
        self.b = b
        self.m = m

    def encrypt(self, plaintext):
        # 加密过程
        return ''.join([self._encrypt_char(c) for c in plaintext])

    def decrypt(self, ciphertext):
        # 解密过程
        return ''.join([self._decrypt_char(c) for c in ciphertext])

    def _encrypt_char(self, char):
        # 对每个字符进行加密
        if char.isalpha():  # 只加密字母
            offset = ord('A') if char.isupper() else ord('a')
            x = ord(char) - offset
            encrypted_char = (self.a * x + self.b) % self.m
            return chr(encrypted_char + offset)
        else:
            return char  # 非字母字符直接返回

    def _decrypt_char(self, char):
        # 对每个字符进行解密
        if char.isalpha():  # 只解密字母
            offset = ord('A') if char.isupper() else ord('a')
            y = ord(char) - offset
            decrypted_char = (self.mod_inverse(self.a, self.m) * (y - self.b)) % self.m
            return chr(decrypted_char + offset)
        else:
            return char  # 非字母字符直接返回

    @staticmethod
    def gcd(a, b):
        # 计算最大公约数
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def mod_inverse(a, m):
        # 计算a在模m下的逆元
        g, x, y = AffineCipher.extended_gcd(a, m)
        if g != 1:
            raise ValueError(f"{a} has no modular inverse under modulus {m}")
        return x % m

    @staticmethod
    def extended_gcd(a, b):
        # 扩展欧几里得算法，返回gcd(a, b)以及x, y，使得ax + by = gcd(a, b)
        if b == 0:
            return a, 1, 0
        g, x1, y1 = AffineCipher.extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y

    @staticmethod
    def check_a_coprime_with_26(a):
        # 检查a是否与26互素
        return AffineCipher.gcd(a, 26) == 1

