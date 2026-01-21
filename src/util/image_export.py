import tkinter
import platform
import os
import io
from PIL import Image, EpsImagePlugin
import pathlib
import pymupdf
from time import sleep
def save1(canvas, pathname):
    canvas.update()
    ps = canvas.postscript(colormode='color', pagewidth=5000)
    img = Image.open(io.BytesIO(ps.encode('utf-8')))
    img.save(pathname)



def save2(pathname):
    """
   Uneix pdfs en uno
    """
    # Code from
    # https://pymupdf.readthedocs.io/en/latest/recipes-images.html#how-to-make-one-pdf-of-all-your-pictures-or-files

    doc = pymupdf.open()  # PDF with the pictures
    imgdir = pathname[:-4]  # where the pics are
    imglist = os.listdir(imgdir)  # list of them

    for i, f in enumerate(imglist):
        img = pymupdf.open(os.path.join(imgdir, f), filetype="txt")  # open pic as document
        rect = img[0].rect  # pic dimension
        pdfbytes = img.convert_to_pdf()  # make a PDF stream
        img.close()  # no longer needed

        os.remove(os.path.join(imgdir, f))

        imgpdf = pymupdf.open("pdf", pdfbytes)  # open stream as PDF
        page = doc.new_page(width=rect.width,  # new page with ...
                            height=rect.height)  # pic dimension
        page.show_pdf_page(rect, imgpdf, 0)  # image fills the page
    if "Win" in platform.system():
        doc.save(pathname)
    else:
        doc.save(pathname)
    pass

def prompt(canvas_list):
    outputfile = tkinter.filedialog.asksaveasfilename(filetypes=[('PDF files', '*.pdf')])
    pathlib.Path(outputfile[:-4]).mkdir(parents=True, exist_ok=True)
    counter = 0
    for canvas in canvas_list:
        counter += 1
        nom = f"Figura_{counter}"
        path = f"{outputfile[:-4]}/{nom}.png"
        save1(canvas, path)
    save2(outputfile)
    os.rmdir(outputfile[:-4])



