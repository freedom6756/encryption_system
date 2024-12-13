class Caesar:
    def __init__(self, shift):
        self.shift = shift

    def encrypt(self, plain_text):
        cipher_text = ""
        for char in plain_text:
            if char.isalpha():  # 判断字符是否为字母
                shift_base = 65 if char.isupper() else 97  # 大写字母或小写字母的ASCII基准
                encrypted_char = chr((ord(char) - shift_base + self.shift) % 26 + shift_base)
                cipher_text += encrypted_char
            else:
                cipher_text += char  # 非字母字符直接加入到密文中
        return cipher_text

    def decrypt(self, cipher_text):
        plain_text = ""
        for char in cipher_text:
            if char.isalpha():  # 判断字符是否为字母
                shift_base = 65 if char.isupper() else 97  # 大写字母或小写字母的ASCII基准
                decrypted_char = chr((ord(char) - shift_base - self.shift) % 26 + shift_base)
                plain_text += decrypted_char
            else:
                plain_text += char  # 非字母字符直接加入到明文中
        return plain_text
