from pydantic import Field
from config import PDFConfig
from pdf_builder import MarkdownToPdfConverter
import os , sys
def registre_tools(mcp):
    @mcp.tool(name="markdown_to_pdf", description="""Method to convert markdown content to pdf
    Recive a markdown in string format
    Return a message indicating task status""")
    def markdown_to_pdf(markdown_to_convert:str=Field(title="content to convert to pdf",
                                                      description="Content string in markdown format to convert to pdf")
                                                      )->str:
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
                        return f"""✓ PDF created in: {file_path} with size: {size:,} bytes"""
            else:
                print("  No files generated")
        
        print("\n" + "="*50)
        print(f"Current working directory: {os.getcwd()}")
        print(f"Python version: {sys.version}")
        print("="*50)

        print("="*20+f"{file_path}"+"="*20)
        

    
