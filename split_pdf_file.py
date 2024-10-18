from PyPDF2 import PdfFileReader, PdfFileWriter
from pathlib import Path
import argparse

def split_pdf(input_file, pages_per_split):
    input_path = Path(input_file)
    
    # Check if input file exists
    if not input_path.is_file():
        raise FileNotFoundError(f"The input file {input_file} does not exist.")

    # Open the PDF file
    with open(input_path, "rb") as infile:
        input_pdf = PdfFileReader(infile)
        total_pages = input_pdf.getNumPages()
        
        # Check if the PDF has pages
        if total_pages == 0:
            raise ValueError("The input PDF file is empty.")
        
        split_pdfs = []
        
        for start in range(0, total_pages, pages_per_split):
            end = min(start + pages_per_split, total_pages)
            
            output_pdf = PdfFileWriter()
            
            for page in range(start, end):
                try:
                    output_pdf.addPage(input_pdf.getPage(page))
                except Exception as e:
                    print(f"Warning: Could not add page {page + 1} due to an error: {e}")
            
            split_pdfs.append(output_pdf)

    return split_pdfs

def save_split_pdfs(split_pdfs, output_directory):
    output_dir = Path(output_directory)
    
    # Create output directory if it doesn't exist
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise OSError(f"Failed to create output directory {output_directory}: {e}")
    
    for index, output_pdf in enumerate(split_pdfs, start=1):
        output_file = output_dir / f"split_{index}.pdf"
        
        # Write the split PDF
        with open(output_file, "wb") as outfile:
            output_pdf.write(outfile)

        print(f"Created: {output_file}")

def main_split_pdf():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Split a PDF into multiple smaller PDFs.")
    parser.add_argument('--input_file', '-i', type=str, required=True, help="Path to the input PDF file.")
    parser.add_argument('--output_directory', '-d', type=str, nargs='?', default='splits', help="Directory to store the split PDF files (default: 'splits').")
    parser.add_argument('--pages_per_split', '-p', type=int, nargs='?', default=10, help="Number of pages per split (default: 10).")
    
    args = parser.parse_args()
    
    # Call the split function with arguments
    split_pdfs = split_pdf(args.input_file, args.pages_per_split)
    save_split_pdfs(split_pdfs, args.output_directory)

if __name__ == "__main__":
    main_split_pdf()
