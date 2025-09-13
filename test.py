import os
import sys
import logging
from config import PDFConfig
from pdf_builder import MarkdownToPdfConverter
# Configurar logging para ver qué está pasando
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main(markdown_to_convert):
    # First, test WeasyPrint
    
    print("\n" + "="*50)
    print("GENERATING PDF")
    print("="*50)
    
    # Example markdown content with various elements
   

    # Generate PDF with header
    custom_config = PDFConfig(margin=0.8, header_height=60, font_size=12)
    converter = MarkdownToPdfConverter(custom_config)
    output_path = os.path.join(custom_config.output_dir, "sample_document.pdf")
    
    if converter.convert(markdown_to_convert, output_path):
        print(f"   ✓ PDF with header created: {output_path}")
    else:
        print("   ✗ PDF generation failed")
    
    # List all generated files
    print("\n" + "="*50)
    print("GENERATED FILES:")
    print("="*50)
    
    if os.path.exists(custom_config.output_dir):
        files = os.listdir(custom_config.output_dir)
        if files:
            for file in files:
                file_path = os.path.join(custom_config.output_dir, file)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)
                    print(f"  - {file} ({size:,} bytes)")
        else:
            print("  No files generated")
    
    print("\n" + "="*50)
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python version: {sys.version}")
    print("="*50)

    print("="*20+f"{file_path}"+"="*20)
if __name__ == "__main__":
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

Some more text with **bold**, *italic*, and `code` formatting.# Sample Document

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

Some more text with **bold**, *italic*, and `code` formatting.# Sample Document

This is a **bold** text and this is *italic* text.

"""
    main(markdown_content)