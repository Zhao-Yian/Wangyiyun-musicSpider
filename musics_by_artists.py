'''
    根据歌手ID爬取歌手所有的歌曲信息并存入数据库
'''

import re
import requests
import time
from musics import sql

headers = {
    'User-Agent': 'Chrome/10'
}

def main(ID):
    try:
        url='https://music.163.com/artist?id='+ID
        html=requests.get(url,headers).text
        get_id(html)
    except Exception as e:
        # 打印错误日志
        print(str(i) + ': ' + str(e))
        time.sleep(0.2)

def get_id(html):
    findlink=re.compile(r'<a href="/song\?id=(\d*)">(.*?)</a></li><li>')
    findname=re.compile(r'<h2 id="artist-name" data-rid=\d* class="sname f-thide sname-max" title=".*?">(.*?)</h2>')
    artist_name=re.findall(findname,html)[0]
    ll=re.findall(findlink,html)
    for i in ll:
        sql.insert_music(i[0],i[1],artist_name)
        time.sleep(0.5)


if __name__ == '__main__':
    artists = sql.get_all_artist()
    count = 0
    for i in artists:
        count = count + 1
        print(count*100/len(artists))
        main(i['ARTIST_ID'])
