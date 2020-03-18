import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import extract_1
#https://stackoverflow.com/questions/26494211/extracting-text-from-a-pdf-file-using-pdfminer-in-python


def pdf_splitter(path):
    #get pdf name without the file extension
    fname = os.path.splitext(os.path.basename(path))[0]
    #load pdf file
    pdf = PdfFileReader(path)

    #iterate through the pages and pull them out into their own separate PDF
    for page in range(2):#pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        #Save files to a separate output folder and add a counter to separate them
        
        '''
        Insert text parser here
          - pull out the P&O, WJ and State
          - create the output filename as 'PO_State'
        '''

        text = extract_1.convert_pdf_to_txt(pdf.getPage(page))
        print(text)
        #final will be = 'output/{PO_num}_{State_name}.pdf'
        output_filename = 'output/{}_page_{}.pdf'.format(fname, page)

        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)

    print(f'Created: {output_filename}')

if __name__ == '__main__':
    path = 'test.pdf'
    pdf_splitter(path)