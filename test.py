import book118
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
if __name__ == '__main__':
    book118.getPDF(137343582)
