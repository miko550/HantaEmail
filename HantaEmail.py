import smtplib, ssl, csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass

# CREDITS to https://realpython.com/python-send-email/

# set up a Gmail address
# Turn Allow less secure apps to ON. Be aware that this makes it easier for others to gain access to your account.
# https://myaccount.google.com/lesssecureapps << to Allow less secure apps

# :::Checklist::::
# paste your html template into <emailform.html>
# paste your email list into <emailList.scv> format [email,name]
# Change your Email Subject

sender_email = "xx@gmail.com" #your email
#sender_password = "xx" # your pass

# Use this if you want to type the email password
sender_password = getpass("Type your password and press enter:")

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, sender_password)
    with open("emailList.csv") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for email, name in reader:

            message = MIMEMultipart("alternative")
            message["Subject"] = f"Congrat {name}"  #Email Subject
            message["From"] = sender_email
            message["To"] = email

            # HTML version of your message
            with open("emailform.html", 'r') as f:
                content = f.read()
            content = content.replace("#REPLACEME#", name)

            html = f""" {content} """

            # Turn these into plain/html MIMEText objects
            htmltxt = MIMEText(html, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(htmltxt)

            #send email
            print(f"Sending email to {name} : {email}")
            server.sendmail(
                sender_email,
                email,
                message.as_string()
            )