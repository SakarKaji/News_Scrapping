import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from .Utils import get_report_file_path
from dotenv import load_dotenv
import os

load_dotenv()


def Report_Email():
    fromaddr = os.getenv('FROM_ADDR')
    password = os.getenv('PASSWORD')
    toaddrs = ['bishalfox@yopmail.com']

    if not fromaddr or not password:
        print("Error: FROM_ADDR and PASSWORD must be set in the .env file")
        return 0

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['Subject'] = "Mail from Scrapy 1 bot"

    body = "This mail contains the scraped news from the last bot run"
    msg.attach(MIMEText(body, 'plain'))

    try:
        filename = get_report_file_path()

        file = filename.split('/')[-1]

        with open(filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            f"attachment; filename= {file}")
            msg.attach(part)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(fromaddr, password)
            for toaddr in toaddrs:
                msg['To'] = toaddr
                server.sendmail(fromaddr, toaddr, msg.as_string())

        print("Email sent successfully")
        return 1
    except Exception as e:
        print(f"Failed to send email: {e}")
        return 0


def error_report_email(data):
    fromaddr = os.getenv('FROM_ADDR')
    password = os.getenv('PASSWORD')
    toaddrs = ['bishalfox@yopmail.com']

    if not fromaddr or not password:
        print("Error: FROM_ADDR and PASSWORD must be set in the .env file")
        return 0

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['Subject'] = "Mail from Scrapy 1 bot"

    body = f"Error in {data}"
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(fromaddr, password)
            for toaddr in toaddrs:
                msg['To'] = toaddr
                server.sendmail(fromaddr, toaddr, msg.as_string())

        print("Email sent successfully")
        return 1

    except Exception as e:
        print(f"Failed to send email: {e}")
        return 0
