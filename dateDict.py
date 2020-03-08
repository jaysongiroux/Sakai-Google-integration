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


def combineTime(dateString):
    h = seperateHour(dateString)
    m = seperateMin(dateString)
    combined = str(h) + ":" + str(m)
    return combined

def dateFormat(dateString):
    month = dict(dateString)
    day = seperateDay(dateString)
    year = seperateYear(dateString)
    combined = str(year)+"-"+str(month)+"-"+str(day)
    return combined

def dateSlashes(dateString):
    month = dict(dateString)
    day = seperateDay(dateString)
    year = seperateYear(dateString)
    return month,day,year

# return false if the assignemtn is not late
def isLate(dateString,id):
    month,day,year = dateSlashes(dateString)
    # print("year: ", year)
    # print("month: ", month)
    # print("day: ", day)
    assignment = datetime(int(year),int(month),int(day))
    current = datetime.now()

    # if assignment is due in the future or due same day as ran
    if assignment > current or assignment == current:
        print("ID: ", id)
        print("Cal: Assignment Date (mm,dd,yyyy): ",month,"-",day,"-",year)
        print("Not late")
        print("----")
        return False
    else:
        print("ID: ", id)
        print("Cal: Assignment Date (mm,dd,yyyy): ",month,"-",day,"-",year)
        print("Late")
        print("----")
        return True


# seperates am or pm and returns the am or pm
def seperateTime(dateString):
    x = re.search("(am)|(pm)", dateString)
    x = x.group()
    print("sep time: ", x)
    return x

def seperateHour(dateString):
    x = re.search("(([0-9]{2})|([0-9])):",dateString)
    x = x.group()
    x = x.strip(":")
    if int(x) < 10:
        x = str("0")+str(x)

    # print("hour: ", x)
    return x


# seperate time from date string
def seperateMin(dateString):
    x = re.search(":[0-9]{2}",dateString)
    x = x.group()
    x = x.strip(":")
    # removes colon\
    print("date string: ", dateString)
    print("seperate Min: ", x)
    return x


def seperateDay(dateString):
    print("date string",dateString)
    x = re.search("([0-9]|[0-9]{2})+,",dateString)
    x = x.group()
    temp = x.strip(",")
    return temp


# seperate and return the year from the string
def seperateYear(dateString):
    x = re.search("[0-9]{4}",dateString)
    x = x.group()
    return x

# Thanks Emily for making sure my months are in order
def dict(month):
    if "Jan" in month:
        return 1
    elif "Feb" in month:
        return 2
    elif  "Mar" in month:
        return 3
    elif  "Apr" in month:
        return 4
    elif  "May" in month:
        return 5
    elif  "Jun" in month:
        return 6
    elif  "Jul" in month:
        return 7
    elif  "Aug" in month:
        return 8
    elif  "Sep" in month:
        return 9
    elif  "Oct" in month:
        return 10
    elif  "Nov" in month:
        return 11
    elif  "Dec" in month:
        return 12
    else:
        return "Error"

"""
Date parsing for assignments
"""
def assignIsLate(dateString,id):
    print("late date string: ", dateString)
    total = re.search("[0-9]{4}-[0-9]{2}-[0-9]{2}",dateString)
    total = total.group()

    year = re.search("[0-9]{4}",str(total))
    year = year.group()

    month = re.search("-[0-9]{2}-",str(total))
    month = re.search("[0-9][0-9]",str(month))
    month = month.group()

    day = re.search("-[0-9][0-9]T",dateString)
    day = day.group()
    day = day.strip("T")
    day = day.strip("-")

    assignment = datetime(int(year), int(month), int(day))
    current = datetime.now()

    # if assignment is due in the future or due same day as ran
    if assignment > current or assignment == current:
        print("----")
        print("assignment ID: ",id)
        print("Assign: Assignment Date (mm,dd,yyyy): ", month, "-", day, "-", year)
        print("Not late")
        print("----")
        return False
    else:
        print("----")
        print("assignment ID: ",id)
        print("Assign: Assignment Date (mm,dd,yyyy): ", month, "-", day, "-", year)
        print("Late")
        print("----")
        return True


def returnDateAndTimeAssign(dateString):
    # print("Date String: ", dateString)
    total = re.search("[0-9]{4}-[0-9]{2}-[0-9]{2}",dateString)
    total = total.group()
    year = re.search("[0-9]{4}",str(total))
    year = year.group()
    month = re.search("-[0-9]{2}-",str(total))
    month = re.search("[0-9][0-9]",str(month))
    month = month.group()
    day = re.search("-[0-9][0-9]T",dateString)
    day = day.group()
    # print("Day: ", day)
    day = re.search("[0-9][0-9]",str(day))
    day = day.group()
    # print("day2: ", day)
    dt = str(year)+"-"+str(month)+"-"+str(day)

    time = re.search("[0-9]{2}:[0-9]{2}:[0-9]{2}",dateString)
    time = time.group()
    hour = re.search("^[0-9]{2}:",time)
    hour = hour.group()
    hour = hour.strip(":")
    minute = re.search(":[0-9]{2}:",time)
    minute = minute.group()
    minute = minute.strip(":")
    time = str(hour) + ":" + str(minute)

    # print("dt, time", dt, time)
    return dt, time
