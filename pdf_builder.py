import os
import logging
from config import PDFConfig
# Configurar logging para ver qué está pasando

from markdown import markdown
from weasyprint import HTML, CSS
from pathlib import Path


class MarkdownToPdfConverter:
    """Converts markdown text to PDF with proper styling and error handling"""
    
    def __init__(self, config=None):
        self.config = config or PDFConfig()
        # Validate configuration on initialization
        self.config.validate_config()
        
    
    def _create_html_document(self, markdown_text, header_image_uri):
        """Create complete HTML document with proper structure"""
        # Convert markdown to HTML with table support and other extensions
        html_content = markdown(markdown_text, extensions=['tables', 'fenced_code', 'codehilite', 'toc'])
        logging.debug("Markdown converted to HTML successfully")
        
        
        # Create complete HTML document with proper structure
        complete_html = f"""<!DOCTYPE html>
                                <html>
                                <head>
                                    <meta charset="UTF-8">
                                    <title>Markdown Document</title>
                                
                                </head>
                                <body>
                                    <div class="content">
                                        {html_content}
                                    </div>
                                </body>
                                </html>"""
        
        logging.debug("HTML document created")
        return complete_html
    
    def _ensure_output_directory(self, output_path):
        """Ensure output directory exists"""
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            logging.info(f"Created output directory: {output_dir}")
    
    def convert(self, markdown_text, output_path):
        """
        Convert markdown text to PDF with proper styling and error handling
        """
        try:
            logging.info(f"Starting PDF generation to: {output_path}")
            
            # Handle header image
            header_img_uri = ""
            if self.config.header_path:
                if os.path.exists(self.config.header_path):
                    abs_path = Path(self.config.header_path).absolute()
                    header_img_uri = abs_path.as_uri()
                    logging.info(f"Header image found at: {abs_path}")
                    logging.debug(f"Header image URI: {header_img_uri}")
                else:
                    logging.warning(f"Header image not found at: {self.config.header_path}")
            
            # Create complete HTML document
            complete_html = self._create_html_document(markdown_text, header_img_uri)
            
            # Ensure output directory exists
            self._ensure_output_directory(output_path)
            
            # Generate PDF
            logging.info("Generating PDF...")
            doc = HTML(string=complete_html)
            doc.write_pdf(target=output_path,stylesheets=[self.config.get_stylesheet()])
            
            # Verify PDF was created
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                logging.info(f"✓ PDF generated successfully: {output_path} (Size: {file_size} bytes)")
                return True
            else:
                logging.error(f"✗ PDF file was not created at: {output_path}")
                return False
                
        except Exception as e:
            logging.error(f"Error generating PDF: {str(e)}", exc_info=True)
            return False
