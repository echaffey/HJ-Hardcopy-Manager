import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import extract
import emailer
#https://stackoverflow.com/questions/26494211/extracting-text-from-a-pdf-file-using-pdfminer-in-python


def pdf_splitter(path):
    """
    Method to split a multi-page PDF into single page files.
    This breaks up the Oracle file into individual hard copies.

    path: filepath of the Oracle multi-page PDF
    """
    #get pdf name without the file extension
    fname = os.path.splitext(os.path.basename(path))[0]
    #load pdf file
    pdf = PdfFileReader(path)

    #iterate through the pages and pull them out into their own separate PDF
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        #just temporary output name to navigate only being able to pull text with a filename
        output_filename = f'output/{fname}_page_{page}.pdf'

        #Save files to a separate output folder and add a counter to separate them
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)

        #Raw text read from PDFs, split into a list for easier retrieval
        text = extract.convert_pdf_to_txt(output_filename)
        text_list = text.split('\n')

        #Remove excess empty string values
        while ('' in text_list):
            text_list.remove('')

        #Find the 'P&O' numbers
        if (PO_pos := text_list.index('P&O:')) >= 0:
            PO_num = text_list[PO_pos + 1].strip()
            
        #Error checking to make sure we're getting the right value.
        #This needs to be updated later
        if (state_pos := text_list.index('STATE:')) >= 0:
            if len(text_list[state_pos + 2].strip()) == 2 and text_list[state_pos + 2].isalpha():
                state = text_list[state_pos + 2].strip()
            elif len(text_list[state_pos + 3].strip()) == 2 and text_list[state_pos + 3].isalpha():
                state = text_list[state_pos + 3].strip()
            else:
                state = ''

        #rename the file to inclue the PO, State and page counter (to remove duplication issues)
        os.rename(output_filename, f'output/{PO_num}_{state}_{page}.pdf' )


if __name__ == '__main__':
    path = 'test.pdf'
    pdf_splitter(path)