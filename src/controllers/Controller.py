from clients.http import HTTPClient
from flask import render_template
import os
import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Controller:
    def __init__(self, pathToConfig):
        self.get_order_info = HTTPClient(pathToConfig, 'ORDER_INFO')
        self.get_trip_info = HTTPClient(pathToConfig, 'TRIP_INFO')
    
    def GetRequestToCourierService(self, payload):
        return self.get_trip_info.get(payload)

    def GetReuqestToOrderService(self, payload):
        return self.get_order_info.get(payload)

    def send_email(self, receipt):
        # Replace sender@example.com with your "From" address. 
        # This address must be verified.
        SENDER = 'k.dimitrov.stag.bg@gmail.com'
        SENDERNAME = 'UBER'

        # Replace recipient@example.com with a "To" address. If your account 
        # is still in the sandbox, this address must be verified.
        #RECIPIENT  = receipt.data['clientEmail']
        RECIPIENT = receipt.data['clientEmail']

        # Replace smtp_username with your Amazon SES SMTP user name.
        USERNAME_SMTP = os.environ['USERNAME_SMTP']

        # Replace smtp_password with your Amazon SES SMTP password.
        PASSWORD_SMTP = os.environ['PASSWORD_SMTP']

        # (Optional) the name of a configuration set to use for this message.
        # If you comment out this line, you also need to remove or comment out
        # the "X-SES-CONFIGURATION-SET:" header below.
        # CONFIGURATION_SET = "ConfigSet"

        # If you're using Amazon SES in an AWS Region other than US West (Oregon), 
        # replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP  
        # endpoint in the appropriate region.
        HOST = "email-smtp.eu-west-3.amazonaws.com"
        PORT = 25

        # The subject line of the email.
        SUBJECT = 'Amazon SES Test (Python smtplib)'

        # The email body for recipients with non-HTML email clients.
        BODY_TEXT = ("Amazon SES Test\r\n"
                    "This email was sent through the Amazon SES SMTP "
                    "Interface using the Python smtplib package."
                    )

        # The HTML body of the email.
        #pdf = pdfkit.from_url(render_template("index.html", data = receipt.data, receiptId = receipt.receiptId))
        BODY_HTML = render_template("email.html", data = receipt.data, receiptId = receipt.receiptId)


        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = SUBJECT
        msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
        msg['To'] = RECIPIENT
        # Comment or delete the next line if you are not using a configuration set
        # msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(BODY_TEXT, 'plain')
        part2 = MIMEText(BODY_HTML, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        # Try to send the message.

        try:  
            server = smtplib.SMTP(HOST, PORT)
            server.ehlo()
            server.starttls()
            #stmplib docs recommend calling ehlo() before & after starttls()
            server.ehlo()
            server.login(USERNAME_SMTP, PASSWORD_SMTP)
            server.sendmail(SENDER, RECIPIENT, msg.as_string())
            server.close()
        # Display an error message if something goes wrong.
        except Exception as e:
            print ("Error: ", e)
        else:
            print ("Email sent!")
