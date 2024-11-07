account_id = ""
client_id= ""
client_secret= ""
# secrete token: ""
# verification token: ""


# curl -X POST https://zoom.us/oauth/token -d 'grant_type=account_credentials' -d 'account_id=account_id' -H 'Host: zoom.us' -H 'Authorization: Basic base64(client_id:client_secret)'


import requests
import pandas as pd


def get_token(account_id):
    # Replace these values with your actual credentials

    # OAuth token URL
    url = "https://zoom.us/oauth/token"

    # Set up the parameters and authentication for the request
    payload = {
        "grant_type": "account_credentials",
        "account_id": account_id
    }
    # Set headers for form data
    headers = {
        "Host": "zoom.us",
        "Authorization": f"Basic HTTPBasicAuth(client_id, client_secret)"
    }

    # Make the POST request
    response = requests.post(url, data=payload, headers=headers)
    access_token = None
    # Handle the response
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print(f"Access Token: {access_token}")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
    return access_token


def get_meeting_reports(month):
    access_token = get_token(account_id)
    if access_token:
        url = f"https://api.zoom.us/v2/report/daily?year=2024&month={month}"

        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)

        return response.json()
    else:
        return False
    

def list_all_meetings(access_token,typeOfMeeting):
    if access_token:
        url = f"https://api.zoom.us/v2/users/email/meetings?type={typeOfMeeting}&page_size=300"

        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)

        return response.json()
    else:
        return False
    
    
def get_participant_reports(access_token,meeting_id):
    if access_token:
        url = f"https://api.zoom.us/v2/report/meetings/{meeting_id}/participants?page_size=300"

        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)

        return response.json()
    else:
        return False
    
    
access_token = get_token(account_id)
scheduled_all_meetings = list_all_meetings(access_token,"scheduled")

lst = []
if scheduled_all_meetings:
    for meeting in scheduled_all_meetings['meetings']:
        participant_records = get_participant_reports(access_token,meeting.get('id'))
        if participant_records:
            try:
                for participant in participant_records.get('participants'):
                    
                    lst.append({
                        "uuid":meeting.get('uuid'),
                        "id":meeting.get('id'),
                        "host_id":meeting.get('host_id'),
                        "topic":meeting.get('topic'),
                        "type":meeting.get('type'),
                        "duration":meeting.get('duration'),
                        "timezone":meeting.get('timezone'),
                        "created_at":meeting.get('created_at'),
                        "join_url":meeting.get('join_url'),
                        "participant_id":participant.get('id'),
                        "user_id":participant.get('user_id'),
                        "name":participant.get('name'),
                        "user_email":participant.get('user_email'),
                        "join_time":participant.get('join_time'),
                        "leave_time":participant.get('leave_time'),
                        "duration":participant.get('duration'),
                        "attentiveness_score":participant.get('attentiveness_score'),
                        "failover":participant.get('failover'),
                        "status":participant.get('status'),
                        "groupId":participant.get('groupId'),
                        "customer_key":participant.get('customer_key'),
                    })
            except Exception as e:
                print("Error on line number 123: ",str(e))
                print(participant_records)
        else:
            print(f"No Participant Found for this meeting {meeting.get('id')}")
else:
    print("No Scheduled meeting found")

print(f"Complete Data: {lst}")
data = pd.DataFrame(lst)
data.to_csv('complete_record.csv')


upcoming_meetings = list_all_meetings(access_token,"upcoming")
print(f"upcoming_meetings: {upcoming_meetings}")
