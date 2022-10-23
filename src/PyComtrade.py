import os.path
import struct
import matplotlib.pyplot as plt
import csv


class ComtradeFile:

    def __init__(self, file_path, file_name):
        self.cfg_path = os.path.join(file_path, file_name + '.cfg')
        self.dat_path = os.path.join(file_path, file_name + '.dat')

        self.channel_num = ...  # 通道总数量
        self.a_chan_num = ...  # 模拟通道数
        self.d_chan_num = ...  # 数字通道数

        self.cfg_info = []  # 存储“.cfg”读入数据
        self.dat_info = []  # 存储“.dat”读入数据

        self.a_chan_info = []  # 存储模拟通道数的信息，格式为字典
        self.a_data_info = []  # 存储模拟通道数的数据

        self.sys_freq = ...  # 系统频率
        self.sample_freq_num = ...  # 采样频率个数
        self.sample_freq = []  # 采样频率
        self.sample_num = []  # 采样点数

        self.data_format = ...  # 数据存储方式 Bin 或者 ASCII
        self.pack_format = ...

        self.dat_read_length = ...  # 每次采样的需要读入的数据长度

        self._read_cfg()
        self._read_dat()

    def _read_cfg(self):
        with open(self.cfg_path) as cfg_file:
            self.cfg_info = [line.replace('\n', '').split(',') for line in cfg_file.readlines()]

        self.channel_num = self.cfg_info[1][0]
        self.a_chan_num = eval(self.cfg_info[1][1].replace('A', ''))
        self.d_chan_num = eval(self.cfg_info[1][2].replace('D', ''))

        self.sys_freq = self.cfg_info[-9][0]
        self.sample_freq_num = self.cfg_info[-8][0]
        self.sample_freq = [self.cfg_info[-6][0], self.cfg_info[-5][0]]
        self.sample_num = [eval(self.cfg_info[-6][1]), eval(self.cfg_info[-5][1])]

        self.data_format = self.cfg_info[-2][0]

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
            self.a_chan_info[i]['K1'] = self.cfg_info[i + 2][10]
            self.a_chan_info[i]['K2'] = self.cfg_info[i + 2][11]
            self.a_chan_info[i]['PorS'] = self.cfg_info[i + 2][12]
            self.a_chan_info[i]['ana_data'] = []

    def _read_dat(self):
        self.dat_read_length = 4 + 4 + 2 * self.a_chan_num + 2 * int(self.d_chan_num / 16)
        self.pack_format = '<' + 'I' * 2 + 'h' * self.a_chan_num + 'H' * int(self.d_chan_num / 16)
        n_struct = struct.Struct(self.pack_format)
        mode = 'rb' if self.data_format == 'BINARY' else 'rb'

        with open(self.dat_path, mode=mode) as dat_file:
            self.a_data_info = [dat_file.read(self.dat_read_length) for i in range(self.sample_num[1])]

        for i in range(self.sample_num[1]):
            n_unpacked_data = n_struct.unpack(self.a_data_info[i])
            for j in range(self.a_chan_num):
                self.a_chan_info[j]['ana_data'].append(n_unpacked_data[2 + j])

        for i in range(self.sample_num[1]):
            for j in range(self.a_chan_num):
                self.a_chan_info[j]['ana_data'][i] = \
                    self.a_chan_info[j]['ana_data'][i] * self.a_chan_info[j]['FA'] + self.a_chan_info[j]['FB']

    def save_csv(self, csv_path):
        os.makedirs(csv_path) if not os.path.exists(csv_path) else ...
        for i in range(self.a_chan_num):
            file_name = self.a_chan_info[i]['a_name']
            with open(os.path.join(csv_path, file_name), 'w') as csv_obj:
                writer = csv.writer(csv_obj)
                writer.writerow(self.a_chan_info[i]['ana_data'])


if __name__ == '__main__':
    test = ComtradeFile('../initial_file', 'BAY01_0001_20221020_114520_483')
    test.save_csv('../csv')
