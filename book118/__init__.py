from .book118 import *
from .pdf import *
from .request import *
from .thread import *

import getopt


def solve_argv(argv):
    help_text = '''python main.py -u <document url>
    -h --help       show help
    -u --url         document url (required)
    -o --output     output file (default `book118.pdf`)
    -p --proxy      proxy url (default using `http_proxy` and `https_proxy`)
    -f --force      force re-download images
    -t --thread     thread number for downloading images
    -s --safe       limit download request in case server refuses
'''

    document_url = None
    http_proxy = os.environ.get("HTTP_PROXY")
    https_proxy = os.environ.get("HTTPS_PROXY")
    force_redownload = False
    output_file = None
    thread_number = 10
    safe_download = False

    try:
        opts, args = getopt.getopt(
            argv, "hu:o:p:ft:s", ["help", "url=", "proxy=", "output=", "force", "thread=", "safe"])
    except getopt.GetoptError:
        print(help_text)
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(help_text)
            exit(0)
        elif opt in ("-u", "--url"):
            document_url = arg
        elif opt in ("-o", "--output"):
            output_file = arg
        elif opt in ("-p", "--proxy"):
            http_proxy = https_proxy = arg
        elif opt in ("-f", "--force"):
            force_redownload = True
        elif opt in ("-t", "--thread"):
            try:
                thread_number = int(arg)
            except:
                pass
        elif opt in ("-s", "--safe"):
            safe_download = True
    if document_url == None:
        print(help_text)
        exit(1)
    return (document_url, http_proxy, https_proxy,
            force_redownload, output_file, thread_number, safe_download)


def main():
    (document_url, http_proxy, https_proxy,
     force_redownload, output_file, thread_number, safe_download) = solve_argv(sys.argv[1:])
    set_proxy(http_proxy, https_proxy)
    if safe_download:
        thread_number = 1
    document_download(document_url, force_redownload,
                      output_file, thread_number, safe_download)
