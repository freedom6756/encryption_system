import random
import sympy
from encryption_system.encryption.ecc_crypto import ECC


class ECDH:
    def __init__(self):
        self.ecc = ECC()

    # 生成大素数p和生成元g
    def generate_large_prime_and_generator(self, bits=512):
        while True:
            q = sympy.randprime(2 ** (bits - 2), 2 ** (bits - 1))
            p = 2 * q + 1
            if sympy.isprime(p):
                break

        for potential_g in range(2, p):
            if sympy.is_primitive_root(potential_g, p):
                g = potential_g
                break

        return p, g

    # 模幂运算
    def mod_exp(self, base, exp, mod):
        return pow(base, exp, mod)

    # Diffie-Hellman算法：生成公钥并计算共享密钥
    def diffie_hellman(self, p, g, a, b):
        A = self.mod_exp(g, a, p)
        B = self.mod_exp(g, b, p)
        shared_secret_A = self.mod_exp(B, a, p)
        shared_secret_B = self.mod_exp(A, b, p)
        return A, B, shared_secret_A, shared_secret_B

    # 生成密钥对（私钥、公钥）
    def generate_key_pair(self):
        private_key = random.randint(1, self.ecc.n - 1)
        public_key = self.ecc.point_mul(self.ecc.G, private_key)
        return private_key, public_key

    # 计算共享密钥
    def compute_shared_secret(self, private_key, public_key):
        shared_secret = self.ecc.point_mul(public_key, private_key)
        return shared_secret

    # 运行Diffie-Hellman算法，提供两个私钥并可以指定bits
    def run_diffie_hellman(self, private_key_A, private_key_B, bits=512):
        p, g = self.generate_large_prime_and_generator(bits)
        A, B, shared_secret_A, shared_secret_B = self.diffie_hellman(p, g, private_key_A, private_key_B)

        result = {
            "p": p,
            "g": g,
            "A": A,
            "B": B,
            "shared_secret_A": shared_secret_A,
            "shared_secret_B": shared_secret_B,
        }

        return result


# 示例使用
if __name__ == "__main__":
    # 示例的私钥
    private_key_A = 12345
    private_key_B = 67890

    # 用户可以指定bits大小，这里使用512作为默认值
    bits = 512

    dh = ECDH()
    result = dh.run_diffie_hellman(private_key_A, private_key_B, bits)

    print("Diffie-Hellman 密钥交换结果:")
    print(f"素数p: {result['p']}")
    print(f"生成元g: {result['g']}")
    print(f"A的公钥: {result['A']}")
    print(f"B的公钥: {result['B']}")
    print(f"A计算的共享密钥: {result['shared_secret_A']}")
    print(f"B计算的共享密钥: {result['shared_secret_B']}")
