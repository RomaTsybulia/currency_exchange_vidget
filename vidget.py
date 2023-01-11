from tkinter import *
from tkinter import ttk

import parse


currencies = parse.get_all_currencies()

ct = Tk()
ct.title("Currency rate to the UAH")
ct.geometry("400x700")

table_frame = Frame(ct)
table_frame.pack()
table_frame.grid()

currency_table = ttk.Treeview(table_frame, height=len(currencies), )
currency_table["columns"] = ("currency", "number_of_units", "value")

currency_table.column("#0", width=0,  stretch=NO)
currency_table.column("currency", anchor=W, width=200)
currency_table.column("number_of_units", anchor=CENTER, width=100)
currency_table.column("value", anchor=W, width=80)

currency_table.heading("#0", text="", anchor=W)
currency_table.heading("currency", text="Currency", anchor=W)
currency_table.heading("number_of_units", text="Number of units", anchor=CENTER)
currency_table.heading("value", text="Value", anchor=W)

for index, value in enumerate(currencies):
    currency_table.insert(
        parent="",
        index='end',
        iid=f"{index}",
        text="",
        values=(value.name, "1", str(value.official_exchange_rate) + " UAH")
    )
currency_table.pack()
ct.mainloop()
