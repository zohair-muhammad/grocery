from cProfile import label
from tracemalloc import Frame
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
        self.selected_product = StringVar()

        self.frames = {}
        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")



        self.show_frame("StartPage")

    def show_frame(self, page_name, name=""):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()



class StartPage(tk.Frame):
    # Start page that directs user to one of three main pages
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Select a region", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        region = ttk.Combobox(self, width=27, textvariable= controller.selected_region, state='readonly')

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

        #sets the default region to Canada
        region.current(0)


        '''
        def on_region_select(event):
            print(region.get())
        

        region.bind("<<ComboboxSelected>>", on_region_select)
        '''
        region.pack()

        label2 = tk.Label(self, text="Select a product", font=controller.title_font)
        label2.pack(side="top", fill="x", pady=10)

        product = ttk.Combobox(self, width=27, textvariable=controller.selected_product, state='readonly')

        product['values'] = ('Milk, 1 litre',
                             'Milk, 2 litres',
                             'Milk, 4 litres',
                             'Eggs, 1 dozen',
                             'Butter, 454 grams',
                             'Apples, per kilogram',
                             'Potatoes, 4.54 kilograms',
                             'White bread, 675 grams',
                             'White rice, 2 kilograms',
                             'Baby food, 128 millilitres',
                             'Ground beef, per kilogram')

        # sets the default product to Milk, 1 litre
        product.current(0)
        product.pack()

        sbutton = tk.Button(self, text="Submit",command=lambda:controller.show_frame("PageOne"))

        sbutton.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller








if __name__ == '__main__':
    app = SampleApp()
    app.mainloop()




