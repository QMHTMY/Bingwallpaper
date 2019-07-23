#!/usr/bin/python3

import re 
import sys
import datetime
import requests
import urllib.request 
import os.path as path
from   bs4 import BeautifulSoup as Soup

class BingWallpapersDownloader():
    def __init__(self):
        self.root_url = ['https://cn.bing.com','https://cn.bing.com/?ensearch=1&FORM=BEHPTB']
        self.headers  = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'} 
        self.save_fold= '/home/shieber/Pictures/BingWallpapers/'

    def SetWallPaperName(self,root_url):
        time = datetime.datetime.now()
        year = str(time.year)
        mnth = str(time.month)
        day  = str(time.day)

        #prototype: /home/shieber/Pictures/BingWallpapers/Bing_cn_2019_7_16.jpeg
        #prototype: /home/shieber/Pictures/BingWallpapers/Bing_en_2019_7_16.jpeg
        if time.month < 10:
            mnth = ''.join(['0',mnth])    #prototype:07

        if root_url==self.root_url[0]:
            picname = ''.join([self.save_fold,'Bing','_','cn','_',year,'_',mnth,'_',day,'.jpeg'])
        else:
            picname = ''.join([self.save_fold,'Bing','_','en','_',year,'_',mnth,'_',day,'.jpeg'])

        return picname

    def GetWallPaperUrl(self,root_url):
        home_page = requests.get(root_url,headers=self.headers)
        if 200 == home_page.status_code:
            home_page.encoding='utf-8'
            soup = Soup(home_page.content,'html.parser')
        else:
            return None
        
        if soup:
            url_patn  = re.compile(r'https://.*\.com') 
            root_url  = url_patn.search(root_url)[0]   #基准url,前缀   
            url_contnt= soup.find('link',rel='preload')
            href_info = url_contnt['href']             #壁纸url,后缀

            picurl    = ''.join([root_url,href_info])  #国际版的root_url和中文版一样

            return picurl
        else:
            return None

    def DownloadWallPaper(self,picurl,picname):
        if not picurl:
            return None

        if not path.exists(picname):
            urllib.request.urlretrieve(picurl,filename=picname)
        else:
            pass

    def main(self):
        for root_url in self.root_url:
            picname = self.SetWallPaperName(root_url)
            picurl  = self.GetWallPaperUrl(root_url)
            self.DownloadWallPaper(picurl,picname)

if __name__ == "__main__":
    downloader = BingWallpapersDownloader()
    downloader.main()
