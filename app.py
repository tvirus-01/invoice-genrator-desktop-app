from tkinter import *
import customtkinter
from customtkinter import *
from db import Database
from threading import Thread
from time import sleep
import pandas as pd
from script import genrate_pdf, genrate_excel, app_dir, output_dir, archive_dir
from sendEmail import send_mail
import os, shutil, datetime
from login import generate_password_hash, set_salt
from  tkinter import ttk
from tkinter.messagebox import askokcancel, showinfo, WARNING


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        set_salt("xhsdh28sjh28wjsik983hsuj")

        self.error_color = "#d93025"
        self.info_color = "#1692EC"
        self.success_color = "#2bd12b"
        self.theme_color = "#242424"

        if os.path.isdir(app_dir) == False:          
            os.mkdir(app_dir)

        if os.path.isdir(output_dir) == False:          
            os.mkdir(output_dir)
        if os.path.isdir(archive_dir) == False:          
            os.mkdir(archive_dir)

        self.db = Database(app_dir+"/invoice.db")

        self.title("Invoice Generator")
        self.geometry("1060x520")

        customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.HomeFrame()
        self.UsersFrame()
        self.LoginFrame()
        self.AdminRegeistrationFrame()
        self.UserViewFrame()

        if self.db.is_any_user_exists() == False:
            self.user_logged_in = False

            self.select_frame_by_name("admin_reg")
        else:
            self.user_session = self.db.check_user_session()
            # print(self.user_session)

            if self.user_session == "no_session":
                self.user_logged_in = False
            else:
                self.user_logged_in = True

            if self.user_logged_in:
                self.authenticate_user()
            else:
                self.select_frame_by_name("login")

    def authenticate_user(self):                
        if self.user_session[4] == "admin":
            self.is_admin = True
        else:
            self.is_admin = False

        self.current_user_name = self.user_session[1]

        self.sideBarFrame()

        if self.is_admin:
            self.select_frame_by_name("home")
        else:
            self.select_frame_by_name("user_view")

    def sideBarFrame(self):
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_user_name = customtkinter.CTkLabel(self.navigation_frame, text=self.user_session[1], compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_user_name.grid(row=0, column=0, padx=20, pady=20)

        if self.is_admin:
            self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=lambda: self.select_frame_by_name("home"))
            self.home_button.grid(row=1, column=0, sticky="ew")

            self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Users", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=lambda: self.select_frame_by_name("users"))
            self.frame_2_button.grid(row=2, column=0, sticky="ew")
        else:
            self.user_home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=lambda: self.select_frame_by_name("user_view"))
            self.user_home_button.grid(row=1, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System",], command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=5, column=0, padx=5, pady=20, sticky="s")
        
        self.logout_btn = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Logout", fg_color="crimson", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.UserLogout)
        self.logout_btn.grid(row=6, column=0, sticky="ew")

    
    def HomeFrame(self):
        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.gbp_rate = StringVar()
        self.gbp_rate_label = CTkLabel(self.home_frame, text='GBP Rate', font=('bold', 14), pady=20)
        self.gbp_rate_label.grid(row=0, column=0, sticky=W, padx=(10, 0))
        self.gbp_rate_entry = CTkEntry(self.home_frame, textvariable=self.gbp_rate, width= 300)
        self.gbp_rate_entry.grid(row=0, column=1, padx=(10, 0))
        
        self.smtp_user = StringVar()
        self.smtp_user_label = CTkLabel(self.home_frame, text='SMTP User', font=('bold', 14), pady=20)
        self.smtp_user_label.grid(row=0, column=2, sticky=W, padx=(50, 0))
        self.smtp_user_entry = CTkEntry(self.home_frame, textvariable=self.smtp_user, width= 300)
        self.smtp_user_entry.grid(row=0, column=3, padx=(10, 20))

        self.smtp_server = StringVar()
        self.smtp_server_label = CTkLabel(self.home_frame, text='SMTP Server', font=('bold', 14), pady=20)
        self.smtp_server_label.grid(row=1, column=0, sticky=W, padx=(10, 0))
        self.smtp_server_entry = CTkEntry(self.home_frame, textvariable=self.smtp_server, width= 300)
        self.smtp_server_entry.grid(row=1, column=1, padx=(10, 0))

        self.smtp_port = StringVar()
        self.smtp_port_label = CTkLabel(self.home_frame, text='SMTP Port', font=('bold', 14), pady=20)
        self.smtp_port_label.grid(row=1, column=2, sticky=W, padx=(50, 0))
        self.smtp_port_entry = CTkEntry(self.home_frame, textvariable=self.smtp_port, width= 300)
        self.smtp_port_entry.grid(row=1, column=3, padx=(10, 20))
        
        self.smtp_pass = StringVar()
        self.smtp_pass_label = CTkLabel(self.home_frame, text='SMTP Pass', font=('bold', 14), pady=20)
        self.smtp_pass_label.grid(row=2, column=0, sticky=W, padx=(10, 0))
        self.smtp_pass_entry = CTkEntry(self.home_frame, textvariable=self.smtp_pass, width= 300, show="*")
        self.smtp_pass_entry.grid(row=2, column=1, padx=(10, 0))

        self.smtp_sender = StringVar()
        self.smtp_sender_label = CTkLabel(self.home_frame, text='SMTP Sender', font=('bold', 14), pady=20)
        self.smtp_sender_label.grid(row=2, column=2, sticky=W, padx=(50, 0))
        self.smtp_sender_entry = CTkEntry(self.home_frame, textvariable=self.smtp_sender, width= 300)
        self.smtp_sender_entry.grid(row=2, column=3, padx=(10, 20))

        self.save_btn = CTkButton(self.home_frame, command=self.save_data, text='Save', width=200, height=40,border_width=1, corner_radius=20, fg_color="#63B3CC", border_color="#63B3CC", hover_color="#242424", font=('Bold', 20))
        self.save_btn.grid(row=3, column=1, padx=30, pady=20, columnspan=1)
        self.msg_label = CTkLabel(self.home_frame, text='', font=('bold', 16))
        self.msg_label.grid(row=3, column=2, sticky=W, padx=(10, 0), columnspan=2)

        self.check_user_data()


        # master data file broswe btn
        self.master_data_file_lebel = CTkLabel(self.home_frame, text='Master Data File', font=('bold', 14))
        self.master_data_file_lebel.grid(row=4, column=1, sticky=W, padx=(80, 0), pady=(30, 0))

        self.browse_master_data_file = CTkButton(self.home_frame, command=lambda: Thread(target=self.browseMasterDataFiles).start(), text='Browse', width=200, height=40,border_width=1, corner_radius=20, fg_color="#63B3CC", border_color="#63B3CC", hover_color="#242424", font=('Bold', 20))
        self.browse_master_data_file.grid(row=5, column=1, padx=(30, 0), pady=10)

        self.master_data_file = CTkLabel(self.home_frame, text='', font=('bold', 12))
        self.master_data_file.grid(row=6, column=1, sticky=W, padx=(80, 0), pady=(5, 0), columnspan=2)

        self.master_data_msg = CTkLabel(self.home_frame, text='', font=('bold', 12))
        self.master_data_msg.grid(row=7, column=1, sticky=W, padx=(80, 0), pady=(5, 0), columnspan=2)

        # email template condition file broswe btn
        self.email_temp_con_file_lebel = CTkLabel(self.home_frame, text='Email Template Condition File', font=('bold', 14))
        self.email_temp_con_file_lebel.grid(row=4, column=2, sticky=W, padx=(130, 0), pady=(30, 0), columnspan=2)

        self.browse_email_temp_con_file = CTkButton(self.home_frame, command=lambda: Thread(target=self.browseEmailTempCon).start(), text='Browse', width=200, height=40,border_width=1, corner_radius=20, fg_color="#63B3CC", border_color="#63B3CC", hover_color="#242424", font=('Bold', 20))
        self.browse_email_temp_con_file.grid(row=5, column=2, padx=(30, 0), pady=10, columnspan=2)

        self.email_temp_con_file = CTkLabel(self.home_frame, text='', font=('bold', 12))
        self.email_temp_con_file.grid(row=6, column=2, sticky=W, padx=(130, 0), pady=(5, 0), columnspan=2)
        
        self.email_temp_con_msg = CTkLabel(self.home_frame, text='', font=('bold', 12))
        self.email_temp_con_msg.grid(row=7, column=3, sticky=W, padx=(10, 0), pady=(5, 0), columnspan=2)
    
    def save_data(self):

        if self.gbp_rate.get() == '' or self.smtp_server.get() == '' or self.smtp_port.get() == ''  or self.smtp_user.get() == ''  or self.smtp_pass.get() == ''  or self.smtp_sender.get() == '':
            self.msg_label.configure(text="!Please include all fields", text_color=self.error_color)
            return

        if self.gbp_rate.get().isdigit():
            pass
        else:
            try:
                float(self.gbp_rate.get())
            except:
                self.msg_label.configure(text="!GBP Rate is not Number", text_color=self.error_color)
                return

        self.db.insert_user_data(self.gbp_rate.get(), self.smtp_server.get(), self.smtp_port.get(), self.smtp_user.get(), self.smtp_sender.get(), self.smtp_pass.get())

        self.msg_label.configure(text="!Saved", text_color=self.success_color)
    
    def check_user_data(self):        
        user_data = self.db.fetch_user_data()

        if len(user_data) == 0:
            pass
        else:
            self.gbp_rate_entry.insert(END, user_data[0][2])
            self.smtp_server_entry.insert(END, user_data[0][3])
            self.smtp_user_entry.insert(END, user_data[0][4])
            self.smtp_sender_entry.insert(END, user_data[0][5])
            self.smtp_pass_entry.insert(END, user_data[0][6])
            self.smtp_port_entry.insert(END, user_data[0][7])
    
    def browseEmailTempCon(self):
        self.filename = filedialog.askopenfilename(
                initialdir = "/",
                title = "Select Email Template Condition File",
                filetypes = (("Excel files","*.xlsx*"),("all files", "*.*")))

        if self.filename == "":
            return

        self.email_temp_con_file.configure(text=self.filename.split("/")[-1])

        self.email_temp_con_msg.configure(text="!Updating Data...", text_color=self.info_color)
        sleep(1)
    
        email_temp_con_data = pd.read_excel(self.filename)
        try:
            email_temp_con_data = email_temp_con_data.set_index("Name").to_dict("index")
        except:
            self.email_temp_con_msg.configure(text="!Inavlid Email Template Condition File.", text_color=self.error_color)
            return

        for contact_name in email_temp_con_data:
            self.db.add_email_condition(contact_name, email_temp_con_data[contact_name]['Type'])

        self.email_temp_con_msg.configure(text="!Data Update Done", text_color=self.success_color)
    
    def browseMasterDataFiles(self):
        self.filename = filedialog.askopenfilename(
                initialdir = "/",
                title = "Select Master Data File",
                filetypes = (("Excel files","*.xlsx*"),("all files", "*.*")))
        
        if self.filename == "":
            return
        
        self.master_data_file.configure(text=self.filename.split("/")[-1])
        self.master_data_msg.configure(text="!Updating Master Data...", text_color=self.info_color)
        sleep(1)
    
        self.master_data = pd.read_excel(self.filename)
        try:
            self.master_data = self.master_data.set_index("*ContactName").to_dict("index")
        except:
            self.master_data_msg.configure(text="!Inavlid Master Data File.", text_color=self.error_color)
            return

        for contact_name in self.master_data:
            self.db.add_master_data(contact_name, self.master_data[contact_name])

        self.master_data_msg.configure(text="!Master Data Updated", text_color=self.success_color)
        sleep(3)
        self.master_data_msg.configure(text="", text_color=self.success_color)
        return


    def UserViewFrame(self):
        # create users frame
        self.user_view_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # lifting file broswe btn
        lifting_fee_file_lebel = CTkLabel(self.user_view_frame, text='Upload Lifting Fee File', font=('bold', 14))
        lifting_fee_file_lebel.grid(row=1, column=0, sticky=W, padx=(150, 0), pady=(100, 0), columnspan=1)

        browse_lifting_file = CTkButton(self.user_view_frame, command=lambda: Thread(target=self.browseLiftingFiles).start(), text='Browse', width=200, height=40,border_width=1, corner_radius=20, fg_color="#63B3CC", border_color="#63B3CC", hover_color="#242424", font=('Bold', 20))
        browse_lifting_file.grid(row=1, column=2, padx=10, pady=(100,0), columnspan=2)

        self.lifting_fee_file = CTkLabel(self.user_view_frame, text='', font=('bold', 12))
        self.lifting_fee_file.grid(row=2, column=0, sticky=W, padx=(150, 0), pady=(5, 0), columnspan=3)

        self.msg_start_process = CTkLabel(self.user_view_frame, text='', font=('bold', 16))
        self.msg_start_process.grid(row=3, column=0, sticky=W, padx=(150, 0), pady=(10, 40), columnspan=3)

        # Account list file broswe btn
        account_list_file_lebel = CTkLabel(self.user_view_frame, text='Upload Account list File', font=('bold', 14))
        account_list_file_lebel.grid(row=4, column=0, sticky=W, padx=(150, 0), pady=(0, 0), columnspan=1)

        browse_account_list_file = CTkButton(self.user_view_frame, command=lambda: Thread(target=self.browseAccountListFiles).start(), text='Browse', width=200, height=40,border_width=1, corner_radius=20, fg_color="#63B3CC", border_color="#63B3CC", hover_color="#242424", font=('Bold', 20))
        browse_account_list_file.grid(row=5, column=2, padx=10, columnspan=2)

        self.account_list_file = CTkLabel(self.user_view_frame, text='', font=('bold', 12))
        self.account_list_file.grid(row=6, column=0, sticky=W, padx=(150, 0), pady=(5, 0), columnspan=3)

        self.account_list_file_process = CTkLabel(self.user_view_frame, text='', font=('bold', 16))
        self.account_list_file_process.grid(row=7, column=0, sticky=W, padx=(150, 0), pady=(20, 0), columnspan=3)

    def browseAccountListFiles(self):
        filename = filedialog.askopenfilename(
                initialdir = "/",
                title = "Select Account List File",
                filetypes = (("Excel files","*.xlsx*"),("all files", "*.*")))
        
        if filename == "":
            return

        self.account_list_file.configure(text=filename.split("/")[-1])

        account_list = pd.read_excel(filename)
        account_list_col = ['SrN0. ', 'Account Name', 'isConsidered']

        if account_list_col != list(account_list.columns):
            self.account_list_file_process.configure(text="!Inavlid Account List File.", text_color=self.error_color)
            return

        for index, row in account_list.iterrows():
            if pd.isna(row['Account Name']) == False:
                self.db.create_account_list(row['Account Name'], self.user_session[1], row['isConsidered'])

        self.account_list_file_process.configure(text="!Process Done.", text_color=self.success_color)
        sleep(3)
        self.account_list_file_process.configure(text="", text_color=self.success_color)
        return

    
    def browseLiftingFiles(self):
        filename = filedialog.askopenfilename(
                initialdir = "/",
                title = "Select Lifiting Fee File",
                filetypes = (("Excel files","*.xlsx*"),("all files", "*.*")))
        
        if filename == "":
            return

        self.lifting_fee_file.configure(text=filename.split("/")[-1])

        user_data = self.db.fetch_user_data()
        if len(user_data) == 0:
            self.msg_start_process.configure(text="!No Email configaration found, please contact with admin", text_color=self.error_color)
            return

        self.msg_start_process.configure(text="!Checking File", text_color=self.info_color)
        sleep(1)

        self.process_de_data(filename, user_data[0])

        self.msg_start_process.configure(text=f"!Process is complete successfully", text_color=self.success_color)
        showinfo(
            title='Process is complete successfully',
            message='All invoice is genrated and sent to email address'
        )
        sleep(3)
        self.msg_start_process.configure(text=f"", text_color=self.success_color)

        return


    def process_de_data(self, filepath, user_data):
        lifting_fee = pd.read_excel(filepath)

        lifting_file_index = ['Buy', 'Buy Amount', 'Sell', 'Sell Amount', 'Fee', 'Total Settlement', 'Beneficiary', 'When Booked', 'When Created', 'Created By', 'Delivery Method', 'Reference', 'Delivery Country ISO Code', 'Delivery Country Name', 'Your Reference', 'Cheque Number', 'Beneficiary ID', 'Execution Date', 'Payment Line Status', 'Payment Number', 'Processing Date', 'Bank Reference Number', 'AccountName', 'Bank Value Date', 'Exchange Rate', 'Our Reference', 'Charges Type', 'USD AMOUNT']

        if list(lifting_fee.columns) != lifting_file_index:
            self.msg_start_process.configure(text="!Invalid File", text_color=self.error_color)
            return

        self.msg_start_process.configure(text="!File is valid", text_color=self.success_color)
        sleep(1)

        today = datetime.date.today()
        first = today.replace(day=1)
        last_month = first - datetime.timedelta(days=1)
        last_month_number = last_month.strftime("%m")
        last_year_number = last_month.strftime("%Y")

        self.msg_start_process.configure(text="!Processing data", text_color=self.info_color)
        sleep(1)

        processed_data = {}
        for index, row in lifting_fee.iterrows():
            if pd.isna(row['AccountName']) == False:
                if row['AccountName'] in processed_data:
                    processed_data[row['AccountName']].append(row.to_dict())
                else:
                    processed_data[row['AccountName']] = [row.to_dict()]

        self.msg_start_process.configure(text="!Generating invoices", text_color=self.info_color)
        sleep(1)

        for account_name in processed_data:
            total_amount = 0

            is_considered = self.db.check_account_list(account_name, self.user_session[1])
            if is_considered:
                for row in processed_data[account_name]:
                    total_amount += row['USD AMOUNT']

                master_data = self.db.fetch_master_data(account_name)
                if len(master_data) == 0:
                    pass
                else:
                    master_data = master_data[0]
                    
                    if master_data[-1].lower() == "active":
                        customer_address = master_data[2]
                        vat_type = master_data[6]
                        email_ids = master_data[3].split(";")

                        invoice_exists = self.db.invoice_exists(account_name, last_month_number, last_year_number)

                        if invoice_exists == False:
                            confirm_creating_invoice = True
                        else:
                            confirm_creating_invoice = self.confirm_genration_invoice(account_name, invoice_exists[-1])

                        if confirm_creating_invoice:
                            self.msg_start_process.configure(text=f"!Creating invoice for {account_name}", text_color=self.info_color)
                            sleep(0.5)

                            num_invoice = self.db.get_num_invoice(last_month_number, last_year_number)
                            
                            create_invoice = genrate_pdf(
                                account_name,
                                customer_address,
                                str(total_amount),
                                vat_type,
                                str(user_data[2]),
                                str(num_invoice+1)
                            )

                            invoice_pdf_file = create_invoice[0]
                            invoice_number = create_invoice[1]

                            invoice_excel_file = genrate_excel(account_name, processed_data[account_name])

                            files = [f'{output_dir}/{invoice_pdf_file}', f'{output_dir}/{invoice_excel_file}']

                            self.msg_start_process.configure(text=f"!Sending email to {account_name}", text_color=self.info_color)
                            sleep(0.5)

                            is_email_auto = self.db.check_email_condition(account_name)
                            
                            if is_email_auto:
                                please_confirm_text = "We will deduct these lifting fees from the respective currency balance."
                            else:
                                please_confirm_text = "Please confirm we are able to deduct these lifting fees from the respective currency balance."

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
                                smtp_pass=user_data[6],
                                please_confirm_text=please_confirm_text
                            )

                            self.msg_start_process.configure(text=f"!Email sent to {account_name}", text_color=self.info_color)
                            sleep(0.5)

                            shutil.move(
                                f'{output_dir}/{invoice_pdf_file}',
                                f'{archive_dir}/{invoice_pdf_file}'
                            )
                            shutil.move(
                                f'{output_dir}/{invoice_excel_file}',
                                f'{archive_dir}/{invoice_excel_file}'
                            )

                            self.db.create_invoice(account_name, invoice_pdf_file.replace(".pdf", ""), invoice_number, last_month_number, last_year_number, self.current_user_name)
                        else:
                            self.msg_start_process.configure(text=f"!No new invoice genrating for {account_name}", text_color=self.info_color)
                            sleep(1)

    def confirm_genration_invoice(self, account_name, user_name):
        answer = askokcancel(
            title= 'Confirmation',
            message= f'Invoice is already generated for {account_name} by {user_name} \nDo you still want to generate a new one?',
            icon=WARNING)

        return answer
    
    
    def UsersFrame(self):
        # create users frame
        self.users_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.user_name = StringVar()
        self.user_name_label = CTkLabel(self.users_frame, text='User Name', font=('bold', 14), pady=20)
        self.user_name_label.grid(row=0, column=0, sticky=W, padx=(10, 0))
        self.user_name_entry = CTkEntry(self.users_frame, textvariable=self.user_name, width= 300)
        self.user_name_entry.grid(row=0, column=1, padx=(10, 0))
        
        self.user_password = StringVar()
        self.user_password_label = CTkLabel(self.users_frame, text='Password', font=('bold', 14), pady=20)
        self.user_password_label.grid(row=0, column=2, sticky=W, padx=(50, 0))
        self.user_password_entry = CTkEntry(self.users_frame, textvariable=self.user_password, width= 300, show="*")
        self.user_password_entry.grid(row=0, column=3, padx=(10, 20))

        self.confirm_password_user = StringVar()
        self.confirm_password_user_label = CTkLabel(self.users_frame, text='Confirm Password', font=('bold', 14), pady=20)
        self.confirm_password_user_label.grid(row=1, column=2, sticky=W, padx=(10, 0))
        self.confirm_password_user_entry = CTkEntry(self.users_frame, textvariable=self.confirm_password_user, width= 300, show="*")
        self.confirm_password_user_entry.grid(row=1, column=3, padx=(10, 0))

        self.create_user = CTkButton(self.users_frame, command=self.create_user, text='Create User', width=200, height=40,border_width=1, corner_radius=20, fg_color="#63B3CC", border_color="#63B3CC", hover_color="#242424", font=('Bold', 20))
        self.create_user.grid(row=1, column=0, padx=30, pady=(20,0), columnspan=2)
        self.create_user_msg = CTkLabel(self.users_frame, text='', font=('bold', 16))
        self.create_user_msg.grid(row=2, column=1, sticky=W, padx=(10, 0), pady=(0,20), columnspan=2)


        style = ttk.Style()
        style.configure(
            "Treeview",
            background="silver",
            foreground="blue",
            rowheight=25,
            fieldbackground="black"
        )

        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Treeview.Heading', background=self.theme_color, foreground=self.info_color, border_color=self.theme_color)
        s.configure('Treeview', background=self.theme_color, fieldbackground=self.theme_color, foreground="white", border_color=self.theme_color)

        self.users_table = ttk.Treeview(self.users_frame, height=15, selectmode ='browse')
        self.users_table['columns'] = ('user_id', 'user_name', 'user_type')
        self.users_table.grid(row=3, column=0, sticky=W, padx=(10, 0), columnspan=4)

        self.users_table.column("#0", width=0,  stretch=NO)

        self.users_table.column("user_id",anchor=CENTER)
        self.users_table.heading("user_id", text="User ID")

        self.users_table.column("user_name",anchor=CENTER)
        self.users_table.heading("user_name", text="User Name")

        self.users_table.column("user_type",anchor=CENTER)
        self.users_table.heading("user_type", text="User Type")

        verscrlbar = ttk.Scrollbar(self.users_frame, orient ="vertical", command = self.users_table.yview)
        verscrlbar.place(x=30+580+5, y=175, height=300+20)

        self.users_table.configure(xscrollcommand = verscrlbar.set)

        self.fill_user_table()

    def fill_user_table(self):
        for item in self.users_table.get_children():
            self.users_table.delete(item)

        users = self.db.fetch_users()

        for user in users:
            self.users_table.insert('', 'end', values=(user[0], user[1], user[4]))
    
    def create_user(self):
        
        if self.user_name.get() == "" or self.user_password.get() == "" or self.confirm_password_user.get() == "":
            self.create_user_msg.configure(text="!Please fill up all fields", text_color=self.error_color)
            return

        if self.user_password.get() != self.confirm_password_user.get():
            self.create_user_msg.configure(text="!Password not matched", text_color=self.error_color)
            return

        password_hash = generate_password_hash(self.user_password.get())
        if self.db.create_user(self.user_name.get(), password_hash, "user") == "user_name_exists":
            self.create_user_msg.configure(text="!User name exists", text_color=self.error_color)
            return

        self.create_user_msg.configure(text=f"!Account for {self.user_name.get()} created succesfully", text_color=self.success_color)

        self.fill_user_table()

    
    def AdminRegeistrationFrame(self):
        self.admin_reg_frame = CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.reg_lebel = CTkLabel(self.admin_reg_frame, text="Create New Admin", font=('Bold', 30), text_color="#cb2d9a")
        self.reg_lebel.grid(row=0, column=0, padx=400, pady=(80,10), columnspan=3)

        self.admin_user_name = StringVar()
        self.admin_user_name_label = CTkLabel(self.admin_reg_frame, text='Admin User Name', font=('bold', 20), pady=20)
        self.admin_user_name_label.grid(row=1, column=1, sticky=W, padx=(120, 0))
        self.admin_user_name_entry = CTkEntry(self.admin_reg_frame, textvariable=self.admin_user_name, width= 300)
        self.admin_user_name_entry.grid(row=2, column=1, padx=(10, 0))
        
        self.admin_password = StringVar()
        self.admin_password_label = CTkLabel(self.admin_reg_frame, text='Password', font=('bold', 20), pady=20)
        self.admin_password_label.grid(row=3, column=1, sticky=W, padx=(120, 0))
        self.admin_password_entry = CTkEntry(self.admin_reg_frame, textvariable=self.admin_password, width= 300, show="*")
        self.admin_password_entry.grid(row=4, column=1, padx=(10, 0))
        
        self.confirm_password = StringVar()
        self.confirm_password_label = CTkLabel(self.admin_reg_frame, text='Confirm Password', font=('bold', 20), pady=20)
        self.confirm_password_label.grid(row=5, column=1, sticky=W, padx=(120, 0))
        self.confirm_password_entry = CTkEntry(self.admin_reg_frame, textvariable=self.confirm_password, width= 300, show="*")
        self.confirm_password_entry.grid(row=6, column=1, padx=(10, 0))

        self.admin_reg_btn = CTkButton(self.admin_reg_frame, text='Register', width=200, height=40,border_width=1, corner_radius=20, fg_color="#37D95B", border_color="#37D95B", hover_color="#242424", font=('Bold', 20), command=self.create_admin)
        self.admin_reg_btn.grid(row=7, column=1, padx=10, pady=20)
        self.admin_reg_err = CTkLabel(self.admin_reg_frame, text='', font=('bold', 16))
        self.admin_reg_err.grid(row=8, column=1, sticky=W, padx=(130, 0))

    def create_admin(self):
        
        if self.admin_user_name.get() == "" or self.admin_password.get() == "" or self.confirm_password.get() == "":
            self.admin_reg_err.configure(text="!Please fill up all fields", text_color=self.error_color)
            return

        if self.admin_password.get() != self.confirm_password.get():
            self.admin_reg_err.configure(text="!Password not matched", text_color=self.error_color)
            return

        password_hash = generate_password_hash(self.admin_password.get())
        self.db.create_user(self.admin_user_name.get(), password_hash, "admin")

        self.login_err.configure(text="!Account created succesfully, please login", text_color=self.success_color)
        self.select_frame_by_name("login")

    
    
    
    def LoginFrame(self):
        # create login frame

        self.login_frame = CTkFrame(self, corner_radius=0, fg_color="transparent")
        
        self.login_label = CTkLabel(self.login_frame, text="Login", font=('Bold', 30), text_color="#2d86cb")
        self.login_label.grid(row=0, column=0, padx=470, pady=(100,10), columnspan=3)

        self.login_option = StringVar()
        self.login_option_select = CTkOptionMenu(self.login_frame, values=["Select", "User", "Admin"], corner_radius=20, font=('Bold', 20), command=self.set_login_option_val)
        self.login_option_select.grid(row=1, column=1, padx=(10, 0), pady=(20, 0))

        self.login_user_name = StringVar()
        self.login_user_name_label = CTkLabel(self.login_frame, text='User Name', font=('bold', 20), pady=20)
        self.login_user_name_label.grid(row=2, column=1, sticky=W, padx=(120, 0))
        self.login_user_name_entry = CTkEntry(self.login_frame, textvariable=self.login_user_name, width= 300)
        self.login_user_name_entry.grid(row=3, column=1, padx=(10, 0))
        
        self.login_password = StringVar()
        self.login_password_label = CTkLabel(self.login_frame, text='Password', font=('bold', 20), pady=20)
        self.login_password_label.grid(row=4, column=1, sticky=W, padx=(120, 0))
        self.login_password_entry = CTkEntry(self.login_frame, textvariable=self.login_password, width= 300, show="*")
        self.login_password_entry.grid(row=5, column=1, padx=(10, 0))

        self.login_btn = CTkButton(self.login_frame, text='Login', width=200, height=40,border_width=1, corner_radius=20, fg_color="#37D95B", border_color="#37D95B", hover_color="#242424", font=('Bold', 20), command=self.login_user)
        self.login_btn.grid(row=6, column=1, padx=10, pady=20)
        self.login_err = CTkLabel(self.login_frame, text='', font=('bold', 16))
        self.login_err.grid(row=7, column=1, sticky=W, padx=(130, 0))

    def set_login_option_val(self, selection):
        self.login_option.set(selection)

    def login_user(self):
        if self.login_user_name.get() == "" or self.login_password.get() == "" or self.login_option.get() == "" or self.login_option.get() == "Select":
            self.login_err.configure(text="!Please fill up all fields", text_color=self.error_color)
            return

        login_val = self.db.check_user_login(self.login_user_name.get(), self.login_password.get(), self.login_option.get().lower())

        if login_val == "user_not_found":
            self.login_err.configure(text="!User not found", text_color=self.error_color)
            return
        elif login_val == "password_err":
            self.login_err.configure(text="!Incorrect Password", text_color=self.error_color)
            return
        elif login_val == "login_success":
            self.user_logged_in = True
            self.user_session = self.db.check_user_session()
            
            self.login_user_name.set("")
            self.login_password.set("")
            self.login_err.configure(text="", text_color=self.error_color)
            
            self.authenticate_user()

    def UserLogout(self):
        self.db.end_user_session(self.user_session[5])
        self.user_logged_in = False
        self.navigation_frame.grid_forget()
        self.select_frame_by_name("login")

    def select_frame_by_name(self, name):
        # set button color for selected button
        if self.user_logged_in and self.is_admin:
            self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
            self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "users" else "transparent")
        elif self.user_logged_in and self.is_admin == False:
            self.user_home_button.configure(fg_color=("gray75", "gray25") if name == "user_view" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

        if name == "user_view":
            self.user_view_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.user_view_frame.grid_forget()
        
        if name == "users":
            self.users_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.users_frame.grid_forget()
        
        if name == "login":
            self.login_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.login_frame.grid_forget()

        if name == "admin_reg":
            self.admin_reg_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.admin_reg_frame.grid_forget()

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

        if new_appearance_mode == "light":
            self.theme_color = "#ffffff"
        else:
            self.theme_color = "#242424"


if __name__ == "__main__":
    app = App()
    app.mainloop()