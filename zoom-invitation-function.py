import jwt
import requests
import json
from time import time


# Enter your API key and your API secret
API_KEY = 'API-KEY'
API_SEC = 'API-SECRET'

# create a function to generate a token
# using the pyjwt library


def generateToken():
	token = jwt.encode(

		# Create a payload of the token containing
		# API Key & expiration time
		{'iss': API_KEY, 'exp': time() + 5000},

		# Secret used to generate token signature
		API_SEC,

		# Specify the hashing alg
		algorithm='HS256'
	)
	return token


# create json data for post requests
meetingdetails = {"topic": "The title of your zoom meeting",
				"type": 2,
				"start_time": "2019-06-14T10: 21: 57",
				"duration": "45",
				"timezone": "Asia/Karachi",
				"agenda": "test",

				"recurrence": {"type": 1,
								"repeat_interval": 1
								},
				"settings": {"host_video": "true",
							"participant_video": "true",
							"join_before_host": "False",
							"mute_upon_entry": "False",
							"watermark": "true",
							"audio": "voip",
							"auto_recording": "cloud"
							}
				}

# send a request with headers including
# a token and meeting details


def createMeeting():
	headers = {'authorization': 'Bearer ' + generateToken(),
			'content-type': 'application/json'}
	r = requests.post(
		f'https://api.zoom.us/v2/users/me/meetings',
		headers=headers, data=json.dumps(meetingdetails))

	print("\n creating zoom meeting ... \n")
	# print(r.text)
	# converting the output into json and extracting the details
	y = json.loads(r.text)
	join_URL = y["join_url"]
	meetingPassword = y["password"]

	print(
		f'\n here is your zoom meeting link {join_URL} and your \
		password: "{meetingPassword}"\n')


# run the create meeting function
createMeeting()