from flask.ext.mail import Mail, Message
from app import app

def send_email(email, pdf):

    mail_ext = Mail(app)
    subject = "Phone Notes"
    receiver = "breno601@gmail.com"
    mail_to_be_sent = Message(subject=subject, recipients=[receiver])
    mail_to_be_sent.body = "This email contains PDF."
    mail_to_be_sent.attach("file.pdf", "application/pdf", pdf)
    mail_ext.send(mail_to_be_sent)
