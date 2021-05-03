from api import config
from apscheduler.schedulers.blocking import BlockingScheduler

from api import clic_sante_api, db_client, email_client, utils

schedule = BlockingScheduler()


def notify_users():
    establishments = db_client.get_establishments()
    previous_availabilities = db_client.get_availabilities()
    current_availabilities = clic_sante_api.get_availabilities(establishments)
    # new_availabilities = utils.identify_new_availabilities(previous_availabilities, current_availabilities)

    for user in db_client.get_users():
        availabilities = current_availabilities  # if user['new_user'] else new_availabilities
        availabilities_of_interest = utils.identify_availabilities_of_interest(availabilities, user)

        if len(availabilities_of_interest) != 0 and user['hours_since_last_email'] >= config.notif_delay:
            email_client.send_notification_email(user, availabilities_of_interest, establishments)
            db_client.update_user_hours_since_last_email(user['email_address'], 0)
        else:
            db_client.update_user_hours_since_last_email(
                user['email_address'],
                min(user['hours_since_last_email'] + 1, config.notif_delay))

        if user['new_user']:
            db_client.toggle_new_user(user['email_address'])

    db_client.update_availabilities(current_availabilities)


schedule.add_job(notify_users, 'cron', hour='0-3,10-23')
schedule.start()
