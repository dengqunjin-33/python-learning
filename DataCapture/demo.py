import datetime
dd = '2020-10-29T03:10:06.000Z'
dd = datetime.datetime.strptime(dd, "%Y-%m-%dT%H:%M:%S.%fZ")
print(dd)