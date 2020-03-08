
# author: jason giroux
# purpose:
# use google API and SAKAI REST API to take assignments in bridges for rwu and transfer them to google calendar
# since some professors do not use the calendar this will combine the assignments section with the calendar section

# defining imports needed for this project

# todo:
#


from SakaiPy import SakaiPy
import json
import dateDict
import combineJson
import google_int

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


    def permissive_json_loads(self):
        with open(self.text) as cred:
            self.info = json.load(cred)

    """
    get calendar from sakai and output to a json file and return a json object
    exlcude classes you are not enrolled in, and assignments that have already passed
    """
    def getCal(self):
        self.sak = SakaiPy.SakaiPy(self.info)
        # used for debugging
        # print(self.sak.session.get_current_user_info())
        self.calendar = self.sak.get_calendar()
        self.calDict = self.calendar.getAllMyEvents()
        self.calStrJson = json.dumps(self.calDict, ensure_ascii=False)
        self.calPartJson = json.loads(self.calStrJson)

        self.calJson = self.calPartJson["calendar_collection"]
        assDict = {}

        # a is the counter
        # b is the json object
        """
        loop through and add to json file if it matches the classes you define above
        """
        for a, b in enumerate(self.calJson):
            # loops through classes to check for dupes
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


        """
        writing to the json file iterated through by the above loop
        """
        self.cal = assDict
        # with open('parsed.json', 'w') as f:
        #     json.dump(assDict, f, indent=2)
        #     f.close()

    def getAssign(self):
        self.sak = SakaiPy.SakaiPy(self.info)
        self.assign = self.sak.get_assignment()
        self.assignDict = self.assign.getAllMyAssignments()
        self.assignDict = self.assignDict["assignment_collection"]
        temp = []
        # determine if there are duplicate assignemts
        # todo: clean this up
        assignDict = {}
        for a, b in enumerate(self.assignDict):
            try:
                if self.cal[b["id"]]:
                    continue
            except KeyError as err:
                # if it is not  late add to json
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

# define the name of your classes to be scanned through and given a JSON file
classes = ["COMSC.492.01-20/SP Integ Senior Design II"]
# classes = []
jason = main(classes)
jason.permissive_json_loads()
jason.getCal()
jason.getAssign()

combineJson.start(jason.contents, jason.cal)
service = google_int.creds()
google_int.Getcalendar(service)
google_int.checkDuplicates(service)

