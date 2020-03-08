# Sakai with Google Calendar Integration
### Objective:
Use this bot to act as a middle man with the Sakai web platform and integrate with google products. As of right now this can only be ran locally.
However, this project will be ported over to be used as a service in the cloud. 

### Features:
- Pulls from Sakai:
  - Assignments
  - Calendar
- Checks between assignments and calendar if there is any duplicates
- Creates a JSON file with all the assignments from Sakai
- Pulls events from current google calendar
- Checks if there are duplicates between the JSON file and the google calendar events
- Inserts events into your google calendar that are 5 min blocks with a pop-up notification 1 hour before due.

### Todo:
- Front end
- Can be run with multiple users
- Make variables at the top that can be modified to fit the user’s need


### Setup:
- Create a JSON file in the base directory called "creds.json"
```
{
  "username": "username",
  "password": "password",
  "baseurl": "schoolPortalURL",
}
```
- ```pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib```
- ```pip install pickle```
- Run: ```python main.py```
- The setup wizard will walk you through how to setup with google apps.
 
 ### Additional Notes:
 - Some schools do not allow this bot to be run on their internet. This has been tested outside of the school's internet. 
 - This Project is in no association with any college.
