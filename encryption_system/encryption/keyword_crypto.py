import string
class KeywordCipher:
    def __init__(self, keyword):
        self.keyword = keyword
        self.cipher_alphabet_lower, self.cipher_alphabet_upper = self.cipher_alphabet(keyword)

    # 生成关键词加密表
    def cipher_alphabet(self, keyword):
        # 去除重复字母
        seen = set()  # 初始化一个空集合跟踪已经遇到的字母，避免重复
        filtered_keyword = ""  # 空字符串用来保存处理后的密钥
        for char in keyword:
            if char.lower() not in seen:  # 处理大写字母的情况
                seen.add(char.lower())
                filtered_keyword += char
        # 填充字母表，去掉已经使用的字母
        alphabet_lower = string.ascii_lowercase  # 小写字母表
        remaining_letters_lower = [char for char in alphabet_lower if char not in seen]
        # 创建密文字母表：首先是密钥的字母，然后是剩下的字母
        cipher_alphabet_lower = filtered_keyword.lower() + ''.join(remaining_letters_lower)
        # 处理大写字母表，使用与小写字母相同的顺序
        cipher_alphabet_upper = cipher_alphabet_lower.upper()
        return cipher_alphabet_lower, cipher_alphabet_upper

    def encrypt(self, plain_text):
        alphabet_lower = string.ascii_lowercase
        cipher_text = ""
        for char in plain_text:
            if char.isalpha():
                # 处理小写字母
                if char.islower():
                    idx = alphabet_lower.index(char)
                    cipher_char = self.cipher_alphabet_lower[idx]
                # 处理大写字母
                elif char.isupper():
                    idx = alphabet_lower.index(char.lower())
                    cipher_char = self.cipher_alphabet_upper[idx]
                cipher_text += cipher_char
            else:
                # 非字母字符保持不变
                cipher_text += char
        return cipher_text

    def decrypt(self, cipher_text):
        alphabet_lower = string.ascii_lowercase
        plain_text = ""
        for char in cipher_text:
            if char.isalpha():
                # 处理小写字母
                if char.islower():
                    idx = self.cipher_alphabet_lower.index(char)
                    plain_char = alphabet_lower[idx]
                # 处理大写字母
                elif char.isupper():
                    idx = self.cipher_alphabet_upper.index(char)
                    plain_char = alphabet_lower[idx]
                # 保持原字母的大小写
                if char.isupper():
                    plain_char = plain_char.upper()
                plain_text += plain_char
            else:
                # 非字母字符保持不变
                plain_text += char
        return plain_text