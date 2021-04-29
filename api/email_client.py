from random import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from api import config, utils

smtpsrv = "smtp.gmail.com"

smtpserver = smtplib.SMTP(smtpsrv, 587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.login(config.email_address, config.email_password)


def send_sign_up_email(sendto, establishments_of_interest, establishments, availabilities):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Vous venez de vous abonner à Alerte Vaccin QC"
    message["From"] = config.email_address
    message["To"] = sendto

    msg = """<html><body>
                <p>Vous venez de vous abonner au service Alerte Vaccin QC</p>
                <p>Vous recevrez un courriel lorsqu'apparaîtra un rendez-vous de vaccination qui respecte les critères suivant:</p>
                <p><b>Cliniques de vaccination:</b></p>"""

    for place in establishments['places']:
        if place['id'] in establishments_of_interest:
            msg = msg + """<p> - """ + place['name_fr'] + ": " + \
                """<i>   """ + place['formatted_address'] + """</i></p>"""

    msg = msg + """<p><b>Disponibilités: </b></p>"""

    for availability in availabilities:

        start_date, start_time = utils.get_datetime_strings(availability['start'])
        end_date, end_time = utils.get_datetime_strings(availability['stop'])

        msg = msg + """<p>Du """ + start_date + " à " + start_time + " jusqu'au " + end_date + " à " + end_time + """</p>"""

    msg = msg + """</body></html>"""

    html = MIMEText(msg, "html")
    message.attach(html)

    smtpserver.sendmail(config.email_address, sendto, message.as_string())
    smtpserver.quit()


def send_notification_email(user, availabilities, establishments):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Ces rendez-vous de vaccination pourraient vous intéresser"
    message["From"] = config.email_address
    message["To"] = user['email_address']

    msg = """<html><body><p>Voici des disponibilités de rendez-vous pour une première dose du vaccin contre la Covid-19 qui pourraient vous intéresser</p>"""

    for place in establishments:
        if place['id'] in user['establishments_of_interest']:
            msg = msg + """<p><b>""" + place['name_fr'] + "</b>: " + \
                """ <i>""" + place['formatted_address'] + """</i></p>"""
            establishment_availabilities = [a for a in availabilities if a['establishment'] == place['establishment']]
            for availability in establishment_availabilities:
                start_date, start_time = utils.get_datetime_strings(availability['start'])
                msg = msg + """<p> - Le """ + start_date + " à " + start_time + """</p>"""

    msg = msg + """</body></html>"""

    html = MIMEText(msg, "html")
    message.attach(html)

    smtpserver.sendmail(config.email_address, user['email_address'], message.as_string())
    smtpserver.quit()


def send_unsubscription_request(email_address, random_code):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Code de confirmation pour vous désabonner"
    message["From"] = config.email_address
    message["To"] = email_address

    msg = """<html><body><p>Voici votre code de confirmation pour vous désabonner du service Alerte Vaccin QC:</p>"""
    msg = msg + """<h1>""" + str(random_code) + """</h1></body></html>"""

    html = MIMEText(msg, "html")
    message.attach(html)

    smtpserver.sendmail(config.email_address, email_address, message.as_string())
    smtpserver.quit()


def send_unsubscription_confirmation(email_address):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Confirmation de votre désabonnement"
    message["From"] = config.email_address
    message["To"] = email_address

    msg = """<html><body><p>Vous venez de vous désabonner au service Alerte Vaccin QC</p></body></html>"""

    html = MIMEText(msg, "html")
    message.attach(html)

    smtpserver.sendmail(config.email_address, email_address, message.as_string())
    smtpserver.quit()
