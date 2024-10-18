from pdf2image import convert_from_path
import sys
import os
import logging
from PyPDF2 import PdfReader

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class PDF2ImageConverter:
    def __init__(self, input_file, output_directory, dpi=300, chunk_size=5):
        self.input_file = input_file
        self.output_directory = output_directory
        self.dpi = dpi
        self.chunk_size = chunk_size
        self.page_count = None
        self.image_paths = []

    def create_output_directory(self):
        """
        Create the output directory if it doesn't exist.
        """
        os.makedirs(self.output_directory, exist_ok=True)

    def get_page_count(self):
        """
        Get the total number of pages in the PDF.
        """
        try:
            with open(self.input_file, 'rb') as f:
                pdf = PdfReader(f)
                self.page_count = len(pdf.pages)
        except Exception as e:
            logging.error(f"Error getting page count: {e}")
            raise RuntimeError(f"Failed to get page count: {e}")

    def get_images(self):
        """
        Convert the PDF to images and save each page to the output directory.
        Returns a list containing the paths of the saved images.
        """
        leading_zeros = len(str(self.page_count))
        for start_page in range(1, self.page_count + 1, self.chunk_size):
            end_page = min(start_page + self.chunk_size - 1, self.page_count)
            try:
                images = convert_from_path(self.input_file, dpi=self.dpi, first_page=start_page, last_page=end_page)
                for i, image in enumerate(images):
                    page_num = start_page + i
                    output_file = os.path.join(self.output_directory, f"page_{str(page_num).zfill(leading_zeros)}.png")
                    print(f"Saving: {output_file}")
                    self.save_image(image, output_file)
                    self.image_paths.append(output_file)
            except Exception as e:
                logging.error(f"Error converting pages {start_page} to {end_page}: {e}")
                raise RuntimeError(f"Failed to convert pages {start_page} to {end_page}: {e}")
        return self.image_paths

    def save_image(self, image, output_file):
        """
        Save the image to the specified output file.
        """
        try:
            image.save(output_file, "PNG")
        except Exception as e:
            logging.error(f"Error saving image {output_file}: {e}")
            raise RuntimeError(f"Failed to save image {output_file}: {e}")

    def convert_to_images(self):
        """
        Convert a PDF file to images and save them to the specified output directory.
        """
        self.create_output_directory()
        self.get_page_count()
        return self.get_images()

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_directory = "images"

    converter = PDF2ImageConverter(input_file, output_directory)
    image_paths = converter.convert_to_images()
    print("Images saved at:", image_paths)

if __name__ == "__main__":
    main()
