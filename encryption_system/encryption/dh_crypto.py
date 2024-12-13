import sympy


# Diffie-Hellman 类
class DiffieHellman:
    def __init__(self, bits=512):
        self.bits = bits
        self.p = None
        self.g = None

    # 定义计算幂模函数
    def mod_exp(self, base, exp, mod):
        return pow(base, exp, mod)

    # 随机生成一个素数 p 和一个生成元 g
    def generate_large_prime_and_generator(self):
        # 生成一个安全素数 p（p = 2q + 1，其中 q 也是素数）
        while True:
            q = sympy.randprime(2 ** (self.bits - 2), 2 ** (self.bits - 1))
            p = 2 * q + 1
            if sympy.isprime(p):
                break

        # 找到 p 的一个生成元 g
        # 原根生成方法基于循环群生成元
        for potential_g in range(2, p):
            if sympy.is_primitive_root(potential_g, p):
                g = potential_g
                break

        self.p = p
        self.g = g
        return p, g

    # Diffie-Hellman 密钥交换过程
    def diffie_hellman(self, a, b):
        # 生成素数 p 和生成元 g
        if not self.p or not self.g:
            self.generate_large_prime_and_generator()

        # A 和 B 计算各自的公钥
        A = self.mod_exp(self.g, a, self.p)  # A 的公钥
        B = self.mod_exp(self.g, b, self.p)  # B 的公钥

        # A 和 B 交换公钥并计算共享密钥
        shared_secret_A = self.mod_exp(B, a, self.p)  # A 计算共享密钥
        shared_secret_B = self.mod_exp(A, b, self.p)  # B 计算共享密钥

        return A, B, shared_secret_A, shared_secret_B

    # 进行密钥交换并返回结果
    def calculate_key_exchange(self, a, b):
        A, B, shared_secret_A, shared_secret_B = self.diffie_hellman(a, b)

        result = {
            'p': self.p,
            'g': self.g,
            'A': A,
            'B': B,
            'shared_secret_A': shared_secret_A,
            'shared_secret_B': shared_secret_B,
        }

        return result
