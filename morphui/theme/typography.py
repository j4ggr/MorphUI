"""
Typography system for MorphUI themes
"""

class Typography:
    """Typography styles for themes"""
    
    @staticmethod
    def get_text_style(style_name):
        """Get text style configuration by name"""
        styles = {
            "display": {
                "font_size": 57,
                "font_weight": "normal",
                "line_height": 64,
                "letter_spacing": -0.25
            },
            "headline": {
                "font_size": 32,
                "font_weight": "normal", 
                "line_height": 40,
                "letter_spacing": 0
            },
            "title": {
                "font_size": 22,
                "font_weight": "medium",
                "line_height": 28,
                "letter_spacing": 0
            },
            "body": {
                "font_size": 16,
                "font_weight": "normal",
                "line_height": 24,
                "letter_spacing": 0.5
            },
            "label": {
                "font_size": 14,
                "font_weight": "medium",
                "line_height": 20,
                "letter_spacing": 0.1
            },
            "caption": {
                "font_size": 12,
                "font_weight": "normal",
                "line_height": 16,
                "letter_spacing": 0.4
            }
        }
        
        return styles.get(style_name, styles["body"])
    
    @staticmethod
    def get_font_size(style_name):
        """Get font size for a text style"""
        return Typography.get_text_style(style_name)["font_size"]