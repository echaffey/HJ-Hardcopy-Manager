import os
from PyPDF2 import PdfFileReader, PdfFileWriter


def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path))[0]
    pdf = PdfFileReader(path)

    for page in range(pdf.getNumPages()):
        print(page)
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        output_filename = 'output/{}_page_{}.pdf'.format(fname, page)

        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)

    print(f'Created: {output_filename}')

if __name__ == '__main__':
    path = 'test.pdf'
    pdf_splitter(path)