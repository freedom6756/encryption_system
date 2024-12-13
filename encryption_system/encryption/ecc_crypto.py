import random


class ECC:
    def __init__(self):
        # 初始化标准椭圆曲线secp256k1的参数
        self.p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        self.a = 0
        self.b = 7
        self.G = (
            55066263022277343669578718895168534326250603453777594175500187360389116729240,
            32670510020758816978083085130507043184471273380659243275938904335757337427599,
        )
        self.n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    # 引入扩展欧几里得算法，用于计算模逆元
    def extend_gcd(self, a, b):
        if b == 0:
            return a, 1, 0
        else:
            g, y, x = self.extend_gcd(b, a % b)
            return g, x, y - (a // b) * x

    # 计算模 b 下的逆元
    def mod_inverse(self, a, b):
        g, x, _ = self.extend_gcd(a, b)
        if g != 1:
            raise ValueError(f"{a} 和 {b} 不互素，逆元不存在")
        return x % b

    # 点加法
    def point_add(self, P, Q):
        if P is None:  # 处理无穷远点
            return Q
        if Q is None:
            return P
        if P == Q:  # 点倍加
            lmb = ((3 * (P[0] ** 2) + self.a) * self.mod_inverse(2 * P[1], self.p)) % self.p
        else:  # 普通点加
            lmb = ((Q[1] - P[1]) * self.mod_inverse(Q[0] - P[0], self.p)) % self.p
        x3 = (lmb ** 2 - P[0] - Q[0]) % self.p
        y3 = (lmb * (P[0] - x3) - P[1]) % self.p
        return x3, y3

    # 点乘法
    def point_mul(self, P, k):
        R = None
        temp = P
        while k:
            if k & 1:
                R = temp if R is None else self.point_add(R, temp)
            temp = self.point_add(temp, temp)
            k >>= 1
        return R

    # 将明文字符串映射为椭圆曲线上的点
    def map_message_to_points(self, message):
        points = []
        for char in message:
            k = ord(char) + 1
            points.append(self.point_mul(self.G, k))
        return points

    # 将椭圆曲线上的点还原为明文字符串
    def map_points_to_message(self, points):
        message = ""
        for point in points:
            temp = None
            k = 0
            while temp != point:
                k += 1
                temp = self.point_mul(self.G, k)
            message += chr(k - 1)
        return message

    # 加密
    def encrypt(self, message, Q, k):
        C1 = self.point_mul(self.G, k)
        points = self.map_message_to_points(message)
        C2 = [self.point_add(point, self.point_mul(Q, k)) for point in points]
        return C1, C2

    # 解密
    def decrypt(self, C1, C2, d):
        dC1 = self.point_mul(C1, d)
        dC1_neg = (dC1[0], -dC1[1] % self.p)  # 计算 dC1 的负值
        points = [self.point_add(point, dC1_neg) for point in C2]
        return points

    # 静态方法：格式化C2的输出，去掉外部的方括号
    @staticmethod
    def format_C2_output(C2):
        return ", ".join(f"({x}, {y})" for x, y in C2)

    # 静态方法：解析C1输入为(x, y)格式
    @staticmethod
    def parse_C1_input(C1_input):
        C1_x, C1_y = map(int, C1_input.strip('()').split(','))
        return C1_x, C1_y

    # 静态方法：解析C2输入为点的列表
    @staticmethod
    def parse_C2_input(C2_input):
        C2 = []
        for point in C2_input.split("),"):
            point = point.strip("() ")
            x_str, y_str = point.split(",")
            C2.append((int(x_str.strip()), int(y_str.strip())))
        return C2



