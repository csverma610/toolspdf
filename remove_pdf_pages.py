import PyPDF2

def remove_pages():
    input_pdf  = input("Enter the path to the input PDF file: ")
    output_pdf = input("Enter the path to save the output PDF file: ")
    pages_to_remove = input("Enter the page numbers to remove (comma-separated, starting from 0): ")
    
    # Convert input string to a list of integers
    pages_to_remove = [int(x) for x in pages_to_remove.split(',')]

    # Open the input PDF file
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        # Loop through all the pages and exclude the ones to be removed
        for page_num in range(len(reader.pages)):
            if page_num not in pages_to_remove:
                page = reader.pages[page_num]
                writer.add_page(page)

        # Write the output PDF
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

    print(f"Pages {pages_to_remove} removed and saved as {output_pdf}")

# Example usage:
remove_pages()

