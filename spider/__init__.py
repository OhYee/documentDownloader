import urllib.request


def makeURL(host, args):
    url = host
    for key in args:
        url += key + '=' + args[key] + '&'
    url = url[0:-1]
    return url


def getHTML(url, byte=False):
    # print("getting " + url)
    response = urllib.request.urlopen(url)
    html = response.read()
    if not byte:
        html = html.decode('utf-8')
    return html
