'''
    根据歌手ID可以下载歌手的部分可免费下载的歌曲并存入文件夹，文件夹默认目录在当前目录下，由于爬取的歌手接近四万，下载全部歌曲
    会导致代码运行非常缓慢接内存不足，所以此代码提供了下载指定歌手歌曲的功能，供用户交互输入。
'''
import re
import requests
import os
import time

headers = {
    'User-Agent': 'Chrome/10'
}

def main():
    try:
        ID=input("请输入歌手ID：")
        url='https://music.163.com/artist?id='+ID
        html=requests.get(url,headers).text
        get_id(html)
    except Exception as e:
        # 打印错误日志
        print(str(e))

def get_id(html):
    findlink=re.compile(r'<a href="/song\?id=(\d*)">(.*?)</a></li><li>')
    findname=re.compile(r'<h2 id="artist-name" data-rid=\d* class="sname f-thide sname-max" title=".*?">(.*?)</h2>')
    singername=re.findall(findname,html)[0]
    creat(singername)
    ll=re.findall(findlink,html)
    for i in ll:
        savemusic(i[1],i[0])
        time.sleep(0.5)

#创建文件夹
def creat(singername):
    if not os.path.exists(singername):
        os.mkdir(singername)  # 如果该目录不存在就创建它
    os.chdir(singername)
#保存文件
def savemusic(name,id):
    url='http://music.163.com/song/media/outer/url?id='+id+'.mp3'
    with open(name+'.m4a','wb') as f:
        print('歌曲《',name,'》 下载中...')
        f.write(requests.get(url=url,headers=headers).content)
        f.close()
        print("《",name,"》下载完成")
        print('')


if __name__ == '__main__':
    main()