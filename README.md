# covid-vaxx-qc-api
Service to send email notifications for covid 19 vaccination availabilities in Quebec according to specified criterias

# Set up steps

1. REQUIREMENTS
A. Make sure Python 3.6+ is installed
B. pip install -r requirements.txt (I recommend using a virtualenv)
C. Create a .env file and add the following attribute: NOTIF_DELAY=12

2. DATABASE
A. Create an account on Mongo Atlas https://www.mongodb.com/cloud/atlas
B. Create a cluster and add a database with the following collections: availabilities, establishments, pending-unsubscriptions, users
C. Create an admin user in your database
D. In the api/config.py, change the mongo_db attribute to the name of your database
E. In the same config file, modify the mongo_connection_string so that it fits yours
F. In the .env file, define the MONGO_PSWD variable with your admin password

3. EMAIL
A. Create a throaway gmail account and make sure the "Less secure app access" setting is on
B. In the .env file, add the gmail account password to a variable named EMAIL_PSWD

4. RECAPTCHA
A. Head to https://www.google.com/recaptcha/admin/create
B. Create a V2 "I'm not a robot" tickbox
C. Make sure you add localhost to the list of domains
D. Copy the secret key and add it to a RECAPTCHA_SECRET variable in the .env file
E. Hold on to the site key for the front end set up

5. RUN THE API
A. Uncomment the "load_dotenv()" statement on line 5 of the config file
in the terminal at the project root (If you're using a virtualenv, make sure its activated):
B. set FLASK_APP=covid_vaxx_qc_api.py
C. flask run

6. RUN THE NOTIFIER
A. Simply call the notify_users function for a one time notification run
B. You can also run the scheduler itself, it's currently set to run every 30 min between 7am and 11pm Eastern Time

