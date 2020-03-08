# Sakai with Google Calendar Integration
### Objective:
Use this bot to act as a middle man with the Sakai web platform and integrate with google products. As of right now this can only be ran locally.
However, this project will be ported over to be used as a service in the cloud. 

### Todo:
- Parse through currently enrolled classes and insert into google calendar
- Custom settings for announcements  

### Setup:
- Create a JSON file in the base directory called "creds.json"
```
{
  "username": "username",
  "password": "password",
  "baseurl": "schoolPortalURL",
  "client":"google client api string"
  "secret":"google secret api string"
}
```
- ```pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib```
- ```pip install pickle```
- Run: ```python main.py```
- The setup wizard will walk you through how to setup with google apps.
 
 ### Additional Notes:
 - Some schools do not allow this bot to be run on their internet. This has been tested outside of the school's internet. 
 - This Project is in no association with any college.
