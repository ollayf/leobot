'''
This Script holds all the important core functions outside of the bot (specifically) but more to do with 
general functions
'''

import datetime

## DATETIME-RELATED
#####################

def manual_convert_SGT(dateTime):
    '''
    Manually converts datetime objects to UTC timing to be taken in by ptb
    '''
    assert isinstance(dateTime, (datetime.datetime, datetime.time)), \
        'Must be datetime.time or datetime.datetime obj'
    assert dateTime.tzinfo == None, 'Must be a naive datetime.time or datetime.datetime object!'
    # if it is a datetime.datetime obj
    if isinstance(dateTime, datetime.datetime):
        diff = datetime.timedelta(hours=8)
        dateTime -= diff
    # else if it is a datetime.time obj
    else:
        hour = dateTime.hour - 8
        # account for if the hour is a value less than 8
        if hour < 0:
            hour = 24 - hour
        dateTime = dateTime.replace(hour=hour)
    # returns the converted times
    return dateTime

def getDatetimeOfNextXDay(isoweekday, hour):
    '''
    Returns a datetime.datetime object with time zone of Singapore, at 0000 hours
    of the date of the iso weekday
    timezone is the timezone we are at as recorded by pytz package
    hour is the hour of the day the time will be set on
    isoweekday value is an integer value corresponding to the day of the week
    e.g. Monday = 1, Sunday = 7
    '''
    assert isinstance(isoweekday, int), 'isoweekday must be an integer!'
    assert 1 <= isoweekday <= 7, 'isoweekday must be between 1 and 7!'

    today = datetime.datetime.now()
    days_ahead = isoweekday - today.isoweekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    date = today + datetime.timedelta(days=days_ahead)
    dateTime = datetime.datetime(date.year, date.month, date.day, hour, 0, 0)
    dateTime = manual_convert_SGT(dateTime)
    return dateTime