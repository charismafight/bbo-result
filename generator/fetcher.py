import time

import os
import requests
import re
import sys

from generator.lin import *


def fetch(file_path):
    """
    fetch game results and return a directory contains lin files
    :param file_path: path of the file
    :return: path of lin files where contains the *.lin
    """
    if os.path.exists(file_path):
        print(file_path + '  exists,delete it first if you want to download it again')

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
    conn.post(hands_url, data=hands_data)

    start_time = int(time.mktime(time.strptime('2017-11-25', '%Y-%m-%d')))
    end_time = int(time.mktime(time.strptime('2017-12-25', '%Y-%m-%d')))
    url = 'http://www.bridgebase.com/myhands/hands.php?username=eve8392&start_time={}&end_time={}'.format(start_time, end_time)
    data = conn.get(url).content.decode()
    GAME_REG = r'<tr class="tourneySummary">([\s\S]*?)(<tr>[\s\S]*?<th colspan="11">[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}</th>[\s\S]*?</tr>|<tr class="even">)'
    # find games
    games = re.findall(GAME_REG, data)
    # find Orange
    orange_game = list(filter(lambda x: 'Orange' in x[0], games))
    if orange_game and len(orange_game) == 1:
        print('orange game found')
    else:
        print('error,0 or over 2 orange games found,please check searching conditions')
        input()
        exit(0)

    rows = re.findall(r'<tr class="team">([\w\W]*?)</tr>', orange_game[0][0])
    url_prefix = 'http://www.bridgebase.com/myhands/'
    lins = []
    results = []
    for i, x in enumerate(rows):
        # print(url_prefix + re.search(r'<A HREF="(.*)">Lin</A>', x).group(1))
        trump_game = re.search(r'<td class="result">([1-7])<span style="[\s\S]*?">([\s\S]*?)</span>([\s\S]*?)</td>', x)
        if trump_game:
            result = ''.join(trump_game.groups())
        else:
            no_trump_game = re.search(r'<td class="result">([\s\S]*?)</td>', x)
            if no_trump_game:
                result = re.search(r'<td class="result">([\s\S]*?)</td>', x).group(1)
            else:
                print('error when getting game number :' + str(i) + ' result,failed!')
                exit(0)
        results.append(result)
        lin = Lin(url_prefix + re.search(r'<A HREF="(.*)">Lin</A>', x).group(1), result)
        lin.fetch_file(conn)
        lins.append(lin)
        # to avoid bbo's anti-scraping rule
        # sleeping to reduce http error 503
        time.sleep(4)

    # with open(sys.path[0] + "\\files\\" + time.strftime('%Y%m%d%H%M', time.localtime(time.time())) + ".lin", 'w') as f:
    with open(file_path, 'w') as f:
        f.writelines(map(str, lins))
    with open(file_path.replace('lin', 'result'), 'w') as f:
        f.writelines('\n'.join(results))
