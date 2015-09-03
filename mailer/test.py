from email.mime.text import MIMEText
from subprocess import Popen, PIPE

msg = MIMEText("hai")
msg["From"] = "pedro@pieinthesky.xyz"
msg["To"] = "pedro.oliv16@gmail.com"
msg["Subject"] = "This is the subject."
p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
p.communicate(bytes(msg.as_string(), 'UTF-8'))
