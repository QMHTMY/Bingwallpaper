#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Author: Shieber
#    Date: 2019.07.16
#
#    一键下载Bing（必应）的每日壁纸并免除掉水印。

import re 
import datetime
import requests
import urllib.request 
import os.path as path
from   bs4 import BeautifulSoup as Soup

class BingWallpapersDownloader():
    def __init__(self):
        self.root = ['https://cn.bing.com','https://cn.bing.com/?ensearch=1&FORM=BEHPTB']
        self.headers  = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'} 
        self.saveFolder = '/home/shieber/Pictures/BingWallpapers/'

    def SetWallPaperName(self,url):
        time = datetime.datetime.now()
        year = str(time.year)
        mnth = str(time.month)
        day  = str(time.day)

        #prototype: /home/shieber/Pictures/BingWallpapers/Bing_cn_2019_7_16.jpeg
        #prototype: /home/shieber/Pictures/BingWallpapers/Bing_en_2019_7_16.jpeg
        if time.month < 10:
            mnth = '0'+mnth    #prototype:07

        if url==self.root[0]:
            picname = ''.join([self.saveFolder,'Bing','_','cn','_',year,'_',mnth,'_',day,'.jpeg'])
        else:
            picname = ''.join([self.saveFolder,'Bing','_','en','_',year,'_',mnth,'_',day,'.jpeg'])

        return picname

    def GetWallPaperUrl(self,url):
        resp = requests.get(url,headers=self.headers)
        if 200 != resp.status_code:
            return None

        resp.encoding='utf-8'
        soup = Soup(resp.content,'html.parser')
        
        if not soup:
            return None

        patn = re.compile(r'https://.*\.com') 
        url  = patn.search(url)[0]       #基准url,前缀   
        cntnt= soup.find('link',rel='preload')
        href = cntnt['href']             #壁纸url,后缀
        picurl = ''.join([url,href])     #国际版的root_url和中文版一样

        return picurl

    def DownloadWallPaper(self,picurl,picname):
        if not picurl:
            return None

        if not path.exists(picname):
            urllib.request.urlretrieve(picurl,filename=picname)

    def main(self):
        for url in self.root:
            picname = self.SetWallPaperName(url)
            picurl  = self.GetWallPaperUrl(url)
            self.DownloadWallPaper(picurl,picname)

if __name__ == "__main__":
    downloader = BingWallpapersDownloader()
    downloader.main()
