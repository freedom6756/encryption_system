class PermutationCipher:
    def __init__(self, key):
        self.key = key
        # 生成置换规则
        self.key_order = self.key_order(key)

    # 根据密钥生成对应的置换规则
    # 密钥的每个字母按字典顺序编号，返回一个包含字母编号的元组
    def key_order(self, key):
        # set()去除重复字母，sorted()按字典顺序排序
        unique_key = ''.join(sorted(set(key), key=key.index))
        # 为每个字母分配编号
        key_order = sorted(range(len(unique_key)), key=lambda i: unique_key[i])
        return key_order

    # 调整文本长度，使其能被block_size整除
    def adjust_text_length(self, text, block_size):
        # 如果文本长度不能被block_size整除，补充空格
        padding_length = (block_size - len(text) % block_size) % block_size
        return text + ' ' * padding_length

    # 加密函数
    def encrypt(self, plaintext):
        # 去除文本中的空格
        plaintext = plaintext.replace(' ', '')
        # 调整明文长度，使其能被密钥长度整除
        block_size = len(self.key)
        plaintext = self.adjust_text_length(plaintext, block_size)
        # 按照密钥长度将明文分块
        blocks = [plaintext[i:i + block_size] for i in range(0, len(plaintext), block_size)]
        # 加密：根据key_order对每一块的字符进行重新排列
        ciphertext = ''
        for block in blocks:
            cipher_block = ''.join(block[i] for i in self.key_order)
            ciphertext += cipher_block
        return ciphertext

    # 解密函数
    def decrypt(self, ciphertext):
        # 确定分组长度
        block_size = len(self.key)
        # 将密文分块
        blocks = [ciphertext[i:i + block_size] for i in range(0, len(ciphertext), block_size)]
        # 根据key_order反向置换字符
        plaintext = ''
        # 对每一个块根据key_order将密文块的字符放回原来的位置
        for block in blocks:
            decrypted_block = [''] * block_size
            for i, char in zip(self.key_order, block):
                decrypted_block[i] = char
            plaintext += ''.join(decrypted_block)
        # 去除补充的空格，恢复原始明文
        return plaintext.rstrip()
