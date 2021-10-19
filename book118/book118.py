import json
import sys
import os
import re
import threading
from .thread import Thread
from .pdf import build_pdf
from .request import get_page
import time


def get_next_pages(info: dict, page: int):
    '''
    根据当前图片获取下六张图片地址
    '''
    result_text = get_page("https://openapi.book118.com/getPreview.html?", {
        "project_id": 1,
        "aid": info["aid"],
        "view_token": info["view_token"],
        "page": str(page),
        "callback": "jQuery",  # 这个参数其实可有可无，名字也无所谓
        "_": int(round(time.time() * 1000))  # 时间戳
    }).text[7:-2]  # 截掉"jQuery("和末尾的");"，得到包含预览图片地址的json
    result = json.loads(result_text)
    return result


def get_page_info(document_url: str) -> dict:
    '''
    获取文档信息
    '''
    preview_webpage = get_page(document_url).text

    info = {"aid": re.findall(r'\d+', re.findall(r'office: {.*\n.*aid: \d+', preview_webpage)[0]),
            # 获得office: {之后的aid，为解密后的id
            "view_token": re.findall(r' view_token: \'.+\'', preview_webpage)[0][14:-1],
            "title": re.findall(r' title: \'.+\'', preview_webpage)[0][9:-1],
            "preview_page": re.findall(r' preview_page: \d+', preview_webpage)[0][15:],  # 可预览的页数
            "actual_page": re.findall(r' actual_page: \d+', preview_webpage)[0][14:]  # 实际文章页数
            }
    if info["preview_page"] != info["actual_page"]:
        print(
            "attention! only {} of {} page(s) are free to preview(download)\n".format(info["preview_page"],
                                                                                      info["actual_page"]))
    return info


def get_image_url_list(info: dict, safe_download: bool) -> list:
    '''
    获取文档预览图片地址列表
    '''
    current_page = 1
    retry = 5
    img_url_list = []
    while current_page <= int(info["preview_page"]):
        json_data = get_next_pages(info, current_page)
        for value in json_data["data"].values():
            if value == '':
                if retry == 0:
                    print("Cannot get correct response, too many fails.")
                    sys.exit(1)
                print("Empty response, retrying {}. Consider using -s(--safe) to limit request frequency".format(retry))
                time.sleep(1)
                retry -= 1
                break
            print("Getting image url {}/{}".format(current_page, info["preview_page"]))
            img_url_list.append("https:" + value)
            current_page += 1
            retry = 5
        if safe_download:
            time.sleep(3)
        else:
            time.sleep(2)
    return img_url_list


def document_download(document_url: str, force_redownload: bool,
                      output_file: str, thread_number: int, safe_download: bool):
    document_id = int(re.findall(
        r"https://max.book118.com/html/\d+/\d+/(\d+).shtm", document_url)[0])
    temp_dir = "./temp/{}".format(document_id)
    temp_file = "{}/{}".format(temp_dir, "img_list")

    if force_redownload or not os.path.exists(temp_file):
        info = get_page_info(document_url)
        if output_file is None:
            output_file = info["title"]
        img_url_list = get_image_url_list(info, safe_download)

        if not os.path.exists("./temp/"):
            os.mkdir("./temp/")
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)
        with open(temp_file, 'w') as f:
            f.write(info["title"] + "\n")
            [f.write(img_url + "\n") for img_url in img_url_list]
    else:
        with open(temp_file, 'r') as f:
            img_url_list = f.read().split("\n")
            if output_file is None:
                output_file = img_url_list[0]
            img_url_list = img_url_list[1:]
            img_url_list = list(filter(lambda x: len(x) > 0, img_url_list))

    download_list = img_url_list if force_redownload else list(filter(
        lambda x: not os.path.exists("{}/{}".format(temp_dir, x[x.rfind('/') + 1:])),
        img_url_list
    ))

    print(download_list)

    lock = threading.Lock()

    def task_pool() -> str:
        '''
        获取一个未下载的图片
        '''
        nonlocal download_list
        img = None
        lock.acquire()
        if len(download_list) != 0:
            img = download_list[0]
        download_list = download_list[1:]
        lock.release()
        return img

    def download_image(thread_id: int, img_url: str):
        with open("{}/{}".format(temp_dir, img_url[img_url.rfind('/') + 1:]), "wb") as f:
            print("Thread", thread_id, "download image", img_url)
            f.write(get_page(img_url).content)
        if safe_download:
            time.sleep(1)

    threads = [Thread(i, download_image, task_pool)
               for i in range(thread_number)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    del threads

    print("Downloading images finished. Generate PDF file ", output_file + '.pdf')

    build_pdf(temp_dir, img_url_list, output_file)

    print("Generating PDF file finished. File name ", output_file + '.pdf')
