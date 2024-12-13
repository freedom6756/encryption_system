import re

class Autokey_Ciphertext:
    def __init__(self, key, filter='[^a-z]'):
        """
        初始化autokey加密类，接受一个密钥和过滤标点的正则表达式
        """
        self.keyword = key.lower()
        self.filter = filter

    def remove_punctuation(self, text):
        """
        移除文本中的标点符号，只保留小写字母
        """
        return re.sub(self.filter, '', text.lower())

    def encrypt(self, text):
        """
        使用autokey加密法加密给定文本
        """
        text = self.remove_punctuation(text)
        res = ""
        key = self.keyword
        for i, c in enumerate(text):
            if i < len(key):
                offset = ord(key[i]) - 97
            else:
                offset = ord(res[i - len(key)]) - 97
            res += chr((ord(c) - 97 + offset) % 26 + 97)
        return res

    def decrypt(self, text):
        """
        使用autokey加密法解密给定文本
        """
        text = self.remove_punctuation(text)
        res = ""
        key = self.keyword
        for i, c in enumerate(text):
            if i < len(key):
                offset = ord(key[i]) - 97
            else:
                offset = ord(text[i - len(key)]) - 97
            res += chr((ord(c) - 97 - offset) % 26 + 97)
        return res

