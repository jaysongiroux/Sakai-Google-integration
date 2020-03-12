"""
this file is to tie in the google developer account using their api.
will configure later for non-developer accounts using SSO
"""
from __future__ import print_function
import json
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import re
import colorify


def creds():
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'googleCredentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    ser = build('calendar', 'v3', credentials=creds)
    return ser


def Getcalendar(ser):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 100 events')
    events_result = ser.events().list(calendarId='primary', timeMin=now,
                                        maxResults=100, singleEvents=True,
                                        orderBy='startTime').execute()

    events = events_result.get('items', [])
    # print(events)
    info = {}
    for a,b in enumerate(events):
        dict = {
            "summary":b["summary"],
            "creator":b["creator"],
            "status":b["status"],
            "organizer":b["organizer"],
            "link":b["htmlLink"],
            "start":b["start"],
            "end":b["end"],
            "reminders":b["reminders"]
        }
        info[b["id"]] = dict

    # writing to json file, no longer needed
    with open("googleCalparsed.json", 'w') as f:
        json.dump(info, f, indent=2)

    return info


def checkDuplicates(ser):
    with open("googleCalparsed.json",'r') as f:
        google = json.load(f)

    with open("final.json",'r') as a:
        portal = json.load(a)

    dup = []
    for a, b in enumerate(portal):
        dupe = False
        for c, d in enumerate(google):
            tempGoogle = google[d]
            tempPortal = portal[b]

            # checks if there are any duplicates
            if str(tempPortal["assignmentId"]) in str(tempGoogle["summary"]):
                dupe = True
                dup.append(tempPortal["assignmentId"])
                colorify.prRed("--- DUPLICATE DETECTED ---")
                print("portal event: ", tempPortal["assignmentId"], " - ", tempPortal["entityTitle"])
                print("google event", tempGoogle["summary"])
                break

        # inserting element
        if dupe is False:
            prepareEvent(tempPortal,ser)

        # no existing elements in the google calendar
        if len(google) == 0:
            colorify.prGreen("DEBUG: No Events In Google Found")
            tempPortal = portal[b]
            prepareEvent(tempPortal, ser)


# adding events to the google calendar
def prepareEvent(tempPortal,ser):
    # how long the event will show up in google
    length = 5
    summary = tempPortal["entityTitle"] +" Assignment ID: "+ tempPortal["assignmentId"]
    startTime = tempPortal["due"] + "T" +tempPortal["dueTime"]+":00.00"

    mins = re.search(":[0-9]{2}",tempPortal["dueTime"]).group().strip(":")
    mins = int(mins) + length

    # adds a 0 if the minutes number is less than 10 to fit the syntax google expects
    if mins < 10:
        mins = str("0")+str(mins)

    hours = re.search("[0-9]{2}:",tempPortal["dueTime"]).group()
    endTime = tempPortal["due"]+"T"+str(hours)+str(mins)+":00.00"

    event = {
        'summary': summary,
        'description': tempPortal["entityTitle"],
        'start': {
            'dateTime': startTime,
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': endTime,
            'timeZone': 'America/New_York',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 60},
            ],
        },
    }
    insertEvent(event, ser)


def insertEvent(obj,ser):
    message = "Inserting event: "+ str(obj["summary"])
    colorify.prGreen(message)
    event = ser.events().insert(
        calendarId='primary',
        body=obj
    ).execute()


# can uncomment this if both the json files are populated and you want to test just the google
# integration functionality
if __name__ == '__main__':
    ser = creds()
    Getcalendar(ser)
    checkDuplicates(ser)