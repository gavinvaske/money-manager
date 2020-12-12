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
            column_category = 'CATEGORY'

            if column_category not in csv:
                csv['CATEGORY'] = 'UNCATEGORIZED'

            csv['CATEGORY'] = csv['CATEGORY'].fillna('UNCATEGORIZED').str.upper().str.strip()
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
        if src_col_name not in csv:
            csv[src_col_name] = file_name
        return csv

    @staticmethod
    def merge_csv_files(directory, dtypes):
        file_names = glob.glob(directory + '/*.csv')
        dataframes = []

        for file_name in file_names:
            csv = pd.read_csv(file_name, dtype=dtypes)
            dataframes.append(csv)

        if (len(dataframes) == 0):
            return []
        return pd.concat(dataframes, axis=0, ignore_index=True)

    @staticmethod
    def generate_monthly_spending_reports(csv, directory, date_col_name='DATE', frequency='M'):
        """
        :param csv: pandas dataframe holding transactional data
        :param directory: path to folder that will hold the generated files
        :param frequency: a panda offset string (see https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases)
        :param date_col_name: name of the date column within the csv param
        :return: None
        """
        period = 'period'
        csv[period] = csv[date_col_name].dt.to_period(frequency)
        csv_grouped = csv.groupby(period)
        spending_by_category_list = []
        unique_categories = csv['CATEGORY'].unique()

        for group_name, group in csv_grouped:
            spending_dict = CsvManager.compute_spending_by_category(group, unique_categories)
            spending_by_category_list.append(pd.Series(spending_dict, index=unique_categories, name=group_name))
            group = group.drop(columns=[period])
            file_path = path.join(directory, str(group_name) + '.csv')
            group.to_csv(file_path, index=None)

        spending_by_category = pd.DataFrame(spending_by_category_list)
        spending_by_category['NET CHANGE'] = round(spending_by_category.sum(axis=1), 2)
        file_path = path.join(directory, 'spending_by_category' + '.csv')
        spending_by_category.to_csv(file_path)

    @staticmethod
    def compute_spending_by_category(transactions, expense_categories):
        spending_by_category = {}

        for category in expense_categories:
            spending_by_category[category] = 0

        grouped_transactions = transactions.groupby('CATEGORY')

        for group_name, group in grouped_transactions:
            spending = round(group['AMOUNT'].sum(), 2)
            spending_by_category[group_name] = spending
        return spending_by_category

    @staticmethod
    def get_start_of_data(transactions):
        return transactions['DATE'].iloc[0]

    @staticmethod
    def get_end_of_data(transactions):
        return transactions['DATE'].iloc[-1]








