# Strava_workout_script
I started getting into body building routines and I track them in strava.
Some friends were curious about my routine, and I do like putting my notes about my routine in the app. 
The problem is that typing it all on my phone is alot for each workout.
Here is a script to write what work out day I was doing and all the movements I did . 

## How others can use this
this is more for people that work out 5 days a week but you can doctor my scripts for you as well.
what is needed
* a csv of all the workouts 
* strava application

### How to Run the application
#### python Libs needed 
```commandline
pip install flask
```
[Here ](https://flask.palletsprojects.com/en/3.0.x/)is the documentation for flask. I used flask to help handle the authentication of the script. 
```commandline
pip install stravalib
```
When looking at strava api documentation from  [this medium article](https://medium.com/analytics-vidhya/accessing-user-data-via-the-strava-api-using-stravalib-d5bee7fdde17) was a huge help on simple commands and how to go about
the strava api . The article is more on a manual approach of what I wanted to do which is where flask comes in. 
Along with the article I used [Strava's api](https://developers.strava.com/docs/reference/) documentation and the [github repo](https://github.com/stravalib/stravalib) to help learn more about the stravalib library.

## Running
for running one will have to make their own application through Strava's developer website as mentioned in the 
medium article. Then a user will have to create a secrets.py in the Secrets folder and put CLIENT_ID and CLIENT_SECRET in the file. 
```python
CLIENT_ID = '<string here> '
CLIENT_SECRET = '<string here>'
```
once this is in place the dev should just be able to run main.py with the command bellow
```commandline
python3 main.py
```

### Notes from the dev
This is a tool mostly to help writing descriptions better for each workout I did. Along with that though I wanted to show 
Strava I am super interested in their company and used their api to make a tool. I use strava alot and would love to
program for them one day. 