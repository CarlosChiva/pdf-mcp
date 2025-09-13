import os
import sys
from markdown import markdown
from weasyprint import HTML, CSS
from pathlib import Path
import logging
from config import PDFConfig

# Configurar logging para ver qué está pasando
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def markdown_to_pdf(markdown_text, output_path, header_image_path=None, config=None):
    """
    Convert markdown text to PDF with proper styling and error handling
    """
    try:
        # Use default config if none provided
        if config is None:
            config = PDFConfig()
        
        logger.info(f"Starting PDF generation to: {output_path}")
        
        # Convert markdown to HTML with table support and other extensions
        html_content = markdown(markdown_text, extensions=['tables', 'fenced_code', 'codehilite', 'toc'])
        logger.debug("Markdown converted to HTML successfully")
        
        # Handle header image
        header_img_uri = ""
        if header_image_path:
            if os.path.exists(header_image_path):
                abs_path = Path(header_image_path).absolute()
                header_img_uri = abs_path.as_uri()
                logger.info(f"Header image found at: {abs_path}")
                logger.debug(f"Header image URI: {header_img_uri}")
            else:
                logger.warning(f"Header image not found at: {header_image_path}")
        
        # Read CSS content directly
        css_content = ""
        css_file_path = "styles.css"
        if os.path.exists(css_file_path):
            with open(css_file_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
            logger.debug("CSS file read successfully")
        else:
            logger.warning(f"CSS file not found at: {css_file_path}")
        
        # Create complete HTML document with proper structure
        complete_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Markdown Document</title>
    <style>
        {css_content}
    </style>
</head>
<body>
    {f'<img src="{header_img_uri}" class="header-image" alt="Header">' if header_img_uri else ''}
    <div class="content">
        {html_content}
    </div>
</body>
</html>"""
        
        logger.debug("HTML document created")
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            logger.info(f"Created output directory: {output_dir}")
        
        # Generate PDF
        logger.info("Generating PDF...")
        doc = HTML(string=complete_html)
        doc.write_pdf(output_path)
        
        # Verify PDF was created
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            logger.info(f"✓ PDF generated successfully: {output_path} (Size: {file_size} bytes)")
            return True
        else:
            logger.error(f"✗ PDF file was not created at: {output_path}")
            return False
            
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}", exc_info=True)
        return False

def main():
    # First, test WeasyPrint
    
    print("\n" + "="*50)
    print("GENERATING PDF")
    print("="*50)
    
    # Example markdown content with various elements
    markdown_content = """
# Sample Document

This is a **bold** text and this is *italic* text.

## Section 1

- Item 1
- Item 2
- Item 3

## Section 2

Here's some code:

```python
def hello():
    print("Hello, World!")
```

## Table Example

| Name | Age | City |
|------|-----|------|
| John | 25  | New York |
| Jane | 30  | London |

> This is a blockquote example.

[Link to Google](https://www.google.com)

---

Some more text with **bold**, *italic*, and `code` formatting.
"""
    
    # Create output directory
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"Created directory: {output_dir}")
    
    header_path = "header.png"

    # Generate PDF with header
    custom_config = PDFConfig(margin=0.8, header_height=60, font_size=12)
    output_path = os.path.join(output_dir, "sample_document.pdf")
    
    if markdown_to_pdf(markdown_content, output_path, header_image_path=header_path, config=custom_config):
        print(f"   ✓ PDF with header created: {output_path}")
    else:
        print("   ✗ PDF generation failed")
    
    # List all generated files
    print("\n" + "="*50)
    print("GENERATED FILES:")
    print("="*50)
    
    if os.path.exists(output_dir):
        files = os.listdir(output_dir)
        if files:
            for file in files:
                file_path = os.path.join(output_dir, file)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)
                    print(f"  - {file} ({size:,} bytes)")
        else:
            print("  No files generated")
    
    print("\n" + "="*50)
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python version: {sys.version}")
    print("="*50)

if __name__ == "__main__":
    main()