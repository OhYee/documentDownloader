import requests

session = requests.Session()
http_proxy = ""
https_proxy = ""
proxies = {}


def set_proxy(_http_proxy: str, _https_proxy: str):
    global http_proxy, https_proxy, proxies
    http_proxy = _http_proxy
    https_proxy = _https_proxy
    proxies = {}
    if http_proxy != '':
        proxies['http'] = http_proxy
    if https_proxy != '':
        proxies['https'] = https_proxy
    print("Proxy has been set", proxies)


def get_page(url: str, params: object = None) -> requests.Response:
    '''
    通过GET访问指定网页（带超时和重传机制），出错直接结束程序
    '''
    global session, http_proxy, https_proxy
    retry = 10
    response = None
    if params == None:
        params = {}
    while retry > 0:
        try:
            response = session.get(
                url, params=params, timeout=10, proxies=proxies)
            break
        except Exception as e:
            print("Get page error: {}, {} times left...".format(e, retry))
            retry -= 1
    if response == None:
        print("Can not get the page {}".format(url))
        exit(1)
    return response
