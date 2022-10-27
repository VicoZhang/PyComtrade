# PyComtrade

读取 Comtrade 数据格式文件。

目前版本为V2.1，后续将在本仓库中进行更新。请注意，这份代码仅为初步实现，后续还有很大的拓展和改进空间，因此欢迎对代码做出修改和补充，同时请将修改后的代码 push 到本仓库中。

## 使用方法

在 src 目录下有两个文件，其中 PyComtrade_Base.py 为内核文件，一般情况下无需修改；
PyComtrade.py 中给出了封装好的 ComtradeFile 类的使用范例，范例中所用到的数据文件在 example 目录下。

## 当前版本实现的功能

1. 通过 ComtradeFile.save_csv() 方法将 Comtrade 文件转换成 csv 数据格式。该格式通用性较强，可导入多种软件。
2. 通过 ComtradeFile.save_png() 方法将 Comtrade 文件转显示为 png 图片。
3. 通过 ComtradeFile.save_mat() 方法将 Comtrade 文件导出为 .mat 文件，可直接导入在 MATLAB 中，做后续分析。

## 当前版本局限性

1. 只能读取二进制格式数据下的模拟通道数据。
2. 未能实现时间与数据点的匹配。
3. ……

上述内容或将在后续更新中进行补充。

