# PyComtrade

读取 `Comtrade` 数据格式文件，并将其转换成 `csv`、`mat`、`png` 等数据格式。其中 `Comtrade` 数据格式参考[COMTRADE文件格式详解](https://blog.csdn.net/Mr_robot_strange/article/details/121905288)。

## 项目结构



## 使用方法

> 假设：`PyComtrade.py` 文件存储于目录：

## 更新日志

#### V2.1

通过 `ComtradeFile.save_mat()` 方法将 `Comtrade` 文件导出为 `.mat` 文件，可直接导入在 MATLAB 中，做后续分析。

#### V2.0

通过 `ComtradeFile.save_csv()` 方法将 `Comtrade` 文件转换成 `csv` 数据格式。该格式通用性较强，可在多种软件中导入。

通过 `ComtradeFile.save_png()` 方法将 `Comtrade` 文件转显示为 `png` 图片。

## 注意事项
1. 对于采样频率，注意同一组数据在不同的部分可能采样频率是不一样的，具体采样频率的值仍需要参考`cfg`文件获取。
2. `mat`文件在读入MATLAB时，如果直接双击打开，可能会出错。保险的做法是将`mat`文件放入MATLAB当前文件夹中，用`load`函数加载。
2. 如果遇到环境依赖问题，可按照文件 自行配置

