# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 21:35:58 2018

@author: me!
"""
## TODO:    TESTING TESTING TESTING
            # DEBUGGING DEBUGGING DEBUGGING
            # church
"""Manga Downloader"""

'''NOTE THIS PROGRAM USES MANGAPANDA.COM
DUNNO SHIT ABOUT THE COPYRIGHT 
IM JUST LEARNING WEB SCRAPING HERE'''
'''ALSO JUST LEARNING CLASSES'''

__version__ = '0.0.1'
__license__ = 'NONE use it however you see fit after all , you downloaded it so thank you'
__author__ = 'Akujobi Clinton C         |i-me-you|'


import requests, os
from bs4 import BeautifulSoup

# to do make exceptions for run time
class MangaDownloader(object):
    '''
MANGA DOWNLOADER: USED FOR DOWNLOADING MANGA FROM MANGAPANDA.COM
HOWTO: MangaDownloader(manga_name, manga_chapter)
FEATURES: Downloads the manga a directory named manga_name
\n
NOTE: MANGA_NAME must be spelt correctly else it won't be found on the site
and an error will be raised same thing if the manga chapter is not available on the site
    '''
    
    def __init__(self, manga_name, manga_chapter):
        self.manga_name = manga_name
        self.chapter = manga_chapter
        self.url = 'http://www.mangapanda.com'
  
    def __str__(self):
        return 'Manga: ' + self.manga_name + ', Chapter: ' + self.chapter
    
    def get_mangaName(self):
        '''
        Used to safely access the manga name outside the class
        '''
        return str(self.manga_name)
   
    def get_mangaSite(self):
        '''
        Used to safely access the url outside class
        '''
        return self.url
   
    def get_mangaChapter(self):
        '''
        Used to safely access the manga chapter searched for outside the class
        '''
        return self.chapter
    
    def check_manga(self):
        '''
        returns true if manga is available at mangapanda
        else tell user there aint none
        '''
        pass
   
    def search_manga(self):
        '''Searches mangapanda for the manga name \n
        if manga is found return link to the manga's page
        else prints error message'''
        
        search_results = self.url + '/search/?w=' + self.manga_name
        
        try:
            res = requests.get(search_results)
            res.raise_for_status()
        except:
            print('Network Error Occured while searching for manga')
        else:
            soup = BeautifulSoup(res.text, 'html.parser')
        
            check = soup.select('.manga_name a')
            if check == []:
                print ('The manga wasn\'t found at', self.get_mangaSite)
            else:
                # choose the first manga on the page
                mangaUrl = self.url + check[0].get('href')
                
                return mangaUrl
            
            
        # TODO MAKE THEM CHOOSE IF MORE THAN ONE MANGA IS FOUND  
        
    def search_manga_episode(self, manga_page):
        '''manga_page = url of a specific manga page eg naruto's page \n
        manga_chapter = int \n
        searches manga_page for manga_chapter \n
        if manga_chapter is present return link to the chapter \n
        Else print error message'''
        
        search_name = self.get_mangaName() + ' ' + str(self.chapter)
        try:
            res = requests.get(manga_page)
            res.raise_for_status()
        except:
            print('Network Error occured while searching for manga chapter')
        else:
            soup = BeautifulSoup(res.text, 'html.parser')
            check = soup.select('a')
                                                   
            for char in check:
                if char.getText() == search_name:
                    
                    chapter_url = self.url + char.get('href')
                    return chapter_url
            
                
    def download_manga(self, chapter_page):
        '''
        chapter_page = a specific manga chapter url
        Downloads manga chapter from chapter_page'''
       
        url = chapter_page
#        print('checking url', url)
        try:
            res = requests.get(url)
            res.raise_for_status()
        except:
            print('Network Error occured while loading', url)
        else:
            soup = BeautifulSoup(res.text, 'html.parser')
            count = soup.select('#selectpage')
            num_pages = count[0].getText().split()[-1]     # i know ryt?/
            print ('number of pages=', num_pages)

            # Making the directory to save it 
            folder_name = str(self.manga_name) + ' ' + str(self.chapter)
            os.makedirs(folder_name, exist_ok=True)
            while not url.endswith(num_pages):
                NoName = requests.get(url)
                soups = BeautifulSoup(NoName.text, 'html.parser')
                manga = soups.select('#img')
                if manga == []:
                    print ('could not find manga page')
                else:
                    try:
                        manga_url = manga[0].get('src')
                        print('Downloading image.... {}'.format(manga_url))
                        download = requests.get(manga_url)
                        download.raise_for_status()
                    except:
                        print ('Network Error occured while downloading image')
                        print ('Trying Again')
                    else:
  #                       saving the image to hard drive 
                        mangaFile = open(os.path.join(folder_name, os.path.basename(manga_url)), 'wb')
                        for byte in download.iter_content(100000):
                            mangaFile.write(byte)
                        mangaFile.close()
                        
                        # Getting the next page
                        next_page = soups.select('.next a')[0]
                        url = self.url + next_page.get('href')
                        
                       

      #      TODO: check whether it download the last page    it doesnt
            print('DONE!')
    
    def Run_App(self):
        '''Runs the Manga downloader App'''
        try:
            x = self.search_manga()
        except:
            print('ERROR OCCURED WHILE SEARCHING FOR MANGA')
        else:
            try:
                y = self.search_manga_episode(x)
            except:
                print('ERROR OCCURED WHILE SEARCHING FOR MANGA EPISODE')
            else:
                self.download_manga(y)
        

if __name__ == '__main__':
    Onepiece = MangaDownloader('One Piece', 902)
    Onepiece.Run_App()
    
#print('WELCOME TO MANGA DOWNLOADER')
#print('')
#print('''This script downloads any manga chapter and saves it in it's own directory
#NOTE: this app uses mangapanda.com so there are a few hiccups
#[1] == manga name must be spelt correctly or it won't find the manga (spelt correctly according to mangapanda site tho)
#[2] == manga chapter must be available or youre gon' get an error message fam
#[3] == it's pretty straightforward , all it does is download the manga, nothng else
#\n
#will add more features but for now , ENJOY!!!''')
#print('')
#manga_name = str(input('Enter the name of the manga you wish to download:'))
#manga_chapter = str(input('Enter the chapter:'))
#print('Downloading {0}, chapter {1}'.format(manga_name, manga_chapter))
#MANGADOWNLOADER = MangaDownloader(manga_name, manga_chapter)
#MANGADOWNLOADER.Run_App()
    
    
    
    
    
    
    

    
    
