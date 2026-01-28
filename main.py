from zipfile import ZipFile
import stats_can
import pandas as pd
from pandas.core.dtypes.common import INT64_DTYPE
from py3_wget import download_file
import numpy as np
from tkinter import *
import os
from pathlib import Path

#Only download data if it doesnt exist in current directory.
data_path = Path(os.getcwd() + '/data.zip')
if not data_path.is_file():
    '''Uses stats_can to get data on retail prices of specific goods, located in a zipfile 
    containing a csv file and metadata'''
    grocery_table = stats_can.sc.get_full_table_download("18-10-0245-01")
    download_file(grocery_table, output_path="data.zip")


#Reads the first file in data.zip to a pandas dataframe, ignoring the metadata file in the folder.
with ZipFile("data.zip", 'r') as z:
    with z.open(z.namelist()[0]) as x:
        df = pd.read_csv(x,dtype={"REF_Date":"string","GEO":"string","DGUID":"string","Products":"string","UOM":"string",
                                  "UOM_ID":int,"SCALAR_FACTOR":"string","SCALAR_ID":int,"VECTOR":"string",
                                  "COORDINATE":float,"VALUE":float,"STATUS":"string","SYMBOL":"string","TERMINATED":"string",
                                  "DECIMALS":int})

#milk_prices = df.loc[(df["GEO"] == 'Ontario') & (df["Products"] == "Milk, 4 litres")]
#print(milk_prices.iloc[0]["VALUE"])
# Python tkinter hello world program


root = Tk()
a = Label(root, text ="Canadian Grocery Price Tracker")
a.pack()

root.mainloop()




