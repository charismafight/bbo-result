import time
import requests
import re
from generator.lin import *

conn = requests.session()

# print(url.format(start_time, end_time))
# login is required
login_url = 'http://www.bridgebase.com/myhands/myhands_login.php?t=%2Fmyhands%2Findex.php%3F'
post_data = {
    't': '/myhands/index.php?',
    'count': 1,
    'username': 'eve8392',
    'password': '19920126',
    'submit': 'Login',
    'keep': 'on',
}
conn.post(login_url, data=post_data)

hands_url = 'http://www.bridgebase.com/myhands/index.php?&from_login=1'
# print(login_response.content.decode())
# bbo needs a MGT timezone offset data,it may be saved into session.so do a post for it,and the response is useless.
hands_data = {
    'offset': '-480',
}
r = conn.post(hands_url, data=hands_data)
# print(r.content.decode())


start_time = int(time.mktime(time.strptime('2017-11-25', '%Y-%m-%d')))
end_time = int(time.mktime(time.strptime('2017-12-25', '%Y-%m-%d')))
url = 'http://www.bridgebase.com/myhands/hands.php?username=eve8392&start_time={}&end_time={}'.format(start_time,
                                                                                                      end_time)
data = conn.get(url).content.decode()
# print(data.content.decode())
rows = re.findall(r'<tr class="team">([\w\W]*?)</tr>', data)
url_prefix = 'http://www.bridgebase.com/myhands/'
# todo <tr class="tourneySummary">[\S\s]*?Orange[\S\s]*?</tr> re find orange
lins = []
for x in rows:
    # print(url_prefix + re.search(r'<A HREF="(.*)">Lin</A>', x).group(1))
    print(x)
    result = ''.join(
        re.search(r'<td class="result">([1-7])<span style="[\s\S]*?">([\s\S]*?)</span>([\s\S]*?)</td>', x).groups())
    print(result)
    lin = Lin(url_prefix + re.search(r'<A HREF="(.*)">Lin</A>', x).group(1), result)
    lin.fetch_file(conn)
    lins.append(lin)
    # to avoid bbo's anti-scraping rule
    # sleeping to reduce http error 503
    time.sleep(5)
