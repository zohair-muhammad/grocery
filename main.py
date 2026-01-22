from zipfile import ZipFile

import stats_can
import pandas as pd
from py3_wget import download_file

'''Uses stats_can to get data on retail prices of specific goods, located in a zipfile 
containing a csv file and metadata'''
grocery_table = stats_can.sc.get_full_table_download("18-10-0245-01")

#Uses py3_wget to overwrite data.zip
download_file(grocery_table,overwrite=True)

with ZipFile("data.zip", 'r') as z:
    with z.open(z.namelist()[0]) as x:
        df = pd.read_csv(x)

print(df.head())





