"""
Helper utilities for MorphUI components
"""
from typing import Any
from typing import Dict
from kivy.core.text import Label as CoreLabel

__all__ = [
    'clean_default_config',
    'calculate_text_size',]

def clean_default_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Clean default config by removing conflicting entries
    
    This function checks for conflicting entries in the provided
    configuration dictionary. Specifically, if both 
    'theme_color_bindings' and 'theme_style' are present, 
    'theme_style' takes precedence.
    
    If 'theme_style' is not present, it removes any keys from
    'theme_color_bindings' that are also explicitly set in the config.
    """
    config = config.copy()
    if 'theme_color_bindings' in config:
        if 'theme_style' in config:
            config.pop('theme_color_bindings')
        else:
            bound_color = config['theme_color_bindings'].copy()
            config['theme_color_bindings'] = {
                k: v for k, v in bound_color.items() if k not in config}
    return config


def calculate_text_size(text, font_size=16, font_name=None):
    """Calculate the size needed to render text"""
    
    label = CoreLabel(text=text, font_size=font_size)
    if font_name:
        label.options['font_name'] = font_name
    
    label.refresh()
    return label.content_size

