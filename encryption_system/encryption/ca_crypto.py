import random
import base64
import hashlib


class CellularAutomatonCryptography:
    def __init__(self, rule_number=30, length=256):
        """初始化元胞自动机加密解密系统
        Args:
            rule_number (int): 使用的规则编号（默认 Rule 30）
            length (int): 元胞自动机的初始状态长度（默认 256）
        """
        self.rule_number = rule_number
        self.length = length

        # 检查规则编号是否有效
        if not (0 <= rule_number <= 255):
            raise ValueError("Rule number must be between 0 and 255.")

    def apply_rule(self, state):
        """根据规则编号应用不同的规则"""
        rule_bin = f"{self.rule_number:08b}"

        next_state = []
        for i in range(1, len(state) - 1):
            left, center, right = state[i - 1], state[i], state[i + 1]
            neighbor_code = 4 * left + 2 * center + right
            next_state.append(int(rule_bin[7 - neighbor_code]))

        return [state[0]] + next_state + [state[-1]]

    def initialize_ca(self, length, key):
        """初始化元胞自动机的起始状态，密钥影响初始化状态"""
        # 使用密钥的哈希值作为种子
        key_hash = hashlib.sha256(key.encode()).hexdigest()[:length // 4]
        # 将密钥的哈希值转换为二进制
        state = [int(bit) for char in key_hash for bit in f"{int(char, 16):04b}"]
        # 补充随机值直到达到指定长度
        state += [random.choice([0, 1]) for _ in range(length - len(state))]
        return state

    def generate_random_sequence(self, length, key):
        """使用元胞自动机生成一个伪随机序列"""
        state = self.initialize_ca(length, key)
        random_sequence = []
        for _ in range(length):
            next_bit = state[0]
            random_sequence.append(next_bit)
            state = self.apply_rule(state)
        return random_sequence

    @staticmethod
    def string_to_bin(message):
        """将字符串转换为二进制列表"""
        return [int(bit) for char in message for bit in f"{ord(char):08b}"]

    @staticmethod
    def bin_to_string(binary_list):
        """将二进制列表转换为字符串"""
        chars = [chr(int(''.join(map(str, binary_list[i:i + 8])), 2)) for i in range(0, len(binary_list), 8)]
        return ''.join(chars)

    @staticmethod
    def bin_to_base64(binary_list):
        """将二进制列表转换为Base64编码"""
        byte_array = bytes((int(''.join(map(str, binary_list[i:i + 8])), 2) for i in range(0, len(binary_list), 8)))
        return base64.b64encode(byte_array).decode('utf-8')

    @staticmethod
    def base64_to_bin(base64_str):
        """将Base64编码转换为二进制列表"""
        byte_array = base64.b64decode(base64_str)
        return [int(bit) for byte in byte_array for bit in f"{byte:08b}"]

    def encrypt(self, message, key):
        """加密消息"""
        message_bin = self.string_to_bin(message)
        random_sequence = self.generate_random_sequence(len(message_bin), key)
        encrypted_bin = [m ^ r for m, r in zip(message_bin, random_sequence)]
        return self.bin_to_base64(encrypted_bin)

    def decrypt(self, encrypted_base64, key):
        """解密消息"""
        encrypted_bin = self.base64_to_bin(encrypted_base64)
        random_sequence = self.generate_random_sequence(len(encrypted_bin), key)
        decrypted_bin = [e ^ r for e, r in zip(encrypted_bin, random_sequence)]
        return self.bin_to_string(decrypted_bin)
