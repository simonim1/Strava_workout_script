import requests
import time
import pickle
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
    activities = client.get_activities(after=)

    for activity in activities:
        my_dict = activity.to_dict()
        print(my_dict)

    act = client.get_activity(9305059575)
    temp = act.to_dict()
    print(temp)
    return temp


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


app.run(debug=True)