from smtplib import SMTPException
from threading import Thread

from flask import abort, current_app
from flask_mail import Message
from app.ext import mail


def _send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except SMTPException:
            abort(505)

def send_mail(subject, recipients, sender, body, html):
    """
    Crea y envia el email

    :param subject:
        Asunto

    :param recipients:
        Lista de receptores
    
    :param sender:
        Email de remitente

    :param body:
        mensaje en texto plano

    :param html:
        mensaje en texto html
    """

    msg = Message(
        subject=subject,
        recipients=recipients,
        sender=sender
    )
    msg.body = body
    msg.html = html
    app = current_app._get_current_object()
    Thread(target=_send_async_email, args=(app, msg)).start()

