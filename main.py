from tkinter import ttk
from tkinter import *
import sqlite3 as sql
import pandas as pd
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
class Klientai(Base):
    __tablename__ = 'klientai'
    
    id = Column(Integer, primary_key=True)
    entry = Column(String)
    dropdown_ug = Column(String)
    dropdown_LAZER = Column(String)
    dropdown_MASAGE = Column(String)


engine = create_engine('sqlite:///client_register.db')  

def register(engine):
    engine=engine  
    Base.metadata.create_all(engine)  
    
    Session = sessionmaker(bind=engine)
    session = Session() 
    

    new_client = Klientai(entry=Entry_for_name.get(),
                          dropdown_ug=dropdown_UG.get(),
                          dropdown_LAZER = dropdown_LAZER.get(),
                          dropdown_MASAGE = dropdown_MASAGE.get())
    session.add(new_client)
    
    session.commit() 
    session.close() 

def get_table_as_dataframe(table_name, connection_string):
    engine = create_engine(connection_string)
    with engine.connect() as connection:
        df = pd.read_sql_table(table_name, connection)
    return df

df = get_table_as_dataframe('klientai', 'sqlite:///client_register.db')

root = Tk()
root.title("Kazkokios klinikos registracijos ir paslaugų aplikacija")
root.geometry('650x615')
root.resizable(True, True)

notebook = ttk.Notebook(root)  # Sukurkite notebook'ą čia

tree_frame = ttk.Frame(notebook)
tree_frame.pack(fill='both', expand=True)
tree = ttk.Treeview(tree_frame)
tree.pack(fill='both', expand=True)
tree["columns"]=("id","entry","dropdown_ug","dropdown_LAZER", "dropdown_MASAGE")

tree.column("id", width=100)
tree.column("entry", width=100)
tree.column("dropdown_ug", width=100)
tree.column("dropdown_LAZER", width=100)
tree.column("dropdown_MASAGE", width=100)

tree.heading("id", text="Stulpelis 0")
tree.heading("entry", text="Stulpelis 1")
tree.heading("dropdown_ug", text="Stulpelis 2")
tree.heading("dropdown_LAZER", text="Stulpelis 3")
tree.heading("dropdown_MASAGE", text="Stulpelis 3")

records = df.to_records(index=False)
final_records = list(records)
count = 0
for row in final_records:
    list_of_row = list(row)
    tree.insert(parent='', index='end', iid=count, text='', values=list_of_row, tags=('evenrow'))
    count += 1  # Padidinkite count reikšmę kiekvieno įrašo įterpimo metu

main_page = ttk.Frame(notebook)
notebook.add(main_page, text='Paciento registravimas paslaugai')

frame_for_name = Frame(main_page)
frame_for_name.grid(row=1, column=1, padx=10, pady=5, sticky=NE)  

frame_for_name_entry = LabelFrame(frame_for_name, text="Iveskite paciento vardą")
frame_for_name_entry.grid(row=0, column=0, padx=3) 

Entry_for_name = Entry(frame_for_name_entry)
Entry_for_name.grid(row=0, column=0, padx=4, pady=2)

frame_for_selections = LabelFrame(main_page, text="Pasirinkite paslaugas")
frame_for_selections.grid(row=2, column=1, padx=3, pady=3)

dropdown_UG = ttk.Combobox(frame_for_selections, values=["","Vienas", "Du", "Trys", "Keturi", "Penki"])
dropdown_UG.grid(row=0, column=0, padx=3, pady=3)  

dropdown_LAZER = ttk.Combobox(frame_for_selections, values=["","Vienas", "Du", "Trys", "Keturi", "Penki"])
dropdown_LAZER.grid(row=1, column=0, padx=3, pady=3)  

dropdown_MASAGE = ttk.Combobox(frame_for_selections, values=["","Vienas", "Du", "Trys", "Keturi", "Penki"])
dropdown_MASAGE.grid(row=2, column=0, padx=3, pady=3)  

frame_for_buttons = LabelFrame(main_page)
frame_for_buttons.grid(row=3, column=1, padx=3, pady=3)

registry_button = Button(frame_for_buttons, text="Registruoti", command=register)
registry_button.grid(row=0, column=0, padx=3, pady=3, sticky=NE)

notebook.pack(fill=BOTH, expand=1)
root.mainloop()
