from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape


def makePDF(imgFileList, pdfFilename):
    pdf = canvas.Canvas(pdfFilename)
    (w, h) = landscape(A4)
    for file in imgFileList:
        pdf.drawImage(file, 0, 0, h, w)
        pdf.showPage()
    pdf.save()
