import requests
import time
import csv
import pickle
from datetime import datetime, timedelta
from stravalib.client import Client
from flask import Flask, request, url_for, session, redirect, render_template

# internal imports
from Secrets.secrets import CLIENT_SECRET, CLIENT_ID, CODE

############################################
#                 Globals                  #
############################################
STRAVA_CLIENT_SECRET = CLIENT_SECRET
STRAVA_CLIENT_ID = CLIENT_ID

############################################
#                 Flask                    #
############################################
app = Flask(__name__)

# set the name of the session cookie
app.config['SESSION_COOKIE_NAME'] ='Strava cookie'

# set a random secret key to sign the cookie
app.secret_key = STRAVA_CLIENT_SECRET

# set the key for the token info in the session dictionary
TOKEN_INFO = 'token_info'

client = Client()

# route to handle logging in
@app.route('/')
def login():
    # create a SpotifyOAuth instance and get the authorization URL
    auth_url = create_strava_oath()
    # redirect the user to the authorization URL
    return redirect(auth_url)

# route to handle the redirect URI after authorization
@app.route('/authorization')
def redirect_page():
    print('in redirect')
    # clear the session
    session.clear()
    # get the authorization code from the request parameters
    print('debug')
    code = request.args.get('code')
    print(code)
    # exchange the authorization code for an access token and refresh token
    token_info = client.exchange_code_for_token(client_id=STRAVA_CLIENT_ID,
                                              client_secret=STRAVA_CLIENT_SECRET,
                                              code=code)
    # save the token info in the session
    session[TOKEN_INFO] = token_info
    # redirect the user to the save_discover_weekly route
    return redirect(url_for('get_user_page',_external=True))


@app.route('/user_activities')
def get_user_page():
    try:
        # get the token info from the session
        token_info = get_token()
    except:
        # if the token info is not found, redirect the user to the login route
        print('User not logged in')
        return redirect("/")

    # so next step is to do after on this
    last_week = datetime.today() - timedelta(days=8)
    activities = client.get_activities(after=last_week)

    activity_list= []
    for activity in activities:
        my_dict = activity.to_dict()
        activity_list.append(my_dict)
        print(my_dict)

    # sorting activities on date
    activity_list.sort(key=lambda x: x['start_date_local'])

    routine_dict = prephase_csv_reader('workout_routines/Prephase_4_weeks.csv')

    variation_one = False
    variation_update(variation_one=variation_one, activity_list=activity_list, csv_routine_dict=routine_dict)


    return routine_dict


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
            spotify_oauth = create_strava_oath()
            token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

        return token_info

def create_strava_oath():
    url = client.authorization_url(client_id=STRAVA_CLIENT_ID,
                             redirect_uri='http://127.0.0.1:5000/authorization',
                             scope=['read_all', 'profile:read_all', 'activity:read_all','activity:write']
                             )
    return url

def prephase_csv_reader(file_name):
    with open(file_name, mode='r') as file:
        # reading the CSV file
        csvFile = csv.reader(file)

        # displaying the contents of the CSV file
        paragraph = " "
        routine_dict = {}
        for lines in csvFile:
            if lines != []:
                print(lines)
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

def variation_update(variation_one=True, activity_list=[], csv_routine_dict={}):

    if variation_one == False:
        upper = 'Upper 1'
    else:
        upper = 'Upper 2'

    day = 0
    for activity in activity_list:
        if activity['type'] == 'WeightTraining':
            if variation_one:
                print(activity['id'])
                if day == 0:
                    update_strava_activity(upper, csv_routine_dict,activity)

                if day == 1:
                    update_strava_activity('Lower 1',csv_routine_dict,activity)

                if day == 2:
                    update_strava_activity(upper, csv_routine_dict, activity)

                if day == 3:
                    update_strava_activity('Lower 2', csv_routine_dict, activity)

                if day == 4:
                    update_strava_activity(upper, csv_routine_dict, activity)

                day += 1

    return csv_routine_dict

def update_strava_activity( routine_key, routine_dict,activity):
    workout_title = routine_key
    description = routine_dict[routine_key]
    client.update_activity(activity['id'], name=workout_title, description=description)



app.run(debug=True)