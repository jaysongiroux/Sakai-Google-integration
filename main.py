
# author: jason giroux
# purpose:
# use google API and SAKAI REST API to take assignments in bridges for rwu and transfer them to google calendar
# since some professors do not use the calendar this will combine the assignments section with the calendar section

# defining imports needed for this project

# todo:
#   pull a list from the entire returned object of assignments and cal and make a list of the classes
#     allow the user to choose which classes they are apart of
#   optimize adding to google calendar by sending single json object instead of multiple single json objects
#   check for assignemnts and cal assignemts that have a changed date or changed time, cancel the originally scheduled event and reschedule with new time/date
#   worst case scenario, time is at 10.719 seconds for initial run to add all assignments. need to cut down to 5 seconds.

from SakaiPy import SakaiPy
import json
import dateDict
import combineJson
from google_int import integration
import threading
import time
import colorify

class main():
    def __init__(self, classes):
        #credentials  file for login
        self.text = "creds.json"

        # raw load for class info before parsing
        self.info = ""

        #  calendar
        self.sak = ""
        self.calendar = ""
        self.calDict = ""
        self.calStrJson = ""
        self.calPartJson = ""
        self.cal = ""

        # assignments
        self.assign = ""
        self.assignDict = ""
        self.assignStrJson = ""
        self.assignPartJson = ""
        self.assignJson = ""
        self.assignCal = ""

        self.classes = classes
        self.contents = ""

    """
    get calendar from sakai and output to a json file and return a json object
    exclude classes you are not enrolled in, and assignments that have already passed
    """
    def getCal(self):
        self.sak = SakaiPy.SakaiPy(self.info)
        self.calendar = self.sak.get_calendar()
        self.calDict = self.calendar.getAllMyEvents()
        self.calStrJson = json.dumps(self.calDict, ensure_ascii=False)
        self.calPartJson = json.loads(self.calStrJson)

        self.calJson = self.calPartJson["calendar_collection"]
        assDict = {}

        # a is the counter
        # b is the json object

        # loop through and add to json file if it matches the classes you define above
        for a, b in enumerate(self.calJson):
            # since Sakai returns classes you have taken in last semester you will need to define the classses you
            # are currently enrolled in.
            for i in range(len(self.classes)):
                temp = b["firstTime"]
                # determines if it matches your classes and if the assignment is late.
                if b["siteName"] == self.classes[i] and not dateDict.isLate(temp["display"],b["assignmentId"]):
                    info = {
                        "assignmentId": b["assignmentId"],
                        "entityTitle": b["entityTitle"],
                        "siteName": b["siteName"],
                        "due": dateDict.dateFormat(temp["display"]),
                        "dueTime": dateDict.combineTime(temp["display"]),
                        "instructions": b["description"],
                        "title": b["title"],
                        "type": b["type"]
                    }
                    assDict[b['assignmentId']] = info
                else:
                    continue

        self.cal = assDict


    def getAssign(self):
        self.sak = SakaiPy.SakaiPy(self.info)
        self.assign = self.sak.get_assignment()
        self.assignDict = self.assign.getAllMyAssignments()
        self.assignDict = self.assignDict["assignment_collection"]
        assignDict = {}
        print(self.assignDict)
        for a, b in enumerate(self.assignDict):
            try:
                if self.cal[b["id"]]:
                    continue

            except KeyError as err:
                # if it is not late add to json
                if not dateDict.assignIsLate(b["dueTimeString"], b["id"]):
                    due, time = dateDict.returnDateAndTimeAssign(b["dueTimeString"])
                    assignInfo = {
                        "assignmentId": b["id"],
                        "entityTitle": b["entityTitle"],
                        "instructions": b["instructions"],
                        "gradebookItemName": b["gradebookItemName"],
                        "due": due,
                        "dueTime": time,
                        "title": b["title"],
                        "type": b["status"]
                    }
                    assignDict[b['id']] = assignInfo
                else:
                    continue

        self.contents = assignDict

    def returnClassList(self):
        return True

    # load the JSON file into self.info
    # this is a getter method for the creds file.
    def permissive_json_loads(self):
        with open(self.text) as cred:
            self.info = json.load(cred)


# define the name of your classes to be scanned through and given a JSON file
classes = ["COMSC.492.01-20/SP Integ Senior Design II"]

start_time = time.time()

jason = main(classes)
jason.permissive_json_loads()

t1 = threading.Thread(target=jason.getCal())
t2 = threading.Thread(target=jason.getAssign())

t1.start()
t2.start()
t1.join()
t2.join()

portal = combineJson.start(jason.contents, jason.cal)
inter = integration(portal)

integration.creds(inter)
integration.Getcalendar(inter)
integration.checkDuplicates(inter)

end_time = time.time()
time_lapsed = end_time - start_time
m = "TIME LAPSED: "+str(time_lapsed)+" s"
colorify.prRed(m)
