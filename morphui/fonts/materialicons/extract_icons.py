#!/usr/bin/env python3
"""
Extract Material Design Icons from cheatsheet.html to TOML format.

This script parses the cheatsheet.html file and extracts icon information
into a TOML file where keys are icon names and values are Unicode codepoints.
"""

import re
from pathlib import Path
from typing import Dict, TextIO, Union, Any, Optional


def extract_icons_from_html(html_file_path: Union[str, Path]) -> Dict[str, str]:
    """
    Extract icon information from the Material Design Icons cheatsheet.html file.

    Parameters
    ----------
    html_file_path : Union[str, Path]
        Path to the cheatsheet.html file

    Returns
    -------
    Dict[str, str]
        Dictionary with icon names as keys and Unicode codepoints as values
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"cheatsheet.html not found at {html_file_path}")
    except Exception as e:
        raise Exception(f"Error reading file: {e}")
    
    # Find the JavaScript icons array
    pattern = r'var\s+icons\s*=\s*\[(.*?)\];'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        raise ValueError("Could not find icons array in the HTML file")
    
    icons_array_content = match.group(1)
    
    # Extract icon name and hex code pairs
    icon_pattern = r'\{name:"([^"]+)",data:"[^"]*",hex:"([^"]+)",version:"[^"]*"\}'
    icon_matches = re.findall(icon_pattern, icons_array_content)
    
    if not icon_matches:
        raise ValueError("Could not extract icon data from the array")
    
    # Build the dictionary
    icons_dict = {}
    
    for name, hex_code in icon_matches:
        # Remove 'F' prefix if present and convert to Unicode format
        if hex_code.startswith('F'):
            hex_code = hex_code[1:]
        
        try:
            unicode_int = int(hex_code, 16)
            unicode_str = f"0F{unicode_int:04X}"
            icons_dict[name] = unicode_str
        except ValueError:
            # Skip icons with invalid hex codes
            continue
    
    return icons_dict


def write_toml(data: Dict[str, Dict[str, Any]], file_handle: TextIO) -> None:
    """
    Simple TOML writer for our specific data structure.

    Parameters
    ----------
    data : Dict[str, Dict[str, Any]]
        Dictionary containing metadata and icons
    file_handle : TextIO
        File handle to write to
    """
    # Write metadata section
    file_handle.write("[metadata]\n")
    for key, value in data["metadata"].items():
        if isinstance(value, str):
            file_handle.write(f'{key} = "{value}"\n')
        else:
            file_handle.write(f'{key} = {value}\n')
    
    file_handle.write("\n[icons]\n")
    
    # Write icons section
    for icon_name, unicode_val in sorted(data["icons"].items()):
        # Escape icon names that contain special characters
        if "-" in icon_name or any(c in icon_name for c in "[]{}()"):
            file_handle.write(f'"{icon_name}" = "{unicode_val}"\n')
        else:
            file_handle.write(f'{icon_name} = "{unicode_val}"\n')


def save_icons_toml(icons_dict: Dict[str, str], output_file: Union[str, Path]) -> None:
    """
    Save the icons dictionary to a TOML file.

    Parameters
    ----------
    icons_dict : Dict[str, str]
        Dictionary containing icon data
    output_file : Union[str, Path]
        Output file path
    """
    # Create TOML structure with metadata and icons
    toml_data = {
        "metadata": {
            "description": "Material Design Icons Unicode mapping",
            "total_icons": len(icons_dict),
            "extracted_from": "cheatsheet.html",
            "format": "Unicode codepoints (U+XXXX)"
        },
        "icons": icons_dict
    }
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            write_toml(toml_data, file)
        print(f"Extracted {len(icons_dict)} icons to {output_file}")
    except Exception as e:
        raise Exception(f"Error saving file: {e}")


def get_material_icons_dict(html_file_path: Optional[Union[str, Path]] = None) -> Dict[str, str]:
    """
    Get Material Design Icons as a dictionary.

    Parameters
    ----------
    html_file_path : Union[str, Path], optional
        Path to cheatsheet.html. If None, uses cheatsheet.html in same directory

    Returns
    -------
    Dict[str, str]
        Dictionary with icon names as keys and Unicode codepoints as values
    """
    if html_file_path is None:
        html_file_path = Path(__file__).parent / "cheatsheet.html"
    
    return extract_icons_from_html(html_file_path)


def main() -> None:
    """Extract icons and save to TOML file."""
    # Paths relative to this script
    script_dir = Path(__file__).parent
    html_file = script_dir / "cheatsheet.html"
    output_file = script_dir / "material_icons.toml"
    
    try:
        # Extract icons
        icons_dict = extract_icons_from_html(html_file)
        
        # Save to TOML file
        save_icons_toml(icons_dict, output_file)
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()