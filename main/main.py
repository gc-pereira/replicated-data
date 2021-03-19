import glob
from save_in_database import SaveDatabase
from export_to_folder import export_file
import pandas as pd

sales_folder = '~/Desktop/Vendas/'
export_folder = '''
                    ~/Desktop/'Destino Vendas'/
                '''

def main(event, context):
    # Open CSV and get a newest file in folder
    list_of_files = glob.glob(sales_folder) # * means all if need specific format then *.csv
    for i in list_of_files:
        df = pd.read_csv(i)
        save = SaveDatabase('vendas', df)
        save.save_in_table()
        
        export_file(i, sales_folder, export_folder)   