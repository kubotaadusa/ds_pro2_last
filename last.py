from bs4 import BeautifulSoup
import requests
import time

# スマホデータ
bmr_list = ['1494', '1460', '1462', '1455', '1476', '1475', '1466', '1482', '1463', '1485', '1462', '1472', '1355', '1270', '1277', '1289', '1274', '1268', '1276', '1274', '1272', '1282', '1271', '1274', '1288', '1272', '1276', '1274', '1269', '1268', '1268']
bmr_list = [int(value) for value in bmr_list]

# HTML全体を取得
url='https://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2022&month=12&day=&view=a2'
for i in url:
    r=requests.get(url)#取得
    time.sleep(1)

# いい感じに変換
html_soup = BeautifulSoup(r.content, 'html.parser')
list = html_soup.find_all('div', itemprop="owns")

# 日にち
day_list=[]

day_tags=soup.find_all('a')
day_list=[x.string for x in day_tags]

del day_list[:25]
del day_list[31:]
day_list = [int(day) for day in day_list]

#  スクレイピングデータ
weather_list_proto=[]

weather_tags=soup.find_all('td',class_='data_0_0')
weather_list_proto=[x.string for x in weather_tags]

weather_list_proto2= [item for item in weather_list_proto if '--' not in item and ':' not in item]

for _ in range(7):
    weather_list_proto2.remove('0.0')

for _ in range(8):
    weather_list_proto2.remove('0.5')

weather_list_proto2.remove('15.5')

del weather_list_proto2[48]
del weather_list_proto2[102]
del weather_list_proto2[102]
del weather_list_proto2[129]
del weather_list_proto2[273]
del weather_list_proto2[273]

weather_list_proto2 = [float(weather) for weather in weather_list_proto2]

weather_list = [weather_list_proto2[i:i+9] for i in range(0, len(weather_list_proto2), 9)]

# まとめリスト作成

git_list=[]

for i in range(len(day_list)):
    git_list.append((day_list[i],weather_list[i],bmr_list[i]))

bmrs_data_list = [(item[0], *item[1], item[2]) for item in git_list]

#データベース構築

import sqlite3
!pwd

#ファイルパス
path ='last.py'

db_name = 'last.sqlite'
con = sqlite3.connect(path + db_name)
con.close()

# テーブルを作成
con = sqlite3.connect(path + db_name)

cur = con.cursor()

sql_create_table_gits = 'CREATE TABLE bmr(day int, avg_gr_hpa int, avg_sea_hpa int, low_sea_hpa int, avg_temp int, high_temp int, low_temp int, vp, avg_hum int, low_hum, bmr int);'

cur.execute(sql_create_table_gits)

con.close()

# データ参照
con = sqlite3.connect(path + db_name)

cur = con.cursor()

sql_select = 'SELECT * FROM bmr;'

cur.execute(sql_select)

for r in cur:
  print(r)

con.close()

# 複数レコード挿入
con = sqlite3.connect(path + db_name)

cur = con.cursor()

sql_insert_many = "INSERT INTO bmr VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"

bmrs_list = []

cur.executemany(sql_insert_many, bmrs_data_list)

con.commit()

con.close()
