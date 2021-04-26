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
    msg = """<html><body>
                <p>Vous venez de vous abonner au service Alerte Vaccin QC</p>
                <p>Vous recevrez un courriel lorsqu'apparaîtra un rendez-vous qui respecte les critères suivant:</p>
                <p><b>Cliniques de vaccination:</b></p>"""

    for place in establishments['places']:
        if place['id'] in establishments_of_interest:
            msg = msg + """<p> - """ + place['name_fr'] + ": " + \
                """<i>   """ + place['formatted_address'] + """</i></p>"""

    msg = msg + """<p><b>Disponibilités: </b></p>"""

    for availabilitie in availabilities:

        start_date, start_time = utils.get_datetime_strings(availabilitie['start'])
        end_date, end_time = utils.get_datetime_strings(availabilitie['stop'])

        msg = msg + """<p>Du """ + start_date + " à " + start_time + " jusqu'au " + end_date + " à " + end_time + """</p>"""

    msg = msg + """</body></html>"""

    message = MIMEMultipart("alternative")
    message["Subject"] = "Vous venez de vous abonner à Alerte Vaccin QC"
    message["From"] = config.email_address
    message["To"] = sendto

    html = MIMEText(msg, "html")
    message.attach(html)

    smtpserver.sendmail(config.email_address, sendto, message.as_string())
    smtpserver.quit()


def send_notification_email(sendto, availabilities, establishments):
    pass


def send_unsubscription_request():
    pass


def send_unsubscription_confirmation():
    pass
