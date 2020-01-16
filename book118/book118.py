import sys
import os
import re
import threading
from .thread import Thread
from .pdf import build_pdf
from .request import get_page


def get_preview_page_url(document_id: int or str) -> str:
    '''
    获取Book118预览页地址
    '''
    return get_page("https://max.book118.com/index.php",  {
        "g": "Home",
        "m": "View",
        "a": "ViewUrl",
        "cid": document_id,
        "flag": 1,
    }).text


def get_next_page(info: object, img: str):
    '''
    根据当前图片获取下一张图片地址
    '''
    result = get_page('https://' + info["domain"] + '.book118.com/PW/GetPage/?', {
        'f': info['Url'],
        'img': img,
        'isMobile': 'false',
        'isNet': 'True',
        'readLimit': info['ReadLimit'],
        'furl': info['Furl']
    }).json()
    return result


def get_page_info(document_id: int or str) -> object:
    '''
    获取文档信息
    '''
    preview_url = get_preview_page_url(document_id)
    preview_page = get_page("https:" + preview_url).text

    info = {
        "domain": re.findall(r'//(.*?)\..*', preview_url)[0]
    }
    forms = re.findall(
        r'<input type="hidden" id="(.*?)" value="(.*?)".*?/>', preview_page)
    for form in forms:
        info[form[0]] = form[1]
    return info


def get_image_list(document_id: int or str, info: object) -> list:
    '''
    获取文档预览图片地址列表
    '''
    img_list = []
    while 1:
        json_data = get_next_page(info, ""if len(
            img_list) == 0 else img_list[-1])
        print("Get image url {}/{} {}".format(
            json_data["PageIndex"], json_data["PageCount"], json_data["NextPage"]
        ))
        img_list.append(json_data["NextPage"])
        if json_data["PageCount"] <= json_data["PageIndex"]:
            break
    return img_list


def document_download(document_id: int or str,  force_redownload: bool,
                      output_file: str, thread_number: int):
    domain = ""
    img_list = []
    temp_dir = "./temp/{}".format(document_id)
    temp_file = "{}/{}".format(temp_dir, "img_list")

    if force_redownload or not os.path.exists(temp_file):
        info = get_page_info(document_id)
        domain = info["domain"]
        img_list = get_image_list(document_id, info)
        if not os.path.exists("./temp/"):
            os.mkdir("./temp/")
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)
        with open(temp_file, 'w') as f:
            f.write(info["domain"]+"\n")
            [f.write(img+"\n") for img in img_list]
    else:
        with open(temp_file, 'r') as f:
            img_list = f.read().split("\n")
            domain = img_list[0]
            img_list = img_list[1:]
            img_list = list(filter(lambda x: len(x) > 0, img_list))

    download_list = img_list if force_redownload else list(filter(
        lambda x: not os.path.exists("{}/{}.jpg".format(temp_dir, x)),
        img_list
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

    def download_image(thread_id: int, img: str):
        with open("{}/{}.jpg".format(temp_dir, img), "wb") as f:
            print("Thread", thread_id, "download image", img)
            f.write(get_page('http://' + domain +
                             '.book118.com/img/?', {'img': img}).content)

    threads = [Thread(i, download_image, task_pool)
               for i in range(thread_number)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    del threads

    print("Downloading images finished. Generate PDF file ", output_file)

    build_pdf(temp_dir, img_list, output_file)

    print("Generating PDF file finished. File name ", output_file)
