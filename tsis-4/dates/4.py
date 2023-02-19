import datetime

f_date = datetime.date.today()
s_date = datetime.date(2023, 2, 15)

print((f_date - s_date).total_seconds())