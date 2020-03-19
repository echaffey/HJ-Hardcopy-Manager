import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Message():


    def __init__(self):
        self.sender_email = "evan.chaffey@gmail.com"
        self.receiver_email = "echaffey@my.uri.edu"
        self.password = 'Strength1991'

        self.message = MIMEMultipart("alternative")
        self.message["Subject"] = "Dog Updates [Automated]"
        self.message["From"] = self.sender_email
        self.message["To"] = self.receiver_email        

    def send_email(self, html_content):
    # Turn these into plain/html MIMEText objects
        # part1 = MIMEText(text, "plain")
        message_HTML = MIMEText(html_content, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        # self.message.attach(part1)
        self.message.attach(message_HTML)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(
                self.sender_email, self.receiver_email, self.message.as_string()
            )
