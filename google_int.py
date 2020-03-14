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

class integration():
    def __init__(self, portal):
        self.creds = None
        self.SCOPES = ["https://www.googleapis.com/auth/calendar"]
        self.ser = None
        self.events = None
        self.info = None
        # mins before the assignment is due
        self.notifacationTime = 60

        # results pulled from google calendar
        self.googleCalenResults = 200

        self.tempPortal = None
        self.tempGoogle = None
        self.portalInfo = portal


    def creds(self):
        print("Getting Google Credentials...")
        """
        Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'googleCredentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.ser = build('calendar', 'v3', credentials=self.creds)

    def Getcalendar(self):
        # define new object for date lib
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        # print('Getting the upcoming 100 events')
        # todo: instead of pulling X events, pull events from now to the last date in the portal assignments
        events_result = self.ser.events().list(calendarId='primary', timeMin=now,
                                            maxResults=self.googleCalenResults, singleEvents=True,
                                            orderBy='startTime').execute()

        self.events = events_result.get('items', [])
        self.info = {}
        for a,b in enumerate(self.events):
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
            self.info[b["id"]] = dict

        return self.info

    def checkDuplicates(self):
        google = self.info
        portal = self.portalInfo

        dup = []
        for a, b in enumerate(portal):
            dupe = False
            for c, d in enumerate(google):
                self.tempGoogle = google[d]
                self.tempPortal = portal[b]

                # checks if there are any duplicates
                if str(self.tempPortal["assignmentId"]) in str(self.tempGoogle["summary"]):
                    dupe = True
                    dup.append(self.tempPortal["assignmentId"])
                    colorify.prRed("--- DUPLICATE DETECTED ---")
                    print("portal event: ", self.tempPortal["assignmentId"], " - ", self.tempPortal["entityTitle"])
                    print("google event", self.tempGoogle["summary"])
                    break

            if len(google) == 0:
                colorify.prGreen("DEBUG: No Events In Google Found")
                self.tempPortal = portal[b]
                # calling prepare event to add it to the google calendar
                self.prepareEvent()

            elif dupe is False:
                self.tempPortal = portal[b]
                # calling prepare event to add it to the google calendar
                self.prepareEvent()



    # adding events to the google calendar
    def prepareEvent(self):
        # how long the event will show up in google
        length = 5
        summary = self.tempPortal["entityTitle"] +" Assignment ID: "+ self.tempPortal["assignmentId"]
        startTime = self.tempPortal["due"] + "T" +self.tempPortal["dueTime"]+":00.00"

        mins = re.search(":[0-9]{2}",self.tempPortal["dueTime"]).group().strip(":")
        mins = int(mins) + length

        # adds a 0 if the minutes number is less than 10 to fit the syntax google expects
        if mins < 10:
            mins = str("0")+str(mins)
        hours = re.search("[0-9]{2}:",self.tempPortal["dueTime"]).group()
        endTime = self.tempPortal["due"]+"T"+str(hours)+str(mins)+":00.00"

        self.event = {
            'summary': summary,
            'description': self.tempPortal["entityTitle"],
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
                    {'method': 'popup', 'minutes': self.notifacationTime},
                ],
            },
        }

        # adding the above object in the google calendar
        self.insertEvent()

    def insertEvent(self):
        message = "Inserting event: "+ str(self.event["summary"])
        colorify.prGreen(message)

        event = self.ser.events().insert(
            calendarId='primary',
            body=self.event
        ).execute()
