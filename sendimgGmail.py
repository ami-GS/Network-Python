import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage

host = "smtp.gmail.com"
port = 587

from_ = "daiki@bci-lab.info"
to = raw_input("input address : ")
passwd = raw_input("input passward : ")
subject = u"件名"
body = "this is body of mail"
images = ["attached_1.jpg", "attached_2.png"]

mmulti = MIMEMultipart()
mmulti["From"] = from_
mmulti["To"] = to
mmulti["Subject"] = subject
mmulti.attach(mtext)

mtext = MIMEText(body, _charset = "iso-2022-jp")

for fn in images:
    with open(fn, "rb") as f:
        img = f.read()
#    img = open(fn, "rb").read()
        mimage = MIMEImage(img, fn[fn.find(".")+1:], filename = fn)
        mimage.add_header("Content-Disposition", "attachment", filename = fn)
        mmulti.attach(mimage)


smtp = smtplib.SMTP(host, port)
smtp.starttls()
smtp.login(from_, passwd)
smtp.sendmail(from_, to, mmulti.as_string())
smtp.close()
