import os.path
import struct
import csv
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image


class ComtradeFile:

    def __init__(self, file_path, file_name):
        self.cfg_path = os.path.join(file_path, file_name + '.cfg')
        self.dat_path = os.path.join(file_path, file_name + '.dat')

        self.channel_num = ...  # 通道总数量
        self.a_chan_num = ...  # 模拟通道数
        self.d_chan_num = ...  # 数字通道数

        self.cfg_info = []  # 存储“.cfg”文件读入数据

        self.a_chan_info = []  # 存储模拟通道数的信息，格式为字典
        self.a_data_info = []  # 存储模拟通道数的数据，用于解析

        self.sys_freq = ...  # 系统频率
        self.sample_freq_num = ...  # 采样频率个数
        self.sample_freq = []  # 采样频率
        self.sample_num = []  # 采样点数

        self.data_format = ...  # 数据存储方式 Bin 或者 ASCII
        self.pack_format = ...  # 数据解析方式

        self.dat_read_length = ...  # 每次解析时需要读入的数据长度

        self._read_cfg()  # 初始化操作
        self._read_dat()  # 初始化操作

    def _read_cfg(self):
        with open(self.cfg_path) as cfg_file:
            self.cfg_info = [line.replace('\n', '').split(',') for line in cfg_file.readlines()]

        # 通道数量信息
        self.channel_num = eval(self.cfg_info[1][0])
        self.a_chan_num = eval(self.cfg_info[1][1].replace('A', ''))
        self.d_chan_num = eval(self.cfg_info[1][2].replace('D', ''))
        print('通道数量解析错误') if self.a_chan_num + self.d_chan_num != self.channel_num else ...

        # 频率信息
        self.sys_freq = eval(self.cfg_info[2+self.channel_num][0])
        print('注意系统频率非50Hz') if self.sys_freq != 50 else ...

        # 采样信息
        self.sample_freq_num = eval(self.cfg_info[3+self.channel_num][0])
        self.sample_freq = [eval(self.cfg_info[4+self.channel_num+i][0]) for i in range(0, self.sample_freq_num)]
        self.sample_num = [eval(self.cfg_info[4+self.channel_num+i][1]) for i in range(0, self.sample_freq_num)]
        ... if self.sample_freq_num == len(self.sample_freq) and self.sample_freq_num == len(
            self.sample_num) else print('采样信息处读取错误')

        # 数据存储信息
        self.data_format = self.cfg_info[-2][0]

        # 模拟量含义
        for i in range(self.a_chan_num):
            self.a_chan_info.append({})
            self.a_chan_info[i]['a_NO.'] = self.cfg_info[i + 2][0]
            self.a_chan_info[i]['a_name'] = self.cfg_info[i + 2][1]
            self.a_chan_info[i]['a_phase'] = self.cfg_info[i + 2][2]
            self.a_chan_info[i]['a_component'] = self.cfg_info[i + 2][3]
            self.a_chan_info[i]['a_unit'] = self.cfg_info[i + 2][4]
            self.a_chan_info[i]['FA'] = float(self.cfg_info[i + 2][5])
            self.a_chan_info[i]['FB'] = float(self.cfg_info[i + 2][6])
            self.a_chan_info[i]['fTime'] = self.cfg_info[i + 2][7]
            self.a_chan_info[i]['fMin'] = self.cfg_info[i + 2][8]
            self.a_chan_info[i]['fMax'] = self.cfg_info[i + 2][9]
            self.a_chan_info[i]['K1'] = float(self.cfg_info[i + 2][10])
            self.a_chan_info[i]['K2'] = float(self.cfg_info[i + 2][11])
            self.a_chan_info[i]['PorS'] = self.cfg_info[i + 2][12]
            self.a_chan_info[i]['ana_data'] = []  # 存储真实信息

        print('cfg文件已正确解析')

    def _read_dat(self):
        self.dat_read_length = 4 + 4 + 2 * self.a_chan_num + 2 * int(self.d_chan_num / 16)  # 单次解析数据字节长度
        self.pack_format = '<' + 'I' * 2 + 'h' * self.a_chan_num + 'H' * int(self.d_chan_num / 16)  # 单词解析数据类型
        n_struct = struct.Struct(self.pack_format)
        mode = 'rb' if self.data_format == 'BINARY' else 'r'  # todo 有待考究

        with open(self.dat_path, mode=mode) as dat_file:
            self.a_data_info = [dat_file.read(self.dat_read_length) for _ in range(self.sample_num[1])]

        # 解析数据
        for i in range(self.sample_num[1]):
            n_unpacked_data = n_struct.unpack(self.a_data_info[i])
            for j in range(self.a_chan_num):
                self.a_chan_info[j]['ana_data'].append(n_unpacked_data[2 + j])

        # 转换成真实值
        for i in range(self.sample_num[1]):
            for j in range(self.a_chan_num):
                self.a_chan_info[j]['ana_data'][i] = \
                    self.a_chan_info[j]['ana_data'][i] * self.a_chan_info[j]['FA'] + self.a_chan_info[j]['FB']

        print('dat文件已正常解析')

    def save_csv(self, path):  # 保存数据位csv格式
        os.makedirs(path) if not os.path.exists(path) else ...
        for i in range(self.a_chan_num):
            file_name = self.a_chan_info[i]['a_name'] + '.csv'
            with open(os.path.join(path, file_name), 'w') as csv_obj:
                writer = csv.writer(csv_obj)
                writer.writerow(self.a_chan_info[i]['ana_data'])
        print("csv数据文件已生成，保存在{}目录下".format(path))

    def save_png(self, path):
        os.makedirs(path) if not os.path.exists(path) else ...
        for i in range(self.a_chan_num):
            plt.plot(self.a_chan_info[i]['ana_data'], linewidth=0.5)
            img_path = path + '/{}.png'.format(self.a_chan_info[i]['a_name'])
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            plt.title('{}'.format(self.a_chan_info[i]['a_name']))
            plt.savefig(img_path)
            plt.close()
        print("图片已经正常绘制，保存在{}目录下".format(path))


if __name__ == '__main__':
    test = ComtradeFile('../test_file/2022-09-16_21-16-52_35kV枇杷岭站A机_10kV石下线CSC-211_录波文件', 'PL10_62_RCD_136_20220916_211652_803')
    test.save_png('../png')

