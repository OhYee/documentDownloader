import re
import json
import os
import shutil
from spider import getHTML, makeURL
from pdf import makePDF
import ssl


class book118:
    def __init__(self, pid):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.pid = str(pid)
        self.pdfInfo = {}
        self.domain = ''
        self.index = -1
        self.total = 0
        self.imgList = []
        self.imgFileList = []

    def getPDF(self):
        # 获取需要的信息
        self.__getPdfInfo()
        print(self.pdfInfo)
        #　获得所有图片的地址
        img = self.pdfInfo.get('Img')
        imgUrl = img if img != None else ""
        while self.index != self.total:
            self.__getNextPage(
                self.imgList[-1]
                if len(self.imgList) != 0 else imgUrl
            )
        # 下载图片
        self.__getIMG()
        # 生成pdf
        makePDF(self.imgFileList, 'book118.pdf')

    def __getPdfInfo(self):
        url = makeURL('https://max.book118.com/index.php?',
                      {
                          'g': 'Home',
                          'm': 'View',
                          'a': 'viewUrl',
                          'cid': str(self.pid),
                          'flag': '1'
                      })
        viewPage = getHTML(url)
        self.domain = re.findall(r'//(.*?)\..*', viewPage)[0]
        rawHTML = getHTML('https:' + viewPage)
        res = re.findall(
            r'<input type="hidden" id="(.*?)" value="(.*?)".*?/>', rawHTML)
        for lst in res:
            self.pdfInfo[lst[0]] = lst[1]

    def __getNextPage(self, imgUrl):
        url = makeURL('https://' + self.domain + '.book118.com/PW/GetPage/?', {
            'f': self.pdfInfo['Url'],
            'img': imgUrl,
            'isMobile': 'false',
            'isNet': 'True',
            'readLimit': self.pdfInfo['ReadLimit'],
            'furl': self.pdfInfo['Furl']
        })
        result = getHTML(url)
        res = json.loads(result)

        if self.total == 0:
            self.total = res['PageCount']
        self.index = res['PageIndex']
        self.imgList.append(res['NextPage'])

        print(self.index, '/', self.total, 'url finish', res['NextPage'])

        return res

    def __getIMG(self):
        if os.path.exists('./temp'):
            shutil.rmtree('./temp')
        os.makedirs('./temp')

        for (idx, img) in enumerate(self.imgList):
            res = getHTML(
                makeURL('http://' + self.domain + '.book118.com/img/?', {'img': img}), byte=True)
            with open('./temp/' + str(idx + 1) + '.jpg', 'wb') as f:
                f.write(res)
            print(idx + 1, '/', self.total,
                  'download finish', str(idx + 1) + '.jpg')
            self.imgFileList.append('./temp/' + str(idx + 1) + '.jpg')
        # ?img=Hs92T42xAvsP_ycWPqjcj8Iw69WUDaxvq4HtxAb3Zl3WYzxX1hdIsZzydhmmGAtm
        pass


if __name__ == '__main__':
    #pdf = book118(115219794)
    pdf = book118(137343582)
    pdf.getPDF()
