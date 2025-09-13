import os
import sys
from markdown import markdown
from weasyprint import HTML, CSS
from pathlib import Path
import logging

# Configurar logging para ver qué está pasando
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class PDFConfig:
    """
    Configuration class for PDF generation
    """
    def __init__(self, margin=1, header_height=50, font_size=12):
        self.margin = margin
        self.header_height = header_height
        self.font_size = font_size

def markdown_to_pdf(markdown_text, output_path, header_image_path=None, config=None):
    """
    Convert markdown text to PDF with proper error handling
    """
    try:
        # Use default config if none provided
        if config is None:
            config = PDFConfig()
        
        logger.info(f"Starting PDF generation to: {output_path}")
        
        # Convert markdown to HTML with table support
        html_content = markdown(markdown_text, extensions=['tables'])
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
        
        # Create complete HTML document
        complete_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: A4;
            margin: {config.margin}in;
            
            @top-center {{
                content: "";
            }}
        }}
        
        body {{
            font-family: Arial, sans-serif;
            font-size: {config.font_size}pt;
            line-height: 1.6;
            color: #333;
        }}
        
        .header-image {{
            position: fixed;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            max-height: {config.header_height}px;
            z-index: 1000;
        }}
        
        .content {{
            margin-top: {config.header_height + 20}px;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            margin-top: 1em;
            margin-bottom: 0.5em;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }}
        
        table th, table td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        
        table th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        
        blockquote {{
            border-left: 4px solid #ddd;
            margin: 1em 0;
            padding-left: 1em;
            color: #666;
        }}
        
        code {{
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: monospace;
        }}
        
        a {{
            color: #3498db;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    {f'<img src="{header_img_uri}" class="header-image" alt="Header">' if header_img_uri else ''}
    <div class="content">
        {html_content}
    </div>
</body>
</html>
"""
        
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

def simple_markdown_to_pdf(markdown_text, output_path):
    """
    Simplified version without header image for testing
    """
    try:
        logger.info(f"Simple PDF generation to: {output_path}")
        
        # Convert markdown to HTML
        html_content = markdown(markdown_text, extensions=['tables'])
        
        # Create simple HTML
        complete_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 12pt;
            margin: 40px;
        }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Generate PDF
        HTML(string=complete_html).write_pdf(output_path)
        
        if os.path.exists(output_path):
            logger.info(f"✓ Simple PDF created: {output_path}")
            return True
        else:
            logger.error(f"✗ Simple PDF not created")
            return False
            
    except Exception as e:
        logger.error(f"Error in simple PDF generation: {str(e)}", exc_info=True)
        return False

def test_weasyprint():
    """
    Test if WeasyPrint is working correctly
    """
    try:
        logger.info("Testing WeasyPrint installation...")
        
        test_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Test</title></head>
        <body><h1>WeasyPrint Test</h1><p>If you see this, WeasyPrint is working!</p></body>
        </html>
        """
        
        test_output = "test_weasyprint.pdf"
        HTML(string=test_html).write_pdf(test_output)
        
        if os.path.exists(test_output):
            logger.info(f"✓ WeasyPrint is working! Test PDF created: {test_output}")
            os.remove(test_output)  # Clean up test file
            return True
        else:
            logger.error("✗ WeasyPrint test failed")
            return False
            
    except Exception as e:
        logger.error(f"WeasyPrint test error: {str(e)}", exc_info=True)
        return False

def main():
    # First, test WeasyPrint
    
    print("\n" + "="*50)
    print("GENERATING PDF")
    print("="*50)
    
    # Example markdown content
    markdown_content = """
        # Sample Document

        This is a **bold** text and this is *italic* text.

        ## Section 1

        - Item 1
        - Item 2
        - Item 3

        ## Table Example

        | Name | Age | City |
        |------|-----|------|
        | John | 25  | New York |
        | Jane | 30  | London |
        | Bob  | 35  | Tokyo |

        ## Another Section

        Some more text here to test the PDF generation.
        """
    
    # Create output directory
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"Created directory: {output_dir}")
    header_path = "header.png"

    # Generate PDF with header
    custom_config = PDFConfig(margin=0.8, header_height=60, font_size=12)
    output_path = os.path.join(output_dir, "sample_with_header.pdf")
    
    if markdown_to_pdf(markdown_content, output_path, header_image_path=header_path, config=custom_config):
        print(f"   ✓ PDF with header created: {output_path}")
    else:
        print("   ✗ PDF with header generation failed")
    
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