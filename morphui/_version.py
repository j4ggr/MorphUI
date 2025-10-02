import tomllib
from pathlib import Path
from importlib.metadata import version
from importlib.metadata import PackageNotFoundError


__all__ = [
    '__version__',
    '__author__',
    '__license__',]

try:
    pyproject_path = Path(__file__).parent.parent / 'pyproject.toml'
    pyproject = tomllib.load(open(pyproject_path, 'rb'))
except FileNotFoundError:
    pyproject = {
        'project': {
            'name': 'MorphUI',
            'version': '0.0.0',
            'authors': [{'name': 'j4ggr'}],
            'license': {'text': 'MIT'},}}
    
try:
    __version__ = version('morphui')
except PackageNotFoundError:
    # If 'MorphUI' is not installed, load the version from pyproject.toml
    __version__ = pyproject['project']['version'] + '.dev0'

__author__ = pyproject['project']['authors'][0]['name']
__license__ = pyproject['project']['license']['text']
