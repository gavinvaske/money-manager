import matplotlib.pyplot as plt
import pandas as pd
from os import path


class PlotManager:

    @staticmethod
    def generate_monthly_spending_graphs(directory):
        file_path = path.join(directory, 'spending_by_category' + '.csv')
        monthly_spending_csv = pd.read_csv(file_path)

        for index, row in monthly_spending_csv.iterrows():
            date = row[0]
            month = pd.to_datetime(date).month_name()
            year = str(pd.to_datetime(date).year)
            spending_categories = []
            spending_amounts = []
            bar_colors = []

            for key in row.keys():
                if key is not row.keys()[0]:
                    spending_categories.append(key)
                    spending_amount = row[key]
                    spending_amounts.append(spending_amount)
                    if spending_amount < 0:
                        bar_colors.append('#EB1229')    # red
                    else:
                        bar_colors.append('#00873C')    # green

            plt.figure(num=None, figsize=(17, 11), dpi=100, facecolor='w', edgecolor='k')
            plt.barh(spending_categories, spending_amounts, color=bar_colors)
            plt.xlabel("Amount ($)", fontweight='bold', fontsize=14)
            plt.ylabel("Spending Categories", fontweight='bold', fontsize=14)
            plt.title("Spending for " + month + ' ' + year, fontweight='bold', fontsize=16)
            plt.grid(linestyle='-', linewidth=.5)
            for file_format in ['.eps', '.jpeg', '.png']:
                file_name = year + '_' + month + '_' + 'spending_chart' + file_format
                graph_file_name = path.join(directory, file_name)
                plt.savefig(graph_file_name)
            plt.close()