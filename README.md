# 文档下载器
可用于下载[book118](https://max.book118.com/)的PDF文档

## 思路
1. 爬虫爬取图片链接
2. 下载图片
3. 将图片拼合成pdf文件

##　使用方法
1. 安装Python3
2. 安装`reportlab`
  `python -m pip install reportlab`
3. 导入book118模块，并调用`makePDF(pid)`方法。
  其中，pid是要下载页面的id(链接中最后的数字)

**仅供学习爬虫及相关知识，请支持正版图书**
*虽然book118上的好多pdf也是盗版吧*