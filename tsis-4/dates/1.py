import datetime

d = datetime.date.today()
delta = datetime.timedelta(days = 500)
print(d - delta)

b_day = datetime.date(2023, 3, 13)
print(b_day - d)