import pandas as pd
import os
from moneymanager.services.CsvManager import CsvManager

if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    input_directory = os.path.join(ROOT_DIR, 'data/input_files')
    output_directory = os.path.join(ROOT_DIR, 'data/output_files')
    dtypes = {
                'DATE': 'object',
                'DESCRIPTION': 'object',
                'AMOUNT': 'float64',
                'CATEGORY': 'object'
    }
    CsvManager.preprocess_csv_files(input_directory)
    transactions = CsvManager.merge_csv_files(input_directory, dtypes)
    transactions['DATE'] = pd.to_datetime(transactions['DATE'])
    transactions = transactions.sort_values(by=['DATE'])

    CsvManager.generate_monthly_data(transactions, output_directory)
    transactions.to_csv(os.path.join(output_directory, 'transactions.csv'), index=None)



