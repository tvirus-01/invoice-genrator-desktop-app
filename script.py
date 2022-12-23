from reportlab.pdfgen import canvas
import os, datetime, string, random
import xlsxwriter

def genrate_pdf(account_name: str, address: str, unit_price: str, vat_type: str, gbp_rate: str):
    today = datetime.datetime.now()
    current_month = today.strftime('%b')
    current_year = today.strftime('%y')
    current_date = f"{today.strftime('%d')}-{current_month}-{today.strftime('%Y')}"

    due_date = today + datetime.timedelta(days=6)
    due_date_str = f"{due_date.strftime('%d')}-{due_date.strftime('%b')}-{due_date.strftime('%Y')}"
    
    invoice_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

    unit_price_gbp = float(unit_price) / float(gbp_rate)
    unit_price_gbp = str(round(unit_price_gbp, 2))

    invoice_title = f"{account_name}-Lifting Fees-{today.strftime('%d')}{today.strftime('%m')}{today.strftime('%Y')}"

    c = canvas.Canvas(f"output/{invoice_title}.pdf", bottomup=0)
    c.setTitle(invoice_title)

    c.setFont("Helvetica", 22)
    c.drawString(25, 100, "TAX INVOICE")

    c.setFont("Times-Roman", 9)

    # Sender Data 
    c.drawString(60, 125, account_name)
    c.drawString(60, 140, address)
    # c.drawString(60, 155, "road, Pudong,")
    # c.drawString(60, 170, "Shanghai")
    # c.drawString(60, 185, "CHINA")

    # Invoice Data 
    c.drawString(350, 80, "Invoice Date")
    c.drawString(350, 90, current_date)
    
    c.drawString(350, 110, "Invoice Number")
    c.drawString(350, 120, invoice_number)
    
    c.drawString(350, 140, "Reference")
    c.drawString(350, 150, f"Lifting Fees - {current_month} {current_year}")
    
    c.drawString(350, 170, "Vat Number")
    c.drawString(350, 180, "2938729129")

    # Receiver Data
    c.drawString(450, 80, "ABC Corporation Limited")
    c.drawString(450, 95, "Office 7.09, 7th Floor")
    c.drawString(450, 105, "Tintagel House")
    c.drawString(450, 115, "492 Albert 492 Albert")
    c.drawString(450, 125, "London")
    c.drawString(450, 135, "SE1 7TY, UK")

    # Amount Desc
    c.line(20, 265, 580, 265)
    c.drawString(25, 250, "Description")
    c.drawString(25, 280, f"Lifting Fees - {current_month} {current_year}")
    
    c.drawString(300, 250, "Quantity")
    c.drawString(300, 280, "1.00")
    
    c.drawString(360, 250, "Unit Price")
    c.drawString(360, 280, unit_price)
    
    c.drawString(430, 250, "Vat")
    c.drawString(430, 280, vat_type)
    
    c.drawString(500, 250, "Amount USD")
    c.drawString(520, 280, unit_price)

    c.setLineWidth(0.5)
    c.line(420, 300, 580, 300)
    
    # total
    c.drawString(440, 320, "Subtotal")
    c.drawString(520, 320, unit_price)
    
    c.drawString(440, 340, "Total zero rated*")
    c.drawString(520, 340, "0.00")

    c.setLineWidth(1)
    c.line(420, 350, 580, 350)
    
    c.drawString(440, 370, "TOTAL USD")
    c.drawString(520, 370, unit_price)
    
    c.drawString(440, 385, "GBP")
    c.drawString(520, 385, unit_price_gbp)

    # GBP
    c.drawString(25, 320, "GBP Equivalent Conversion")
    c.drawString(25, 330, f"1 GBP = {gbp_rate} USD")

    c.drawString(25, 350, "VAT RATE")
    c.drawString(25, 365, vat_type)
    
    c.drawString(125, 350, "NET AMOUNT")
    c.drawString(125, 365, unit_price_gbp)
    
    c.drawString(195, 350, "VAT")
    c.drawString(195, 365, "0.00")


    # Other Data 
    c.setFont("Times-Bold", 12)
    c.drawString(25, 460, f"Due Date: {due_date_str}")

    c.setFont("Times-Roman", 9)
    c.drawString(25, 475, "Beneficiary Bank: Citibank N.A, Citigroup Centre 2, 25 Canada Square, Canary Wharf, London, E14 5LB")
    c.drawString(25, 490, "Beneficiary: MARTRUST CORP LTD")
    
    c.drawString(25, 520, "USD Account")
    c.drawString(25, 535, "Sort code: 18-50-08 Account number: 17786220")
    c.drawString(25, 550, "IBAN: GB06CITI18500817786220 Swift Code: CITIGB2L")
    
    c.drawString(25, 580, "EUR Account")
    c.drawString(25, 595, "Sort code: 18-50-08 Account number: 18498911")
    c.drawString(25, 610, "IBAN account: GB15CITI18500818498911 Swift Code: CITIGB2L")
    
    c.drawString(25, 640, "GBP Account")
    c.drawString(25, 655, "Sort code: 18-50-08 Account number: 17786212")
    c.drawString(25, 670, "IBAN account: GB28CITI18500817786212 Swift Code: CITIGB2L")

    c.drawString(25, 700, "Classification: Private and Confidential")
    c.setFont("Times-Roman", 7)
    c.drawString(25, 800, "Company Registration No: 07498933. Registered Office: Office 7.09, 7th Floor, Tintagel House, 492 Albert Embankment, London, SE1 7TY, UK")

    c.showPage()
    c.save()

    return [f"{invoice_title}.pdf", invoice_number]

def genrate_excel(account_name: str, lifting_data: list):
    today = datetime.datetime.now()
    current_month = today.strftime('%B')
    current_year = today.strftime('%Y')

    file_name = f"{account_name}-Lifting Fees-{today.strftime('%d')}{today.strftime('%m')}{today.strftime('%Y')}"
    
    workbook = xlsxwriter.Workbook(f'output/{file_name}.xlsx')

    cell_fill = workbook.add_format()
    cell_fill.set_pattern(1)
    cell_fill.set_bg_color('#B4C6E7')
    cell_fill.set_bold()

    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 1, 35)
    worksheet.set_column(2, 27, 15)

    worksheet.write('A2', 'Account Name', cell_fill)
    worksheet.write('B2', account_name)

    worksheet.write('A3', f"Lifting Fee For {current_month} {current_year}")
    worksheet.write('A4', 'Classification : Private and Confidential')

    col_name_exists = False
    col_name_row = 4
    data_row = 5

    for data in lifting_data:
        col = 0
        
        for index in data:
            if not col_name_exists:
                worksheet.write(col_name_row, col, index, cell_fill)
            
            try:
                worksheet.write(data_row, col, data[index])
            except:
                pass

            col += 1
        
        col_name_exists = True
        data_row += 1
    
    workbook.close()

    return f'{file_name}.xlsx'