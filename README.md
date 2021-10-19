# 文档下载器

[![Sync to Gitee](https://github.com/OhYee/documentDownloader/workflows/Sync%20to%20Gitee/badge.svg)](https://gitee.com/OhYee/documentDownloader) [![Publish to PyPI](https://github.com/OhYee/documentDownloader/workflows/Publish%20to%20PyPI/badge.svg)](https://pypi.org/project/documentDownloader/) [![Publish to TestPyPI](https://github.com/OhYee/documentDownloader/workflows/Publish%20to%20TestPyPI/badge.svg)](https://test.pypi.org/project/documentDownloader/) [![Release](https://github.com/OhYee/documentDownloader/workflows/Release/badge.svg)](https://github.com/OhYee/documentDownloader/releases)   
[![version](https://img.shields.io/github/v/tag/OhYee/documentDownloader)](https://github.com/OhYee/documentDownloader/tags) [![pypi version](https://img.shields.io/pypi/v/documentDownloader)](https://pypi.org/project/documentDownloader/) [![License](https://img.shields.io/github/license/OhYee/documentDownloader)](./LICENSE)  

可用于下载[book118](https://max.book118.com/)的PDF文档

## 思路

1. 爬虫爬取图片链接
2. 下载图片
3. 将图片拼合成pdf文件

## 参数说明

|参数             |解释                                                                                                |必备参数|
|:----------------|:--------------------------------------------------------------------------------------------------|:------|
|`-h`、`--help`   |显示帮助                                                                                            |❌     |
|`-u`、`--url`    |要下载的文件的网页地址                                                                           |✔      |
|`-o`、`--output` |文件保存名，默认是文档的标题.pdf                                                                       |❌     |
|`-p`、`--proxy`  |设置要使用的代理地址（默认使用环境变量中`HTTP_PROXY`和`HTTPS_PROXY`设置的值），可以使用`-p ''`强制设置不走代理 |❌     |
|`-f`、`--force`  |强制重新下载，不使用缓存                                                                               |❌     |
|`-t`、`--thread` |要使用的线程数，如不指定默认是10                                                                                        |❌    |
|`-s`、`--safe`   |如果被服务器拒绝可以打开此选项，将强制单线程，并增加请求和下载的间隔时间                                                                                        |❌    |

## 使用模块

### 使用已上传到 PyPI 的包
```bash
python3 -m pip install documentDownloader
```

安装完成后即可直接使用 `documentDownloader` 命令

如：`documentDownloader -u https://max.book118.com/html/2020/0109/5301014320002213.shtm -o '单身人群专题研究报告-2019' -p http://127.0.0.1:1080 -f -t 20`

### 直接使用源码中的 main.py 

克隆该项目，或在[releases](https://github.com/OhYee/documentDownloader/releases)页面选择版本下载

1. 安装Python3
2. 安装依赖模块(Pillow、reportlab、requests) `python -m pip install -r requirements.txt`
3. 使用 `python3 main.py` 执行

如：`python main.py -u https://max.book118.com/html/2020/0109/5301014320002213.shtm -o '单身人群专题研究报告-2019' -p http://127.0.0.1:1080 -f -t 20`

**仅供学习爬虫及相关知识，请支持正版图书**  
*虽然book118上的好多pdf也是盗版吧*

## 贡献列表

- [OhYee](https://github.com/OhYee)
- [JodeZer](https://github.com/JodeZer)

## 更新

- 2019-01-29: Book118网站更新,更改对应部分代码. [@JodeZer](https://github.com/JodeZer)
- 2020-01-09: 重构代码，增加多线程下载加速，允许使用代理，允许通过已有缓存直接建立pdf，自动识别图片大小生成pdf [@OhYee](https://github.com/OhYee)
- 2020-05-25: 发布到 PyPI
- 2021-10-18: Book118网站更新，更改部分代码； 设置默认导出pdf的文件名为文档标题； 对无法免费预览全文的文档增加提示； 调整请求间隔为2秒(实测请求间隔小于2秒很可能会返回空地址)； 增加"慢速下载"选项，防止下载过快被服务器拒绝。[@alxt17](https://github.com/alxt17)