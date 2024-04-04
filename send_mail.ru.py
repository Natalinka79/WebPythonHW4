import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

fromaddr = 'Natalinka.79@mail.ru'
toaddr = "Natalinka.79@mail.ru"
mypass = "UPyPCmL6pKv6LwyDfCcy"
reportname = "log.txt"

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = 'Hello from Python'

with open(reportname, 'rb') as f:
    part = MIMEApplication(f.read(), Name=basename(reportname))
    part['Content-Disposition'] = 'attachment; filename="%s' % basename(reportname)
    msg.attach(part)

body = 'Это пробное сообщение'
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
server.login(fromaddr, mypass)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()