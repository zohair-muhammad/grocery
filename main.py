from zipfile import ZipFile
import stats_can
import pandas as pd
from pandas.core.dtypes.common import INT64_DTYPE
from py3_wget import download_file
import numpy as np
import tkinter as tk
from tkinter import ttk, StringVar
from tkinter import font as tkfont
import os
from pathlib import Path



selected_product = ''

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


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.minsize(500,500)
        self.title("Grocery Price Tracker")

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.selected_region = StringVar()
        frame = StartPage(parent=container, controller=self)
        self.frames = {"StartPage": frame}
        frame.grid(row=0, column=0, sticky="nsew")



        self.show_frame("StartPage")

    def show_frame(self, page_name, name=""):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def get_region(self):
        return self.selected_region


class StartPage(tk.Frame):
    # Start page that directs user to one of three main pages
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Select a region", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        region = ttk.Combobox(self, width=27, textvariable= controller.get_region(), state='readonly')

        #Adding combobox drop down list
        region['values'] = ('Canada',
                                  'Newfoundland and Labrador',
                                  'Prince Edward Island',
                                  'Nova Scotia',
                                  'New Brunswick',
                                  'Quebec',
                                  'Ontario',
                                  'Manitoba',
                                  'Saskatchewan',
                                  'Alberta',
                                  'British Columbia')
        region.current(0)
        region.pack()


if __name__ == '__main__':
    app = SampleApp()
    app.mainloop()




