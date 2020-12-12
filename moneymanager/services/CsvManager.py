import pandas as pd
import glob
import os
from os import path
import re


class CsvManager:
    @staticmethod
    def validate_columns(csv_columns, expected_csv_columns):
        return True

    @staticmethod
    def get_transaction_data(directory, dtypes):
        files_names = [f for f in os.listdir(directory) if path.isfile(path.join(directory, f))]

        for file_name in files_names:
            file_path = path.join(directory, file_name)
            csv = pd.read_csv(file_path)
            csv = CsvManager.convert_column_names(csv)
            csv = CsvManager.add_source_column(csv, re.sub('\.csv$', '', file_name))
            column_category = os.getenv("CATEGORY_COLUMN")

            if column_category not in csv:
                csv[column_category] = 'UNCATEGORIZED'

            csv[column_category] = csv[column_category].fillna('UNCATEGORIZED').str.upper().str.strip()
        return CsvManager.merge_csv_files(directory, dtypes)

    @staticmethod
    def convert_column_names(csv, to_upper=True):
        if to_upper:
            csv = csv.rename(str.upper, axis='columns')
        else:
            csv = csv.rename(str.lower, axis='columns')
        return csv

    @staticmethod
    def add_source_column(csv, file_name):
        source_column = os.getenv("SOURCE_COLUMN")

        if source_column not in csv:
            csv[source_column] = file_name
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
    def generate_monthly_spending_reports(csv, directory, frequency='M'):
        """
        :param csv: pandas dataframe holding transactional data
        :param directory: path to folder that will hold the generated files
        :param frequency: a panda offset string (see https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases)
        :return: None
        """
        period = 'period'
        csv[period] = csv[os.getenv("DATE_COLUMN")].dt.to_period(frequency)
        csv_grouped = csv.groupby(period)
        spending_by_category_list = []
        unique_categories = csv[os.getenv("CATEGORY_COLUMN")].unique()

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

        grouped_transactions = transactions.groupby(os.getenv("CATEGORY_COLUMN"))

        for group_name, group in grouped_transactions:
            spending = round(group[os.getenv("AMOUNT_COLUMN")].sum(), 2)
            spending_by_category[group_name] = spending
        return spending_by_category

    @staticmethod
    def get_start_of_data(transactions):
        return transactions[os.getenv("DATE_COLUMN")].iloc[0]

    @staticmethod
    def get_end_of_data(transactions):
        return transactions[os.getenv("DATE_COLUMN")].iloc[-1]








