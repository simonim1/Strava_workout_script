from Secrets.secrets import CLIENT_ID
from stravalib.client import Client

############################################
#               constants                  #
############################################
CONST_ACTIVTY = 'WeightTraining'
REDIRECT_URI = 'http://127.0.0.1:5000/authorization'
SCOPE_LIST = ['read_all', 'profile:read_all', 'activity:read_all', 'activity:write']
DEFAULT_WEIGHTRAINING_TITLES = ['Morning Weight Training','Lunch Weight Training', 'Night Weight Training', 'Afternoon Weight Training']

class Strava:
    def __init__(self):
        self.strava_client = Client()

    def create_strava_oath(self):
        '''
        :return: Return the oauth URL needed to login to strava application
        '''
        url = self.client.authorization_url(client_id=CLIENT_ID,
                                       redirect_uri=REDIRECT_URI,
                                       scope=SCOPE_LIST
                                       )
        return url

    def update_strava_activity(self,routine_key, routine_dict, activity):
        '''
        :param routine_key: The csv string of day you are wanting to write
        :param routine_dict: the workout routine dictionary
        :param activity: strava activity object
        :return: rewrite activity and send the resonse
        '''
        try:
            workout_title = self.update_activity_name(activity,routine_key)
            description = self.update_description(activity,routine_dict[routine_key])

            res = self.strava_client.update_activity(activity['id'], name=workout_title, description=description)
        except Exception as  e:
            print("error calling strava api")
            print(e)

        return res.json()

    def update_activity_name(self,activity, routine_title):
        '''
        :param activity: is an activity object from Strava
        :param routine_title: the title of the csv routine day
        :return: some strava workouts when imported I change the title, in this case I want to append the work out day
        to the title else it can be rewritten
        '''
        if activity['name'] in DEFAULT_WEIGHTRAINING_TITLES:
            return routine_title
        return activity['name'] + ' ' + routine_title

    def update_description(self,activity, description):
        '''
        :param activity:
        :param description:
        :return:some strava workouts when imported I change the discription, in this case I want to append the work out description
        to the description else it can be rewritten
        '''
        if activity['description'] == None:
            return description
        return activity['description'] + '\n' + description

    def get_weight_traning_activities(self, after):
        '''
        :param after: Datetime object of the start date of all the weight training activites you get
        :return: list of dictionaries that are weight training activities
        '''
        try:
            weight_trainings_list = []
            activities = self.strava_client.get_activities(after=after)

            for activity in activities:
                my_dict = activity.to_dict()
                if activity['type'] == 'WeightTraining':
                    weight_trainings_list.append(my_dict)

            # sorting activities on date
            weight_trainings_list.sort(key=lambda x: x['start_date_local'])
            return weight_trainings_list

        except Exception as e:
            print(" Error grabbing weight training activities ")
            print(e)




    def csv_prefase_weight_training_update(self,variation_one=True, activity_list=[], csv_routine_dict={}):
        '''
        :param variation_one: Boolean to be variation 2 or 1 default to be variation 1 ( look in read me to userstand variation)
        :param activity_list: list of activites from strava
        :param csv_routine_dict: dictionary with
        :return: return the workout routing
        '''
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
                        self.update_strava_activity(upper, csv_routine_dict,activity)
                    if day == 1:
                        self.update_strava_activity('Lower 1',csv_routine_dict,activity)
                    if day == 2:
                        self.update_strava_activity(upper, csv_routine_dict, activity)
                    if day == 3:
                        self.update_strava_activity('Lower 2', csv_routine_dict, activity)
                    if day == 4:
                        self.update_strava_activity(upper, csv_routine_dict, activity)
                    day += 1

        return csv_routine_dict