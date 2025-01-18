from termcolor import colored
import datetime
from tkinter import *
import customtkinter as ctk
import mysql.connector

# MYSQL FUNCTIONS
# if not exists create the database to store tables
def create_db():
    db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    )
    cursor=db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS accounting_diary;")
    db.commit()
    print(colored("TEST 1", "yellow"),":",colored("PASSED", "green"),colored("\nDatabase created:", "green"),db)

create_db()

# tries database function
try:
    db=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="accounting_diary"
    )
    cursor=db.cursor()
    print(colored("TEST 2", "yellow"),":",colored("PASSED", "green"),colored("\nDatabase created:", "green"),db)
except:
    print(colored("TEST 2", "yellow"),":",colored("ERROR", "red"))


table=str()
lines=str()


def get_lines(self):
    global lines
    STRINGVAR_lines.get()
    if STRINGVAR_lines.get()=="all lines":
        cursor.execute(f"SELECT id")
        print(lines)
    elif STRINGVAR_lines.get()=="20 lines":
        lines=20
        print(lines)
    elif STRINGVAR_lines.get()=="100 lines":
        lines=100
        print(lines)
    elif STRINGVAR_lines.get()=="200 lines":
        lines=200
        print(lines)
    open_table()

# WIDGET FUNCTIONS

# identifies
def table_option(self):
    option_table = STRINGVAR_table_option.get()
    if option_table=="SELECT TABLE":
        try:
            select_table()
            print(colored("TEST 3.1", "yellow"),":",colored("PASSED | buttom select table work", "green"))
        except:
            print(colored("TEST 3.1", "yellow"),":",colored("ERROR | button select table NOT work", "red"))

    elif option_table=="NEW TABLE":
        try:
            new_table()
            print(colored("TEST 3.2", "yellow"),":",colored("PASSED | function new table work", "green"))
        except:
            print(colored("TEST 3.2", "yellow"),":",colored("ERROR | function new table NOT work", "red"))

# executes the NEW TABLE button function !!!
def new_table():
    dialog=ctk.CTkInputDialog(text="name of new table")
    dialog.geometry("%dx%d+%d+%d" % (200, 200, C.winfo_width()/2-100, C.winfo_height()/2-100))
    nt_name=dialog.get_input()

    new_table_query=f"""CREATE TABLE IF NOT EXISTS {nt_name}(
                        day date not null,
                        id_operation int not null,
                        account varchar(100) not null,
                        description varchar(500) not null,
                        debit int,
                        credit int,
                        PRIMARY KEY(id_operation) 
                    )"""
    cursor.execute(new_table_query)
    db.commit()

# executes the SELECT TABLE button finction
def select_table():
    cursor.execute("SHOW tables")
    tables=list()

    for x in cursor.fetchall():
        tables.append(x[0])

    global dialog_select_table
    dialog_select_table=ctk.CTkToplevel()
    dialog_select_table.geometry("%dx%d+%d+%d" % (250, 200, root.winfo_x() + 960/2, root.winfo_y() + 540/2))
    dialog_select_table.attributes("-topmost",1)

    conteinerframe_tables=ctk.CTkScrollableFrame(dialog_select_table)
    for x in tables:
        ctk.CTkButton(conteinerframe_tables, text=x, command=lambda: get_table(x),text_color="#333333").pack()
    conteinerframe_tables.pack(fill=BOTH, expand=True)

# gets the table user selected  
def get_table(x):
    global table
    table=x
    dialog_select_table.destroy()
    open_table()

# opens the selected table and shows it on 
def open_table():
    day_query=f"SELECT day FROM {table} ORDER BY id_operation DESC"
    id_operation_query=f"SELECT id_operation FROM {table} ORDER BY id_operation DESC"
    account_query=f"SELECT account FROM {table} ORDER BY id_operation DESC"
    description_query=f"SELECT description FROM {table} ORDER BY id_operation DESC"
    debit_query=f"SELECT debit FROM {table} ORDER BY id_operation DESC"
    credit_query=f"SELECT credit FROM {table} ORDER BY id_operation DESC"

    cursor.execute(id_operation_query)
    ids_operation=cursor.fetchmany(lines)
    
    cursor.execute(day_query)
    days=cursor.fetchmany(lines)

    cursor.execute(account_query)
    accounts=cursor.fetchmany(lines)

    cursor.execute(description_query)
    descriptions=cursor.fetchmany(lines)

    cursor.execute(debit_query)
    debits=cursor.fetchmany(lines)

    cursor.execute(credit_query)
    credits=cursor.fetchmany(lines)

    lfrows=1
    for id in ids_operation:
        Grid.rowconfigure(LF,lfrows,weight=1)
        ctk.CTkLabel(LF, text=id, text_color="#15B388", font=("Roboto", 18), fg_color="#2B292A").grid(row=lfrows, column=1,padx=1, sticky="NSEW")
        ctk.CTkLabel(LF, text=days[lfrows-1], text_color="#15B388", font=("Roboto", 18), fg_color="#2B292A").grid(row=lfrows, column=0,padx=1, sticky="NSEW")
        ctk.CTkLabel(LF, text=accounts[lfrows-1][0], text_color="#15B388", font=("Roboto", 16), fg_color="#2B292A").grid(row=lfrows, column=2,padx=1, sticky="NSEW")
        ctk.CTkLabel(LF, text=descriptions[lfrows-1][0], text_color="#15B388", font=("Roboto", 13), fg_color="#2B292A", wraplength=250).grid(row=lfrows, column=3,padx=1, sticky="NSEW")
        if isinstance(debits[lfrows-1][0], int):
            ctk.CTkLabel(LF, text=debits[lfrows-1], text_color="#15B388", font=("Roboto", 18), fg_color="#2B292A").grid(row=lfrows, column=4,padx=1, sticky="NSEW")
        else: 
            ctk.CTkLabel(LF, text="", text_color="#15B388", font=("Roboto", 18), fg_color="#2B292A").grid(row=lfrows, column=4,padx=1, sticky="NSEW")
        if isinstance(credits[lfrows-1][0], int):
            ctk.CTkLabel(LF, text=credits[lfrows-1], text_color="#15B388", font=("Roboto", 18), fg_color="#2B292A").grid(row=lfrows, column=5,padx=1, sticky="NSEW")
        else:
            ctk.CTkLabel(LF, text="", text_color="#15B388", font=("Roboto", 18), fg_color="#2B292A").grid(row=lfrows, column=5,padx=1, sticky="NSEW")

        lfrows+=1
    
def close_table():
    for widget in LF.winfo_children():
        if widget.grid_info()['row'] >0:
            widget.destroy()

# NEW OPERATION

def operation(name):        # definisce la schermanta per aggiugere/modifcare le operazioni
    if table:
        global w_NO
        w_NO=ctk.CTkToplevel()
        w_NO.geometry("%dx%d+%d+%d" % (500, 200, C.winfo_width()/4, C.winfo_height()/2))
        w_NO.attributes("-topmost",1)
        w_NO.title(name)
        w_NO.resizable(False,False)
        Grid.columnconfigure(w_NO,0,weight=1)
        Grid.rowconfigure(w_NO,0,weight=1)
        f_NW=ctk.CTkFrame(w_NO,fg_color="#2B2B2B")
        f_NW.grid(row=0,column=0,sticky="NSEW")
        Grid.columnconfigure(f_NW,0,weight=1)
        Grid.columnconfigure(f_NW,1,weight=1)
        Grid.rowconfigure(f_NW,0,weight=10)
        Grid.rowconfigure(f_NW,2,weight=1)
        q=ctk.CTkFrame(f_NW)
        q.grid(row=0, column=0, sticky="NSEW", rowspan=2)
        Grid.rowconfigure(q,0,weight=2)
        Grid.rowconfigure(q,0,weight=1)
        Grid.columnconfigure(q,0,weight=1)

        des_f=ctk.CTkFrame(f_NW, fg_color="#2B2B2B")    # frame that conteins entry of description
        des_f.grid(row=0,column=1,sticky="NSEW", padx=15)
        Grid.columnconfigure(des_f,0,weight=1)
        Grid.rowconfigure(des_f,0,weight=1)
        Grid.rowconfigure(des_f,1,weight=10)
        des_lb=ctk.CTkLabel(des_f, text="operation description", fg_color="#15B388", text_color="#333333",font=("Roboto", 18),corner_radius=1).grid(row=0, column=0, sticky="NSEW",padx=5, pady=1)
        global des_e
        des_e=ctk.CTkTextbox(des_f,text_color="#15B388",font=("Roboto", 14),corner_radius=1)
        des_e.grid(row=1, column=0,sticky="NSEW")
        
        dan_f=ctk.CTkFrame(q, fg_color="#2B2B2B")    # frame that conteins entry of Date, Account, Number
        dan_f.grid(row=0,column=0,sticky="NSEW", padx=15)
        Grid.columnconfigure(dan_f,0,weight=1)
        Grid.columnconfigure(dan_f,1,weight=2)
        Grid.rowconfigure(dan_f,0,weight=1)
        Grid.rowconfigure(dan_f,1,weight=1)
        Grid.rowconfigure(dan_f,2,weight=1)
        day=ctk.CTkLabel(dan_f, text="date", fg_color="#15B388", text_color="#333333",font=("Roboto", 14),corner_radius=1).grid(row=0,column=0, sticky="NSEW", pady=15)
        account=ctk.CTkLabel(dan_f, text="account", fg_color="#15B388", text_color="#333333",font=("Roboto", 14),corner_radius=1).grid(row=2,column=0, sticky="NSEW", pady=15)
        global day_e, account_e
        day_e=ctk.CTkTextbox(dan_f,text_color="#15B388",font=("Roboto", 14),corner_radius=1, )
        day_e.grid(row=0, column=1, sticky="NSW", pady=15)
        day_e.insert("0.0","XXXX-XX-XX")
        day_e.bind('<FocusIn>', lambda e: day_e.delete("0.0",END))

    def not_future():
        date=day_e.get('1.0', END)
        try1=date.strip("\n").split("-")
        try1=datetime.datetime(int(try1[0]),int(try1[1]),int(try1[2]))
        now=datetime.datetime.now()
        if try1>now:
            day_e.delete('1.0', END)
            day_e.insert("0.0",now.strftime("%Y-%m-%d"))
    day_e.bind('<FocusOut>', lambda e: not_future())

    account_e=ctk.CTkTextbox(dan_f,text_color="#15B388",font=("Roboto", 14),corner_radius=1)
    account_e.grid(row=2, column=1, sticky="NSW", pady=15)

    dc_f=ctk.CTkFrame(q, fg_color="#2B2B2B")
    dc_f.grid(row=1,column=0,sticky="NSEW",padx=10, pady=5)
    Grid.columnconfigure(dc_f,0,weight=1)
    Grid.columnconfigure(dc_f,1,weight=1)
    Grid.rowconfigure(dc_f,0,weight=1)
    Grid.rowconfigure(dc_f,1,weight=1)
    dr_l=ctk.CTkLabel(dc_f, text="debit", fg_color="#15B388", text_color="#333333",font=("Roboto", 14),corner_radius=1).grid(row=0, column=0,sticky="NSEW",padx=5)
    cr_l=ctk.CTkLabel(dc_f, text="credit", fg_color="#15B388", text_color="#333333",font=("Roboto", 14),corner_radius=1).grid(row=0, column=1,sticky="NSEW",padx=5)    
    global dr_e,cr_e
    dr_e=ctk.CTkTextbox(dc_f,text_color="#15B388",font=("Roboto", 14),corner_radius=1,height=25,width=150)
    dr_e.grid(row=1,column=0,sticky="NSEW",padx=5)
    cr_e=ctk.CTkTextbox(dc_f,text_color="#15B388",font=("Roboto", 14),corner_radius=1,height=25,width=150)
    cr_e.grid(row=1,column=1,sticky="NSEW",padx=5)

    send=ctk.CTkButton(f_NW,text="SEND",command=lambda:get_new_operation_data(name),font=("Roboto", 14),corner_radius=6).grid(row=1,column=1,sticky="NSEW",padx=10, pady=10)
    if name=="modify operation":
        open_settings()



# modify
def get_number_operation(name):     #crea una scheda che permette di selezionare l'operazione da modificare
    if table:
        dialog=ctk.CTkInputDialog(text="insert number of operation", title=name)
        dialog.geometry("%dx%d+%d+%d" % (200, 200, C.winfo_width()/2-100, C.winfo_height()/2-100))
        dialog.attributes("-topmost",1)
        global number
        number=dialog.get_input()
        if number:
            operation(name)

def open_settings():    # riporta i dati dell'operazione selezionata per poi poterla modificare

    date_query=f"SELECT day FROM {table} WHERE id_operation={number}"
    account_query=f"SELECT account FROM {table} WHERE id_operation={number}"
    description_query=f"SELECT description FROM {table} WHERE id_operation={number}"
    debit_query=f"SELECT debit FROM {table} WHERE id_operation={number}"
    credit_query=f"SELECT credit FROM {table} WHERE id_operation={number}"

    cursor.execute(date_query)
    day_e.delete("0.0",END)
    day_e.insert("0.0",cursor.fetchone())
    cursor.execute(account_query)
    account_e.insert("0.0",cursor.fetchone()[0])
    cursor.execute(description_query)
    des_e.insert("0.0",cursor.fetchone()[0])
    cursor.execute(debit_query)
    dr_e.insert("0.0",cursor.fetchone())
    cursor.execute(credit_query)
    cr_e.insert("0.0",cursor.fetchone())

def get_new_operation_data(name):   #prende i dati nella scheda secondaria di inserimento perazione e la scrive sul database
    ex=False

    #date
    date=day_e.get('1.0', END)
    date.strip("\n")
    try:
        try2=date.split("-")
        try2=datetime.datetime(int(try2[0]),int(try2[1]),int(try2[2]))
    except IndexError:
        ex=True
    #account
    account=account_e.get('1.0', END)
    account.strip("\n")
    #id operation
    try:
        number_query=f"SELECT id_operation FROM {table} ORDER BY id_operation DESC LIMIT 1;"
        cursor.execute(number_query)
        n=(cursor.fetchall())[0][0]+1
    except :
        n=1
    #description
    desc=des_e.get('1.0', END)
    desc.strip("\n")
    # debit 
    dr=dr_e.get('1.0', END)
    dr=dr.strip("\n")
    try:
        dr=int(dr)
    except:
        pass
    #credit
    cr=cr_e.get('1.0', END)
    cr=cr.strip("\n")
    try:
        cr=int(cr)
    except:
        pass

    if name=="new operation":
        query_cr=f"INSERT INTO {table} (day,id_operation,account,description,credit) VALUES('{date}',{n},'{account}','{desc}',{cr})"
        query_dr=f"INSERT INTO {table} (day,id_operation,account,description,debit) VALUES('{date}',{n},'{account}','{desc}',{dr})"
        
        if isinstance(cr, int) and cr>0:
            cursor.execute(query_cr)
            open_table()
            w_NO.destroy()
            db.commit()
        elif isinstance(dr, int) and dr>0:
            cursor.execute(query_dr)
            open_table()
            w_NO.destroy()
            db.commit()
        else:
            day_e.delete("0.0",END)
            day_e.insert("0.0","XXXX-XX-XX")
            des_e.delete('1.0', END)
            dr_e.delete('1.0', END)
            cr_e.delete('1.0', END)
            account_e.delete('1.0', END)

    elif name=="modify operation":
        query_cr=(f"UPDATE {table} SET day='{date}' WHERE id_operation={number}",
                  f"UPDATE {table} SET account='{account}' WHERE id_operation={number}",
                  f"UPDATE {table} SET description='{desc}' WHERE id_operation={number}",
                  f"UPDATE {table} SET credit={cr} WHERE id_operation={number}")
        query_dr=(f"UPDATE {table} SET day='{date}' WHERE id_operation={number}",
                  f"UPDATE {table} SET account='{account}' WHERE id_operation={number}",
                  f"UPDATE {table} SET description='{desc}' WHERE id_operation={number}",
                  f"UPDATE {table} SET debit={dr} WHERE id_operation={number}")

        if isinstance(cr, int) and cr>0:
            for x in query_cr:
                cursor.execute(x)
            open_table()
        elif isinstance(dr, int) and dr>0:
            for x in query_dr:
                cursor.execute(x)
            open_table()
        w_NO.destroy()
        db.commit()
    
# delete button          delete last operation
def delete():
    if table:
        query_select_delete=f"SELECT id_operation FROM {table} ORDER BY id_operation DESC LIMIT 1 "
        cursor.execute(query_select_delete)
        n_delete=cursor.fetchone()
        n_delete=n_delete[0]
        query_delete=f"DELETE FROM {table} WHERE id_operation={n_delete};"
        cursor.execute(query_delete)
        close_table()
        open_table()
        db.commit()

# RightFrame's functions of buttons 
# search operation from dates
def search_date():
    date=s_date.get()
    date.strip()
    try:
        date=date.split("-")
        date=datetime.datetime(int(date[0]),int(date[1]),int(date[2]))
        date.strftime("%Y-%m-%d")
        close_table()

        day_query=f"SELECT day FROM {table} WHERE day='{date}' ORDER BY id_operation DESC"
        id_operation_query=f"SELECT id_operation FROM {table} WHERE day='{date}' ORDER BY id_operation DESC"
        account_query=f"SELECT account FROM {table} WHERE day='{date}' ORDER BY id_operation DESC"
        description_query=f"SELECT description FROM {table} WHERE day='{date}' ORDER BY id_operation DESC"
        debit_query=f"SELECT debit FROM {table} WHERE day='{date}' ORDER BY id_operation DESC"
        credit_query=f"SELECT credit FROM {table} WHERE day='{date}' ORDER BY id_operation DESC"

        cursor.execute(id_operation_query)
        ids_operation=cursor.fetchmany(lines)
        
        cursor.execute(day_query)
        days=cursor.fetchmany(lines)

        cursor.execute(account_query)
        accounts=cursor.fetchmany(lines)

        cursor.execute(description_query)
        descriptions=cursor.fetchmany(lines)

        cursor.execute(debit_query)
        debits=cursor.fetchmany(lines)

        cursor.execute(credit_query)
        credits=cursor.fetchmany(lines)

        lfrows=1
        for id in ids_operation:
            Grid.rowconfigure(LF,lfrows,weight=1)
            ctk.CTkLabel(LF, text=id, text_color="#15B388", font=("Roboto", 18), fg_color="#2B292A").grid(row=lfrows, column=1,padx=1, sticky="NSEW")
            ctk.CTkLabel(LF, text=days[lfrows-1], text_color="#15B388", font=("Roboto", 18), fg_color="#2B292A").grid(row=lfrows, column=0,padx=1, sticky="NSEW")
            ctk.CTkLabel(LF, text=accounts[lfrows-1][0], text_color="#15B388", font=("Roboto", 16), fg_color="#2B292A").grid(row=lfrows, column=2,padx=1, sticky="NSEW")
            ctk.CTkLabel(LF, text=descriptions[lfrows-1][0], text_color="#15B388", font=("Roboto", 13), fg_color="#2B292A", wraplength=250).grid(row=lfrows, column=3,padx=1, sticky="NSEW")
            if isinstance(debits[lfrows-1][0], int):
                ctk.CTkLabel(LF, text=debits[lfrows-1], text_color="#15B388", font=("Roboto", 18), fg_color="#2B292A").grid(row=lfrows, column=4,padx=1, sticky="NSEW")
            else: 
                ctk.CTkLabel(LF, text="", text_color="#15B388", font=("Roboto", 18), fg_color="#2B292A").grid(row=lfrows, column=4,padx=1, sticky="NSEW")
            if isinstance(credits[lfrows-1][0], int):
                ctk.CTkLabel(LF, text=credits[lfrows-1], text_color="#15B388", font=("Roboto", 18), fg_color="#2B292A").grid(row=lfrows, column=5,padx=1, sticky="NSEW")
            else:
                ctk.CTkLabel(LF, text="", text_color="#15B388", font=("Roboto", 18), fg_color="#2B292A").grid(row=lfrows, column=5,padx=1, sticky="NSEW")

            lfrows+=1

    except ValueError:
        DATE.delete(0,END)
        DATE.insert(0, "ERROR")
        DATE.after(1000, lambda: DATE.delete(0,END))


def search_account():
    account=s_account.get()
    account.strip()

    close_table()

    day_query=f"SELECT day FROM {table} WHERE account like '%{account}%'"
    id_operation_query=f"SELECT id_operation FROM {table} WHERE account like '%{account}%'"
    account_query=f"SELECT account FROM {table} WHERE account like '%{account}%'"
    description_query=f"SELECT description FROM {table} WHERE account like '%{account}%'"
    debit_query=f"SELECT debit FROM {table} WHERE account like '%{account}%'"
    credit_query=f"SELECT credit FROM {table} WHERE account like '%{account}%'"

    cursor.execute(id_operation_query)
    ids_operation=cursor.fetchmany(lines)
    print(day_query)
    
    cursor.execute(day_query)
    days=cursor.fetchmany(lines)

    cursor.execute(account_query)
    accounts=cursor.fetchmany(lines)

    cursor.execute(description_query)
    descriptions=cursor.fetchmany(lines)

    cursor.execute(debit_query)
    debits=cursor.fetchmany(lines)

    cursor.execute(credit_query)
    credits=cursor.fetchmany(lines)

    lfrows=1
    for id in ids_operation:
        Grid.rowconfigure(LF,lfrows,weight=1)
        ctk.CTkLabel(LF, text=id, text_color="#15B388", font=("Roboto", 18), fg_color="#2B292A").grid(row=lfrows, column=1,padx=1, sticky="NSEW")
        ctk.CTkLabel(LF, text=days[lfrows-1], text_color="#15B388", font=("Roboto", 18), fg_color="#2B292A").grid(row=lfrows, column=0,padx=1, sticky="NSEW")
        ctk.CTkLabel(LF, text=accounts[lfrows-1][0], text_color="#15B388", font=("Roboto", 16), fg_color="#2B292A").grid(row=lfrows, column=2,padx=1, sticky="NSEW")
        ctk.CTkLabel(LF, text=descriptions[lfrows-1][0], text_color="#15B388", font=("Roboto", 13), fg_color="#2B292A", wraplength=250).grid(row=lfrows, column=3,padx=1, sticky="NSEW")
        if isinstance(debits[lfrows-1][0], int):
            ctk.CTkLabel(LF, text=debits[lfrows-1], text_color="#15B388", font=("Roboto", 18), fg_color="#2B292A").grid(row=lfrows, column=4,padx=1, sticky="NSEW")
        else: 
            ctk.CTkLabel(LF, text="", text_color="#15B388", font=("Roboto", 18), fg_color="#2B292A").grid(row=lfrows, column=4,padx=1, sticky="NSEW")
        if isinstance(credits[lfrows-1][0], int):
            ctk.CTkLabel(LF, text=credits[lfrows-1], text_color="#15B388", font=("Roboto", 18), fg_color="#2B292A").grid(row=lfrows, column=5,padx=1, sticky="NSEW")
        else:
            ctk.CTkLabel(LF, text="", text_color="#15B388", font=("Roboto", 18), fg_color="#2B292A").grid(row=lfrows, column=5,padx=1, sticky="NSEW")

        lfrows+=1


# GRIDING FUNCTIONS

# grids hight bar widgets
def grid_widget(Frame, bool):
    x=0
    if bool==True:
        for widget in Frame.winfo_children():
            Grid.columnconfigure(Frame,x,weight=1)
            widget.grid(row=0, column=x, padx=10, pady=10, sticky="NSEW")
            x+=1
    else:
        for widget in Frame.winfo_children():
            Grid.columnconfigure(Frame,x,weight=1)
            widget.grid(row=x, column=0, padx=40, pady=15, sticky="NSEW")
            x+=1

ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("green")
root = ctk.CTk()
root.title("accounting diary")
root.geometry("960,540")
#"{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight())
root.resizable(True, True)
root.minsize(960,540)
root.lift()
Grid.columnconfigure(root,0,weight=1)
Grid.rowconfigure(root,0,weight=1)
Grid.rowconfigure(root,1,weight=100)
Grid.rowconfigure(root,2,weight=1)

HB=ctk.CTkFrame(root)                       #HightBar 
HB.grid(row=0, column=0, sticky="NSEW")
Grid.rowconfigure(HB,0,weight=0)

# Hightbar's widgets
new=ctk.CTkButton(HB, text="NEW", text_color="#333333", font=("Roboto", 18), command=lambda: operation("new operation"))
delete=ctk.CTkButton(HB, text="DELETE", text_color="#333333", font=("Roboto", 18), command=delete)
modify=ctk.CTkButton(HB, text="MODIFY", text_color="#333333", font=("Roboto", 18),command=lambda: get_number_operation("modify operation"))
STRINGVAR_lines=ctk.StringVar()
order_by=ctk.CTkOptionMenu(HB, values=["20 lines","100 lines","200 lines","all lines"],variable=STRINGVAR_lines,command=get_lines, text_color="#333333", font=("Roboto", 18))
order_by.set("LINES")
grid_widget(HB, True)

C=ctk.CTkFrame(root)                        #Center
C.grid(row=1, column=0, sticky="NSEW")
Grid.columnconfigure(C,0,weight=67)
Grid.columnconfigure(C,1,weight=1)
Grid.rowconfigure(C,0,weight=1)

LF=ctk.CTkScrollableFrame(C)                #LeftFrame
LF.grid(row=0, column=0, sticky="NSEW")
Grid.rowconfigure(LF,0,weight=1)
Grid.columnconfigure(LF,0,weight=1)
Grid.columnconfigure(LF,1,weight=1)
Grid.columnconfigure(LF,2,weight=5)
Grid.columnconfigure(LF,3,weight=10)
Grid.columnconfigure(LF,4,weight=4)
Grid.columnconfigure(LF,5,weight=4)

ctk.CTkLabel(LF, text="DATE",fg_color="#15B388",text_color="#333333", font=("Roboto", 18)).grid(row=0, column=0,padx=1, sticky="NSEW")
ctk.CTkLabel(LF, text="N.",fg_color="#15B388",text_color="#333333", font=("Roboto", 18)).grid(row=0, column=1,padx=1, sticky="NSEW")
ctk.CTkLabel(LF, text="ACCOUNT",fg_color="#15B388",text_color="#333333", font=("Roboto", 18)).grid(row=0, column=2,padx=1, sticky="NSEW")
ctk.CTkLabel(LF, text="DESCRIPTION",fg_color="#15B388",text_color="#333333", font=("Roboto", 18)).grid(row=0, column=3,padx=1, sticky="NSEW")
ctk.CTkLabel(LF, text="DEBIT",fg_color="#15B388",text_color="#333333", font=("Roboto", 18)).grid(row=0, column=4,padx=1, sticky="NSEW")
ctk.CTkLabel(LF, text="CREDIT",fg_color="#15B388",text_color="#333333", font=("Roboto", 18)).grid(row=0, column=5,padx=1, sticky="NSEW")


RF=ctk.CTkFrame(C)                          #RightFrame
RF.grid(row=0,column=1, sticky="NSEW")
Grid.columnconfigure(HB,0,weight=1)
SEARCH=ctk.CTkLabel(RF, text="SEARCH", text_color="#15B388", font=("Roboto", 30))
global B_DATE, B_ACCOUNT
s_date=ctk.StringVar()
B_DATE=ctk.CTkButton(RF, text=" date", text_color="#333333", font=("Roboto", 20), command=search_date)
DATE=ctk.CTkEntry(RF, text_color="#15B388", font=("Roboto", 18), textvariable=s_date)
s_account=ctk.StringVar()
B_ACCOUNT=ctk.CTkButton(RF, text=" account", text_color="#333333", font=("Roboto", 20), command=search_account)
ACCOUNT=ctk.CTkEntry(RF, text_color="#15B388", font=("Roboto", 18), textvariable=s_account)

grid_widget(RF, False)

LB=ctk.CTkFrame(root)                        #LowBar
LB.grid(row=2, column=0, sticky="NSEW")
Grid.rowconfigure(LB,0,weight=1)
Grid.columnconfigure(LB,0,weight=13)
Grid.columnconfigure(LB,1,weight=1)

STRINGVAR_table_option=ctk.StringVar()
TABLE=ctk.CTkOptionMenu(LB, values=["SELECT TABLE","NEW TABLE"],variable=STRINGVAR_table_option, command=table_option, text_color="#333333", font=("Roboto", 18))
TABLE.set("TABLE")
TABLE.grid(row=0, column=1, sticky="NSEW")



root.mainloop()

