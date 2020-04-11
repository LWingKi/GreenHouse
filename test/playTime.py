from datetime import datetime, timedelta, timezone
now = datetime.now() # current time in UTC
future = now + timedelta(hours=24) 

by24hours = now + timedelta(hours=24) # move clock by 20 hours
print("Move clock by 24 hours: {by24hours:%I:%M %p}".format(**vars()))  # AM/PM
print("actual value ",by24hours)
if(now >= by24hours):
    print ("shit")
else:
    print ("wait")
