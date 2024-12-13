class ColumnPermutationCipher:
    def __init__(self, keyword):
        self.keyword = keyword
        self.cols = len(keyword)  # 列数为关键字的长度
        self.column_order = self.get_column_order()  # 根据关键字获取列的顺序

    def get_column_order(self):
        # 创建一个列表存储列的顺序索引
        column_order = list(range(self.cols))
        # 根据关键字的字母顺序对列索引进行排序
        sorted_order = sorted(column_order, key=lambda x: self.keyword[x])
        # key=lambda x: self.keyword[x]表示根据每个索引位置的字母来排序
        return sorted_order

    # 创建矩阵
    def create_matrix(self, text, rows):
        matrix = []
        index = 0

        # 按行列存储文本
        for i in range(rows):
            row = []
            for j in range(self.cols):
                # 如果还有剩余的字符，则填充当前行的列
                if index < len(text):
                    row.append(text[index])
                    index += 1
                else:
                    row.append(' ')  # 如果文本不足，填充空格
            matrix.append(row)
        return matrix

    # 加密函数
    def encrypt(self, plaintext):
        # 计算需要的行数，确保文本能够填充到矩阵
        rows = (len(plaintext) + self.cols - 1) // self.cols
        matrix = self.create_matrix(plaintext, rows)  # 创建加密矩阵

        ciphertext = []
        # 按照列顺序读取矩阵的内容，按列拼接生成密文
        for col in self.column_order:
            for row in range(rows):
                ciphertext.append(matrix[row][col])
        return ''.join(ciphertext).rstrip()  # 将密文拼接为字符串，去掉末尾的空格

    # 解密函数
    def decrypt(self, ciphertext):
        # 计算需要的行数，确保密文能够填充到矩阵
        rows = (len(ciphertext) + self.cols - 1) // self.cols
        matrix = [[''] * self.cols for _ in range(rows)]  # 创建空矩阵

        # 将密文按列顺序填充到矩阵中
        index = 0
        for col in self.column_order:
            for row in range(rows):
                if index < len(ciphertext):
                    matrix[row][col] = ciphertext[index]
                    index += 1

        # 读取矩阵内容按行拼接得到明文
        decryptedtext = []
        for row in range(rows):
            decryptedtext.extend(matrix[row])

        return ''.join(decryptedtext).rstrip()  # 将解密后的字符拼接为字符串，去掉末尾的空格