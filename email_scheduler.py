import schedule
from app import UpdateMailing, AnnualMailing

# def verification_mailer():
#     UpdateMailing.get(UpdateMailing)

def annual_mailer():
    AnnualMailing.get(AnnualMailing)

# schedule.every(1).days.do(verification_mailer)
# schedule.every(7).days.do(annual_mailer)
# schedule.every(10).seconds.do(verification_mailer)
schedule.every(10).seconds.do(annual_mailer)

while True:
    schedule.run_pending()