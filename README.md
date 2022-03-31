# 31/03/2022
Please note that this service is now disabled as the vaccination campaign in Québec is reaching its end.
GET Establishments is the only endpoint that still works for demonstration purposes on the web app.
The other endpoints will return 200 but won't do anything. Again just for demonstration purpose in the web app.
The notification service has been shut down. Nothing to change in the code.

# covid-vaxx-qc-api
Service to send email notifications for covid 19 vaccination availabilities in Quebec according to specified criterias

# Set up steps

### REQUIREMENTS
1. Make sure Python 3.6+ is installed
2. pip install -r requirements.txt (I recommend using a virtualenv)
3. Create a .env file and add the following attribute: NOTIF_DELAY=12

### DATABASE
1. Create an account on Mongo Atlas https://www.mongodb.com/cloud/atlas
2. Create a cluster and add a database with the following collections: availabilities, establishments, pending-unsubscriptions, users
3. Create an admin user in your database
4. In the api/config.py, change the mongo_db attribute to the name of your database
5. In the same config file, modify the mongo_connection_string so that it fits yours
6. In the .env file, define the MONGO_PSWD variable with your admin password

### EMAIL
1. Create a throaway gmail account and make sure the "Less secure app access" setting is on
2. In the config file, change the email address to the one you just created
3. In the .env file, add the gmail account password to a variable named EMAIL_PSWD

### RECAPTCHA
1. Head to https://www.google.com/recaptcha/admin/create
2. Create a V2 "I'm not a robot" tickbox
3. Make sure you add localhost to the list of domains
4. Copy the secret key and add it to a RECAPTCHA_SECRET variable in the .env file
5. Hold on to the site key for the front end set up

### RUN THE API
1. Uncomment the "load_dotenv()" statement on line 5 of the config file
2. in the terminal at the project root: set FLASK_APP=covid_vaxx_qc_api.py
3. flask run

### RUN THE NOTIFIER
1. Simply call the notify_users function for a one time notification run
2. You can also run the scheduler itself, it's currently set to run every 30 min between 7am and 11pm Eastern Time

# Running tests
In the project root folder run this command
```
pytest -v
```
