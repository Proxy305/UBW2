from reportlab.pdfgen import canvas
from PIL import Image

#useful tip
# get image size
#img = Image.open(img_file_name)
#img.size # this returns a tuple

class merge:
    def __init__(self, pdf_file_name, size = None):
        self.canvas = canvas.Canvas(file_name, size)

    def addPage(img_file_name):
        canvas.drawImage(img_file_name, 0, 0)
        canvas.showPage()

    def save():
        self.canvas.save()