class PDFConfig:
    """
    Configuration class for PDF generation
    """
    def __init__(self, margin=1, header_height=50, font_size=12):
        self.margin = margin
        self.header_height = header_height
        self.font_size = font_size