class DoublePlayfairCipher:
    def __init__(self, key1, key2):
        # 将密钥转换为小写并将所有的'j'替换为'i'
        self.key1 = key1.lower().replace('j', 'i')
        self.key2 = key2.lower().replace('j', 'i')
        # 使用两个密钥生成两个Playfair矩阵
        self.matrix1 = self.create_playfair_matrix(self.key1)
        self.matrix2 = self.create_playfair_matrix(self.key2)

    def create_playfair_matrix(self, key):
        # 创建一个5x5的Playfair矩阵
        unique_key = ""
        # 去除密钥中的重复字母
        for char in key:
            if char not in unique_key:
                unique_key += char
        # Playfair密码表的字母表，'j'被视为'i'
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

    def find_position(self, char, matrix):
        # 查找字符在Playfair矩阵中的位置，返回行和列
        for i, row in enumerate(matrix):
            for j, col in enumerate(row):
                if col == char:
                    return i, j
        return None

    def encrypt_pair(self, a, b, matrix):
        # 加密一对字符，返回加密后的字符
        row_a, col_a = self.find_position(a, matrix)
        row_b, col_b = self.find_position(b, matrix)
        if row_a == row_b:
            # 如果a和b在同一行，替换为同一行的下一个字符
            return matrix[row_a][(col_a + 1) % 5] + matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            # 如果a和b在同一列，替换为同一列的下一个字符
            return matrix[(row_a + 1) % 5][col_a] + matrix[(row_b + 1) % 5][col_b]
        else:
            # 如果a和b既不在同一行也不在同一列，交换a和b的位置
            return matrix[row_a][col_b] + matrix[row_b][col_a]

    def decrypt_pair(self, a, b, matrix):
        # 解密一对字符，返回解密后的字符
        row_a, col_a = self.find_position(a, matrix)
        row_b, col_b = self.find_position(b, matrix)
        if row_a == row_b:
            # 如果a和b在同一行，替换为同一行的前一个字符
            return matrix[row_a][(col_a - 1) % 5] + matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            # 如果a和b在同一列，替换为同一列的前一个字符
            return matrix[(row_a - 1) % 5][col_a] + matrix[(row_b - 1) % 5][col_b]
        else:
            # 如果a和b既不在同一行也不在同一列，交换a和b的位置
            return matrix[row_a][col_b] + matrix[row_b][col_a]

    def encrypt(self, text):
        # 加密明文
        # 1. 预处理明文
        plain_text = self.preprocess_text(text)
        cipher_text = ""
        # 2. 使用第一个矩阵进行加密
        for i in range(0, len(plain_text), 2):
            cipher_text += self.encrypt_pair(plain_text[i], plain_text[i + 1], self.matrix1)
        # 3. 使用第二个矩阵进行加密
        encrypted_text = ""
        for i in range(0, len(cipher_text), 2):
            encrypted_text += self.encrypt_pair(cipher_text[i], cipher_text[i + 1], self.matrix2)
        return encrypted_text

    def decrypt(self, text):
        # 解密密文
        # 1. 使用第二个矩阵解密
        decrypted_text = ""
        for i in range(0, len(text), 2):
            decrypted_text += self.decrypt_pair(text[i], text[i + 1], self.matrix2)
        # 2. 使用第一个矩阵解密
        plain_text = ""
        for i in range(0, len(decrypted_text), 2):
            plain_text += self.decrypt_pair(decrypted_text[i], decrypted_text[i + 1], self.matrix1)
        # 3. 去除最后可能出现的多余的'X'，并恢复原始明文的字符
        decrypted_text = self.remove_x_padding(plain_text)
        return decrypted_text

    def remove_x_padding(self, text):
        # 清理解密后填充的'X'字符
        if len(text) > 1 and text[-1] == 'x' and text[-2] != 'x':
            text = text[:-1]  # 删除末尾的x字符
        # 清理插入的x字符
        return text.replace('x', '')
