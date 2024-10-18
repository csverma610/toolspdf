import PyPDF2
import sys

def pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Example usage
pdf_path = sys.argv[1]
extracted_text = pdf_to_text(pdf_path)
print(extracted_text)

