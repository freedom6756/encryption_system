class Autokey_Plaintext:
    # 定义字母表
    DIC = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self, key):
        self.key = key.lower()  # 密钥转换为小写

    # 加密函数
    def encrypt(self, plaintext):
        ciphertext = ""  # 初始化密文字符串
        key = self.key + plaintext  # 将密钥与明文拼接，形成初始密钥
        key_index = 0  # 密钥位置的索引
        for char in plaintext:
            if char.isalpha():  # 只对字母进行加密
                # 获取当前明文字母和密钥字母的索引
                char_index = self.DIC.index(char.lower())
                key_index_char = self.DIC.index(key[key_index].lower())
                # 通过维吉尼亚密码公式进行加密：密文字母 = (明文字母 + 密钥字母) % 26
                encrypted_char = self.DIC[(char_index + key_index_char) % 26]
                # 保持字母的大小写
                if char.isupper():
                    ciphertext += encrypted_char.upper()
                else:
                    ciphertext += encrypted_char
                # 增加密钥的位置索引
                key_index += 1
            else:
                # 对非字母字符不加密，直接添加到密文
                ciphertext += char
        return ciphertext

    # 解密函数
    def decrypt(self, ciphertext):
        plaintext = ""  # 初始化明文字符串
        key_index = 0  # 密钥位置的索引
        key = self.key  # 初始密钥
        for char in ciphertext:
            if char.isalpha():  # 只对字母进行解密
                # 获取当前密文字母和密钥字母的索引
                char_index = self.DIC.index(char.lower())
                key_index_char = self.DIC.index(key[key_index].lower())
                # 通过维吉尼亚密码公式进行解密：明文字母 = (密文字母 - 密钥字母) % 26
                decrypted_char = self.DIC[(char_index - key_index_char) % 26]
                # 保持字母的大小写
                if char.isupper():
                    plaintext += decrypted_char.upper()
                else:
                    plaintext += decrypted_char
                # 增加密钥的位置索引并将解密后的字符添加到密钥
                key += decrypted_char
                key_index += 1
            else:
                # 对非字母字符不解密，直接添加到明文
                plaintext += char
        return plaintext