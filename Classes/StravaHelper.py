from Secrets.secrets import

CONST_ACTIVTY = 'WeightTraining'

class StravaHelper:
    def __init__(self):
        self.auth_url =

    def _create_strava_oath():
        url = client.authorization_url(client_id=STRAVA_CLIENT_ID,
                                       redirect_uri='http://127.0.0.1:5000/authorization',
                                       scope=['read_all', 'profile:read_all', 'activity:read_all', 'activity:write']
                                       )
        return url