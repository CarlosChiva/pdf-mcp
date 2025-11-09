import os
from dotenv import load_dotenv
from weasyprint import HTML, CSS

# Load environment variables from .env file
load_dotenv()

class PDFConfig:
    """
    Configuration class for PDF generation
    """
    def __init__(self, margin: int = None,
                header_height: int = None,
                font_size: int = None,
                stylesheet_path: str = None,
                header_path: str = None,
                output_dir: str = None):
        # Use environment variables with defaults
        self._margin = margin if margin else int(os.getenv('PDF_MARGIN', 1))
        self._header_height = header_height if header_height else int(os.getenv('PDF_HEADER_HEIGHT', 50))
        self._font_size = font_size if font_size else int(os.getenv('PDF_FONT_SIZE', 12))
        self._stylesheet_path = stylesheet_path if stylesheet_path else os.getenv('PDF_STYLESHEET_PATH', "styles/styles.css")
        self._header_path = header_path if header_path else os.getenv('PDF_HEADER_PATH', "images/header.png")
        self.output_dir = output_dir if output_dir else os.getenv('PDF_OUTPUT_DIR', "output")
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
            print(f"Created directory: {self.output_dir}")
    
    @property
    def margin(self) -> int:
        """Get margin value"""
        return self._margin
    
    @margin.setter
    def margin(self, value: int):
        """Set margin value with validation"""
        if value < 0:
            raise ValueError("Margin cannot be negative")
        self._margin = value
    
    @property
    def header_height(self) -> int:
        """Get header height value"""
        return self._header_height
    
    @header_height.setter
    def header_height(self, value: int):
        """Set header height value with validation"""
        if value < 0:
            raise ValueError("Header height cannot be negative")
        self._header_height = value
    
    @property
    def font_size(self) -> int:
        """Get font size value"""
        return self._font_size
    
    @font_size.setter
    def font_size(self, value: int):
        """Set font size value with validation"""
        if value <= 0:
            raise ValueError("Font size must be positive")
        self._font_size = value
    
    @property
    def stylesheet_path(self) -> str:
        """Get stylesheet path"""
        return self._stylesheet_path
    
    @stylesheet_path.setter
    def stylesheet_path(self, value: str):
        """Set stylesheet path"""
        self._stylesheet_path = value
    
    @property
    def header_path(self) -> str:
        """Get header path"""
        return self._header_path
    
    @header_path.setter
    def header_path(self, value: str):
        """Set header path"""
        self._header_path = value
    
    def get_stylesheet(self) -> CSS:
        """Get stylesheet as CSS object"""
        return CSS(self.stylesheet_path)
    
    def validate_config(self):
        """Validate configuration values"""
        if self.margin < 0:
            raise ValueError("Margin cannot be negative")
        if self.header_height < 0:
            raise ValueError("Header height cannot be negative")
        if self.font_size <= 0:
            raise ValueError("Font size must be positive")
