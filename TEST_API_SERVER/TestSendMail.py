from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

user = "hospitalsmartbracelet@gmail.com"
port = 587
host = 'smtp.gmail.com'
password = "Agosto.2020"
token = ""  #token aplication


# create message object instance
msg = MIMEMultipart()



# setup the parameters of the message

msg['From'] = user
msg['To'] = "wisrovi.rodriguez@gmail.com"
msg['Subject'] = "Subscription"




# add in the message body
message = "Thank you"
msg.attach(MIMEText(message, 'plain'))




# create server
server = smtplib.SMTP('{}: {}'.format(host, port))
server.starttls()


# Login Credentials for sending the mail
if len(token) > 0:
    password = token
server.login(msg['From'], password)




# send the message via the server.
server.sendmail(msg['From'], msg['To'], msg.as_string())
server.quit()





print("successfully sent email to %s:" % (msg['To']))