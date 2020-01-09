# 文档下载器

可用于下载[book118](https://max.book118.com/)的PDF文档

## 思路

1. 爬虫爬取图片链接
2. 下载图片
3. 将图片拼合成pdf文件

## 使用方法

1. 安装Python3
2. 安装依赖模块(Pillow、reportlab、requests) `python -m pip install -r requirements.txt`
3. 使用相应命令下载内容

```
python main.py -i <document id>
    -h --help       show help
    -i --id         document id (required)
    -o --output     output file (default `book118.pdf`)
    -p --proxy      proxy url (default using `http_proxy` and `https_proxy`)
    -f --force      force re-download images
    -t --thread     thread number for downloading images
```

完整命令：`python main.py -i https://max.book118.com/html/2020/0109/5301014320002213.shtm -o '单身人群专题研究报告-2019.pdf' -p http://127.0.0.1:1080 -f -t 20`
其中，文档id可以直接使用id本身(`5301014320002213`)，也可以使用页面链接(`https://max.book118.com/html/2020/0109/5301014320002213.shtm`)

**仅供学习爬虫及相关知识，请支持正版图书**  
*虽然book118上的好多pdf也是盗版吧*

## 贡献列表

- [OhYee](https://github.com/OhYee)
- [JodeZer](https://github.com/JodeZer)

## 更新

- 2019-01-29: Book118网站更新,更改对应部分代码. [@JodeZer](https://github.com/JodeZer)
- 2020-01-09: 重构代码，增加多线程下载加速，允许使用代理，允许通过已有缓存直接建立pdf，自动识别图片大小生成pdf [@OhYee](https://github.com/OhYee)