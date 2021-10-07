#!/usr/bin/env python3
# datecompare_python.py
# version 0.2
# By Allan Taylor
# 10/05/2021
#
# Problem statement: User should be able to compare two dates in the following 
# format: MM/DD/YYYY
#
# Optionally, the user may input timestamp data in the following format: 
# HH:mm:SS
#
# The program should compare on date values only: it should ignore whether the
# timestamps themselves are different, and compare only on day, month, and 
# year values.
#
# Also, the program should account for basic variation in how single day and 
# month values are input: that is, it should be able to tell that literals 
# such as '01' and '1' represent the same value, and compare them accordingly.
#
#
# Usage: 
# In Windows CMD window: py datecompare_python.py
# In Bash: python3 datecompare_python.py
#
# Revisions:
#
# 0.1 - 10/05-10/06/2021: initial commit, syntax, logic error correction as 
#     described in the Git revision log
#
# 0.2 - 10/07/2021: Added function to create ISO formatted date strings, take
#     date objects, compare them, return value describing relation of first 
#     parameter to second parameter. Named this new function compareDateObjects.
#     Changed the name of old function compareDateObjects to compareDateStrings,
#     to more accurately reflect it's new functionality. Changed some variable names
#     in the main body to reflect the difference between string and date object
#     responsibility. Added functionality to return report of date relations. 
#     Updated comments in main body to reflect introduction of date objects.
#

from datetime import date
from datetime import timedelta
import sys
import re
import string




# validate if the digit(s) representing the day comprise a valid
# day of the month (01-31)
def validateDayInput(inputDay):
    filter = re.compile(r'(^0?[1-9]$|^[12][0-9]$|^3[01]$)')
    matchedNumber = filter.match(inputDay)
    if (matchedNumber):
        return True

    return False

# validate if the digit(s) representing the month comprise a valid
# month of the year (01-12)
def validateMonthInput(inputMonth):
    filter = re.compile(r'(^1[0-2]$|^0?[1-9]$)')
    matchedNumber = filter.match(inputMonth)
    if (matchedNumber):
        return True

    return False

# validate if the digit(s) representing the year comprise a valid
# 4 digit year (0000-9999)
# This check is far less stringent than the other two
def validateYearInput(inputYear):
    filter = re.compile(r'(^[0-9]{4}$)')
    matchedNumber = filter.match(inputYear)
    if (matchedNumber):
        return True

    return False

# returns 4 digit year data that does not include timestamp data
# (that is, HH:mm:SS data)
def returnSanitizedYear(inputYear):
    filter = re.compile(r'(^[0-9]{4})')
    matchedNumber = filter.match(inputYear)
    if (matchedNumber):
        return matchedNumber.group()

    return None

# Creates ISO formatted string: YYYY-MM-DD
def returnISOFormattedString(inputYear, inputMonth, inputDay):
    # If one of these parameters is None, no point in trying to build a
    # string from them, return None. Otherwise return the ISO formatted
    # hyphenated string.
    if ((inputYear != None) and (inputMonth != None) and (inputDay != None)):
        # This needs to be done for inputDay and inputMonth: for ISO formatting,
        # both of these values NEED to be two digits, regardless of what the user
        # input.
        workInputDay = re.sub(r'^[1-9]$', '0' + inputDay, inputDay)
        workInputMonth = re.sub(r'^[1-9]$', '0' + inputMonth, inputMonth)
        return inputYear + "-" + workInputMonth + "-" + workInputDay

    return None

# boolean function, performs comparison on values treated as days
# in the date data
def compareDays(baseDay, compareDay):
    # Stick a 0 in front of any single digit string, so that we may
    # compare apples to apples. If the string already has 2 digits
    # in it, the string will remain unchanged.
    workBaseDay = re.sub(r'^[1-9]$', '0' + baseDay, baseDay)
    workCompareDay = re.sub(r'^[1-9]$', '0' + compareDay, compareDay)
    
    if (workBaseDay == workCompareDay):
        return True

    return False

# boolean function, performs comparison on values treated as months in the
# date data
def compareMonths(baseMonth, compareMonth):
    # Stick a 0 in front of any single digit string, so that we may
    # compare apples to apples. If the string already has 2 digits
    # in it, the string will remain unchanged.
    workBaseMonth = re.sub(r'^[1-9]$', '0' + baseMonth, baseMonth)
    workCompareMonth = re.sub(r'^[1-9]$', '0' + compareMonth, compareMonth)
    
    if (workBaseMonth == workCompareMonth):
        return True

    return False

# boolean function, performs comparison on values treated as years
# in the date data
def compareYears(baseYear, compareYear):
    if (baseYear == compareYear):
        return True

    return False



# wrapper function, performs comparisons on all date values in the base 
# and compare lists generated in the main body
def compareDateObjects(workBaseDateObject, workCompareDateObject):
    # if one of these objects is None, don't try to compare, return maximum
    # negative number the system can produce.
    if ((workBaseDateObject == None) or (workCompareDateObject == None)):
        return -sys.maxint

    # return positive 1, 0, or negative 1 based on whether base date is
    # after, on the day of, or before the compare date
    if (workBaseDateObject > workCompareDateObject):
        return 1
    elif (workBaseDateObject == workCompareDateObject):
        return 0
    elif (workBaseDateObject < workCompareDateObject):
        return -1

    # if here, something unforseen has happened, return maximum negative
    # number system will allow
    return -sys.maxint

# wrapper function, performs comparisons on all string values in the base 
# and compare lists generated in the main body
def compareDateStrings(workBaseDate, workCompareDate):
    validateThatDaysMatch = compareDays(workBaseDate[0], workCompareDate[0])
    validateThatMonthsMatch = compareMonths(workBaseDate[1], workCompareDate[1])
    validateThatYearsMatch = compareYears(returnSanitizedYear(workBaseDate[2]), returnSanitizedYear(workCompareDate[2]))

    if (validateThatDaysMatch and validateThatMonthsMatch and validateThatYearsMatch):
        return True

    return False

# basic validation function, ensures that something that looks like a date is input
# into the system before continuing
def validateRawDateInput(inputDate):
    filter = re.compile(r'^\s*[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}.*$')    
    matchedNumber = filter.match(inputDate)
    if (matchedNumber):
        return matchedNumber.group().strip()

    return None


### Main Program Execution ###

# This gets the raw user data to be validated
rawUserInputBaseDate = input("Enter a date in the following format: MM/DD/YYYY. Optionally input time in the following format: HH:mm:SS: ")
rawUserInputCompareDate = input("Enter another date in the following format: MM/DD/YYYY. Optionally input time in the following format: HH:mm:SS: ")

# This obtains strings that are guaranteed to have only date data
# or empty objects
validatedBaseDate = validateRawDateInput(rawUserInputBaseDate)
validatedCompareDate = validateRawDateInput(rawUserInputCompareDate)

# If either date string is None, one of the dates is bad, exit the demo
if ((validatedBaseDate == None) or (validatedCompareDate == None)):
    print("One of your dates is malformed. Date must have a month, day, and year component for basic comparison. Demo exiting.")
    quit()

# Do a split on our datelike strings based on the '/' symbol
baseDateList = re.split(r'/', validatedBaseDate)
compareDateList = re.split(r'/', validatedCompareDate)

# If the resulting lists do not have exactly 3 entries, they aren't
# date objects, exit the demo.
if ((len(baseDateList) != 3) or (len(compareDateList) != 3)):
    print("One of your dates is malformed. Date must have a month, day, and year component for basic comparison. Demo exiting.")
    quit()


# Validate the day, month, and year of the base and compare lists we have
# made.
#
# Month - list[0]
# Day - list[1]
# Year - list[2]
#
# Values are out of order due to presentation in US/Western hemisphere
baseDayValidated = validateDayInput(baseDateList[1])
baseMonthValidated = validateMonthInput(baseDateList[0])

# This operates on the sanitized year, as the year portion of this list
# may include unwanted time data.
baseYearValidated = validateYearInput(returnSanitizedYear(baseDateList[2]))

compareDayValidated = validateDayInput(compareDateList[1])
compareMonthValidated = validateMonthInput(compareDateList[0])

# This operates on the sanitized year, as the year portion of this list
# may include unwanted time data.
compareYearValidated = validateYearInput(returnSanitizedYear(compareDateList[2]))


# If this chained or statement equals true, one of these values did not validate.
# This means that one of the components doesn't match as a date entry.
# Exit the demo.
if ((not(baseDayValidated)) or (not(baseMonthValidated)) or (not(baseYearValidated))):
    print("One of your base date components does not follow valid date syntax. Demo exiting.")
    quit()

# If this chained or statement equals true, one of these values did not validate.
# This means that one of the components doesn't match as a date entry.
# Exit the demo.
if ((not(compareDayValidated)) or (not(compareMonthValidated)) or (not(compareYearValidated))):
    print("One of your compare date components does not follow valid date syntax. Demo exiting.")
    quit()

print("\nTesting string value equality now:")
# At this point, we can be reasonably certain that we are working with
# date strings. This is the comparison of those strings.
finalDateStringValidation = compareDateStrings(baseDateList, compareDateList)


# If true, print that the two date strings match.
if (finalDateStringValidation):
    print("Tested: base date %s matches compare date %s\n"%(validatedBaseDate, validatedCompareDate))
else:    # Otherwise print that the values do not match
    print("Tested: base date %s does NOT match compare date %s\n"%(validatedBaseDate, validatedCompareDate))

# 10/07/2021 - Added to allow comparison of date values as opposed to date strings.
print("Testing numeric date value equality now:")

# Create ISO formatted strings: YYYY-MM-DD from strings taken from the date strings above.
baseDateStringISOFormat = returnISOFormattedString(returnSanitizedYear(baseDateList[2]), baseDateList[0], baseDateList[1])
compareDateStringISOFormat = returnISOFormattedString(returnSanitizedYear(compareDateList[2]), compareDateList[0], compareDateList[1])


# If one of these date strings is None, there was a problem, don't try to generate date
# objects from them, exit the demo.
if ((baseDateStringISOFormat == None) or (compareDateStringISOFormat == None)):
    print("There was an error in generating an ISO format string. Exiting demo.")
    quit()

# Generate date objects from our ISO formatted date strings

try:
    baseDateObjectISOFormat = date.fromisoformat(baseDateStringISOFormat)
    compareDateObjectISOFormat = date.fromisoformat(compareDateStringISOFormat)
    
    # Compare the date objects we have just created
    dateComparisonResult = compareDateObjects(baseDateObjectISOFormat, compareDateObjectISOFormat)
    
    # If the result is anything other than 1, 0, or -1, there was an error, notify the user and exit the demo.
    if (dateComparisonResult == 1):
        print("Tested: base date %s comes AFTER date %s\n"%(validatedBaseDate, validatedCompareDate))
    elif (dateComparisonResult == 0):
        print("Tested: base date %s is IDENTICAL to date %s\n"%(validatedBaseDate, validatedCompareDate))
    elif (dateComparisonResult == -1):
        print("Tested: base date %s comes BEFORE date %s\n"%(validatedBaseDate, validatedCompareDate))
    else:
        print("There was an error in the comparison. One of the date objects is in an improper format, or is in a proper format, but not a date (such as 02/30/2021, or 06/31/2021)")
        quit()
except BaseException:
    print("There was an error in the date creation. One of the date objects is in an improper format, or is in a proper format, but not a date (such as 02/30/2021, or 06/31/2021)")
    quit()


# Thank the user for using the demo program, program exits.
print("Thank you for using the datecompare demo program. Exiting demo.")
