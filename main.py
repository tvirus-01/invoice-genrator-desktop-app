from tkinter import *
import customtkinter
from customtkinter import *
from db import Database
from threading import Thread
from time import sleep
import pandas as pd
from script import genrate_pdf, genrate_excel
from sendEmail import send_mail
import os, shutil

db = Database("invoice.db")

error_color = "#d93025"
info_color = "#1692EC"
success_color = "#2bd12b"

def save_data():
    db = Database("invoice.db")

    if user_name.get() == '' or gbp_rate.get() == '' or smtp_server.get() == '' or smtp_port.get() == ''  or smtp_user.get() == ''  or smtp_pass.get() == ''  or smtp_sender.get() == '':
        msg_label.configure(text="!Please include all fields", text_color=error_color)
        return

    if gbp_rate.get().isdigit():
        pass
    else:
        try:
            float(gbp_rate.get())
        except:
            msg_label.configure(text="!GBP Rate is not Number", text_color=error_color)
            return

    db.insert_user_data(gbp_rate.get(), smtp_server.get(), smtp_port.get(), smtp_user.get(), smtp_sender.get(), smtp_pass.get())

    msg_label.configure(text="!Saved", text_color=success_color)

def check_user_data():
    db = Database("invoice.db")
    
    user_data = db.fetch_user_data()
    user_name.set(os.getlogin())

    if len(user_data) == 0:
        pass
    else:
        gbp_rate_entry.insert(END, user_data[0][2])
        smtp_server_entry.insert(END, user_data[0][3])
        smtp_user_entry.insert(END, user_data[0][4])
        smtp_sender_entry.insert(END, user_data[0][5])
        smtp_pass_entry.insert(END, user_data[0][6])
        smtp_port_entry.insert(END, user_data[0][7])

def browseLiftingFiles():
    filename = filedialog.askopenfilename(
            initialdir = "/",
            title = "Select a File",
            filetypes = (("Excel files","*.xlsx*"),("all files", "*.*")))
    lifting_fee_file.configure(text=filename)

def browseMasterDataFiles():
    filename = filedialog.askopenfilename(
            initialdir = "/",
            title = "Select a File",
            filetypes = (("Excel files","*.xlsx*"),("all files", "*.*")))
    master_data_file.configure(text=filename)


def update_master_data(filepath, db):    
    try:
        master_data = pd.read_excel(filepath)
        master_data = master_data.set_index("*ContactName").to_dict("index")

        for contact_name in master_data:
            db.add_master_data(contact_name, master_data[contact_name])

        sleep(1)
        return "success"
    except:
        return "failed"


def process_de_data(filepath, user_data, db):
    lifting_fee = pd.read_excel(filepath)
    
    processed_data = {}
    for index, row in lifting_fee.iterrows():
        if row['AccountName'] in processed_data:
            processed_data[row['AccountName']].append(row.to_dict())
        else:
            processed_data[row['AccountName']] = [row.to_dict()]

    for account_name in processed_data:
        total_amount = 0

        for row in processed_data[account_name]:
            total_amount += row['USD AMOUNT']

        master_data = db.fetch_master_data(account_name)
        if len(master_data) == 0:
            pass
        else:
            customer_address = master_data[0][2]
            vat_type = master_data[0][6]
            email_ids = master_data[0][3].split(";")

            create_invoice = genrate_pdf(
                account_name,
                customer_address,
                str(total_amount),
                vat_type,
                str(user_data[2])
            )

            invoice_pdf_file = create_invoice[0]
            invoice_number = create_invoice[1]

            invoice_excel_file = genrate_excel(account_name, processed_data[account_name])

            files = [f'output/{invoice_pdf_file}', f'output/{invoice_excel_file}']

            send_mail(
                send_from=user_data[5],
                send_to=email_ids,
                files=files,
                invoice_number=invoice_number,
                receiver_name=account_name,
                total_amount=total_amount,
                smtp_server=user_data[3],
                smtp_port=user_data[7],
                smtp_user=user_data[4],
                smtp_pass=user_data[6]
            )

            shutil.move(
                f'output/{invoice_pdf_file}',
                f'archive/{invoice_pdf_file}'
            )
            shutil.move(
                f'output/{invoice_excel_file}',
                f'archive/{invoice_excel_file}'
            )


def start_process():
    db = Database("invoice.db")

    user_data = db.fetch_user_data()
    if len(user_data) == 0:
        msg_start_process.configure(text="!Please fillup all data before starting process", text_color=error_color)
        return

    master_data_file_path = master_data_file.cget('text')
    lifting_fee_file_path = lifting_fee_file.cget('text')

    if lifting_fee_file_path == "":
        msg_start_process.configure(text="!Lifting Fee File is required", text_color=error_color)
        return

    if master_data_file_path != "":
        msg_start_process.configure(text="!Master Data found updating data", text_color=info_color)
        if update_master_data(master_data_file_path, db) == "failed":
            msg_start_process.configure(text="!Master Data File Invalid", text_color=error_color)
            return

    msg_start_process.configure(text="!Genrating invoices", text_color=info_color)
    process_de_data(lifting_fee_file_path, user_data[0], db)
    sleep(1)

    msg_start_process.configure(text="!Process Done", text_color=success_color)

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("1020x520")
app.title("Invoice Generator")

user_name = StringVar()
user_name_label = CTkLabel(app, text='User Name', font=('bold', 14), pady=20)
user_name_label.grid(row=0, column=0, sticky=W, padx=(10, 0))
user_name_entry = CTkEntry(app, textvariable=user_name, width= 300, state=DISABLED)
user_name_entry.grid(row=0, column=1, padx=(10, 0))

gbp_rate = StringVar()
gbp_rate_label = CTkLabel(app, text='GBP Rate', font=('bold', 14), pady=20)
gbp_rate_label.grid(row=0, column=2, sticky=W, padx=(70, 0))
gbp_rate_entry = CTkEntry(app, textvariable=gbp_rate, width= 300)
gbp_rate_entry.grid(row=0, column=3, padx=(10, 0))

smtp_server = StringVar()
smtp_server_label = CTkLabel(app, text='SMTP Server', font=('bold', 14), pady=20)
smtp_server_label.grid(row=1, column=0, sticky=W, padx=(10, 0))
smtp_server_entry = CTkEntry(app, textvariable=smtp_server, width= 300)
smtp_server_entry.grid(row=1, column=1, padx=(10, 0))

smtp_port = StringVar()
smtp_port_label = CTkLabel(app, text='SMTP Port', font=('bold', 14), pady=20)
smtp_port_label.grid(row=1, column=2, sticky=W, padx=(70, 0))
smtp_port_entry = CTkEntry(app, textvariable=smtp_port, width= 300)
smtp_port_entry.grid(row=1, column=3, padx=(10, 0))

smtp_user = StringVar()
smtp_user_label = CTkLabel(app, text='SMTP User', font=('bold', 14), pady=20)
smtp_user_label.grid(row=2, column=0, sticky=W, padx=(10, 0))
smtp_user_entry = CTkEntry(app, textvariable=smtp_user, width= 300)
smtp_user_entry.grid(row=2, column=1, padx=(10, 0))

smtp_sender = StringVar()
smtp_sender_label = CTkLabel(app, text='SMTP Sender', font=('bold', 14), pady=20)
smtp_sender_label.grid(row=2, column=2, sticky=W, padx=(70, 0))
smtp_sender_entry = CTkEntry(app, textvariable=smtp_sender, width= 300)
smtp_sender_entry.grid(row=2, column=3, padx=(10, 0))

smtp_pass = StringVar()
smtp_pass_label = CTkLabel(app, text='SMTP Pass', font=('bold', 14), pady=20)
smtp_pass_label.grid(row=3, column=2, sticky=W, padx=(70, 0))
smtp_pass_entry = CTkEntry(app, textvariable=smtp_pass, width= 300, show="*")
smtp_pass_entry.grid(row=3, column=3, padx=(10, 0))


save_btn = CTkButton(app, command=lambda: Thread(target=save_data).start(), text='Save', width=200, height=40,border_width=1, corner_radius=20, fg_color="#63B3CC", border_color="#63B3CC", hover_color="#242424", font=('Bold', 20))
save_btn.grid(row=3, column=0, padx=10, pady=20)
msg_label = CTkLabel(app, text='', font=('bold', 16))
msg_label.grid(row=3, column=1, sticky=W, padx=(70, 0))


# lifting file broswe btn
lifting_fee_file_lebel = CTkLabel(app, text='Lifting Fee File', font=('bold', 14))
lifting_fee_file_lebel.grid(row=4, column=0, sticky=W, padx=(150, 0), pady=(30, 0), columnspan=2)

browse_lifting_file = CTkButton(app, command=browseLiftingFiles, text='Browse', width=200, height=40,border_width=1, corner_radius=20, fg_color="#63B3CC", border_color="#63B3CC", hover_color="#242424", font=('Bold', 20))
browse_lifting_file.grid(row=5, column=0, padx=10, pady=10, columnspan=2)

lifting_fee_file = CTkLabel(app, text='', font=('bold', 12))
lifting_fee_file.grid(row=6, column=0, sticky=W, padx=(10, 0), pady=(5, 0), columnspan=2)


# master data file broswe btn
master_data_file_lebel = CTkLabel(app, text='Master Data File', font=('bold', 14))
master_data_file_lebel.grid(row=4, column=3, sticky=W, padx=(10, 0), pady=(30, 0))

browse_master_data_file = CTkButton(app, command=browseMasterDataFiles, text='Browse', width=200, height=40,border_width=1, corner_radius=20, fg_color="#63B3CC", border_color="#63B3CC", hover_color="#242424", font=('Bold', 20))
browse_master_data_file.grid(row=5, column=3, padx=(10, 0), pady=10, columnspan=1)

master_data_file = CTkLabel(app, text='', font=('bold', 12))
master_data_file.grid(row=6, column=3, sticky=W, padx=(10, 0), pady=(5, 0), columnspan=2)

# start process
start_btn = CTkButton(app, command=lambda: Thread(target=start_process).start(), text='Start Process', width=400, height=40,border_width=1, corner_radius=20, fg_color="#37D95B", border_color="#37D95B", hover_color="#242424", font=('Bold', 20))
start_btn.grid(row=7, column=0, padx=0, pady=20, columnspan=2)

msg_start_process = CTkLabel(app, text='', font=('bold', 16))
msg_start_process.grid(row=7, column=3, sticky=W, padx=(10, 0), columnspan=2)

check_user_data()
app.mainloop()