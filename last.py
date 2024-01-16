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

# リスト作成
day_list=[]
avg_list=[]
high_list=[]
low_list=[]

for i, element in enumerate(list):
    # 日にち
    day=element.find('a')
    day_text = day.get_text(strip=True)
    day_list.append(day_text)

    #  平均
    avg=element.find('td',class_="data_0_0")
    avg_text = avg.get_text(strip=True)
    avg_list.append(avg_text)

    #  最高
    high=element.find('a',class_="Link d-inline-block")
    high_text = high.get_text(strip=True)
    high_list.append(high_text)

    #  最低
    low=element.find('a',class_="Link d-inline-block")
    low_text = low.get_text(strip=True)
    low_list.append(low_text)

git_list=[]

for i in range(len(day_list)):
    git_list.append((day_list[i],avg_list[i],high_list[i],low_list[i],bmr_list[i]))