"""
The viswaternet.utils.convert_excel converts excel data to a format usable by
viswaternet.
"""
import os
import pandas as pd


def convert_excel(self, file, parameter_type, data_type, element_index, value_index):
    """Converts an excel file into the correct dictionary structure needed to
    be used with viswaternet functions.
    
    Arguments
    ---------
    file : string
        Excel file to be formatted.
        
    data_type : string
        The type of data that the excel data is (Unique, continuous, or discrete.)
        
    element_index : int
        The excel column that contains element names. Column A in excel is
        considered the 0th column for use with viswaternet.
        
    value_index : int
        The excel column that contains element data. Column A in excel is 
        considered the 0th column for use with viswaternet.
    """
    model=self.model
    if data_type == "unique":
        element_list = {}
        dirname = os.getcwd()
        dataFile = os.path.join(dirname, file)

        df = pd.read_excel(dataFile, dtype=str)
        bins = sorted(pd.unique(df.iloc[:, value_index]))

        for binName in bins:

            element_list[binName] = {}
        
        if parameter_type=='node':
            for element, data in zip(
                df.iloc[:, element_index].dropna(), df.iloc[:, value_index].dropna()
            ):
    
                element_list[data][element] = model["node_names"].index(element)
                
        if parameter_type=='link':
            for element, data in zip(
                df.iloc[:, element_index].dropna(), df.iloc[:, value_index].dropna()
            ):
    
                element_list[data][element] = model["G_pipe_name_list"].index(element)
                
        return element_list, bins
    if data_type == "continuous" or "discrete":
        dirname = os.getcwd()
        dataFile = os.path.join(dirname, file)

        df = pd.read_excel(dataFile)
        element_list = pd.Series(
            data=df.iloc[:, value_index].values, index=df.iloc[:, element_index].values
        )
        data = {}
        data["element_list"] = element_list
        data["index"] = list(str(i) for i in list(element_list.index))
        return data
