###################################################################
##### FUNCTIONS TO UPLOAD, GENERATE AND OBTAIN INFO FROM TRIANGLES:
###################################################################


import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta





###################################################################
# To generate a triangle from a data base in .csv 

def triangle_from_csv(file: str, base_period: str, dev_period: str, aggr_values: str, lob_column: str = None, lob_name: str = None):
    
    """
    Function to upload triangles from a data base in .csv format. 
    Database must include a column for origin period (ie. Acc.Years), Development period (Lags), and the values to upload (ie. Incurrec Losses).

    Parameters
    ----------
    file: (str)
        Name of file to read

    base_period: (str)
        Name of the column that refers to the origin period.  

    dev_period: (str)
        Name of the column that refers to the development period.  

    aggr_values: (str)  
        Name of the column that refers to the values to aggregate (payments, incurred costs, reserves...).  

    lob_column: (str)
        Name of the column that refers to LoB in case the data need to be filtered. None as default.

     lob_name: (str)
        Name of the LoB we want to filter. None as default.         
    """

    data = pd.read_csv(file)

    if lob_column is None and lob_name is None:
        triangle = data.pivot_table(index=base_period, columns=dev_period, values=aggr_values, aggfunc='sum')
    else:
        data_lob = data[data[lob_column] == lob_name]
        triangle = data_lob.pivot_table(index=base_period, columns=dev_period, values=aggr_values, aggfunc='sum')
    
    return triangle

###################################################################



###################################################################
# Functions to improve the upload of triangle:

# Función para convertir números de columna a letras
def num_to_col(n):
    col = ''
    while n > 0:
        n, rem = divmod(n-1, 26)
        col = chr(65 + rem) + col
    return col

###################################################################



###################################################################
# Functions to create series:

def generate_date_series(start_year, month, periodicity, n):

    # Validar periodicidad
    valid_periods = {
        "annual": 12,
        "biannual": 6,
        "three_times_year": 4,
        "quarterly": 3,
        "bimonthly": 2,
        "monthly": 1,
    }

    if periodicity not in valid_periods:
        raise ValueError(f"Periodicidad no válida. Debe ser una de {list(valid_periods.keys())}")

    # Configurar intervalo en meses
    interval = valid_periods[periodicity]

    # Crear la lista de fechas
    start_date = datetime(start_year, month, 1)
    date_series = []

    # Generar las fechas hasta alcanzar la dimensión n
    current_date = start_date
    while len(date_series) < n:
        date_series.append(current_date.strftime("%m/%Y"))
        current_date += relativedelta(months=interval)

    return date_series

###################################################################



###################################################################
# To upload a triangle from .xlsx file (the triangle is created in excel)

# The initial point of reference is the starting of the triangle. The AY and DY are needed in the excel file.

def upload_triangle_excel(file: str, sheet: str, init_col: int, init_row: int, dim: int, start_year: int, month: int = 12, periodicity: str = 'annual'):
    col_inicial_letra = num_to_col(init_col)
    col_final_letra = num_to_col(init_col + dim-1)

    AccidentYear = generate_date_series(start_year=start_year, month=month, periodicity=periodicity, n=dim)
    

    df = pd.read_excel(
        file, 
        sheet_name=sheet, 
        usecols=f'{col_inicial_letra}:{col_final_letra}', 
        skiprows= init_row - 1, 
        nrows = dim,
        header=None
    )
    # Añadir la columna de AccidentYear
    df.insert(0, 'AccidentYear', AccidentYear)
    df.set_index('AccidentYear', inplace=True)
    
    df.columns = list(range(1, df.shape[1]+1))

    return df

###################################################################




####################################################################
## To upload a triangle from .xlsx file (the triangle is created in excel)
#
## The initial point of reference is the starting of the triangle. The AY and DY are needed in the excel file.
#
#def upload_triangle_xlsx(file: str, sheet: str, init_col: int, init_row: int, dim: int):
#    col_inicial_letra = num_to_col(init_col - 1)
#    col_final_letra = num_to_col(init_col + dim-1)
#    
#    df = pd.read_excel(
#        file, 
#        sheet_name=sheet, 
#        usecols=f'{col_inicial_letra}:{col_final_letra}', 
#        skiprows=init_row - 2, 
#        nrows = dim 
#    )
#
#    df.columns = ['DevelopmentLag'] + list(range(1, df.shape[1]))
#    df.set_index('DevelopmentLag', inplace=True)
#    df.index.name = 'AccidentYear'
#
#    return df
#
####################################################################



###################################################################
# Graph the evolution of values in a triangle by AY and DY

def graph_values(triangle):

    # Graph by Accident Year
    fig1 = px.line(triangle.T, title='Values by Accident Year')
    fig1.update_xaxes(title='Dev Period')
    fig1.update_yaxes(title='Values')

    # Graph by Development Year
    fig2 = px.line(triangle, title='Values by Development Period')
    fig2.update_xaxes(title='Accident Year')
    fig2.update_yaxes(title='Values')

    #Mostramos los gráficos:
    fig1.show()
    fig2.show()

###################################################################



###################################################################
# Convert a cummulative triangle to a incremental triangle:

def incr_to_cum(incr_triangle):
    rows, cols = incr_triangle.shape
    cum_triangle = incr_triangle.copy()  
    
    for i in range(rows):
        for j in range(1, cols):
            cum_triangle.iloc[i, j] += incr_triangle.iloc[i, j-1]
    
    return cum_triangle

###################################################################



###################################################################
# Convert an incremental triangle to a cummulative one:

def cum_to_incr(cum_triangle):
    rows, cols = cum_triangle.shape
    incr_triangle = cum_triangle.copy()  
    
    for i in range(rows):
        for j in range(1, cols):
            incr_triangle.iloc[i, j] -= cum_triangle.iloc[i, j-1]
    
    return incr_triangle

###################################################################



###################################################################
# Link Factors:

def linkfactor_triangle(triangulo):
    num_rows, num_cols = triangulo.shape
    triangle_factors = np.zeros((num_rows, num_cols))
    
    for i in range(num_rows):
        for j in range(num_cols):
            period = j + 1
            if period < num_cols: 
                factor = triangulo.iloc[i, period] / triangulo.iloc[i, period - 1] 
            else:
                factor = 1
            triangle_factors[i, j] = factor

    
    Fij_factors = pd.DataFrame(triangle_factors[:-1,:-1], index=triangulo.index[:-1], columns=triangulo.columns[:-1])

    return Fij_factors


###################################################################



###################################################################
# Function to represent a triangle in heatmap format:

def heatmap_format(triangle, fmt=".4f"):
    plt.figure(figsize=(15, 4))
    sns.heatmap(triangle, cmap='Reds', annot=True, fmt=fmt)
    #plt.title('Link Factors Fij')
    plt.xlabel('Dev Periods')
    plt.ylabel('Acc Years')
    plt.show()

###################################################################



###################################################################
# Function to obtain the last diag from a (projected) triangle:

def last_diag(tr):
    num_rows, num_cols = tr.shape
    diag = []
    for i in range(num_rows):
        diag.append(tr.iloc[i, num_rows - i - 1])
    
    return diag

###################################################################



###################################################################
# Function to obtain a theoric triangle (first period developed with development factors):

def theoric_tr(tr, dev_f):
    theoric_tr = tr.copy()

    # Completar el triángulo con los factores de desarrollo
    for i in range(theoric_tr.shape[0]):
        for j in range(1, theoric_tr.shape[1]):
            if j != 0 and i + j < theoric_tr.shape[1]:
                theoric_tr.iloc[i, j] = tr.iloc[i, j-1] * dev_f[j-1]

    return theoric_tr

###################################################################



###################################################################
# Function to obtain a standar error triangle:

def residual_tr(tr, dev_f):

    theoric_tr = tr.copy()


###################################################################























