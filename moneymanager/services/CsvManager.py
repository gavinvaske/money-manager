import pandas as pd
import glob
import os
from os import path
import re


class CsvManager:
    @staticmethod
    def preprocess_csv_files(directory):
        files_names = [f for f in os.listdir(directory) if path.isfile(path.join(directory, f))]

        for file_name in files_names:
            file_path = path.join(directory, file_name)
            csv = pd.read_csv(file_path)
            csv = CsvManager.convert_column_names(csv)
            csv = CsvManager.add_source_column(csv, re.sub('\.csv$', '', file_name))
            csv.to_csv(file_path, index=None)

    @staticmethod
    def convert_column_names(csv, to_upper=True):
        if to_upper:
            csv = csv.rename(str.upper, axis='columns')
        else:
            csv = csv.rename(str.lower, axis='columns')
        return csv

    @staticmethod
    def add_source_column(csv, file_name, src_col_name='SOURCE'):
        csv[src_col_name] = file_name
        return csv


    @staticmethod
    def merge_csv_files(directory, dtypes):
        file_names = glob.glob(directory + '/*.csv')
        dataframes = []

        for file_name in file_names:
            csv = pd.read_csv(file_name, dtype=dtypes)
            dataframes.append(csv)

        return pd.concat(dataframes, axis=0, ignore_index=True)

    @staticmethod
    def generate_monthly_data(csv, directory, date_col_name='DATE'):
        col_month_year = 'month_year'
        csv[col_month_year] = csv[date_col_name].dt.to_period('M')
        csv_grouped = csv.groupby(col_month_year)

        for group_name, df_group in csv_grouped:
            df_group = df_group.drop(columns=[col_month_year])
            file_path = path.join(directory, str(group_name) + '.csv')
            df_group.to_csv(file_path, index=None)



