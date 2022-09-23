from pdf2image import convert_from_path
from pytesseract import image_to_string
import pytesseract
import os
list_of_pdfs = [val for val in list_of_files if val.endswith(".pdf")]

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\patelp21\AppData\Local\Tesseract-OCR\tesseract"

def convert_pdf_to_img(pdf_file):
    return convert_from_path(pdf_file)
#                             ,poppler_path= r'C:\Users\patelp21\Downloads\Code File\poppler-0.68.0_x86.7z\bin')

#poppler_path=r'C:\Program Files\poppler-0.68.0\bin'

def convert_image_to_text(file):
    
    text = image_to_string(file, config='--psm 11')
    #text = image_to_string(file)
    return text

def get_text_from_any_pdf(pdf_file):
    images = convert_pdf_to_img(pdf_file)
    final_text = ''
    for pg, img in enumerate(images):
        final_text += convert_image_to_text(img)
    return final_text

os.chdir(r"C:\Users\patelp21\Downloads\Code File\Code File\2007_to_2013\txts")

for each_pdf in list_of_pdfs:
    try:
        pdf_data = (get_text_from_any_pdf(each_pdf))
    except:
        continue
    text_file = open(each_pdf[:8] +".txt", "w")
    n = text_file.write(pdf_data)
    text_file.close()