"""
Typography system for MorphUI components
"""

class Typography:
    """Typography definitions for consistent text styling"""
    
    # Font sizes (in sp)
    FONT_SIZE_DISPLAY = 32
    FONT_SIZE_HEADLINE = 24
    FONT_SIZE_TITLE = 20
    FONT_SIZE_BODY = 16
    FONT_SIZE_LABEL = 14
    FONT_SIZE_CAPTION = 12
    
    # Font weights (Kivy doesn't have built-in font weights, but can be used with custom fonts)
    FONT_WEIGHT_LIGHT = "Light"
    FONT_WEIGHT_REGULAR = "Regular"
    FONT_WEIGHT_MEDIUM = "Medium"
    FONT_WEIGHT_BOLD = "Bold"
    
    # Line heights (multipliers of font size)
    LINE_HEIGHT_TIGHT = 1.2
    LINE_HEIGHT_NORMAL = 1.4
    LINE_HEIGHT_LOOSE = 1.6
    
    # Letter spacing (in sp)
    LETTER_SPACING_TIGHT = -0.5
    LETTER_SPACING_NORMAL = 0.0
    LETTER_SPACING_LOOSE = 0.5
    
    @classmethod
    def get_text_style(cls, style_name):
        """Get predefined text style configuration"""
        styles = {
            'display': {
                'font_size': cls.FONT_SIZE_DISPLAY,
                'font_weight': cls.FONT_WEIGHT_BOLD,
                'line_height': cls.LINE_HEIGHT_TIGHT,
            },
            'headline': {
                'font_size': cls.FONT_SIZE_HEADLINE,
                'font_weight': cls.FONT_WEIGHT_MEDIUM,
                'line_height': cls.LINE_HEIGHT_TIGHT,
            },
            'title': {
                'font_size': cls.FONT_SIZE_TITLE,
                'font_weight': cls.FONT_WEIGHT_MEDIUM,
                'line_height': cls.LINE_HEIGHT_NORMAL,
            },
            'body': {
                'font_size': cls.FONT_SIZE_BODY,
                'font_weight': cls.FONT_WEIGHT_REGULAR,
                'line_height': cls.LINE_HEIGHT_NORMAL,
            },
            'label': {
                'font_size': cls.FONT_SIZE_LABEL,
                'font_weight': cls.FONT_WEIGHT_REGULAR,
                'line_height': cls.LINE_HEIGHT_NORMAL,
            },
            'caption': {
                'font_size': cls.FONT_SIZE_CAPTION,
                'font_weight': cls.FONT_WEIGHT_REGULAR,
                'line_height': cls.LINE_HEIGHT_NORMAL,
            }
        }
        return styles.get(style_name, styles['body'])