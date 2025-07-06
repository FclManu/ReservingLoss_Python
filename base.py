
###################################################################
##### LIBRARIES:
###################################################################


###### General Libraries ######
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

###### Created Libraries ######
import triangles as tr
import dev_factor as devf
import tail_factor as tailf
import deterministic as dt
import tests_cl as tcl



###################################################################
# Functions to upload triangles:
###################################################################

# From DataBase:

def upload_triangle_from_csv(file: str, base_period: str, dev_period: str, aggr_values: str, lob_column: str = None, lob_name: str = None, type_triangle: str = None):

    """
    Function to upload triangles from a data base in .csv format. 
    Database must include a column for origin period (ie. Acc.Years), Development period (Lags), and the values to upload (ie. Incurrec Losses).

    Parameters
    ----------
    file: (str)  
        Path of file to read  

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

     type_triangle: (str)  
        The type of triangle to assign a class. None as a default value. Possible options:  
            - 'CumPayments'  
            - 'IncPayments'  
            - 'CaseReserves'  
            - 'Incurred'  

    """

    if type_triangle == None:
        triangle = tr.triangle_from_csv(file, base_period, dev_period, aggr_values, lob_column, lob_name)
        return triangle

    elif type_triangle == 'CumPayments':
        triangle = tr.triangle_from_csv(file, base_period, dev_period, aggr_values, lob_column, lob_name)
        return CumPayments_triangle(triangle)
    
    elif type_triangle == 'IncrPayments':
        triangle = tr.triangle_from_csv(file, base_period, dev_period, aggr_values, lob_column, lob_name)
        return IncPayments_triangle(triangle)
    
    elif type_triangle == 'CaseReserves':
        triangle = tr.triangle_from_csv(file, base_period, dev_period, aggr_values, lob_column, lob_name)
        return CaseReserves_triangle(triangle)
    
    elif type_triangle == 'Incurred':
        triangle = tr.triangle_from_csv(file, base_period, dev_period, aggr_values, lob_column, lob_name)
        return Incurred_triangle(triangle)
    
    else: return print('Include a valid type_triangle or review the inputs.')


# From a triangle already built in excel:

def upload_triangle_from_excel(file: str, sheet: str, init_col: int, init_row: int, dim: int, start_year: int, month: int = 12, periodicity: str = 'annual', type_triangle: str = None):

    """
    Function to upload triangles from a data base in .csv format.   
    Database must include a column for origin period (ie. Acc.Years), Development period (Lags), and the values to upload (ie. Incurrec Losses).  

    Parameters  
    ----------  
    file: (str)  
        Path of file to read  

    sheet: (str)  
        Sheet of location of the triagle.    

    init_col: (int)  
        Number of the column in which the triangle starts.    

    init_row: (int)    
        Number of the row in which the triangle starts.    

    dim: (int)  
        Number of rows/columns to read, or dimension of triangle.  

    start_year: (int)  
        First origin year.  

     month: (int)  
        First origin month.         

     periodicity: (str)  
        Periodicity of the triangle:  
            - 'Annual'    
            - 'biannual'    
            - 'three_times_year'    
            - 'quarterly'    
            - 'bimonthly'    
            - 'monthly'      

     type_triangle: (str)  
        The type of triangle to assign a class. None as a default value. Possible options:  
            - 'CumPayments'    
            - 'IncPayments'    
            - 'CaseReserves'    
            - 'Incurred'    
            
    """

    if type_triangle == None:
        triangle = tr.upload_triangle_excel(file, sheet, init_col, init_row, dim, start_year, month, periodicity)
        return triangle

    elif type_triangle == 'CumPayments':
        triangle = tr.upload_triangle_excel(file, sheet, init_col, init_row, dim, start_year, month, periodicity)
        return CumPayments_triangle(triangle)
    
    elif type_triangle == 'IncrPayments':
        triangle = tr.upload_triangle_excel(file, sheet, init_col, init_row, dim, start_year, month, periodicity)
        return IncPayments_triangle(triangle)
    
    elif type_triangle == 'CaseReserves':
        triangle = tr.upload_triangle_excel(file, sheet, init_col, init_row, dim, start_year, month, periodicity)
        return CaseReserves_triangle(triangle)
    
    elif type_triangle == 'Incurred':
        triangle = tr.upload_triangle_excel(file, sheet, init_col, init_row, dim, start_year, month, periodicity)
        return Incurred_triangle(triangle)
    
    else: return print('Include a valid type_triangle or review the inputs.')



###################################################################
# Classes of triangles to integrate functions:
###################################################################

# Generic triangle class:

class triangle():

    """
    Class to include common methods for all type of triangles.  

    Atributes  
    ----------  
        - diag  
        - graph_tr  
        - heatmap  
        - show  
    """

    def __init__(self, input_triangle): 
        
        self.input_triangle = pd.DataFrame(input_triangle)
    
    
    def graph_tr(self): # Graph values of the triangle by AY and DY
        """
        Graph the triangle by Accident Period and Development Period.
        """
        return tr.graph_values(self.input_triangle)
    
    # Show the triangle with a heatcolor format
    def heatmap(self):
        """
        Graph the triangle in a coloured format.
        """
        return tr.heatmap_format(self.input_triangle, fmt=",.0f")
  
    # Returns the last diag of the triangle
    def diag(self):
        """
        Returns the last diagonal of the triangle.
        """
        return tr.last_diag(self.input_triangle)
    
    # Atributo shape para obtener las dimensiones
    @property
    def shape(self):
        return self.input_triangle.shape
    
    # Proporcionar acceso directo a iloc
    @property
    def iloc(self):
        return self.input_triangle.iloc
    
    # Proporcionar acceso directo a T
    @property
    def T(self):
        return self.data.T
    
    # Método para acceder al DataFrame directamente
    def show(self):
        """
        Returns the triangle in dataframe format.
        """
        formatted_df = self.input_triangle.applymap(lambda x: "{:,.2f}".format(x))
        return formatted_df
    
    # Representación personalizada
    def __repr__(self):
        return f"({self.input_triangle})"
    


# Cummulative Payments Triangle Class:

class CumPayments_triangle(triangle):

    """
    Class to include Cumulative Payment Triangles.  

    Atributes  
    ----------  
        - diag   
        - graph_tr  
        - heatmap  
        - show  
        - link_factors  
        - heatmap_linkf  
        - graph_linkf  
        - get_dev_f  
        - graph_dev_f  
        - chainladder  
        - bf  
    """

    def __init__(self, input_triangle):
        self.input_triangle = input_triangle

    # Convert the cummulative triangle to an incremental one:
    def to_incr(self):
        """
        Returns the cummulative triangle into an incremental one.
        """
        #return tr.cum_to_incr(self.input_triangle)
        incr_tr = tr.cum_to_incr(self.input_triangle)
        return IncPayments_triangle(incr_tr)
        
    # Returns the link factor triangle
    def link_factors(self):
        """
        Returns the link factors.
        """
        return tr.linkfactor_triangle(self.input_triangle)
    
    # Returns the link factor triangle with a heat color format
    def heatmap_linkf(self):
        """
        Show LinkFactors (Fij) in a heat coloured format in order to improve interpretation.
        """
        fij = tr.linkfactor_triangle(self.input_triangle)
        return tr.heatmap_format(fij)
    
    # Graph link factors of the triangle by AY and DY
    def graph_linkf(self):
        """
        Graph Link Factors (Fij) by Accident Period and Development Period
        """
        fij = tr.linkfactor_triangle(self.input_triangle)
        return tr.graph_values(fij)
    
    #Get development factors wo ignore any link ratio
    #def get_dev_f(self, method, cal_y_ignore, acc_y_ignore, f_ignore):
    #    return devf.df_generator(self.input_triangle, method, cal_y_ignore, acc_y_ignore, f_ignore)
    def get_dev_f(self, method='vol_weight', cal_y_ignore = 0, acc_y_ignore = 0, f_ignore = None):
        """
        Returns the Development Factors in order to project losses.  

        Parameters  
        ----------  
        method: (str)  
            Method to estimate development factors. Possible values:  
                - 'all': Returns a summary of all metrics.  
                - 'avg': Arithmetic mean of the Link Factors.   
                - 'vol_weight': Weighted average of the factors by the amount of claims (giving greater weight to factors with a higher claim frequency). (Most used)  
                - 'time_weight': Weighted average of the factors, giving more weight to the most recent factors compared to older periods.  
                - 'median': Median of the step factors.  
                - 'geom_avg': Geometric average.  
                - 'medial_avg': Arithmetic mean, ignoring the maximum and minimum Link Factors.  
                - 'min': Value of the minimum Link Factor.  
                - 'max': Value of the maximum Link Factor.  
        
        cal_y_ignore: (int)  
            Number of calendar periods to ignore. Set 0 as default.  

        acc_y_ignore: (int)  
            Number of accident periods to ignore. Set 0 as default.  

        f_ignore: (array)  
            Array in order to include the Fij to ignore. ie: [('12/2014', 1), ('12/2016', 1), ('12/2013', 2)].  
            Set None as default.  


        Atributes  
        ----------  
            graph_df: Graph the Development Factors.  
            cdf: Returns the cummulative development factors.  
            inv_df: Returns the inverse values of cummulative development factors.  
            tail_f: Returns tail factors according to defferent attributes.  
            graph_tail_f: Graph tail factors according to defferent attributes.  
        """
        factor = devf.df_generator(self.input_triangle, method, cal_y_ignore, acc_y_ignore, f_ignore)
        return dev_f(factor)
    
    # Graph development Factors
    def graph_devf(self, method, cal_y_ignore, acc_y_ignore, f_ignore):
        """
        Graph the Development Factors in order to project losses.  
  
        Parameters  
        ----------  
        method: (str)  
            Method to estimate development factors. Possible values:  
                - 'all': Returns a summary of all metrics.  
                - 'avg': Arithmetic mean of the Link Factors.   
                - 'vol_weight': Weighted average of the factors by the amount of claims (giving greater weight to factors with a higher claim frequency). (Most used)  
                - 'time_weight': Weighted average of the factors, giving more weight to the most recent factors compared to older periods.  
                - 'median': Median of the step factors.  
                - 'geom_avg': Geometric average.  
                - 'medial_avg': Arithmetic mean, ignoring the maximum and minimum Link Factors.  
                - 'min': Value of the minimum Link Factor.  
                - 'max': Value of the maximum Link Factor.  
          
        cal_y_ignore: (int)  
            Number of calendar periods to ignore. Set 0 as default.  
  
        acc_y_ignore: (int)  
            Number of accident periods to ignore. Set 0 as default.  
  
        f_ignore: (array)  
            Array in order to include the Fij to ignore. ie: [('12/2014', 1), ('12/2016', 1), ('12/2013', 2)].  
            Set None as default.  
        """
        return devf.graph_methods_df(self.input_triangle, method, cal_y_ignore=0, acc_y_ignore=0, f_ignore=None)


    def tests_cl(self, dev_f, test):
        """
        Returns different tests in order to analyse if data are enough propper to use Loss Developments methods.  
  
        Parameters  
        ----------  
        dev_f: (array)  
            Development factors to develop the triangle. It may be the DF calculated with the method 'graph_df' or a customized array.  
            Dimension must match with 'len(triangle)-1'.  
  
        test: (str)  
            Test to show:  
                - 'linear': Show graphs by Development Periods in order to analyse the linearity of LinkFactors Fij.  
                - 'residual': Show the graphs of residual in order to understand if they are randomly distributed or not.  
                - 'calendar':  
                - 'correlation': Show the   
        """

        if test == 'linear':
            return tcl.linear_test(self.input_triangle, dev_f, test)
        elif test == 'residual':
            print('mmmm')
        elif test == 'calendar':
            print('mmmm')
        elif test == 'correlation':
            print('mmmm')
        else:
            print('Introduce a correct test name. "linear", "residual", "calendar" or "correlation" are the valid options.')
        


    # Project triangle Chain-Ladder Method
    def chainladder(self, dev_f, tail_f = None):
        """
        Project Loss development Method. Returns the projected triangle.  

        Parameters  
        ----------  
        dev_f: (array)  
            Development factors to develop the triangle. It may be the DF calculated with the method 'graph_df' or a customized array.  
            Dimension must match with 'len(triangle)-1'.  
  
        tail_f: (array)  
            Tail_factors to add after Development Factors. Set None as default  
  
        Atributes  
        ----------  
            diag: Returns the last diagonal of the triangle (actual).  
            ultimate: Returns the ultimate projected.  
            show: Returns the developed triangle in a data frame format.  
            ibnr: Returns the IBNR by accident period.  
            reserve: Returns the Reserves by accident period.  
        """
        projection = dt.chainladder(self.input_triangle, dev_f, tail_f)
        return Payments_developed_tr(projection)
    
    # Project triangle Bornhuetter-Ferguson Method
    def bf(self, dev_f, a_priori_ult, tail_f = None):
        """
        Project Bornhuetter-Ferguson Method. Returns the projected triangle.  
  
        Parameters  
        ----------  
        dev_f: (array)  
            Development factors to develop the triangle. It may be the DF calculated with the method 'graph_df' or a customized array.  
            Dimension must match with 'len(triangle)-1'.  
          
        a_priori_ult: (array)  
            a priori Ultimate in order to project by BF.   
  
        tail_f: (array)  
            Tail_factors to add after Development Factors. Set None as default  
  
        Atributes  
        ----------  
            diag: Returns the last diagonal of the triangle (actual).  
            ultimate: Returns the ultimate projected.  
            show: Returns the developed triangle in a data frame format.  
            ibnr: Returns the IBNR by accident period.  
            reserve: Returns the Reserves by accident period.  
        """
        projection = dt.bf(self.input_triangle, dev_f, a_priori_ult, tail_f)
        return Payments_developed_tr(projection)
    

    # Project triangle Cape-Cod Method
    def cape_cod(self, dev_f, premiums, tail_f = None):
        """
        Project Bornhuetter-Ferguson Method. Returns the projected triangle.  
  
        Parameters  
        ----------  
        dev_f: (array)  
            Development factors to develop the triangle. It may be the DF calculated with the method 'graph_df' or a customized array.  
            Dimension must match with 'len(triangle)-1'.  
          
        premiums: (array)  
            Premiums by Origin Period
  
        tail_f: (array)  
            Tail_factors to add after Development Factors. Set None as default  
  
        Atributes  
        ----------  
            diag: Returns the last diagonal of the triangle (actual).  
            ultimate: Returns the ultimate projected.  
            show: Returns the developed triangle in a data frame format.  
            ibnr: Returns the IBNR by accident period.  
            reserve: Returns the Reserves by accident period.  
        """
        projection = dt.capecod(self.input_triangle, dev_f, premiums, tail_f)
        return Payments_developed_tr(projection)


# Incremental Payments Triangle Class:

class IncPayments_triangle(triangle):

    """
    Class to include Incremental Payment Triangles.  
  
    Atributes  
    ----------  
        - diag  
        - graph_tr  
        - heatmap  
        - show  
        - to_cum  
    """

    def __init__(self, input_triangle):
        self.input_triangle =input_triangle

    # Convert the incremental triangle to a cummulative one:
    def to_cum(self):
        """
        Returns the incremental triangle into an cumulative one.
        """
        #return tr.incr_to_cum(self.input_triangle)
        cum_tr = tr.incr_to_cum(self.input_triangle)
        return IncPayments_triangle(cum_tr)


# Case Reserves Triangle Class:

class CaseReserves_triangle(triangle):

    """
    Class to include Case Reserve Triangles.  
  
    Atributes  
    ----------  
        - diag  
        - graph_tr  
        - heatmap  
        - show  
    """

    def __init__(self, input_triangle):
        self.input_triangle = input_triangle


# Incurred Cost Triangle Class:

class Incurred_triangle(triangle):

    """
    Class to include Incurred Costs Triangles.  
  
    Atributes  
    ----------  
        - diag  
        - graph_tr  
        - heatmap  
        - show  
        - link_factors  
        - heatmap_linkf  
        - graph_linkf  
        - get_dev_f  
        - graph_dev_f  
        - chainladder  
        - bf  
    """

    def __init__(self, input_triangle):
        self.input_triangle =input_triangle
    
    # Returns the link factor triangle
    def link_factors(self):
        """
        Returns the link factors.
        """
        return tr.linkfactor_triangle(self.input_triangle)
    
    # Returns the link factor triangle with a heat color format
    def heatmap_linkf(self):
        """
        Show LinkFactors (Fij) in a heat coloured format in order to improve interpretation.
        """
        fij = tr.linkfactor_triangle(self.input_triangle)
        return tr.heatmap_format(fij)
    
    # Graph link factors of the triangle by AY and DY
    def graph_linkf(self):
        """
        Graph Link Factors (Fij) by Accident Period and Development Period
        """
        fij = tr.linkfactor_triangle(self.input_triangle)
        return tr.graph_values(fij)
    
    #Get development factors wo ignore any link ratio
    #def get_dev_f(self, method, cal_y_ignore, acc_y_ignore, f_ignore):
    #    return devf.df_generator(self.input_triangle, method, cal_y_ignore, acc_y_ignore, f_ignore)
    def get_dev_f(self, method='vol_weight', cal_y_ignore=0, acc_y_ignore=0, f_ignore=None):
        """  
        Returns the Development Factors in order to project losses.  
  
        Parameters  
        ----------  
        method: (str)  
            Method to estimate development factors. Possible values:  
                - 'all': Returns a summary of all metrics.  
                - 'avg': Arithmetic mean of the Link Factors.   
                - 'vol_weight': Weighted average of the factors by the amount of claims (giving greater weight to factors with a higher claim frequency). (Most used)  
                - 'time_weight': Weighted average of the factors, giving more weight to the most recent factors compared to older periods.  
                - 'median': Median of the step factors.  
                - 'geom_avg': Geometric average.  
                - 'medial_avg': Arithmetic mean, ignoring the maximum and minimum Link Factors.  
                - 'min': Value of the minimum Link Factor.  
                - 'max': Value of the maximum Link Factor.  
          
        cal_y_ignore: (int)  
            Number of calendar periods to ignore. Set 0 as default.  
  
        acc_y_ignore: (int)  
            Number of accident periods to ignore. Set 0 as default.  
  
        f_ignore: (array)  
            Array in order to include the Fij to ignore. ie: [('12/2014', 1), ('12/2016', 1), ('12/2013', 2)].  
            Set None as default.  
  
  
        Atributes  
        ----------  
            graph_df: Graph the Development Factors.  
            cdf: Returns the cummulative development factors.  
            inv_df: Returns the inverse values of cummulative development factors.  
            tail_f: Returns tail factors according to defferent attributes.  
            graph_tail_f: Graph tail factors according to defferent attributes.  
        """
        factor = devf.df_generator(self.input_triangle, method, cal_y_ignore, acc_y_ignore, f_ignore)
        return dev_f(factor)
    
    # Graph development Factors
    def graph_devf(self, method, cal_y_ignore=0, acc_y_ignore=0, f_ignore=None):
        """
        Graph the Development Factors in order to project losses.  
  
        Parameters  
        ----------  
        method: (str)  
            Method to estimate development factors. Possible values:  
                - 'all': Returns a summary of all metrics.  
                - 'avg': Arithmetic mean of the Link Factors.   
                - 'vol_weight': Weighted average of the factors by the amount of claims (giving greater weight to factors with a higher claim frequency). (Most used)  
                - 'time_weight': Weighted average of the factors, giving more weight to the most recent factors compared to older periods.  
                - 'median': Median of the step factors.  
                - 'geom_avg': Geometric average.  
                - 'medial_avg': Arithmetic mean, ignoring the maximum and minimum Link Factors.  
                - 'min': Value of the minimum Link Factor.  
                - 'max': Value of the maximum Link Factor.  
          
        cal_y_ignore: (int)  
            Number of calendar periods to ignore. Set 0 as default.  
  
        acc_y_ignore: (int)  
            Number of accident periods to ignore. Set 0 as default.  
  
        f_ignore: (array)  
            Array in order to include the Fij to ignore. ie: [('12/2014', 1), ('12/2016', 1), ('12/2013', 2)].  
            Set None as default.  
        """
        return devf.graph_methods_df(self.input_triangle, method, cal_y_ignore, acc_y_ignore, f_ignore)



    def tests_cl(self, dev_f, test):
        """
        Returns different tests in order to analyse if data are enough propper to use Loss Developments methods.  
  
        Parameters  
        ----------  
        dev_f: (array)  
            Development factors to develop the triangle. It may be the DF calculated with the method 'graph_df' or a customized array.  
            Dimension must match with 'len(triangle)-1'.  
  
        test: (str)  
            Test to show:  
                - 'linear': Show graphs by Development Periods in order to analyse the linearity of LinkFactors Fij.    
                - 'residual': Show the graphs of residual in order to understand if they are randomly distributed or not.    
                - 'calendar':    
                - 'correlation': Show the     
        """

        if test == 'linear':
            return tcl.linear_test(self.input_triangle, dev_f)
        elif test == 'residual':
            print('mmmm')
        elif test == 'calendar':
            print('mmmm')
        elif test == 'correlation':
            print('mmmm')
        else:
            print('Introduce a correct test name. "linear", "residual", "calendar" or "correlation" are the valid options.')



    # Project triangle Chain-Ladder Method
    def chainladder(self, dev_f, tail_f = None):
        """
        Project Loss development Method. Returns the projected triangle.  

        Parameters  
        ----------    
        dev_f: (array)  
            Development factors to develop the triangle. It may be the DF calculated with the method 'graph_df' or a customized array.  
            Dimension must match with 'len(triangle)-1'.  
  
        tail_f: (array)  
            Tail_factors to add after Development Factors. Set None as default  
  
        Atributes  
        ----------  
            diag: Returns the last diagonal of the triangle (actual).  
            ultimate: Returns the ultimate projected.  
            show: Returns the developed triangle in a data frame format.  
            ibnr: Returns the IBNR by accident period.  
            reserve: Returns the Reserves by accident period.  
        """
        projection = dt.chainladder(self.input_triangle, dev_f, tail_f)
        return Incurred_developed_tr(projection)
    
    # Project triangle Bornhuetter-Ferguson Method
    def bf(self, dev_f, a_priori_ult, tail_f = None):
        """
        Project Bornhuetter-Ferguson Method. Returns the projected triangle.  
  
        Parameters  
        ----------  
        dev_f: (array)  
            Development factors to develop the triangle. It may be the DF calculated with the method 'graph_df' or a customized array.  
            Dimension must match with 'len(triangle)-1'.  
          
        a_priori_ult: (array)  
            a priori Ultimate in order to project by BF.   
  
        tail_f: (array)  
            Tail_factors to add after Development Factors. Set None as default  
  
        Atributes  
        ----------  
            diag: Returns the last diagonal of the triangle (actual).  
            ultimate: Returns the ultimate projected.  
            show: Returns the developed triangle in a data frame format.  
            ibnr: Returns the IBNR by accident period.  
            reserve: Returns the Reserves by accident period.  
        """
        projection = dt.bf(self.input_triangle, dev_f, a_priori_ult, tail_f)
        return Incurred_developed_tr(projection)
    


    # Project triangle Cape-Cod Method
    def cape_cod(self, dev_f, premiums, tail_f = None):
        """
        Project Bornhuetter-Ferguson Method. Returns the projected triangle.  
  
        Parameters  
        ----------  
        dev_f: (array)  
            Development factors to develop the triangle. It may be the DF calculated with the method 'graph_df' or a customized array.  
            Dimension must match with 'len(triangle)-1'.  
          
        premiums: (array)  
            Premiums by Origin Period
  
        tail_f: (array)  
            Tail_factors to add after Development Factors. Set None as default  
  
        Atributes  
        ----------  
            diag: Returns the last diagonal of the triangle (actual).  
            ultimate: Returns the ultimate projected.  
            show: Returns the developed triangle in a data frame format.  
            ibnr: Returns the IBNR by accident period.  
            reserve: Returns the Reserves by accident period.  
        """
        projection = dt.capecod(self.input_triangle, dev_f, premiums, tail_f)
        return Incurred_developed_tr(projection)




###################################################################
# Class to define Development Factors:
###################################################################




def custom_devf(*args):
    """
    Allow customize the development factors .  
  
    Parameters  
    ----------  
    distribution: (float)  
        It is possible to introduce a vector, or an individual factor.  
        If a vector is included, it will include the factor in the same position.  
        Example: custom_devf(vol_f, time_f, 1.2, avg_f, 1.2, 1.5, 1.1, 1, 1)  
    """
    factors = devf.custom_df(*args)
    return dev_f(factors)



class dev_f(np.ndarray):

    """
    Class to include Development Factor array. Input must be a numpy array.  
  
    Atributes  
    ----------  
        - graph_df  
        - cdf  
        - show  
        - inv_df  
        - tail_f  
        - graph_tail_f  
    """

    def __init__(self, df):
        self.df = df

    #def __repr__(self):
    #    # Show a summary of the input
    #    return f"{self.df})"
    
    # Graph de selected DF
    def graph_df(self):
        """
        Graph the Development Factor(s).
        """
        return devf.graph_df(self.df)
    
    # Get CDF (Cummulated DF)
    def cdf(self):
        """
        Resturn the cumulative development factors (CDF).
        """
        return devf.prod_df(self.df)
    
    # Get inverse CDF
    def inv_df(self):
        """
        Returns the inverse cumulative development factors (1/CDF).
        """
        return devf.inv_df(self.df)
    
    # Get Tail Factors:
    def tail_f(self, distribution, only_tail = 1, num_factors = 5):
        """
        Estimates the tail factors according to a distribution given.  
  
        Parameters  
        ----------  
        distribution: (str)  
            Distribution to use in tail factor calculation:    
                - 'all': Shows a summary of the all possible estimations.    
                - 'exp': Uses exponential distribution.    
                - 'inv_power': Uses inverse power distribution.    
                - 'power': Uses power distribution.    
                - 'weibull': Uses Weibull distribution.    
  
          
        only_tail: (int)  
            Only can take 1 or 0 values:  
                - 1: The function will return only the tail factor estimated.    
                - 0: The function will return the tail factor as well as the rest of factors adjusted to the selected distribution.  
  
        num_factors: (int)  
            Number of tail_factors to add after Development Factors. Set None as default.  
        """
        tail_f, cum_tail_f, rsq_tail_f, rsq_adj_tail_f = tailf.summary_tail_f(self.df, distribution, only_tail, num_factors)
        return tail_f
    
    # Get Cumulative Tail Factors:
    def cum_tail_f(self, distribution, only_tail = 1, num_factors = 5):
        """
        Estimates the cumulative tail factor according to a distribution given (Product of all tail factors).  
  
        Parameters  
        ----------  
        distribution: (str)  
            Distribution to use in tail factor calculation:    
                - 'all': Shows a summary of the all possible estimations.    
                - 'exp': Uses exponential distribution.    
                - 'inv_power': Uses inverse power distribution.    
                - 'power': Uses power distribution.    
                - 'weibull': Uses Weibull distribution.    
  
          
        only_tail: (int)  
            Only can take 1 or 0 values:  
                - 1: The function will return only the tail factor estimated.    
                - 0: The function will return the tail factor as well as the rest of factors adjusted to the selected distribution.  
  
        num_factors: (int)  
            Number of tail_factors to add after Development Factors. Set None as default.  
        """
        tail_f, cum_tail_f, rsq_tail_f, rsq_adj_tail_f = tailf.summary_tail_f(self.df, distribution, only_tail, num_factors)
        return cum_tail_f


    # Get Tail Factors:
    def rsq_tail_f(self, distribution, only_tail = 1, num_factors = 5):
        """
        Calculates the R Squared Adjusted of tail factors according data included.  
  
        Parameters  
        ----------  
        distribution: (str)  
            Distribution to use in tail factor calculation:    
                - 'all': Shows a summary of the all possible estimations.    
                - 'exp': Uses exponential distribution.    
                - 'inv_power': Uses inverse power distribution.    
                - 'power': Uses power distribution.    
                - 'weibull': Uses Weibull distribution.    
  
          
        only_tail: (int)  
            Only can take 1 or 0 values:  
                - 1: The function will return only the tail factor estimated.    
                - 0: The function will return the tail factor as well as the rest of factors adjusted to the selected distribution.  
  
        num_factors: (int)  
            Number of tail_factors to add after Development Factors. Set None as default.  
        """
        tail_f, cum_tail_f, rsq_tail_f, rsq_adj_tail_f = tailf.summary_tail_f(self.df, distribution, only_tail, num_factors)
        return rsq_tail_f
    
    # Get Cumulative Tail Factors:
    def rsq_adj_tailf(self, distribution, only_tail = 1, num_factors = 5):
        """
        Calculates the R Squared Adjusted of tail factors according data included.    
  
        Parameters  
        ----------  
        distribution: (str)  
            Distribution to use in tail factor calculation:    
                - 'all': Shows a summary of the all possible estimations.    
                - 'exp': Uses exponential distribution.    
                - 'inv_power': Uses inverse power distribution.    
                - 'power': Uses power distribution.    
                - 'weibull': Uses Weibull distribution.    
  
          
        only_tail: (int)  
            Only can take 1 or 0 values:  
                - 1: The function will return only the tail factor estimated.    
                - 0: The function will return the tail factor as well as the rest of factors adjusted to the selected distribution.  
  
        num_factors: (int)  
            Number of tail_factors to add after Development Factors. Set None as default.  
        """
        tail_f, cum_tail_f, rsq_tail_f, rsq_adj_tail_f = tailf.summary_tail_f(self.df, distribution, only_tail, num_factors)
        return rsq_adj_tail_f

    
    # Graph Tail Factors:
    def graph_tail_f(self, distribution, num_factors=5):
        """
        Estimates the tail factors according to a distribution given.  
  
        Parameters  
        ----------  
        distribution: (str)  
            Distribution to use in tail factor calculation:    
                - 'all': Shows a summary of the all possible estimations.    
                - 'exp': Uses exponential distribution.    
                - 'inv_power': Uses inverse power distribution.    
                - 'power': Uses power distribution.    
                - 'weibull': Uses Weibull distribution.    
  
        num_factors: (int)  
            Number of tail_factors to add after Development Factors. Set None as default.  
        """

        return tailf.graph_tail_f(self.df, distribution, num_factors)
    
    def __new__(cls, input_triangle):
        # Convierte el input a un numpy array
        obj = np.asarray(input_triangle).view(cls)
        return obj
    
    def __array_finalize__(self, obj):
        if obj is None:
            return


###################################################################
# Classes to define Projected triangles:
###################################################################


# Generic methods for Projected Triangles:

class developed_tr():

    """
    Class to include a developed Triangle.  
  
    Atributes  
    ----------  
        - diag  
        - ultimate  
        - show  
    """

    def __init__(self, developed_tr):
        self.developed_tr = pd.DataFrame(developed_tr)
    
    # Get the last diagonal:
    def diag(self):
        """
        Returns the last diagonal of the triangle (actual)
        """
        return tr.last_diag(self.developed_tr)
    
    #Get the Ultimate:
    def ultimate(self):
        """
        Returns the Ultimate of the projection.
        """
        return dt.get_ultimate(self.developed_tr)
    
    # Atributo shape para obtener las dimensiones
    @property
    def shape(self):
        return self.developed_tr.shape
    
    # Proporcionar acceso directo a iloc
    @property
    def iloc(self):
        return self.developed_tr.iloc
    
    # Método para acceder al DataFrame directamente
    def show(self):
        """
        Returns the projected triangle in dataframe format.
        """
        formatted_df = self.developed_tr.applymap(
            lambda x: "{:,.2f}".format(x) if isinstance(x, (int, float)) else x
        )
        return formatted_df
    
    # Representación personalizada
    def __repr__(self):
        return self.developed_tr
    

# Methods for Cummulative Payments Projected Triangles:

class Payments_developed_tr(developed_tr):

    """
    Class to include a developed Payment Triangle.  
  
    Atributes  
    ----------  
        - diag  
        - ultimate  
        - show  
        - ibnr  
        - reserve  
    """

    def __init__(self, developed_tr):
        self.developed_tr = developed_tr

    def __repr__(self):
        # Show the input
        return f"{self.developed_tr})"
    
    # Get the IBNR:
    def ibnr(self, case_reserves = None):
        """
        Returns the IBNR of the projected triangle:  
        IBNR = Ultimate - Diag. (Payments) - Case Reserves (Diag of Case Reserves Triangle)  
  
        Parameters  
        ----------  
        case_reserves: (array)  
            Case reserves in array format by Acciden Period (Diag of Case Reserves Triangle).  
        """
        if case_reserves == None:
            return print('Case Reserves needed')
            #ibnr = None
        else:
            ult = np.array(dt.get_ultimate(self.developed_tr))
            diag = np.array(tr.last_diag(self.developed_tr))
            case_reserves = np.array(case_reserves)
            ibnr = ult - diag - case_reserves
            return ibnr
    
    #Get the reserves:
    def reserve(self):
        """
        Returns the Reserve of the projected triangle:  
        Reserve = Ultimate - Diag. (Payments)  
        """
        ult = np.array(dt.get_ultimate(self.developed_tr))
        diag = np.array(tr.last_diag(self.developed_tr))
        reserves = ult - diag
        return reserves


# Methods for Incurred Cost Projected Triangles:

class Incurred_developed_tr(developed_tr):

    """
    Class to include an Incurred Cost Triangle.  
  
    Atributes  
    ----------  
        - diag  
        - ultimate  
        - show  
        - ibnr  
        - reserve  
    """

    def __init__(self, developed_tr):
        self.developed_tr = developed_tr

    def __repr__(self):
        # Show the input
        return f"{self.developed_tr})"
    
    # Get the IBNR:
    def ibnr(self):
        """
        Returns the IBNR of the projected triangle:  
        IBNR = Ultimate - Diag. (Incurred Cost)  
        """
        ult = np.array(dt.get_ultimate(self.developed_tr))
        diag = np.array(tr.last_diag(self.developed_tr))
        ibnr = ult - diag
        return ibnr

    #Get the reserves:
    def reserve(self, case_reserves = None, payments = None):
        """
        Returns the Reserves of the projected triangle:  
        Reserve = Ultimate - Diag. (Incurred Cost) - Case Reserves  
        or  
        Reserve = Ultimate - Payments  
  
        Parameters: At least one of the two parameters needed.  
        ----------  
        case_reserves: (array)  
            Case reserves in array format by Acciden Period (Diag of Case Reserves Triangle).  
        payments: (array)  
            Payments in array format by Acciden Period (Diag of CumPayments Triangle).  
        """
        if case_reserves == None and payments == None:
            return print('Case Reserves or payments needed')
            #reserves = None
        elif case_reserves == None:
            ult = np.array(dt.get_ultimate(self.developed_tr))
            diag = np.array(tr.last_diag(self.developed_tr))
            payments = np.array(payments)
            reserves = ult - payments
            return reserves
        else:
            ult = np.array(dt.get_ultimate(self.developed_tr))
            diag = np.array(tr.last_diag(self.developed_tr))
            case_reserves = np.array(case_reserves)
            reserves = ult - diag + case_reserves
            return reserves


    



















