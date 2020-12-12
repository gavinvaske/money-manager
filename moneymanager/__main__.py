import pandas as pd
import os
from moneymanager.services.CsvManager import CsvManager
from moneymanager.services.PlotManager import PlotManager

GENERATE_MONTHLY_REPORT = True

if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    input_directory = os.path.join(ROOT_DIR, os.getenv("INPUT_DIRECTORY"))
    output_directory = os.path.join(ROOT_DIR, os.getenv("OUTPUT_DIRECTORY"))
    dtypes = {
                'DATE': 'object',
                'DESCRIPTION': 'object',
                'AMOUNT': 'float64',
                'CATEGORY': 'object',
                'SOURCE': 'object'
    }
    CsvManager.preprocess_csv_files(input_directory)
    transactions = CsvManager.merge_csv_files(input_directory, dtypes)

    if (len(transactions) == 0):
        raise RuntimeError('No transactions found.')

    transactions['DATE'] = pd.to_datetime(transactions['DATE'])
    transactions = transactions.sort_values(by=['DATE'])

    start_date = CsvManager.get_start_of_data(transactions).strftime(os.getenv("DATE_FORMAT"))
    end_date = CsvManager.get_end_of_data(transactions).strftime(os.getenv("DATE_FORMAT"))
    file_name = 'transactions' + '_' + start_date + '_' + end_date + '.csv'
    transactions.to_csv(os.path.join(output_directory, file_name), index=None)

    if GENERATE_MONTHLY_REPORT:
        CsvManager.generate_monthly_spending_reports(transactions, output_directory)
        PlotManager.generate_monthly_spending_graphs(output_directory)




