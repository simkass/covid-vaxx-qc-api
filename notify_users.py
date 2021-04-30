import json

from apscheduler.schedulers.blocking import BlockingScheduler

from api import clic_sante_api, db_client, email_client, utils

schedule = BlockingScheduler()


def notify_users():
    establishments = db_client.get_establishments()
    previous_availabilities = db_client.get_availabilities()
    current_availabilities = clic_sante_api.get_availabilities(establishments)
    new_availabilities = utils.identify_new_availabilities(previous_availabilities, current_availabilities)
    for user in db_client.get_users():
        availabilities = current_availabilities if user['new_user'] else new_availabilities
        availabilities_of_interest = utils.identify_availabilities_of_interest(availabilities, user)
        email_client.send_notification_email(user, availabilities_of_interest, establishments)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


schedule.add_job(notify_users, 'interval', minutes=1)
schedule.start()
