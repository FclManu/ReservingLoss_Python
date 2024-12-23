###################################################################
##### FUNCTIONS TO OBTAIN TAIL FACTORS:
###################################################################



import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy.stats import pearsonr

import triangles as tr
import dev_factor as dfm


###################################################################
# TAIL FACTOR ADJUSTMENT - Exponential Distribution:
###################################################################

def exp_adj_factor(dev_factors, only_tail = 1, num_factors = 5):

    ## If only_tail=1, returns only tails factors, if = 0 returns dev_f + tail
    
    dev_period = np.arange(1, len(dev_factors) + 1)
    
    #Filtrado de datos a ajustar para evitar errores de calculo pr factores < 1
    dev_period_filtered = dev_period[np.array(dev_factors) > 1]
    factores_filtered = np.array(dev_factors)[np.array(dev_factors) > 1]

    #Factor Cola exponencial:
    dist_model = LinearRegression().fit(dev_period_filtered.reshape(-1,1), np.log(factores_filtered - 1))
    #tail_model.intercept_
    #tail_model.coef_
    if only_tail == 0:
        adj_factors = np.array([(i+len(dev_factors)*only_tail + 1) for i in range(len(dev_factors)+num_factors)])
    else:
        adj_factors = np.array([(i+len(dev_factors)*only_tail + 1) for i in range(num_factors)])
    adj_factors = np.exp(dist_model.intercept_ + dist_model.coef_*adj_factors) + 1
     
    r = pearsonr(dev_period_filtered, np.log(factores_filtered - 1))
    r_squared = r.statistic**2

    r_sq_adj = 1 - ((len(dev_period_filtered) - 1) * (1 - r_squared)) / (len(dev_period_filtered) - 1 - 1)
    
    prod_adj_factors = adj_factors.prod()

    return(adj_factors, prod_adj_factors, r_squared, r_sq_adj)

###################################################################




###################################################################
# TAIL FACTOR ADJUSTMENT - Inverse Power Distribution:
###################################################################

def invpower_adj_factor(dev_factors, only_tail = 1, num_factors = 5):

    ## If only_tail=1, returns only tails factors, if = 0 returns dev_f + tail
    
    dev_period = np.arange(1, len(dev_factors) + 1)
    
    #Filtrado de datos a ajustar para evitar errores de calculo pr factores < 1
    dev_period_filtered = dev_period[np.array(dev_factors) > 1]
    factores_filtered = np.array(dev_factors)[np.array(dev_factors) > 1]

    #Factor Cola Potencia Inversa:
    dist_model = LinearRegression().fit(np.log(dev_period_filtered).reshape(-1,1), np.log(factores_filtered - 1))
    #tail_model.intercept_
    #tail_model.coef_
    if only_tail == 0:
        adj_factors = np.array([(i+len(dev_factors)*only_tail + 1) for i in range(len(dev_factors)+num_factors)])
    else:
        adj_factors = np.array([(i+len(dev_factors)*only_tail + 1) for i in range(num_factors)])
    adj_factors = np.exp(dist_model.intercept_ + dist_model.coef_*np.log(adj_factors)) + 1
        
    r = pearsonr(np.log(dev_period_filtered), np.log(factores_filtered - 1))
    r_squared = r.statistic**2

    r_sq_adj = 1 - ((len(dev_period_filtered) - 1) * (1 - r_squared)) / (len(dev_period_filtered) - 1 - 1)
    
    prod_adj_factors = adj_factors.prod()

    return(adj_factors, prod_adj_factors, r_squared, r_sq_adj)

###################################################################


###################################################################
# TAIL FACTOR ADJUSTMENT - Weibull Distribution:
###################################################################

def weibull_adj_factor(dev_factors, only_tail = 1, num_factors = 5):

    ## If only_tail=1, returns only tails factors, if = 0 returns dev_f + tail
    
    dev_period = np.arange(1, len(dev_factors) + 1)
    
    #Filtrado de datos a ajustar para evitar errores de calculo pr factores < 1
    dev_period_filtered = dev_period[np.array(dev_factors) > 1]
    factores_filtered = np.array(dev_factors)[np.array(dev_factors) > 1]

    #Factor Cola Weibull:
    dist_model = LinearRegression().fit(np.log(dev_period_filtered).reshape(-1,1), np.log(np.log(factores_filtered/(factores_filtered - 1))))
    #tail_model.intercept_
    #tail_model.coef_
    if only_tail == 0:
        adj_factors = np.array([(i+len(dev_factors)*only_tail + 1) for i in range(len(dev_factors)+num_factors)])
    else:
        adj_factors = np.array([(i+len(dev_factors)*only_tail + 1) for i in range(num_factors)])
    adj_factors = (np.exp(np.exp(dist_model.intercept_ + dist_model.coef_*np.log(adj_factors)))) / (np.exp(np.exp(dist_model.intercept_ + dist_model.coef_*np.log(adj_factors)))-1)
    
    r = pearsonr(np.log(dev_period_filtered), np.log(np.log(factores_filtered/(factores_filtered - 1))))
    r_squared = r.statistic**2

    r_sq_adj = 1 - ((len(dev_period_filtered) - 1) * (1 - r_squared)) / (len(dev_period_filtered) - 1 - 1)
    
    prod_adj_factors = adj_factors.prod()

    return(adj_factors, prod_adj_factors, r_squared, r_sq_adj)

###################################################################



###################################################################
# TAIL FACTOR ADJUSTMENT - Power Distribution:
###################################################################



def power_adj_factor(dev_factors, only_tail = 1, num_factors = 5):

    ## If only_tail=1, returns only tails factors, if = 0 returns dev_f + tail
    
    dev_period = np.arange(1, len(dev_factors) + 1)
    
    #Filtrado de datos a ajustar para evitar errores de calculo pr factores < 1
    dev_period_filtered = dev_period[np.array(dev_factors) > 1]
    factores_filtered = np.array(dev_factors)[np.array(dev_factors) > 1]

    #Factor Cola Potencia:
    dist_model = LinearRegression().fit(dev_period_filtered.reshape(-1,1), np.log(np.log(factores_filtered)))
    #tail_model.intercept_
    #tail_model.coef_
    if only_tail == 0:
        adj_factors = np.array([(i+len(dev_factors)*only_tail + 1) for i in range(len(dev_factors)+num_factors)])
    else:
        adj_factors = np.array([(i+len(dev_factors)*only_tail + 1) for i in range(num_factors)])
    adj_factors = np.exp(np.exp(dist_model.intercept_ + dist_model.coef_*adj_factors)) 
        
    r = pearsonr(dev_period_filtered, np.log(np.log(factores_filtered)))
    r_squared = r.statistic**2

    r_sq_adj = 1 - ((len(dev_period_filtered) - 1) * (1 - r_squared)) / (len(dev_period_filtered) - 1 - 1)
    
    prod_adj_factors = adj_factors.prod()

    return(adj_factors, prod_adj_factors, r_squared, r_sq_adj)

###################################################################


###################################################################
# TAIL FACTOR ADJUSTMENT - Includes values and metrics for each adjustment:
###################################################################

def summary_tail_f(dev_factors, distribution = 'all', only_tail = 1, num_factors = 10):

    #resumen de factores de desarrollo:
    if distribution == 'all':
        periodos = list(range(1, num_factors))
        periodos.extend(['Producto', 'R2', 'R2Adj'])
        
        summary_adj_factors = {
            #'Periodos': periodos,
            'Exponential': exp_adj_factor(dev_factors, only_tail, num_factors),
            'Inverse Power': invpower_adj_factor(dev_factors, only_tail, num_factors),
            'Weibull': weibull_adj_factor(dev_factors, only_tail, num_factors),
            'Power': power_adj_factor(dev_factors, only_tail, num_factors)
            }
        df = pd.DataFrame(summary_adj_factors)
        #df.set_index('Periodos', inplace=True)
        return(df)
    
    elif distribution == 'exp':   
        return exp_adj_factor(dev_factors, only_tail, num_factors)
    
    elif distribution == 'inv_power':
        return invpower_adj_factor(dev_factors, only_tail, num_factors)
        
    elif distribution == 'weibull':
        return weibull_adj_factor(dev_factors, only_tail, num_factors)
    
    elif distribution == 'power':
        return power_adj_factor(dev_factors, only_tail, num_factors)
    
    else:
        return("select distribution")

###################################################################



###################################################################
# TAIL FACTOR ADJUSTMENT - Graph and show values and metrics for a distribution:
###################################################################

def graph_adjusted_tail(dev_factors, adj_f, adj_rsq, adj_rsq_adj):

    fig = go.Figure()

    # Deterministic DF
    fig.add_trace(go.Scatter(
        x=list(range(len(dev_factors))),
        y=dev_factors,
        mode='markers',   # Representar como puntos
        name='Deterministic DF'
    ))

    # Exponential DF
    fig.add_trace(go.Scatter(
        x=list(range(len(adj_f))),
        y=adj_f,
        mode='lines',     # Representar como líneas
        name='Adjusted DF'
    ))

    # Agregar títulos y etiquetas a los ejes
    fig.update_layout(
        title='Deterministic DF vs. Exponential adj. DF',
        xaxis_title='Dev.Period',
        yaxis_title='DF'
    )

    fig.add_annotation(text=f"R sq.: {adj_rsq:.2%}",
                       xref="paper", yref="paper",
                       x=0.95, y=0.85, showarrow=False)

    fig.add_annotation(text=f"Adj. R sq.: {adj_rsq_adj:.2%}",
                       xref="paper", yref="paper",
                       x=0.95, y=0.75, showarrow=False)

    # Mostrar el gráfico
    fig.show()

###################################################################



###################################################################
# TAIL FACTOR ADJUSTMENT - Graph and show values and metrics for each adjustment:
###################################################################

def graph_tail_f(dev_factors, distribution = 'all', num_factors = 4):

    exp_f, cum_exp_f, rsq_exp, rsq_adj_exp = summary_tail_f(dev_factors, distribution = 'exp', only_tail=0, num_factors=num_factors)
    inv_f, cum_inv_f, rsq_inv, rsq_adj_inv = summary_tail_f(dev_factors, distribution = 'inv_power', only_tail=0, num_factors=num_factors)
    weibull_f, cum_weibull_f, rsq_weibull, rsq_adj_weibull = summary_tail_f(dev_factors, distribution = 'weibull', only_tail=0, num_factors=num_factors)
    power_f, cum_power_f, rsq_power, rsq_adj_power = summary_tail_f(dev_factors, distribution = 'power', only_tail=0, num_factors=num_factors)

    if distribution == 'all':

        # Crear un layout de subplots de 2x2
        fig = make_subplots(rows=2, cols=2, subplot_titles=('DF vs. Exp', 'DF vs. Inv Power', 'DF vs. Weibull', 'DF vs. Power'))

        # EXPONENTIAL (Gráfico 1)
        fig.add_trace(go.Scatter(
            x=list(range(len(dev_factors))),
            y=dev_factors,
            mode='markers',
            name='Deterministic DF'
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=list(range(len(exp_f))),
            y=exp_f,
            mode='lines',
            name='Adjusted DF - Exp.'
        ), row=1, col=1)

        fig.add_annotation(text=f"R sq.: {rsq_exp:.2%}",
                           xref="paper", yref="paper",
                           x=0.4, y=0.95, showarrow=False)

        fig.add_annotation(text=f"Adj. R sq.: {rsq_adj_exp:.2%}",
                           xref="paper", yref="paper",
                           x=0.4, y=0.85, showarrow=False)

        # INVERSE POWER (Gráfico 2)
        fig.add_trace(go.Scatter(
            x=list(range(len(dev_factors))),
            y=dev_factors,
            mode='markers',
            name='Deterministic DF'
        ), row=1, col=2)

        fig.add_trace(go.Scatter(
            x=list(range(len(inv_f))),
            y=inv_f,
            mode='lines',
            name='Adjusted DF - Inv. Power'
        ), row=1, col=2)

        fig.add_annotation(text=f"R sq.: {rsq_inv:.2%}",
                           xref="paper", yref="paper",
                           x=0.97, y=0.95, showarrow=False)

        fig.add_annotation(text=f"Adj. R sq.: {rsq_adj_inv:.2%}",
                           xref="paper", yref="paper",
                           x=0.97, y=0.85, showarrow=False)

        # WEIBULL (Gráfico 3)
        fig.add_trace(go.Scatter(
            x=list(range(len(dev_factors))),
            y=dev_factors,
            mode='markers',
            name='Deterministic DF'
        ), row=2, col=1)

        fig.add_trace(go.Scatter(
            x=list(range(len(weibull_f))),
            y=weibull_f,
            mode='lines',
            name='Adjusted DF - Weibull'
        ), row=2, col=1)

        fig.add_annotation(text=f"R sq.: {rsq_weibull:.2%}",
                           xref="paper", yref="paper",
                           x=0.4, y=0.25, showarrow=False)

        fig.add_annotation(text=f"Adj. R sq.: {rsq_adj_weibull:.2%}",
                           xref="paper", yref="paper",
                           x=0.4, y=0.15, showarrow=False)

        # POWER (Gráfico 4)
        fig.add_trace(go.Scatter(
            x=list(range(len(dev_factors))),
            y=dev_factors,
            mode='markers',
            name='Deterministic DF'
        ), row=2, col=2)

        fig.add_trace(go.Scatter(
            x=list(range(len(power_f))),
            y=power_f,
            mode='lines',
            name='Adjusted DF - Power'
        ), row=2, col=2)

        fig.add_annotation(text=f"R sq.: {rsq_power:.2%}",
                           xref="paper", yref="paper",
                           x=0.97, y=0.25, showarrow=False)

        fig.add_annotation(text=f"Adj. R sq.: {rsq_adj_power:.2%}",
                           xref="paper", yref="paper",
                           x=0.97, y=0.15, showarrow=False)

        # Actualizar los títulos de los ejes para los cuatro gráficos
        fig.update_layout(
            title_text="Adjusted DF + Tail Factor",
            xaxis_title='',
            yaxis_title='',
            showlegend=False
        )

        # Mostrar el gráfico
        fig.show()


    elif distribution == 'exp':
        f = exp_f
        rsq = rsq_exp
        rsq_adj = rsq_adj_exp
        graph_adjusted_tail(dev_factors, f, rsq, rsq_adj)

    elif distribution == 'inv_power':
        f = inv_f
        rsq = rsq_inv
        rsq_adj = rsq_adj_inv
        graph_adjusted_tail(dev_factors, f, rsq, rsq_adj)

    elif distribution == 'power':
        f = power_f
        rsq = rsq_power
        rsq_adj = rsq_adj_power
        graph_adjusted_tail(dev_factors, f, rsq, rsq_adj)

    elif distribution == 'weibull':
        f = weibull_f
        rsq = rsq_weibull
        rsq_adj = rsq_adj_weibull
        graph_adjusted_tail(dev_factors, f, rsq, rsq_adj)
    
    else:
        return("select distribution")


###################################################################






































