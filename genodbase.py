import requests
from curl_cffi import requests as requests2
from bs4 import BeautifulSoup
import httplib2
import os
from pathlib import Path
import sys
import json
import time
import threading
import  settings




def GetFromCgamos(katalog,start,stop,number_trs):   
    print (settings.trs)
    lock = threading.Lock()
    katalog=katalog.rstrip()
    if katalog[-1:]=='/':
        katalog=katalog[:-1]

    if getattr(sys, 'frozen', False):
        script_path = Path(sys.executable).parent
    elif __file__:
        script_path = Path(__file__).parent
    if not os.path.isdir(script_path.joinpath(os.path.basename(katalog))):
        dir_new=script_path.joinpath(os.path.basename(katalog))
        os.mkdir(dir_new)
    
    url_documenta=f'{katalog}/'
    print (url_documenta)
    headers ={'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36', 'Referer':f'{katalog}/'}   
    s = requests.Session()
    s.headers = headers 
    response = s.get(url_documenta)
    #print (response.content)
    bs = BeautifulSoup(response.text,"lxml")
    temp = bs.find_all('li', class_='swiper-slide')
    #print (temp)
    urls_image_opisey=[]
    for li in temp:
        urls_image_opisey.append (li.find('img')['data-src'])  
    rr_len=len(temp)
    with lock:
        
        settings.trs[number_trs]['count_rec']=rr_len
    print (f'Найдено {rr_len} изображений: ')
    #for i,img in enumerate(urls_image_opisey):
    #    print (f'{i+1}. https://cgamos.ru/{img}')
    #Убрано потомучто по прямым сылка не показывает и не качает
    if  start=='':
        start=1
    if  stop=='':
        stop=rr_len
    if int(start)<=rr_len:
        settings.trs[number_trs]['status']='0'
        for i in range(int(start)-1,int(stop)):
            data = s.get('https://cgamos.ru'+urls_image_opisey[i]) 
            with open(script_path.joinpath(os.path.basename(katalog),str(i+1).zfill(4) +".jpg"), "wb") as out:
                out.write(data.content)
            with lock:    
                settings.trs[number_trs]['status']=int(settings.trs[number_trs]['status'])+1
            #print (f'Скачено {settings.trs[number_trs]["status"]} изображений.')
    s.close()


