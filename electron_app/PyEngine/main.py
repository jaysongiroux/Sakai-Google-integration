
# author: jason giroux
# purpose:
# use google API and SAKAI REST API to take assignments in bridges for rwu and transfer them to google calendar
# since some professors do not use the calendar this will combine the assignments section with the calendar section

# defining imports needed for this project

# todo:
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
        self.fetchedClasses = []
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
        counter = 0
        for a, b in enumerate(self.calJson):
            # appending to self.fetchedclasses if any class are new
            if a == 0 or not self.fetchedClasses[counter-1] == b["siteName"]:
                self.fetchedClasses.append(b["siteName"])
                counter = counter + 1

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
        # self.returnClassList()

    """
    fetches the assignments from sakai and stores them in self.contents
    """
    def getAssign(self):
        self.sak = SakaiPy.SakaiPy(self.info)
        self.assign = self.sak.get_assignment()
        self.assignDict = self.assign.getAllMyAssignments()
        self.assignDict = self.assignDict["assignment_collection"]
        assignDict = {}
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

    """
    calendar returns classes that you are not enrolled in. this method will look through the returns object 
    from the calendar and create a list of all the classes it pulled
    retuned list from cal = self.cal
    """
    def returnClassList(self):
        # a = counter, b = object
        for a, b in enumerate(self.calJson):
            print("printing b")
            print(b)
            temp = self.calJson[b]
            self.fetchedClasses.append(temp["siteName"])

        print("Fetched classes from Calendar: ", self.fetchedClasses)

    # load the JSON file into self.info
    # this is a getter method for the creds file.
    def permissive_json_loads(self):
        with open(self.text) as cred:
            self.info = json.load(cred)


# define the name of your classes to be scanned through and given a JSON file
classes = ["COMSC.492.01-20/SP Integ Senior Design II", "COMSC.410.01-20/SP Artificial Intelligence", "COMSC.440.01-20/SP LangTranslation/Compiler Dsgn", "PHYS.330.01-20/SP Intro Phys Oceanography" ]

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
m = "Classes detected: " + str(jason.fetchedClasses)
colorify.prGreen(m)
m = "TIME LAPSED: "+str(time_lapsed)+" s"
colorify.prRed(m)
