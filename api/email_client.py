import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import random

from api import config, utils

unsub = """<h3>Pour vous désabonner, visitez <a href='https://www.alertevaccin.ca/unsubscribe'>Alerte Vaccin</a>.</h3>"""


def email_login():
    smtpsrv = "smtp.gmail.com"
    smtpserver = smtplib.SMTP(smtpsrv, 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(config.email_address, config.email_password)
    return smtpserver


def create_message(subject, sendto):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = config.email_address
    message["To"] = sendto
    return message


def send_email(smtpserver, sendto, message, txt_msg, html_msg):
    txt = MIMEText(txt_msg, "plain")
    html = MIMEText(html_msg, "html")
    message.attach(txt)
    message.attach(html)
    smtpserver.sendmail(config.email_address, sendto, message.as_string())
    smtpserver.quit()


def create_establishment_title(place):
    url = "https://clients3.clicsante.ca/" + str(place["establishment"]) + "/take-appt?unifiedService=237&portalPlace=" + str(place["id"])
    return """<a href=""" + url + """><p><h2>""" + place['name_fr'] + """</a></h2><i>""" + place['formatted_address'] + """</i></p>"""


def send_sign_up_email(sendto, establishments_of_interest, availabilities):
    smtpserver = email_login()
    message = create_message("Abonnement à Alerte Vaccin QC", sendto)

    html_msg = """<html><body><h2>Vous venez de vous abonner au service Alerte Vaccin QC</h2>
             <h3>Vous recevrez un courriel lorsqu'apparaîtra un rendez-vous de vaccination qui respecte les critères suivants:</h3>
             <h2>Cliniques de vaccination:</h2><table><tr><th>Clinique</th><th>Adresse</th></tr>"""

    for place in establishments_of_interest:
        html_msg = html_msg + """<tr><td>""" + place['name_fr'] + \
            """</td><td>""" + place['formatted_address'] + """</td></tr>"""

    html_msg = html_msg + """</table><h2>Disponibilités: </h2>"""

    for availability in availabilities:
        start_date, start_time = utils.get_datetime_full_strings(availability['start'])
        end_date, end_time = utils.get_datetime_full_strings(availability['stop'])

        html_msg = html_msg + """<h4>Du """ + start_date + " à " + start_time + " jusqu'au " + end_date + " à " + end_time + """</h4>"""

    html_msg = html_msg + unsub + """<p><b>Alerte Vaccin QC</b></p></body></html>"""

    txt_msg = "Vous venez de vous abonner au service Alerte Vaccin QC"

    send_email(smtpserver, sendto, message, txt_msg, html_msg)


def send_notification_email(user, availabilities, establishments):
    smtpserver = email_login()
    message = create_message(
        "Ces rendez-vous de vaccination contre la Covid-19 pourraient vous intéresser", user['email_address'])

    html_msg = """<html><body><h3>Voici des disponibilités de rendez-vous pour une première dose du vaccin contre la Covid-19 qui pourraient vous intéresser</h3>"""

    for place in establishments:
        if place['id'] in user['establishments_of_interest']:

            start_times = []
            just_started = True
            
            establishment_availabilities = sorted([a for a in availabilities if a['establishment'] == place['establishment']], key=lambda k: k['start'])

            if len(establishment_availabilities) != 0:
                html_msg = html_msg + create_establishment_title(place)
                previous_start_date, _ = utils.get_datetime_full_strings(establishment_availabilities[0]['start'], True)

                for availability in establishment_availabilities:
                    start_date, start_time = utils.get_datetime_full_strings(availability['start'], True)
                    

                    if (start_date != previous_start_date and not just_started) or len(establishment_availabilities) == 1:
                        if len(start_times) > 1:
                            html_msg = html_msg + """<h4>""" + previous_start_date + " - " + "Entre " + start_times[0] + " et " + start_times[len(start_times) - 1] + """</h4>"""
                        else:
                            html_msg = html_msg + """<h4>""" + previous_start_date + " - " + start_times[0] + """</h4>"""
                        start_times = []

                    start_times.append(start_time)
                    just_started = False
                    previous_start_date = start_date

    html_msg = html_msg + """<h3>Pour réserver un rendez-vous, visitez <a href='https://portal3.clicsante.ca/'>Clic-Santé</a>.</h3>"""
    html_msg = html_msg + unsub + """<p><b>Alerte Vaccin QC</b></p></body></html>"""

    send_email(smtpserver, user['email_address'], message, "", html_msg)


def send_unsubscription_request(sendto, random_code):
    smtpserver = email_login()
    message = create_message("Code de confirmation pour vous désabonner", sendto)

    msg = """<html><body><h3>Voici votre code de confirmation pour vous désabonner du service Alerte Vaccin QC:</h3>"""
    msg = msg + """<h1>""" + str(random_code) + """</h1><p><b>Alerte Vaccin QC</b></p></body></html>"""

    html = MIMEText(msg, "html")
    message.attach(html)

    smtpserver.sendmail(config.email_address, sendto, message.as_string())
    smtpserver.quit()


def send_unsubscription_confirmation(sendto):
    smtpserver = email_login()
    message = create_message("Confirmation de votre désabonnement", sendto)

    msg = """<html><body><h2>Vous venez de vous désabonner du service Alerte Vaccin QC</h2>
                <p>Merci d'avoir utilisé notre service</p>
                <p><b>Alerte Vaccin QC</b></p></body></html>"""

    html = MIMEText(msg, "html")
    message.attach(html)

    smtpserver.sendmail(config.email_address, sendto, message.as_string())
    smtpserver.quit()
