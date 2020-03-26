#pip install pdfminer.six
#pip install PyPDF2
#https://stackoverflow.com/questions/26494211/extracting-text-from-a-pdf-file-using-pdfminer-in-python

import os
import re
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO 
import datetime
import sys


DEVELOPMENT = True

if DEVELOPMENT:
    SAVE_FOLDER = os.path.join('output')
else:
    SAVE_FOLDER = r'F:\\USERS\\PUBLIC\\Hardcopy Storage\\CSR Hardcopies'

def split_PDF(path):
    """
    Method to split a multi-page PDF into single page files.
    This breaks up the Oracle file into individual hardcopies.

    path: filepath of the Oracle multi-page PDF
    """

    #get pdf name without the file extension and load pdf file
    fname     = os.path.splitext(os.path.basename(path))[0]
    pdf       = PdfFileReader(path)
    TIMESTAMP = datetime.datetime.now().strftime("%m%d_")

    #iterate through the pages and pull them out into their own separate PDF
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        #Create a temporary output name to create the file with
        #before parsing and renaming it later
        output_filename = f'output/{fname}_page_{page}.pdf'

        #Save files to a separate output folder and add a counter to separate them
        try:
            counter = 0
            #If the file doesnt exist already, create it. 
            if not os.path.exists(output_filename):
                with open(output_filename, 'wb') as out:
                    pdf_writer.write(out)
            else:
                #Account for if theres the same zip and same state scanned at the same time
                while os.path.exists(os.path.join(SAVE_FOLDER, f'delete_{fname}_{TIMESTAMP}{counter}.pdf')):
                    counter += 1
                    output_filename = os.path.join(SAVE_FOLDER, f'delete_{fname}_{TIMESTAMP}{counter}.pdf')
                with open(output_filename, 'wb') as out:
                    pdf_writer.write(out)
        
            #Raw text read in from PDFs, split into a list for easier retrieval
            text   = convert_pdf_to_txt(output_filename)

            #Find the 'P&O' numbers
            PO_num = str(re.search(r'(P&O:\s*)(\d{7})', text).group(2))

            #Find the state initials
            state  = str(re.search(r'(\d{7}\s)([A-Z]{2})', text).group(2))

            #rename the file to inclue the PO, State and page counter (to remove duplication issues)
            new_filename = os.path.join(SAVE_FOLDER, f'{PO_num}_{state}_{TIMESTAMP}.pdf')

            #if the file doesnt exist, rename the temp filename to the new one
            if not os.path.exists(new_filename):
                os.rename(output_filename, new_filename)

            else:
                #If it already exists, append a counter number to the end to not remove duplicates
                while os.path.exists(os.path.join(SAVE_FOLDER, f'{PO_num}_{state}_{TIMESTAMP}{counter}.pdf')):
                    counter += 1

                new_filename = os.path.join(SAVE_FOLDER, f'{PO_num}_{state}_{TIMESTAMP}{counter}.pdf')
                # os.remove(output_filename)
                os.rename(output_filename, new_filename)
        except:
            print('------ Something happened here, but let\'s just pretend it didn\'t ------')

def convert_pdf_to_txt(path):
    """
    Parses the text from a PDF at the given path.
    path: filepath of the PDF to parse.
    return: str
    """
    rsrcmgr     = PDFResourceManager()
    retstr      = StringIO()
    codec       = 'utf-8'
    laparams    = LAParams()
    device      = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp          = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password    = ""
    maxpages    = 10
    caching     = True
    pagenos     = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    #Make sure everything is closed as to not run into file issues
    fp.close()
    device.close()
    retstr.close()

    #Returns PDF text as string
    return text