# PyComtrade

读取 Comtrade 数据格式文，其中 Comtrade 数据格式采取1999年标准。

目前代码版本为V2.1，后续将在本仓库中进行更新。
请注意，这份代码仅为初步实现，后续还有很大的拓展和改进空间，因此欢迎对代码做出修改和补充，同时请将修改后的代码 push 到本仓库中。

## 使用方法

在 src 目录下有两个文件，其中 PyComtrade_Base.py 为内核文件，一般情况下无需修改；
PyComtrade.py 中给出了封装好的 ComtradeFile 类的使用范例，范例中所用到的数据文件在 example 目录下。

## 当前版本实现的功能

1. 通过 ComtradeFile.save_csv() 方法将 Comtrade 文件转换成 csv 数据格式。该格式通用性较强，可在多种软件中导入。
2. 通过 ComtradeFile.save_png() 方法将 Comtrade 文件转显示为 png 图片。
3. 通过 ComtradeFile.save_mat() 方法将 Comtrade 文件导出为 .mat 文件，可直接导入在 MATLAB 中，做后续分析。

## 当前版本局限性

1. 只能读取二进制格式数据下的模拟通道数据。
2. 未能实现时间与数据点的匹配。
3. ……

上述内容或将在后续更新中进行补充。

## 使用注意事项
1. 对于采样频率，注意同一组数据在不同的部分可能采样频率是不一样的，具体采样频率的值仍需要参考cfg文件获取。
2. mat文件在读入MATLAB时，如果直接双击打开，可能会出错。保险的做法是将mat文件放入MATLAB当前文件夹中，用load函数加载。

