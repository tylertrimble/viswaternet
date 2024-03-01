import os
import pandas as pd


def convert_excel(self,
                  file,
                  parameter_type,
                  data_type,
                  element_index,
                  value_index):
    model = self.model
    if data_type == "unique":
        interval_results = {}
        dirname = os.getcwd()
        dataFile = os.path.join(dirname, file)

        df = pd.read_excel(dataFile, dtype=str)
        interval_names = sorted(pd.unique(df.iloc[:, value_index]))

        for interval in interval_names:

            interval_results[interval] = {}

        if parameter_type == 'node':
            for element, data in zip(
                df.iloc[:, element_index].dropna(
                ), df.iloc[:, value_index].dropna()
            ):

                interval_results[data][element] = model["node_names"].index(
                    element)

        if parameter_type == 'link':
            for element, data in zip(
                    df.iloc[:, element_index].dropna(),
                    df.iloc[:, value_index].dropna()):
                interval_results[data][element] = \
                    model["G_pipe_name_list"].index(element)

        return interval_results, interval_names
    if data_type == "continuous" or "discrete":
        dirname = os.getcwd()
        dataFile = os.path.join(dirname, file)

        df = pd.read_excel(dataFile)
        element_list = df.iloc[:, element_index]
        results = df.iloc[:, value_index]
        data = {}
        data["element_list"] = element_list.tolist()
        data["results"] = results.tolist()
        return data
