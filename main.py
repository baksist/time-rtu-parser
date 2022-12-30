from bs4 import BeautifulSoup as BS
from ics import Calendar, Event
from datetime import datetime, timedelta
import requests

r = requests.get("http://time-rtu.ru/?view=table&group=БББО-05-19")
r.encoding = "UTF-8"

html_raw = r.text
html = BS(html_raw, 'html.parser')

cal = Calendar()

cards = html.find_all(id="card")
for card in cards:
    date = card.find(id="date").text.split('(')[1][:10]
    pary = card.find_all("tr")
    for i in range(len(pary)):
        if len(pary[i]) > 0:
            start_hour = pary[i].find(id='time').text.strip()

            class_data = pary[i].find(id='lesson')
            title = class_data.find(id='dist').text.strip()
            aud = class_data.find(id='aud').text.strip()
            prepod = class_data.find(id='prepod').text.strip()

            time_a = datetime.strptime(
                (f'{date} {start_hour}'), '%d.%m.%Y %H:%M') - timedelta(hours=3)

            if not '- -' in title:
                para = Event(
                        name=title,
                        begin=time_a.strftime('%F %T'),
                        duration=timedelta(seconds=5400),
                        location=aud.replace('ауд.', ''),
                        description=f"Ведёт {prepod}")

                cal.events.add(para)

with open('/home/matt/pary.ics', 'w') as f:
    f.writelines(cal)
