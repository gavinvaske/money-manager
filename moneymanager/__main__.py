import pandas as pd
import os
from moneymanager.services.CsvManager import CsvManager
from moneymanager.services.PlotManager import PlotManager

IMPORT_TRANSACTIONS = True
IMPORT_FROM_MULTIPLE_SOURCES = not IMPORT_TRANSACTIONS
GENERATE_MONTHLY_REPORT = True

if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    input_directory = os.path.join(ROOT_DIR, 'data/input_files')
    output_directory = os.path.join(ROOT_DIR, 'data/output_files')
    dtypes = {
                'DATE': 'object',
                'DESCRIPTION': 'object',
                'AMOUNT': 'float64',
                'CATEGORY': 'object',
                'SOURCE': 'object'
    }
    CsvManager.preprocess_csv_files(input_directory)
    transactions = CsvManager.merge_csv_files(input_directory, dtypes)
    transactions['DATE'] = pd.to_datetime(transactions['DATE'])
    transactions = transactions.sort_values(by=['DATE'])

    start_date = CsvManager.get_start_of_data(transactions).strftime("%m-%d-%Y")
    end_date = CsvManager.get_end_of_data(transactions).strftime("%m-%d-%Y")
    file_name = 'transactions' + '_' + start_date + '_' + end_date + '.csv'
    transactions.to_csv(os.path.join(output_directory, file_name), index=None)


    if GENERATE_MONTHLY_REPORT:
        CsvManager.generate_monthly_spending_reports(transactions, output_directory)
        PlotManager.generate_monthly_spending_graphs(output_directory)




