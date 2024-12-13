class PlayfairCipher:
    def __init__(self, key):
        # 将密钥转换为小写并将所有的'j'替换为'i'
        self.key = key.lower().replace('j', 'i')
        # 使用密钥生成Playfair矩阵
        self.matrix = self.create_playfair_matrix(self.key)

    def create_playfair_matrix(self, key):
        # 创建一个5x5的Playfair密钥矩阵
        unique_key = ""
        # 去除密钥中的重复字母
        for char in key:
            if char not in unique_key:
                unique_key += char
        # Playfair密码表的字母表，包含a-z字母，'j'被视为'i'
        alphabet = "abcdefghiklmnopqrstuvwxyz"  # 不包括'j'，'j'视为'i'
        matrix = []
        # 将密钥中的字母填充到矩阵中
        for char in unique_key:
            if char not in matrix:
                matrix.append(char)
        # 将不在密钥中的字母填充到矩阵中
        for char in alphabet:
            if char not in matrix:
                matrix.append(char)
        # 返回5x5矩阵，按行分配
        return [matrix[i:i + 5] for i in range(0, 25, 5)]

    def preprocess_text(self, text):
        # 预处理明文，符合Playfair加密规则
        # 1. 转换为小写字母
        # 2. 将字母'j'视为'i'
        # 3. 去除所有非字母字符
        # 4. 将明文拆分为两两一组，若某一组字母重复，则在第二个字母后插入'X'
        text = text.lower().replace('j', 'i')
        processed_text = ""
        text = text.replace(" ", "")  # 移除空格
        i = 0
        while i < len(text):
            # 如果相邻两个字母相同，则在第二个字母后插入'X'
            if i + 1 < len(text) and text[i] == text[i + 1]:
                processed_text += text[i] + 'x'
                i += 1
            else:
                processed_text += text[i]
                if i + 1 < len(text):
                    processed_text += text[i + 1]
                else:
                    processed_text += 'x'  # 如果只有一个字母，添加'X'使其成为一对
                i += 2
        return processed_text

    def find_position(self, char):
        # 查找字符在Playfair矩阵中的位置，返回行和列
        for i, row in enumerate(self.matrix):
            for j, col in enumerate(row):
                if col == char:
                    return i, j
        return None

    def encrypt_pair(self, a, b):
        # 加密一对字符，返回加密后的字符
        row_a, col_a = self.find_position(a)  # 获取字符a的位置
        row_b, col_b = self.find_position(b)  # 获取字符b的位置
        if row_a == row_b:
            # 如果a和b在同一行，替换为同一行的下一个字符
            return self.matrix[row_a][(col_a + 1) % 5] + self.matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            # 如果a和b在同一列，替换为同一列的下一个字符
            return self.matrix[(row_a + 1) % 5][col_a] + self.matrix[(row_b + 1) % 5][col_b]
        else:
            # 如果a和b既不在同一行也不在同一列，交换a和b的位置
            return self.matrix[row_a][col_b] + self.matrix[row_b][col_a]

    def decrypt_pair(self, a, b):
        # 解密一对字符，返回解密后的字符
        row_a, col_a = self.find_position(a)  # 获取字符a的位置
        row_b, col_b = self.find_position(b)  # 获取字符b的位置
        if row_a == row_b:
            # 如果a和b在同一行，替换为同一行的前一个字符
            return self.matrix[row_a][(col_a - 1) % 5] + self.matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            # 如果a和b在同一列，替换为同一列的前一个字符
            return self.matrix[(row_a - 1) % 5][col_a] + self.matrix[(row_b - 1) % 5][col_b]
        else:
            # 如果a和b既不在同一行也不在同一列，交换a和b的位置
            return self.matrix[row_a][col_b] + self.matrix[row_b][col_a]

    def encrypt(self, text):
        # 加密明文
        # 1. 预处理明文
        plain_text = self.preprocess_text(text)
        cipher_text = ""
        # 2. 将预处理后的明文按两两字符加密
        for i in range(0, len(plain_text), 2):
            cipher_text += self.encrypt_pair(plain_text[i], plain_text[i + 1])
        return cipher_text

    def decrypt(self, text):
        # 解密密文
        plain_text = ""
        # 1. 每两两一组解密密文
        for i in range(0, len(text), 2):
            plain_text += self.decrypt_pair(text[i], text[i + 1])
        # 2. 去除最后可能出现的多余的'X'，并恢复原始明文的字符
        decrypted_text = plain_text.rstrip('x')
        # 3. 恢复'j'为'i'
        decrypted_text = decrypted_text.replace('i', 'j')
        # 4. 去除因重复字母插入的'X'，如果它不是最后一个字符
        if len(decrypted_text) > 1 and decrypted_text[-1] == 'x' and decrypted_text[-2] != 'x':
            decrypted_text = decrypted_text[:-1]
        return decrypted_text