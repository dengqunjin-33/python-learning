import pymysql
db = pymysql.connect(host='58.67.156.39', port=6033, user='jiyu', passwd='jiyu', db='exchange_otc', charset='utf8')
cursor = db.cursor()
sql = """
CREATE TABLE jin_shi_calendar (
    id int primary key NOT NULL,
    country VARCHAR(200),
    time_period VARCHAR(200),
    name VARCHAR(200),
    unit VARCHAR(200),
    previous VARCHAR(200),
    consensus VARCHAR(200),
    actual VARCHAR(200),
    affect VARCHAR(200),
    revised VARCHAR(200),
    indicator_id VARCHAR(200),
    pub_time VARCHAR(200),
    star VARCHAR(200)
)
"""

cursor.execute(sql)