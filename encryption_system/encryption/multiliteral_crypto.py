import re

class MultiliteralCipher:
    def __init__(self, key):
        # 设置密钥并准备字母表（全部小写字母）
        self.key = key.lower()
        self.keywordList = [chr(i) for i in range(97, 123) if chr(i) != 'j']  # a-z (去掉j)

    def removePunctuation(self, text):
        """ 清除文本中的非字母字符并将字母转换为小写 """
        filter = '[^a-z]'
        return re.sub(filter, '', text.lower())

    def encrypt(self, plaintext):
        """ 使用Multiliteral Cipher加密 """
        # 处理明文，替换j为i
        plain = self.removePunctuation(plaintext).replace('j', 'i')
        cipher = ''
        for i in range(len(plain)):
            # 获取明文字母在字母表中的位置
            row = int(self.keywordList.index(plain[i]) / 5)
            col = self.keywordList.index(plain[i]) % 5
            # 用密钥中对应位置的字母替换
            cipher += self.key[row]
            cipher += self.key[col]
        return cipher

    def decrypt(self, ciphertext):
        """ 使用Multiliteral Cipher解密 """
        # 清除密文中的非字母字符
        cipher = self.removePunctuation(ciphertext).replace('j', 'i')
        plain = ''
        # 两两遍历密文
        for i in range(0, len(cipher), 2):
            row = self.key.index(cipher[i])
            col = self.key.index(cipher[i + 1])
            # 通过密钥中字母的位置找出明文中对应字母的索引
            num = row * 5 + col
            plain += self.keywordList[num]
        return plain
