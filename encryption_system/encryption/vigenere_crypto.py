import string
class VigenereCipher:
    def __init__(self, key):
        self.key = key  # 密钥
        self.lower_tab = string.ascii_lowercase  # 小写字母表
        self.upper_tab = string.ascii_uppercase  # 大写字母表
        self.digit_tab = string.digits           # 数字字符表

    def encrypt(self, text):
        cipher_text = ''  # 存储加密后的文本
        key_index = 0  # 密钥字符的索引
        for char in text:
            if char.isupper():  # 处理大写字母
                # 将密钥字符转换为大写并计算偏移
                offset = ord(self.key[key_index % len(self.key)].upper()) - ord('A')
                # 根据偏移量加密当前大写字母
                cipher_text += self.upper_tab[(self.upper_tab.index(char) + offset) % 26]
                key_index += 1  # 移动密钥字符的索引
            elif char.islower():  # 处理小写字母
                # 将密钥字符转换为小写并计算偏移
                offset = ord(self.key[key_index % len(self.key)].lower()) - ord('a')
                # 根据偏移量加密当前小写字母
                cipher_text += self.lower_tab[(self.lower_tab.index(char) + offset) % 26]
                key_index += 1  # 移动密钥字符的索引
            elif char.isdigit():  # 处理数字字符
                # 计算当前密钥字符的偏移量（大写字母），
                # 假设用大写字母的偏移来加密数字
                offset = ord(self.key[key_index % len(self.key)].upper()) - ord('A')
                # 根据偏移量加密当前数字字符
                cipher_text += self.digit_tab[(self.digit_tab.index(char) + offset) % 10]
                key_index += 1  # 移动密钥字符的索引
            else:  # 其他字符不加密处理，直接添加
                cipher_text += char
        return cipher_text

    def decrypt(self, text):
        plain_text = ''  # 存储解密后的文本
        key_index = 0  # 密钥字符的索引
        for char in text:
            if char.isupper():  # 处理大写字母
                # 计算当前密钥字符的偏移量
                offset = ord(self.key[key_index % len(self.key)].upper()) - ord('A')
                # 根据偏移量解密当前大写字母
                plain_text += self.upper_tab[(self.upper_tab.index(char) - offset) % 26]
                key_index += 1  # 移动密钥字符的索引
            elif char.islower():  # 处理小写字母
                # 计算当前密钥字符的偏移量
                offset = ord(self.key[key_index % len(self.key)].lower()) - ord('a')
                # 根据偏移量解密当前小写字母
                plain_text += self.lower_tab[(self.lower_tab.index(char) - offset) % 26]
                key_index += 1  # 移动密钥字符的索引
            elif char.isdigit():  # 处理数字字符
                # 计算当前密钥字符的偏移量
                offset = ord(self.key[key_index % len(self.key)].upper()) - ord('A')
                # 根据偏移量解密当前数字字符
                plain_text += self.digit_tab[(self.digit_tab.index(char) - offset) % 10]
                key_index += 1  # 移动密钥字符的索引
            else:  # 其他字符不解密处理，直接添加
                plain_text += char
        return plain_text