import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import datetime

today = datetime.datetime.now()
current_month = today.strftime('%B')
current_year = today.strftime('%Y')

def send_mail(send_from, send_to, files, invoice_number, receiver_name, total_amount, smtp_server, smtp_port, smtp_user, smtp_pass, please_confirm_text):
    assert isinstance(send_to, list)

    subject = f'Invoice {invoice_number} from Martrust Corporation Limited for {receiver_name} - Lifting Fees - {current_month} {current_year}'

    text = f"""
        Hello,

        Please find attached your Lifting Fees - {current_month} {current_year} invoice {invoice_number} for USD {total_amount}.

        {please_confirm_text}

        If you have any questions, please let us know.

        Thanks,
        Martrust Corporation Limited
    """

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )

        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)


    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.starttls()
    smtp.login(smtp_user, smtp_pass)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()