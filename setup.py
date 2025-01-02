import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.2.0'
PACKAGE_NAME = 'ReservingLoss'
AUTHOR = 'Manuel Fernández-Clemente Lozano'
AUTHOR_EMAIL = 'manuel.fdezclemente@gmail.com'
URL = 'https://github.com/FclManu'

LICENSE = 'MIT'
DESCRIPTION = 'Python Library as a Non Life Reserving tool.'
try:
    LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    'pandas>=1.0',
    'numpy>=1.18',
    'plotly>=5.0',
    'matplotlib>=3.0',
    'seaborn>=0.11',
    'IPython>=7.0',
    'openpyxl>=3.0',
    'scikit-learn>=0.24',
    'scipy>=1.5',
    'python-dateutil>=2.8'
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
)