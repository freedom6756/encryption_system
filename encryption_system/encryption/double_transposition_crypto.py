class DoubleTranspositionCipher:
    def __init__(self, first_keyword, second_keyword):
        self.first_keyword = first_keyword
        self.second_keyword = second_keyword
        self.first_cols = len(first_keyword)
        self.second_cols = len(second_keyword)
        self.first_order = self.get_column_order(first_keyword)
        self.second_order = self.get_column_order(second_keyword)

    # 根据关键字获取列的顺序
    def get_column_order(self, keyword):
        column_order = list(range(len(keyword)))
        return sorted(column_order, key=lambda x: keyword[x])

    # 创建矩阵
    def create_matrix(self, text, cols):
        rows = (len(text) + cols - 1) // cols
        matrix = []
        index = 0

        for _ in range(rows):
            row = []
            for _ in range(cols):
                if index < len(text):
                    row.append(text[index])
                    index += 1
                else:
                    row.append(' ')  # 填充空格
            matrix.append(row)
        return matrix

    def read_matrix_by_columns(self, matrix, column_order):
        rows = len(matrix)
        ciphertext = []
        for col in column_order:
            for row in range(rows):
                ciphertext.append(matrix[row][col])
        return ''.join(ciphertext).rstrip()

    def write_matrix_by_columns(self, ciphertext, rows, cols, column_order):
        matrix = [[''] * cols for _ in range(rows)]
        index = 0
        for col in column_order:
            for row in range(rows):
                if index < len(ciphertext):
                    matrix[row][col] = ciphertext[index]
                    index += 1
        return matrix

    def encrypt(self, plaintext):
        # 第一次列置换
        rows_1 = (len(plaintext) + self.first_cols - 1) // self.first_cols
        matrix_1 = self.create_matrix(plaintext, self.first_cols)
        intermediate_cipher = self.read_matrix_by_columns(matrix_1, self.first_order)

        # 第二次列置换
        rows_2 = (len(intermediate_cipher) + self.second_cols - 1) // self.second_cols
        matrix_2 = self.create_matrix(intermediate_cipher, self.second_cols)
        final_cipher = self.read_matrix_by_columns(matrix_2, self.second_order)

        return final_cipher

    def decrypt(self, ciphertext):
        # 第二次列置换的逆操作
        rows_2 = (len(ciphertext) + self.second_cols - 1) // self.second_cols
        matrix_2 = self.write_matrix_by_columns(ciphertext, rows_2, self.second_cols, self.second_order)
        intermediate_text = ''.join(''.join(row) for row in matrix_2).rstrip()

        # 第一次列置换的逆操作
        rows_1 = (len(intermediate_text) + self.first_cols - 1) // self.first_cols
        matrix_1 = self.write_matrix_by_columns(intermediate_text, rows_1, self.first_cols, self.first_order)
        plaintext = ''.join(''.join(row) for row in matrix_1).rstrip()

        return plaintext
