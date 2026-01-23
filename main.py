from zipfile import ZipFile

import numpy
import stats_can
import pandas as pd
from pandas.core.dtypes.common import INT64_DTYPE
from py3_wget import download_file
import numpy as np

'''Uses stats_can to get data on retail prices of specific goods, located in a zipfile 
containing a csv file and metadata'''
grocery_table = stats_can.sc.get_full_table_download("18-10-0245-01")

#Uses py3_wget to overwrite data.zip, overwrites file of exists.
download_file(grocery_table,overwrite=True, output_path="data.zip")

#Reads the first file in data.zip to a pandas dataframe, ignoring the metadata file in the folder.
with ZipFile("data.zip", 'r') as z:
    with z.open(z.namelist()[0]) as x:
        df = pd.read_csv(x,dtype={"REF_Date":"string","GEO":"string","DGUID":"string","Products":"string","UOM":"string",
                                  "UOM_ID":int,"SCALAR_FACTOR":"string","SCALAR_ID":int,"VECTOR":"string",
                                  "COORDINATE":float,"VALUE":float,"STATUS":"string","SYMBOL":"string","TERMINATED":"string",
                                  "DECIMALS":int})







