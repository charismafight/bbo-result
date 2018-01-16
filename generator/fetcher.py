import time
import requests

conn = requests.session()

start_time = int(time.mktime(time.strptime('2017-12-25', '%Y-%m-%d')))
end_time = int(time.mktime(time.strptime('2017-12-27', '%Y-%m-%d')))

url = 'http://www.bridgebase.com/myhands/hands.php?username=eve8392&start_time={}&end_time={}'.format(start_time,
                                                                                                      end_time)
# print(url.format(start_time, end_time))
# login is required
index_url = 'http://www.bridgebase.com/myhands/index.php'
login_url = 'http://www.bridgebase.com/myhands/myhands_login.php?t=%2Fmyhands%2Findex.php%3F'
conn.get(index_url)
post_data = {
    't': '/myhands/index.php?',
    'count': 1,
    'username': 'eve8392',
    'password': '19920126',
    'submit': 'Login',
    'keep': 'on',
}
login_response = conn.post(login_url, post_data)
#print(login_response.content.decode())
r = conn.get(url)
print(r.content.decode())
