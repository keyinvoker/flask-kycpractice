import schedule
# import time
from app import ScheduledMailing

def annual_mailing():
    ScheduledMailing.get(ScheduledMailing)

schedule.every(7).days.do(annual_mailing)

while True:
    schedule.run_pending()