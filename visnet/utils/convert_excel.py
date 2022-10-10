# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 20:46:43 2022

@author: Tyler
"""
import os
import pandas as pd


def convert_excel(model, file, data_type, element_index, value_index):
    """Converts an excel file into the correct dictionary structure needed to
    be used with drawing functions.
    Arguments:
    model: Takes dictionary. Uses input file name to give each image a unique
    name.
    file: Takes string. Location in Directory where excel file is located.
    data_type: Takes string. Type of data that is being extracted. Unique data
    is data that is seperated into groups such as pressure groups. Discrete
    data is numerical and is"""

    if data_type == "unique":
        element_list = {}
        dirname = os.getcwd()
        dataFile = os.path.join(dirname, file)

        df = pd.read_excel(dataFile, dtype=str)
        bins = sorted(pd.unique(df.iloc[:, value_index]))

        for binName in bins:

            element_list[binName] = {}
        for node, data in zip(
            df.iloc[:, element_index].dropna(), df.iloc[:, value_index].dropna()
        ):

            element_list[data][node] = model["G_pipe_name_list"].index(node)
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
