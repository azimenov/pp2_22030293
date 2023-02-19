import datetime
c_time = datetime.date.today()
print(f"Today: {c_time}")

delta = datetime.timedelta(days = 1)
print(f"Yesterday: {c_time - delta}")
print(f"Tommorow: {c_time + delta}")