"""
批量化处理示例
"""

import os
from PyComtrade import ComtradeFile

files = os.listdir('Comtrade_files')
for file in files:
    name = os.listdir(os.path.join('Comtrade_files', file))
    reader = ComtradeFile(file_path=os.path.join('Comtrade_files', file), file_name=name[0].replace('.cfg', ''))
    reader.save_csv(csv_path='../csv/{}'.format(file))

