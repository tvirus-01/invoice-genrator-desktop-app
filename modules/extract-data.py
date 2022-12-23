import pandas as pd
from script import genrate_pdf, genrate_excel
from sendEmail import send_mail
import shutil

lifting_fee = pd.read_excel('input/Lifting_Fee_November_2022.xlsx')
master_data = pd.read_excel('input/Master_Data.xlsx')
master_data = master_data.set_index("*ContactName").to_dict("index")
GBP_RATE = 1.18255

processed_data = {}

for index, row in lifting_fee.iterrows():

    if row['AccountName'] in processed_data:
        processed_data[row['AccountName']].append(row.to_dict())
    else:
        processed_data[row['AccountName']] = [row.to_dict()]

for data in processed_data:
    total_amount = 0

    for row in processed_data[data]:
        total_amount += row['USD AMOUNT']

    create_invoice = genrate_pdf(
        data,
        master_data[data]['Customer Address'],
        str(total_amount),
        master_data[data]['VAT Type'],
        str(GBP_RATE)
    )

    invoice_pdf_file = create_invoice[0]
    invoice_number = create_invoice[1]

    invoice_excel_file = genrate_excel(data, processed_data[data])

    send_to = master_data[data]['Email id'].split(";")
    files = [f'output/{invoice_pdf_file}', f'output/{invoice_excel_file}']

    send_mail(
        "ffries6@gmail.com",
        send_to,
        files,
        invoice_number,
        data,
        total_amount
    )

    shutil.move(
        f'output/{invoice_pdf_file}',
        f'archive/{invoice_pdf_file}'
    )
    shutil.move(
        f'output/{invoice_excel_file}',
        f'archive/{invoice_excel_file}'
    )