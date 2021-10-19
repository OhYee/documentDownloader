from PIL import Image
from reportlab.pdfgen import canvas
import os
import sys

def build_pdf(temp_dir: str, img_list: list, output_file: str):
    pdf = canvas.Canvas('./' + output_file + '.pdf')
    for img in img_list:
        file_path = "{}/{}".format(temp_dir, img[img.rfind('/') + 1:])
        if not os.path.exists(file_path):
            print("Some images missing, please use -f(--force) to force re-download")
            sys.exit(1)
        w, h = Image.open(file_path).size
        pdf.setPageSize((w, h))
        pdf.drawImage(file_path, 0, 0, w, h)
        pdf.showPage()
    pdf.save()
