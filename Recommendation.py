'''
    每日推荐歌单生成
'''
import re
import urllib.request
import urllib.error
import urllib.parse
from musics import sql

def get_all_recommendationSong():  # 获取所有高流行度歌曲名称和id
    url = 'http://music.163.com/discover/toplist?id=19723756'  # 网易云音乐url
    header = {  # 请求头部
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    request = urllib.request.Request(url=url, headers=header)
    html = urllib.request.urlopen(request).read().decode('utf8')  # 打开url
    html = str(html)  # 转换成str
    pat1 = r'<ul class="f-hide"><li><a href="/song\?id=\d*?">.*</a></li></ul>'  # 进行第一次筛选的正则表达式
    result = re.compile(pat1).findall(html)  # 用正则表达式进行筛选
    result = result[0]  # 获取tuple的第一个元素

    pat2 = r'<li><a href="/song\?id=\d*?">(.*?)</a></li>'  # 进行歌名筛选的正则表达式
    pat3 = r'<li><a href="/song\?id=(\d*?)">.*?</a></li>'  # 进行歌ID筛选的正则表达式
    song_name = re.compile(pat2).findall(result)  # 获取所有高流行度歌曲名称
    song_id = re.compile(pat3).findall(result)  # 获取所有高流行度歌曲对应的Id

    return song_name, song_id

def saveSong(song_name, song_id):
    num = 0
    while num < len(song_name):
        print('正在抓取第%d首歌曲...' % (num + 1))
        sql.insert_recommendation_music(song_id[num],song_name[num])
        print('第%d首歌曲抓取成功' % (num + 1))
        num += 1


if __name__ == '__main__':
    song_name, song_id = get_all_recommendationSong()
    saveSong(song_name,song_id)
