import fitz  # PyMuPDF
from PIL import Image
import os
import tempfile

class PDFSplitter:
    def __init__(self, pdf_path, dpi=300, threshold=128):
        self.pdf_path = pdf_path
        self.dpi = dpi
        self.threshold = threshold
        self.temp_files = []
        self.split_pdf()

    def split_pdf(self):
        # Extract the base name of the PDF file without the extension
        base_name = os.path.splitext(os.path.basename(self.pdf_path))[0]
        
        # Open the PDF
        pdf_document = fitz.open(self.pdf_path)
        
        # Iterate over each page
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            
            # Increase resolution by specifying dpi
            zoom = self.dpi / 72  # PDF default resolution is 72 dpi
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # Convert the pixmap to a PIL image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Convert the image to grayscale
            img = img.convert("L")
            
            # Convert the grayscale image to bitonal (black and white) with adjusted threshold
            bitonal_img = img.point(lambda x: 0 if x < self.threshold else 255, '1')
            
            # Define the temporary output path
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".tif")
            temp_path = temp_file.name
            temp_file.close()
            
            # Save the image as TIFF with Group 4 compression
            bitonal_img.save(temp_path, format="TIFF", compression="group4", dpi=(self.dpi, self.dpi))
            
            # Keep track of the temporary file path
            self.temp_files.append(temp_path)

        print(f"PDF split into {len(pdf_document)} bitonal TIFF files with Group 4 compression")

    def get_temp_files(self):
        return self.temp_files

    def cleanup(self):
        for temp_file in self.temp_files:
            try:
                os.remove(temp_file)
            except OSError:
                pass
        self.temp_files = []

    def __del__(self):
        self.cleanup()

# Example usage
#pdf_paths = ["~/Downloads/document1.pdf", "~/Downloads/document2.pdf"]
#for pdf_path in pdf_paths:
#    pdf_splitter = PDFSplitter(pdf_path, dpi=300, threshold=150)
#    print(pdf_splitter.get_temp_files())
#    pdf_splitter = None  # This will trigger the destructor and cleanup
