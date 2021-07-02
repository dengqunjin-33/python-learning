import pymysql

db = pymysql.connect(host='139.159.244.194', port=3306, user='root', passwd='abc123456@', db='jinshi', charset='utf8')
cursor = db.cursor()
cursor.execute("select version()")
# 创建金10数据表sql
# sql = """create table data(
#   id CHAR(20) NOT NULL primary key,
#   type tinyint,
#   create_time DATETIME,
#   tags varchar(50),
#   important tinyint,
#   channel char(20) ) """

#金10信息表sql
# sql = """CREATE TABLE jin_shi_info (
#       id CHAR(20) NOT NULL primary key,
#       pic VARCHAR(200),
#       title VARCHAR(200),
#       content text,
#       flag VARCHAR(200),
#       name VARCHAR(200),
#       star VARCHAR(200),
#       type TINYINT,
#       unit VARCHAR(200),
#       actual VARCHAR(200),
#       affect VARCHAR(200),
#       country CHAR(50),
#       data_id VARCHAR(200),
#       measure VARCHAR(200),
#       revised VARCHAR(200),
#       previous VARCHAR(200),
#       pub_time DATETIME,
#       consensus VARCHAR(200),
#       time_period VARCHAR(200),
#       indicator_id VARCHAR(200)) """

# 金10remark表sql
sql = """
CREATE TABLE jin_shi_remark (
    id int primary key auto_increment,
    jid CHAR(20) NOT NULL,
    link VARCHAR(200),
    remark_id int,
    type VARCHAR(30),
    title VARCHAR(200),
    content text
)
"""

cursor.execute(sql)