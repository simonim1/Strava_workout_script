import time
import csv

from flask import Flask, request, url_for, session, redirect, render_template

# internal imports
from Secrets.secrets import CLIENT_SECRET, CLIENT_ID
from Classes.StravaHelper import Strava

############################################
#                 Globals                  #
############################################
STRAVA_CLIENT_SECRET = CLIENT_SECRET
STRAVA_CLIENT_ID = CLIENT_ID

############################################
#                 Flask                    #
############################################
app = Flask(__name__,template_folder='FrontEnd')

# set the name of the session cookie
app.config['SESSION_COOKIE_NAME'] ='Strava cookie'

# set a random secret key to sign the cookie
app.secret_key = STRAVA_CLIENT_SECRET

# set the key for the token info in the session dictionary
TOKEN_INFO = 'token_info'

strava = Strava()

# route to handle logging in
@app.route('/')
def login():
    # create a StravaOAuth instance and get the authorization URL
    auth_url = strava.create_strava_oath()
    # redirect the user to the authorization URL
    return redirect(auth_url)

# route to handle the redirect URI after authorization
@app.route('/authorization')
def redirect_page():
    print('in redirect')
    # clear the session
    session.clear()
    # get the authorization code from the request parameters
    code = request.args.get('code')

    # exchange the authorization code for an access token and refresh token
    token_info = strava.strava_client.exchange_code_for_token(client_id=STRAVA_CLIENT_ID,
                                              client_secret=STRAVA_CLIENT_SECRET,
                                              code=code)
    # save the token info in the session
    session[TOKEN_INFO] = token_info
    # redirect the user to the save_discover_weekly route
    return redirect(url_for('get_user_input',_external=True))

@app.route('/user_input')
def get_user_input():
    return render_template('input.html')

@app.route('/user_activities', methods = ['POST'])
def get_user_page():
    try:
        # get the token info from the session
        token_info = get_token()

        #grabbing user input
        if request.method == 'POST':
            form_data = request.form
            start_date = form_data['date']
            variation_one = form_data['Variation']

        activity_list = strava.get_weight_traning_activities(after=start_date)

        routine_dict = prephase_csv_reader('workout_routines/Prephase_4_weeks.csv')

        response = strava.csv_prefase_weight_training_update(variation_one, activity_list=activity_list,
                                                             csv_routine_dict=routine_dict)
    except:
        # if the token info is not found, redirect the user to the login route
        print('User not logged in')
        return redirect("/")


    return render_template('success.html', value = str(response))


############################################
#                 helpers                  #
############################################
# function to get the token info from the session
def get_token():
        token_info = session.get(TOKEN_INFO, None)
        if not token_info:
            # if the token info is not found, redirect the user to the login route
            redirect(url_for('login', _external=False))

        # check if the token is expired and refresh it if necessary
        now = int(time.time())

        is_expired = token_info['expires_at'] - now < 60
        if (is_expired):
            strava_oauth = strava.create_strava_oath()
            token_info = strava_oauth.refresh_access_token(token_info['refresh_token'])

        return token_info

def prephase_csv_reader(file_name):
    with open(file_name, mode='r') as file:
        # reading the CSV file
        csvFile = csv.reader(file)

        # displaying the contents of the CSV file
        paragraph = " "
        routine_dict = {}
        for lines in csvFile:
            if lines != []:
                sententence = " ".join(lines) + '\n '
                paragraph = paragraph + sententence
            else:
                if 'Upper 1' in paragraph:
                    routine_dict['Upper 1'] = paragraph
                    paragraph = " "
                if 'Lower 1' in paragraph:
                    routine_dict['Lower 1'] = paragraph
                    paragraph = " "
                if 'Upper 2' in paragraph:
                    routine_dict['Upper 2'] = paragraph
                    paragraph = " "

            # last routine in the list so there doesnt need to be checking
        routine_dict['Lower 2'] = paragraph
        paragraph = " "
        return routine_dict




app.run(debug=True)