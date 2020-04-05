import requests as rq
from bs4 import BeautifulSoup as BS
import re
import os

headers = {
    #'Referer':'http://music.163.com/',
    #'Host':'music.163.com',
    'Accept': '*/*',
    'Accept-Encoding': 'identity;q=1, *;q=0',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    #'Host': 'm10.music.126.net',
    'Range': 'bytes=0-',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

clound = 'http://music.163.com/song/media/outer/url?id='

def getMusic(ID, path):
    try:
        url = clound +ID+'.mp3'
        tmp = rq.get(url, headers=headers)
        tmp.raise_for_status()
        print('Downloading......')
        with open(path, 'wb') as f:
            f.write(tmp.content)
        print('Download %s successfully!' % path)
    except:
        print('Fail to download!')

def getMusicList(ID):
    url = 'https://music.163.com/playlist?id='+ID
    s = rq.session()
    response = s.get(url, headers=headers).content.decode('utf8','ignore')
    soup = BS(response, 'lxml')
    name = soup.find('h2',{'class','f-ff2 f-brk'}).text                       
    ls = soup.find('ul', {'class':'f-hide'})  
    song_list = ls.find_all('a')
    print('We all get %d songs' % len(song_list))
    song_dict = {}                                        
    for one_song in song_list:
        title = one_song.text
        ID = one_song['href'].replace('/song?id=','')
        song_dict[title] = ID
        print('title %s :\tID %s' % (title, ID) )
    return name, song_dict

def main():
    ID = input('Please id for song list:')
    title,song_dict = getMusicList(ID)
    if not os.path.exists(title):
        os.mkdir(title)

    for one_title in song_dict.keys():
        print('Start to download',one_title)
        save_path = os.path.join(title,one_title+'.mp3')
        getMusic(song_dict[one_title], save_path)

if __name__ == '__main__':
    main()