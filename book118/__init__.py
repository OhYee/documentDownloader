from .book118 import *
from .pdf import *
from .request import *
from .thread import *

import getopt


def solve_argv(argv):
    help_text = '''python main.py -i <document id>
    -h --help       show help
    -i --id         document id (required)
    -o --output     output file (default `book118.pdf`)
    -p --proxy      proxy url (default using `http_proxy` and `https_proxy`)
    -f --force      force re-download images
    -t --thread     thread number for downloading images
'''

    document_id = None
    http_proxy = os.environ.get("HTTP_PROXY")
    https_proxy = os.environ.get("HTTPS_PROXY")
    force_redownload = False
    output_file = "./book118.pdf"
    thread_number = 10

    try:
        opts, args = getopt.getopt(
            argv, "hi:o:p:ft:", ["help", "id=", "proxy=", "output=", "force", "thread="])
    except getopt.GetoptError:
        print(help_text)
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(help_text)
            exit(0)
        elif opt in ("-i", "--id"):
            try:
                document_id = int(arg)
            except:
                document_id = int(re.findall(
                    r"https://max.book118.com/html/\d+/\d+/(\d+).shtm", arg)[0])
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
    if document_id == None:
        print(help_text)
        exit(1)
    return (document_id, http_proxy, https_proxy,
            force_redownload, output_file, thread_number)


def main():
    (document_id, http_proxy, https_proxy,
     force_redownload, output_file, thread_number) = solve_argv(sys.argv[1:])
    set_proxy(http_proxy, https_proxy)

    document_download(document_id, force_redownload,
                      output_file, thread_number)
