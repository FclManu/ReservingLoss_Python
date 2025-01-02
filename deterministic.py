###################################################################
##### FUNCTIONS TO PROJECT BY DETERMINISTIC MODELS:
###################################################################

import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


import triangles as tr
import dev_factor as devf
import tail_factor as tailf
#import base
from base import *

###################################################################
# ULTIMATE
###################################################################


def get_ultimate(developed_tr):
    num_rows, num_cols = developed_tr.shape
    ult = []
    for i in range(num_rows):
        ult.append(developed_tr.iloc[i, num_cols - 1])
    
    return ult




###################################################################
# CHAIN-LADDER
###################################################################


def chainladder(triangle, dev_f, tail_f=None):
    projected_tr = triangle.copy()
    
    # Complete triangle with development factors
    for i in range(projected_tr.shape[0]):
        for j in range(1, projected_tr.shape[1]):
            if pd.isna(projected_tr.iloc[i, j]):
                projected_tr.iloc[i, j] = projected_tr.iloc[i, j-1] * dev_f[j-1]

    # Include tail factors if necessary
    if tail_f is not None:
        tail_n = len(tail_f)
        for k in range(tail_n):
            new_col_name = 'Tail ' + str(k + 1)
            projected_tr[new_col_name] = projected_tr.iloc[:, -1] * tail_f[k]  # Use the last value available
    
    # Gives format to numbers:
    projected_tr = projected_tr#.applymap(lambda x: "{:,.0f}".format(x) if not pd.isna(x) else x) 

    return projected_tr


###################################################################
# BORNHUETTER-FERGUSON
###################################################################

def bf(triangle, dev_f, a_priori_ult, tail_f = None):
    
    a, b = triangle.shape

    if len(a_priori_ult) != a:
        return print('a priori ultimate dimension does not match with triangle dim.')
    
    elif tail_f is None:
        projected_tr = triangle.copy()

        Y = devf.inv_df(dev_f)

        for i in range(projected_tr.shape[0]):
            for j in range(1, projected_tr.shape[1]):
                if pd.isna(projected_tr.iloc[i, j]):
                    if j == projected_tr.shape[1]-1:
                        projected_tr.iloc[i, j] = projected_tr.iloc[i, j-1] + (1 - Y[j-1]) * a_priori_ult[i]
                    else:
                        projected_tr.iloc[i, j] = projected_tr.iloc[i, j-1] + (Y[j] - Y[j-1]) * a_priori_ult[i]

        return projected_tr
    

    else:

        projected_tr = triangle.copy()

        for k in range(len(tail_f)):
            new_col_name = 'Tail ' + str(k + 1)
            projected_tr[new_col_name] = np.nan

        dev_f_b = np.concatenate((dev_f, tail_f), axis = 0)

        Y = devf.inv_df(dev_f_b)

        for i in range(projected_tr.shape[0]):
            for j in range(1, projected_tr.shape[1]):
                if pd.isna(projected_tr.iloc[i, j]):
                    if j == projected_tr.shape[1]-1:
                        projected_tr.iloc[i, j] = projected_tr.iloc[i, j-1] + (1 - Y[j-1]) * a_priori_ult[i]
                    else:
                        projected_tr.iloc[i, j] = projected_tr.iloc[i, j-1] + (Y[j] - Y[j-1]) * a_priori_ult[i]

        return projected_tr




###################################################################
# CAPE-COD
###################################################################

def capecod(triangle, dev_f, premiums, tail_f = None):
    
    a, b = triangle.shape

    if len(premiums) != a:
        return print('premiums dimension does not match with triangle dim.')
    
    elif tail_f is None:
        projected_tr = triangle.copy()

        diagonal = tr.last_diag(triangle)
        sum_diag = sum(diagonal)
        
        Y = devf.inv_df(dev_f)

        used_up_prem =[]
        for i in range(1, len(premiums)+1):
            if i == 1:
                used_up_prem.append(premiums[i-1]*1)
            else:
                used_up_prem.append(premiums[i-1]*Y[len(premiums)-i])

        k = sum_diag / sum(used_up_prem)

        for i in range(projected_tr.shape[0]):
            for j in range(1, projected_tr.shape[1]):
                if pd.isna(projected_tr.iloc[i, j]):
                    if j == projected_tr.shape[1]-1:
                        projected_tr.iloc[i, j] = projected_tr.iloc[i, j-1] + (1 - Y[j-1]) * premiums[i] * k
                    else:
                        projected_tr.iloc[i, j] = projected_tr.iloc[i, j-1] + (Y[j] - Y[j-1]) * premiums[i] * k

        return projected_tr
    

    else:

        projected_tr = triangle.copy()

        diagonal = tr.last_diag(triangle)
        sum_diag = sum(diagonal)

        for z in range(len(tail_f)):
            new_col_name = 'Tail ' + str(z + 1)
            projected_tr[new_col_name] = np.nan

        dev_f_b = np.concatenate((dev_f, tail_f), axis = 0)

        Y = devf.inv_df(dev_f_b)

        used_up_prem =[]
        for i in range(1, len(premiums)+1):
            used_up_prem.append(premiums[i-1]*Y[len(premiums)-i])

        k = sum_diag / sum(used_up_prem)

        for i in range(projected_tr.shape[0]):
            for j in range(1, projected_tr.shape[1]):
                if pd.isna(projected_tr.iloc[i, j]):
                    if j == projected_tr.shape[1]-1:
                        projected_tr.iloc[i, j] = projected_tr.iloc[i, j-1] + (1 - Y[j-1]) * premiums[i] * k
                    else:
                        projected_tr.iloc[i, j] = projected_tr.iloc[i, j-1] + (Y[j] - Y[j-1]) * premiums[i] * k

        return projected_tr





#def bf(triangle, dev_f, a_priori_ult):
#    
#    a, b = triangle.shape
#
#    if len(a_priori_ult) != a:
#        return print('a priori ultimate dimension does not match with triangle dim.')
#    
#    else:
#        projected_tr = triangle.copy()
#        Y = devf.inv_df(dev_f)
#
#        for i in range(projected_tr.shape[0]):
#            for j in range(1, projected_tr.shape[1]):
#                if pd.isna(projected_tr.iloc[i, j]):
#                    if j == projected_tr.shape[1]-1:
#                        projected_tr.iloc[i, j] = projected_tr.iloc[i, j-1] + (1 - Y[j-1]) * a_priori_ult[i]
#                    else:
#                        projected_tr.iloc[i, j] = projected_tr.iloc[i, j-1] + (Y[j] - Y[j-1]) * a_priori_ult[i]
#
#        return projected_tr






















#INCLUIR DENTRO DE LA FUNCIÓN ANTERIOR, LA POSIBILIDAD DE INCLUIR LA CASO A CASO PARA PROYECTAR incurr Y SACAR LA RESERVA.
#INCLUIR COMO OUTPUTS EL TRIANGULO PROYECTADO (QUE YA ESTÁ), EL ULTIMATE, LA DIAGONAL, LA RESERVA (Ult.-Diag para pagos, Ult-CaseR para Incurr), y la IBNR (Reserva - CaseR para Pagos y Ult-Diag para incurr)


#'''
#-calculo de chain-ladder
#
#-calculo de bornhuetter-ferguson
#
#-calculo grossing up
#
#-calculo munich-cl
#
#
#
#
#
#'''