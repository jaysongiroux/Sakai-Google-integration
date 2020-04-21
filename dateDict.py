"""
This file is used for separating information and parsing it into a format that python can read
and create comparisons between.

example input: Mar 3, 2020 2:00 pm
need to turn that into mm/dd/yyyy format w/ sep time

todo:
- time comparison not just date comparison for if an assignment is late.
"""

import re
from datetime import *
import colorify


def combineTime(dateString):
    return str(seperateHour(dateString)) + ":" + str(seperateMin(dateString))

def dateFormat(dateString):
    return seperateYear(dateString)+"-"+str(dict(dateString))+"-"+seperateDay(dateString)

def dateSlashes(dateString):
    return str(dict(dateString)),seperateDay(dateString),seperateYear(dateString)


# return false if the assignment is not late
def isLate(dateString,id):
    month,day,year = dateSlashes(dateString)
    assignment = datetime(int(year),int(month),int(day))
    current = datetime.now()

    # if assignment is due in the future or due same day as ran
    if assignment > current or assignment == current:
        colorify.prGreen("---- Not Late ----")
        print("ID: ", id)
        print("Cal: Assignment Date (mm,dd,yyyy): ",month,"-",day,"-",year)
        return False
    else:
        colorify.prRed("---- Late ----")
        print("ID: ", id)
        print("Cal: Assignment Date (mm,dd,yyyy): ",month,"-",day,"-",year)
        return True

# sep am or pm and returns the am or pm
def seperateTime(dateString):
    return re.search("(am)|(pm)", dateString).group()


def seperateHour(dateString):
    x = re.search("(([0-9]{2})|([0-9])):",dateString).group().strip(":")
    if int(x) < 10:
        x = str("0")+str(x)
    return x


# seperate time from date string
def seperateMin(dateString):
    return re.search(":[0-9]{2}",dateString).group().strip(":")


def seperateDay(dateString):
    return re.search("([0-9]|[0-9]{2})+,",dateString).group().strip(",")


# seperate and return the year from the string
def seperateYear(dateString):
    return re.search("[0-9]{4}",dateString).group()

# used as a dict for portal when returning months
def dict(month):
    if "Jan" in month:
        return 1
    elif "Feb" in month:
        return 2
    elif "Mar" in month:
        return 3
    elif "Apr" in month:
        return 4
    elif "May" in month:
        return 5
    elif "Jun" in month:
        return 6
    elif "Jul" in month:
        return 7
    elif "Aug" in month:
        return 8
    elif "Sep" in month:
        return 9
    elif "Oct" in month:
        return 10
    elif "Nov" in month:
        return 11
    elif "Dec" in month:
        return 12


"""
To return true or false if the given date is considered late or not late to the day this script is run
true = LATE
false = NOT LATE 
"""
def assignIsLate(dateString,id):
    total = re.search("[0-9]{4}-[0-9]{2}-[0-9]{2}",dateString).group()

    year = re.search("[0-9]{4}",str(total)).group()

    month = re.search("-[0-9]{2}-",str(total))
    month = re.search("[0-9][0-9]",str(month)).group()

    day = re.search("-[0-9][0-9]T",dateString).group().strip("T").strip("-")

    assignment = datetime(int(year), int(month), int(day))
    current = datetime.now()

    # if assignment is due in the future or due same day as ran
    if assignment > current or assignment == current:
        colorify.prGreen("---- Not Late ----")
        print("assignment ID: ",id)
        print("Assign: Assignment Date (mm,dd,yyyy): ", month, "-", day, "-", year)
        return False
    else:
        colorify.prRed("---- Late ----")
        print("assignment ID: ",id)
        print("Assign: Assignment Date (mm,dd,yyyy): ", month, "-", day, "-", year)
        return True


def returnDateAndTimeAssign(dateString):
    total = re.search("[0-9]{4}-[0-9]{2}-[0-9]{2}",dateString).group()
    year = re.search("[0-9]{4}",str(total)).group()
    month = re.search("-[0-9]{2}-",str(total))
    month = re.search("[0-9][0-9]",str(month)).group()
    day = re.search("-[0-9][0-9]T",dateString).group()
    day = re.search("[0-9][0-9]",str(day)).group()

    time = re.search("[0-9]{2}:[0-9]{2}:[0-9]{2}", dateString).group()
    hour = re.search("^[0-9]{2}:", time).group().strip(":")
    minute = re.search(":[0-9]{2}:", time).group().strip(":")

    dt = str(year)+"-"+str(month)+"-"+str(day)
    time = str(hour) + ":" + str(minute)

    return dt, time

# return true if the event has been res
# todo: finish this function. right now this seperates the google time down next will need comparisons for date and time
def isResched(portalTime, portalDate, google):
    '''
    split the google format into comparable chunks using the date time library
    '''
    googleTime = re.search("T[0-9]{2}:[0-9]{2}").group().strip("T")

    print("checking")
    return True


# test information
# portalTime = "04:00"
# portalDate = "2020-5-5"
# googleStart = "2020-05-05T04:00:00-04:00"
# isResched(portalTime,portalDate,googleStart)