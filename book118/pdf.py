from PIL import Image
from reportlab.pdfgen import canvas


def build_pdf(temp_dir: str, img_list: list, output_file: str):
    pdf = canvas.Canvas(output_file)
    for img in img_list:
        file_path = "{}/{}.jpg".format(temp_dir, img)
        w, h = Image.open(file_path).size
        pdf.setPageSize((w, h))
        pdf.drawImage(file_path, 0, 0, w, h)
        pdf.showPage()
    pdf.save()
