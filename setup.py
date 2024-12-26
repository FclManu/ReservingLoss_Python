import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.1' 
PACKAGE_NAME = 'ReservingLoss' 
AUTHOR = 'Manuel Fernández-Clemente Lozano' 
AUTHOR_EMAIL = 'manuel.fdezclemente@gmail.com' 
URL = 'https://github.com/FclManu'

LICENSE = 'MIT' 
DESCRIPTION = 'Python Library as a Non Life Reserving tool.'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') 
LONG_DESC_TYPE = "text/markdown"


#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
      'pandas',
      'numpy',
      'plotly.express',
      'plotly.graph_objects',
      'plotly.subplots',
      'matplotlib.pyplot',
      'seaborn',
      'IPython.display',
      'openpyxl',
      'datetime',
      'dateutil.relativedelta',
      'sklearn.linear_model',
      'sklearn.metrics',
      'scipy.setup'
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
    include_package_data=True
)