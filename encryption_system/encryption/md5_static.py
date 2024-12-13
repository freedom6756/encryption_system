import math


class MD5_Static:
    def __init__(self):
        # 初始化常量
        self.A = '0x67452301'
        self.B = '0xefcdab89'
        self.C = '0x98badcfe'
        self.D = '0x10325476'
        self.Ti_count = 1

        # 定义每轮运算中的函数
        self.F = lambda x, y, z: ((x & y) | ((~x) & z))
        self.G = lambda x, y, z: ((x & z) | (y & (~z)))
        self.H = lambda x, y, z: (x ^ y ^ z)
        self.I = lambda x, y, z: (y ^ (x | (~z)))
        self.L = lambda x, n: (((x << n) | (x >> (32 - n))) & (0xffffffff))

        # 定义每轮循环左移的位数
        self.shi_1 = (7, 12, 17, 22) * 4
        self.shi_2 = (5, 9, 14, 20) * 4
        self.shi_3 = (4, 11, 16, 23) * 4
        self.shi_4 = (6, 10, 15, 21) * 4

        # 定义每轮中的M[]的顺序
        self.m_1 = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
        self.m_2 = (1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12)
        self.m_3 = (5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2)
        self.m_4 = (0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9)

    def T(self, i):
        """生成常数T[i]"""
        result = (int(4294967296 * abs(math.sin(i)))) & 0xffffffff
        return result

    def shift(self, shift_list):
        """按MD5规则左移并更新顺序"""
        shift_list = [shift_list[3], shift_list[0], shift_list[1], shift_list[2]]
        return shift_list

    def fun(self, fun_list, f, m, shi):
        """执行MD5的一轮运算"""
        count = 0
        while count < 16:
            xx = int(fun_list[0], 16) + f(int(fun_list[1], 16), int(fun_list[2], 16), int(fun_list[3], 16)) + int(
                m[count], 16) + self.T(self.Ti_count)
            xx = xx & 0xffffffff
            ll = self.L(xx, shi[count])
            fun_list[0] = hex((int(fun_list[1], 16) + ll) & 0xffffffff)
            fun_list = self.shift(fun_list)
            count += 1
            self.Ti_count += 1
        return fun_list

    def genM16(self, order, ascii_list, f_offset):
        """生成每轮的M[]数组"""
        ii = 0
        m16 = [0] * 16
        f_offset = f_offset * 64
        for i in order:
            i = i * 4
            m16[ii] = '0x' + ''.join((ascii_list[i + f_offset] + ascii_list[i + 1 + f_offset] + ascii_list[
                i + 2 + f_offset] + ascii_list[i + 3 + f_offset]).split('0x'))
            ii += 1
        for c in m16:
            ind = m16.index(c)
            m16[ind] = self.reverse_hex(c)
        return m16

    def reverse_hex(self, hex_str):
        """翻转十六进制数的字节顺序"""
        hex_str = hex_str[2:]
        hex_str_list = [hex_str[i:i + 2] for i in range(0, len(hex_str), 2)]
        hex_str_list.reverse()
        return '0x' + ''.join(hex_str_list)

    def show_result(self, f_list):
        """格式化并显示结果"""
        result = ''
        f_list1 = [0] * 4
        for i in f_list:
            f_list1[f_list.index(i)] = self.reverse_hex(i)[2:]
            result += f_list1[f_list.index(i)]
        return result

    def hash(self, input_m):
        """计算输入消息的MD5值"""
        abcd_list = [self.A, self.B, self.C, self.D]
        self.Ti_count = 1

        # 将输入转为ascii列表
        ascii_list = list(map(hex, map(ord, input_m)))
        msg_lenth = len(ascii_list) * 8
        ascii_list.append('0x80')

        # 填充消息
        while (len(ascii_list) * 8 + 64) % 512 != 0:
            ascii_list.append('0x00')

        # 添加消息的长度信息
        msg_lenth_0x = hex(msg_lenth)[2:]
        msg_lenth_0x = '0x' + msg_lenth_0x.rjust(16, '0')
        msg_lenth_0x_big_order = self.reverse_hex(msg_lenth_0x)[2:]
        msg_lenth_0x_list = ['0x' + msg_lenth_0x_big_order[i:i + 2] for i in range(0, len(msg_lenth_0x_big_order), 2)]
        ascii_list.extend(msg_lenth_0x_list)

        # 处理每个512位的分组
        for i in range(0, len(ascii_list) // 64):
            aa, bb, cc, dd = abcd_list
            order_1 = self.genM16(self.m_1, ascii_list, i)
            order_2 = self.genM16(self.m_2, ascii_list, i)
            order_3 = self.genM16(self.m_3, ascii_list, i)
            order_4 = self.genM16(self.m_4, ascii_list, i)

            # 执行4轮运算
            abcd_list = self.fun(abcd_list, self.F, order_1, self.shi_1)
            abcd_list = self.fun(abcd_list, self.G, order_2, self.shi_2)
            abcd_list = self.fun(abcd_list, self.H, order_3, self.shi_3)
            abcd_list = self.fun(abcd_list, self.I, order_4, self.shi_4)

            # 将结果与初始的A, B, C, D进行相加
            output_a = hex((int(abcd_list[0], 16) + int(aa, 16)) & 0xffffffff)
            output_b = hex((int(abcd_list[1], 16) + int(bb, 16)) & 0xffffffff)
            output_c = hex((int(abcd_list[2], 16) + int(cc, 16)) & 0xffffffff)
            output_d = hex((int(abcd_list[3], 16) + int(dd, 16)) & 0xffffffff)
            abcd_list = [output_a, output_b, output_c, output_d]
            self.Ti_count = 1

        return self.show_result(abcd_list)

    def check_message(self, message):
        """直接计算MD5并返回结果"""
        return self.hash(message)
