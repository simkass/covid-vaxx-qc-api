from random import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from api import config, utils


def email_login():
    smtpsrv = "smtp.gmail.com"

    smtpserver = smtplib.SMTP(smtpsrv, 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(config.email_address, config.email_password)
    return smtpserver


def send_sign_up_email(sendto, establishments_of_interest, availabilities):
    smtpserver = email_login()
    message = MIMEMultipart("alternative")
    message["Subject"] = "Abonnement à Alerte Vaccin QC"
    message["From"] = config.email_address
    message["To"] = sendto

    msg = """<html><body>
                <h2>Vous venez de vous abonner au service Alerte Vaccin QC</h2>
                <h3>Vous recevrez un courriel lorsqu'apparaîtra un rendez-vous de vaccination qui respecte les critères suivants:</h3>
                <h2>Cliniques de vaccination:</h2>
                <table>
                    <tr
                        <th>Clinique</th>
                        <th>Adresse</th>
                    </tr>"""

    for place in establishments_of_interest:
        msg = msg + """<tr><td>""" + place['name_fr'] + """</td><td>""" + \
            place['formatted_address'] + """</td></tr>"""

    msg = msg + """</table><h2>Disponibilités: </h2>"""

    for availability in availabilities:

        start_date, start_time = utils.get_datetime_full_strings(
            availability['start'])
        end_date, end_time = utils.get_datetime_full_strings(
            availability['stop'])

        msg = msg + """<h4>Du """ + start_date + " à " + start_time + \
            " jusqu'au " + end_date + " à " + end_time + """</h4>"""

    msg = msg + """<h3>Pour vous désabonner, visitez <a href='https://www.alertevaccin.ca/unsubscribe'>Alerte Vaccin</a>.</h3>"""
    msg = msg + """<p><b>Alerte Vaccin QC</b></p></body></html>"""

    html = MIMEText(msg, "html")
    message.attach(html)

    smtpserver.sendmail(config.email_address, sendto, message.as_string())
    smtpserver.quit()


def send_notification_email(user, availabilities, establishments):
    smtpserver = email_login()
    message = MIMEMultipart("alternative")
    message["Subject"] = "Ces rendez-vous de vaccination contre la Covid-19 pourraient vous intéresser"
    message["From"] = config.email_address
    message["To"] = user['email_address']

    msg = """<html><body><h3>Voici des disponibilités de rendez-vous pour une première dose du vaccin contre la Covid-19 qui pourraient vous intéresser</h3>"""

    for place in establishments:
        if place['id'] in user['establishments_of_interest']:

            previous_start_date = ''
            establishment_availabilities = [
                a for a in availabilities if a['establishment'] == place['establishment']]

            if len(establishment_availabilities) != 0:
                msg = msg + """<p><h2>""" + place['name_fr'] + "</h2> " + \
                            """ <i>""" + \
                    place['formatted_address'] + """</i></p>"""

                for availability in establishment_availabilities:
                    start_date, start_time = utils.get_datetime_full_strings(
                        availability['start'], True)
                    if start_date != previous_start_date:
                        msg = msg + """<h4>""" + start_date + """<h4>"""
                        previous_start_date = start_date
                    msg = msg + start_time + ", "

    msg = msg + """<h3>Pour réserver un rendez-vous, visitez <a href='https://portal3.clicsante.ca/'>Clic-Santé</a>.</h3>"""
    msg = msg + """<h3>Pour vous désabonner, visitez <a href='https://www.alertevaccin.ca/unsubscribe'>Alerte Vaccin</a>.</h3>"""

    msg = msg + """<p><b>Alerte Vaccin QC</b></p></body></html>"""

    html = MIMEText(msg, "html")
    message.attach(html)

    smtpserver.sendmail(config.email_address,
                        user['email_address'], message.as_string())
    smtpserver.quit()


def send_unsubscription_request(email_address, random_code):
    smtpserver = email_login()
    message = MIMEMultipart("alternative")
    message["Subject"] = "Code de confirmation pour vous désabonner"
    message["From"] = config.email_address
    message["To"] = email_address

    msg = """<html><body><h3>Voici votre code de confirmation pour vous désabonner du service Alerte Vaccin QC:</h3>"""
    msg = msg + """<h1>""" + \
        str(random_code) + """</h1><p><b>Alerte Vaccin QC</b></p></body></html>"""

    html = MIMEText(msg, "html")
    message.attach(html)

    smtpserver.sendmail(config.email_address,
                        email_address, message.as_string())
    smtpserver.quit()


def send_unsubscription_confirmation(email_address):
    smtpserver = email_login()
    message = MIMEMultipart("alternative")
    message["Subject"] = "Confirmation de votre désabonnement"
    message["From"] = config.email_address
    message["To"] = email_address

    msg = """<html><body><h2>Vous venez de vous désabonner du service Alerte Vaccin QC</h2>
                <p>Merci d'avoir utilisé notre service</p>
                <p><b>Alerte Vaccin QC</b></p></body></html>"""

    html = MIMEText(msg, "html")
    message.attach(html)

    smtpserver.sendmail(config.email_address,
                        email_address, message.as_string())
    smtpserver.quit()
