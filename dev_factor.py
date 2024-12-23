###################################################################
##### FUNCTIONS TO OBTAIN DEVELOPMENT FACTORS:
###################################################################



import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


import triangles as tr


###################################################################
# To obtain volume weight factors, wo excluding any factor:

def quick_df(triangle):
    #Calculo de factores de desarrollo por volume-weight sin ignorar factores.
    dev_f = []
    for col in triangle.columns[:-1]:
        dev_f.append(triangle[(col+1)].sum() / triangle[col][:-int(col)].sum())
    dev_f = np.array(dev_f)
    
    return(dev_f)

###################################################################



###################################################################
# Graph development factors:

def graph_df(df):
    fig1 = px.line(df, title='Development Factors')
    fig1.update_xaxes(title='Development periods')
    fig1.update_yaxes(title='DF')
    fig1.show()

###################################################################




###################################################################
# Weight triangle in order to apply to link factors:

def weight_lf(linkfactors_tr, cal_y_ignore=0, acc_y_ignore=0, f_ignore=None):
    weight_tr = linkfactors_tr.notnull().astype(int)

    # Ignorar por año calendario:
    for i in range(cal_y_ignore):
        for j in range(cal_y_ignore):
            if i + j < cal_y_ignore:
                weight_tr.iloc[:j+1, :i+1] = 0

    # Ignorar por año accidente:
    weight_tr.iloc[:acc_y_ignore, :] = 0

    # Modificar posiciones específicas si se proporciona la lista
    if f_ignore:
        for pos in f_ignore:
            row, column = pos
            weight_tr.loc[row, column] = 0

    return weight_tr






###################################################################
# Next definitions introduce formulas to obtain DF according different methods:
###################################################################



###################################################################
# Arithmetric mean:
###################################################################

def avg_df(triangulo, cal_y_ignore = 0, acc_y_ignore = 0, f_ignore = None):

    #Generamos array de factores
    dev_f = []
    
    #Generamos triángulo de factores:
    LF_tr = tr.linkfactor_triangle(triangulo).fillna(0)
    
    #Generamos los pesos:
    weight_tr = weight_lf(LF_tr, cal_y_ignore, acc_y_ignore, f_ignore).fillna(0)
    
    for col in LF_tr.columns[:]:
            if np.array(np.sum(weight_tr.iloc[:len(weight_tr)-(col-1), col-1])) == 0:
                dev_f.append(1)
            else:  
                dev_f.append(np.dot(np.array(LF_tr.iloc[:len(LF_tr)-(col-1), col-1]), np.array(weight_tr.iloc[:len(LF_tr)-(col-1), col-1])) / np.array(weight_tr.iloc[:len(LF_tr)-(col-1), col-1].sum()))
    
        #return(LF_tr, weight_tr)
    return(dev_f)

###################################################################



###################################################################
# Volume-weighted average: (Most frequent option)
###################################################################

def volweight_df(triangulo, cal_y_ignore = 0, acc_y_ignore = 0, f_ignore = None):

    #Generamos array de factores
    dev_f = []
    
    #Generamos triángulo de factores:
    LF_tr = tr.linkfactor_triangle(triangulo).fillna(0)
    
    #Generamos los pesos:
    weight_tr = weight_lf(LF_tr, cal_y_ignore, acc_y_ignore, f_ignore).fillna(0)
    
    for col in LF_tr.columns[:]:
            if np.array(np.sum(weight_tr.iloc[:len(weight_tr)-(col-1), col-1])) == 0:
                dev_f.append(1)
            else:  
                dev_f.append(np.sum(np.array(LF_tr.iloc[:len(LF_tr)-(col-1), col-1]) * np.array(triangulo.iloc[:len(LF_tr)-(col-1), col-1]) * np.array(weight_tr.iloc[:len(LF_tr)-(col-1), col-1])) / np.sum(np.array(triangulo.iloc[:len(LF_tr)-(col-1), col-1]) * np.array(weight_tr.iloc[:len(LF_tr)-(col-1), col-1])))

    
    return(dev_f)

###################################################################



###################################################################
# Time-weighted average:
###################################################################

def timeweight_df(triangulo, cal_y_ignore = 0, acc_y_ignore = 0, f_ignore = None):

    #Generamos array de factores
    dev_f = []
    
    #Generamos triángulo de factores:
    LF_tr = tr.linkfactor_triangle(triangulo).fillna(0)
    
    #Generamos los pesos:
    weight_tr = weight_lf(LF_tr, cal_y_ignore, acc_y_ignore, f_ignore).fillna(0)

    for col in LF_tr.columns[:]:
            if np.array(np.sum(weight_tr.iloc[:len(weight_tr)-(col-1), col-1])) == 0:
                dev_f.append(1)
            else:            
                time_weight = np.arange(1, len(LF_tr)+2-col)
                dev_f.append(np.sum(np.array(LF_tr.iloc[:len(LF_tr)-(col-1), col-1]) * np.array(time_weight) * np.array(weight_tr.iloc[:len(LF_tr)-(col-1), col-1])) / np.sum(np.array(time_weight) * np.array(weight_tr.iloc[:len(LF_tr)-(col-1), col-1])))
        
    return(dev_f)
###################################################################



###################################################################
# Median of Fj
###################################################################

def median_df(triangulo, cal_y_ignore = 0, acc_y_ignore = 0, f_ignore = None):

    #Generamos array de factores
    dev_f = []
    
    #Generamos triángulo de factores:
    LF_tr = tr.linkfactor_triangle(triangulo).fillna(0)
    
    #Generamos los pesos:
    weight_tr = weight_lf(LF_tr, cal_y_ignore, acc_y_ignore, f_ignore).fillna(0)

    for col in LF_tr.columns[:]:
            if np.array(np.sum(weight_tr.iloc[:len(weight_tr)-(col-1), col-1])) == 0:
                dev_f.append(1)
            else:
                # Verificar si hay algún cero en weight_tr en la misma posición
                if 0 in weight_tr.iloc[:len(weight_tr)-(col-1), col-1].values:
                    # Si hay un cero, ignorar los valores correspondientes en LF_tr
                    dev_f.append(np.median(LF_tr.iloc[:len(weight_tr)-(col-1), col-1][weight_tr.iloc[:len(weight_tr)-(col-1), col-1] != 0]))
                else:
                    dev_f.append(np.median(LF_tr.iloc[:len(weight_tr)-(col-1), col-1]))

    return(dev_f)
###################################################################



###################################################################
# Geometric average of Fj:
###################################################################

def geom_df(triangulo, cal_y_ignore = 0, acc_y_ignore = 0, f_ignore = None):

    #Generamos array de factores
    dev_f = []
    
    #Generamos triángulo de factores:
    LF_tr = tr.linkfactor_triangle(triangulo).fillna(0)
    
    #Generamos los pesos:
    weight_tr = weight_lf(LF_tr, cal_y_ignore, acc_y_ignore, f_ignore).fillna(0)

    for col in LF_tr.columns[:]:
            if np.sum(weight_tr.iloc[:len(weight_tr)-(col-1), col-1]) == 0:
                dev_f.append(1)
            else:
                # Verificar si hay algún cero en weight_tr en la misma posición
                if 0 in weight_tr.iloc[:len(weight_tr)-(col-1), col-1].values:
                    # Si hay un cero, ignorar los valores correspondientes en LF_tr
                    eval = []
                    eval = LF_tr.iloc[:len(weight_tr)-(col-1), col-1][weight_tr.iloc[:len(weight_tr)-(col-1), col-1] != 0]
                    dev_f.append(np.prod(eval[:]) ** (1 / len(eval[:])))
                else:
                    eval = []
                    eval = LF_tr.iloc[:len(weight_tr)-(col-1), col-1]
                    dev_f.append(np.prod(eval[:]) ** (1 / len(eval[:])))

    return(dev_f)
###################################################################



###################################################################
# Arithmetric mean excluding max and min Fj:
###################################################################

def medialavg_df(triangulo, cal_y_ignore = 0, acc_y_ignore = 0, f_ignore = None):

    #Generamos array de factores
    dev_f = []
    
    #Generamos triángulo de factores:
    LF_tr = tr.linkfactor_triangle(triangulo).fillna(0)
    
    #Generamos los pesos:
    weight_tr = weight_lf(LF_tr, cal_y_ignore, acc_y_ignore, f_ignore).fillna(0)

    for col in LF_tr.columns[:]:
            if np.sum(weight_tr.iloc[:len(weight_tr)-(col-1), col-1]) == 0:
                dev_f.append(1)
            else:
                # Verificar si hay algún cero en weight_tr en la misma posición
                if 0 in weight_tr.iloc[:len(weight_tr)-(col-1), col-1].values:
                    # Si hay un cero, ignorar los valores correspondientes en LF_tr
                    eval = []
                    eval = LF_tr.iloc[:len(weight_tr)-(col-1), col-1][weight_tr.iloc[:len(weight_tr)-(col-1), col-1] != 0]
                    if len(eval) <=2:        
                        dev_f.append(np.mean(eval[:]))
                    else:
                        dev_f.append(np.mean(eval[(eval != np.max(eval)) & (eval != np.min(eval))]))
                else:
                    eval = []
                    eval = LF_tr.iloc[:len(weight_tr)-(col-1), col-1]
                    if len(eval) <=2:        
                        dev_f.append(np.mean(eval[:]))
                    else:
                        dev_f.append(np.mean(eval[(eval != np.max(eval)) & (eval != np.min(eval))]))
    
    return(dev_f)   
###################################################################



###################################################################
# Max factor:
###################################################################

def min_df(triangulo, cal_y_ignore = 0, acc_y_ignore = 0, f_ignore = None):

    #Generamos array de factores
    dev_f = []
    
    #Generamos triángulo de factores:
    LF_tr = tr.linkfactor_triangle(triangulo).fillna(0)
    
    #Generamos los pesos:
    weight_tr = weight_lf(LF_tr, cal_y_ignore, acc_y_ignore, f_ignore).fillna(0)

    for col in LF_tr.columns[:]:
            if np.sum(weight_tr.iloc[:len(weight_tr)-(col-1), col-1]) == 0:
                dev_f.append(1)
            else:
                # Verificar si hay algún cero en weight_tr en la misma posición
                if 0 in weight_tr.iloc[:len(weight_tr)-(col-1), col-1].values:
                    # Si hay un cero, ignorar los valores correspondientes en LF_tr
                    dev_f.append(np.min(LF_tr.iloc[:len(weight_tr)-(col-1), col-1][weight_tr.iloc[:len(weight_tr)-(col-1), col-1] != 0]))
                else:
                    dev_f.append(np.min(LF_tr.iloc[:len(weight_tr)-(col-1), col-1]))

    return(dev_f)
###################################################################



###################################################################
# Min factor:
###################################################################

def max_df(triangulo, cal_y_ignore = 0, acc_y_ignore = 0, f_ignore = None):

    #Generamos array de factores
    dev_f = []
    
    #Generamos triángulo de factores:
    LF_tr = tr.linkfactor_triangle(triangulo).fillna(0)
    
    #Generamos los pesos:
    weight_tr = weight_lf(LF_tr, cal_y_ignore, acc_y_ignore, f_ignore).fillna(0)
    
    for col in LF_tr.columns[:]:
            if np.sum(weight_tr.iloc[:len(weight_tr)-(col-1), col-1]) == 0:
                dev_f.append(1)
            else:
                # Verificar si hay algún cero en weight_tr en la misma posición
                if 0 in weight_tr.iloc[:len(weight_tr)-(col-1), col-1].values:
                    # Si hay un cero, ignorar los valores correspondientes en LF_tr
                    dev_f.append(np.max(LF_tr.iloc[:len(weight_tr)-(col-1), col-1][weight_tr.iloc[:len(weight_tr)-(col-1), col-1] != 0]))
                else:
                    dev_f.append(np.max(LF_tr.iloc[:len(weight_tr)-(col-1), col-1]))
    return(dev_f)
###################################################################



###################################################################
# Aggreation of different methods:
###################################################################

def df_generator(triangulo, method = 'all', cal_y_ignore = 0, acc_y_ignore = 0, f_ignore = None):
    
    #resumen de factores de desarrollo:
    if method == 'all':
        #periodos = list(range(1, len(triangulo)))
        summary_devf = {
            #'Periodos': periodos,
            'Simple avg': avg_df(triangulo, cal_y_ignore, acc_y_ignore, f_ignore),
            'Volume-Weight avg.': volweight_df(triangulo, cal_y_ignore, acc_y_ignore, f_ignore),
            'Time-Weight avg.': timeweight_df(triangulo, cal_y_ignore, acc_y_ignore, f_ignore),
            'Median': median_df(triangulo, cal_y_ignore, acc_y_ignore, f_ignore),
            'Geometric avg.': geom_df(triangulo, cal_y_ignore, acc_y_ignore, f_ignore),
            'Medial avg.': medialavg_df(triangulo, cal_y_ignore, acc_y_ignore, f_ignore),
            'Min': min_df(triangulo, cal_y_ignore, acc_y_ignore, f_ignore),
            'Max': max_df(triangulo, cal_y_ignore, acc_y_ignore, f_ignore)
            }
        df = pd.DataFrame(summary_devf)
        return(df)

    #Calculamos los factores en función del método seleccionado:
    elif method == 'avg':
        return avg_df(triangulo, cal_y_ignore, acc_y_ignore, f_ignore)
        
        
    elif method == 'vol_weight':
        return volweight_df(triangulo, cal_y_ignore, acc_y_ignore, f_ignore)
        
        
    elif method == 'time_weight':
        return timeweight_df(triangulo, cal_y_ignore, acc_y_ignore, f_ignore)
        
        
    elif method == 'median':
        return median_df(triangulo, cal_y_ignore, acc_y_ignore, f_ignore)         
    
    
    elif method == 'geom_avg':
        return geom_df(triangulo, cal_y_ignore, acc_y_ignore, f_ignore)
        
        
    elif method == 'medial_avg':
        return medialavg_df(triangulo, cal_y_ignore, acc_y_ignore, f_ignore)
        
        
    elif method == 'min':
        return min_df(triangulo, cal_y_ignore, acc_y_ignore, f_ignore)           
        
        
    elif method == 'max':
        return max_df(triangulo, cal_y_ignore, acc_y_ignore, f_ignore)
        
        
    else:
        return print("select a valid method")

###################################################################



###################################################################
# Graph DF according all methods:
###################################################################

def graph_methods_df(triangle, method, cal_y_ignore, acc_y_ignore, factors_to_ignore):

    summary_df = df_generator(triangle, method=method, cal_y_ignore=cal_y_ignore, acc_y_ignore=acc_y_ignore, f_ignore = factors_to_ignore)
    fig2 = px.line(summary_df, title='Development Factors')
    fig2.update_xaxes(title='Development Periods')
    fig2.update_yaxes(title='DF')
    fig2.show()
    summary_df

###################################################################



###################################################################
# Graph a given array of DF:
###################################################################

def graph_df(dev_f):

    fig2 = px.line(dev_f, title='Development Factors')
    fig2.update_xaxes(title='Development Periods')
    fig2.update_yaxes(title='DF')
    fig2.show()

###################################################################



###################################################################
# Calculate CDF
###################################################################

def prod_df(dev_f):
    #Factores de desarrollo acumulado
    cum_devf = []
    for i in range(len(dev_f)):
        cum_devf.append(np.prod(dev_f[i:len(dev_f)]))
    
    return cum_devf

###################################################################



###################################################################
# Calculate Inverse Development Factors
###################################################################

def inv_df(dev_f):
    #Factores de desarrollo acumulado
    cum_devf = []
    for i in range(len(dev_f)):
        cum_devf.append(np.prod(dev_f[i:len(dev_f)]))
    
    #Inverso del productorio
    inv_cum_devf = []
    for i in range(len(cum_devf)):
        inv_cum_devf.append(1 / (cum_devf[i]))
    
    return inv_cum_devf

###################################################################

