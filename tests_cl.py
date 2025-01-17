###################################################################
##### FUNCTIONS TO VISUALIZE TESTS FOR CHAIN-LADDER ASSUMPTIONS:
###################################################################

import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from scipy.stats import linregress


import triangles as tr
import dev_factor as devf
import tail_factor as tailf
#import base
from base import *
import deterministic as dt

###################################################################
# LINEARITY TEST
###################################################################
  
import plotly.graph_objects as go
import pandas as pd

def linear_test(triangle, dev_f):

    theoric_tr = tr.theoric_tr(triangle, dev_f)


    n = triangle.shape[1]  # Número de columnas (años de desarrollo)

    # Crear gráficos para cada año de desarrollo
    for i in range(n - 2):  # Evitar el último año (sin datos T+1)
        fig = go.Figure()

        # Datos para el año i
        acc_period = triangle.iloc[:-(i+1), 0] #Año acc.
        x_data = triangle.iloc[:-(i+1), i]  # Todas las filas menos la última, columna i
        y_theoric = theoric_tr.iloc[:-(i+1), i+1]  # Todas las filas menos la última, columna i+1
        y_empiric = triangle.iloc[:-(i+1), i+1]  # Todas las filas menos la última, columna i+1

        # Realizar regresión lineal para los valores empíricos
        slope_e, intercept_e, r_value_e, p_value_e, std_err_e = linregress(x_data, y_empiric)
        r_squared_e = r_value_e**2  # R cuadrado para los valores empíricos

        # Agregar la línea de valores teóricos
        fig.add_trace(go.Scatter(
            x=x_data,
            y=y_theoric,
            mode='lines+markers',
            name='Valor Teórico',
            line=dict(color='blue'),
            marker=dict(symbol='circle', size=4)
        ))

        # Agregar los puntos de valores empíricos
        fig.add_trace(go.Scatter(
            x=x_data,
            y=y_empiric,
            mode='markers',
            name='Valor Empírico',
            marker=dict(color='orange', symbol='circle', size=6)
        ))

        # Personalizar el diseño
        fig.update_layout(
            title=f'Development Period {i + 1} - R²: {r_squared_e:.4f}',
            xaxis_title='Period t',
            yaxis_title='Period t+1',
            legend=dict(x=1, y=1, bgcolor='rgba(255,255,255,0)'),
            font=dict(size=14)
        )

        # Mostrar el gráfico
        fig.show()



###################################################################
# RESIDUAL TEST
###################################################################

def residual_test(triangle, dev_f):

    theoric_tr = tr.theoric_tr(triangle, dev_f)

    






















###################################################################
# CALENDAR TEST
###################################################################
























###################################################################
# CORRELATION TEST
###################################################################


























