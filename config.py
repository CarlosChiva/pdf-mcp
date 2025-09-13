import os
from weasyprint import HTML, CSS

class PDFConfig:
    """
    Configuration class for PDF generation
    """
    def __init__(self, margin=1, header_height=50, font_size=12,stylesheet_path="styles.css"):
        self.margin = margin
        self.header_height = header_height
        self.font_size = font_size
            # Create output directory
        self.output_dir = "output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
            print(f"Created directory: {self.output_dir}")
        self.stylesheet_path = stylesheet_path    
    def get_stylesheet(self)-> CSS:
        return CSS(self.stylesheet_path)     
    