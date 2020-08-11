#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Author: Shieber
#    Date: 2019.07.16
#
#    一键下载Bing（必应）的每日壁纸并免除掉水印。

import re 
import time
import requests
import urllib.request 
import os.path as path
from   bs4 import BeautifulSoup as Soup

class BingWallpapersDownloader():
    def __init__(self):
        self.root     = ['https://cn.bing.com', 'https://cn.bing.com/?ensearch=1&FORM=BEHPTB']
        self.headers  = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'} 

        self.saveDir  = '/home/shieber/Pictures/BingWallpapers/'
        self.midName  = 'Bing_cn_'
        self.midName  = 'Bing_en_'

    def _set_wallpaper_name(self, url):
        tm   = time.localtime()
        year, mon, day = tm.tm_year, tm.tm_mon, tm.tm_mday

        year = str(year)
        mon  = '0' + str(mon) if mon < 10 else str(mon)  #month-prototype:07
        day  = '0' + str(day) if day < 10 else str(day)  #day-prototype:07

        if url==self.root[0]:
            picName = ''.join([self.saveDir, self.midName, year, '_', mon, '_', day, '.jpeg'])
        else:
            picName = ''.join([self.saveDir, self.midName, year, '_', mon, '_', day, '.jpeg'])

        return picName

        #prototype: /home/shieber/Pictures/BingWallpapers/Bing_cn_2019_07_16.jpeg
        #prototype: /home/shieber/Pictures/BingWallpapers/Bing_en_2019_07_16.jpeg

    def _get_wallpaper_url(self, url):
        resp = requests.get(url, headers=self.headers)
        if 200 != resp.status_code:
            return None

        resp.encoding='utf-8'
        soup = Soup(resp.content, 'html.parser')
        if not soup:
            return None

        patn = re.compile(r'https://.*\.com') 
        url  = patn.search(url)[0]       #基准url,前缀   
        cntnt= soup.find('link', rel='preload')
        href = cntnt['href']             #壁纸url,后缀
        picUrl = ''.join([url, href])     #国际版的root_url和中文版一样

        return picUrl

    def _download_wallpaper(self, picUrl, picName):
        if not picUrl:
            return None

        if not path.exists(picName):
            urllib.request.urlretrieve(picUrl, filename=picName)

    def download(self):
        for url in self.root:
            picName = self._set_wallpaper_name(url)
            picUrl  = self._get_wallpaper_url(url)
            self._download_wallpaper(picUrl, picName)

if __name__ == "__main__":
    bwpdownloader = BingWallpapersDownloader()
    bwpdownloader.download()
