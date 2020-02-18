import requests
from bs4 import BeautifulSoup
import json
import os
clear = lambda: os.system("cls")
def listToString(s):
    string = ""
    
    for n in s:
        if(s.index(n) != len(s)-1):
            string += n + '%20'
        else:   
            string += n
    
    return string

def getIds(dic):
    retval=[]
    for url in dic:
        urrl=dic[url]
        retval.append(urrl.split('/')[-3])
    return retval

def GetNewsApi(i):
    
    req = requests.get("https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid="+i)
    data = req.json()
    newscount = len(data['appnews']['newsitems'])
    content={}
    for i in range(0,newscount-1):
        title= data['appnews']['newsitems'][i]['title']
        url=data['appnews']['newsitems'][i]['url']
        content.update({title:url})
    return content
        

def SearchGame():
    gameName = input("Search Game: ")
    name_list = gameName.split(" ")
    searchName = listToString(name_list)

    steamMainPage = requests.post("https://store.steampowered.com/search/?term="+searchName)
    soup = BeautifulSoup(steamMainPage.text , "html5lib")

    div = soup.find('div',{"id":"search_resultsRows"})
    #div = soup.find_all("a",{"class":"search_result_row ds_collapse_flag"})['href']

    urls=[]
    names=[]
    c=0
    for a in div.find_all('a', href=True):
        urls.append(a['href'])
        c+=1
        if(c==5):
            break
    c1=0
    for n in div.find_all('span',{'class':'title'}):
        names.append(n.get_text())
        c1+=1
        if(c1==5):
            break
    dic = dict(zip(names,urls))

    clear()
    print("You Searched for  : ",gameName )
    count = 0
    for name in names:
        count +=1
        print(count,") ", name)
    inp = int(input("Choose a game : "))
    content = {}
    if(inp == 1): content = GetNewsApi(getIds(dic)[0])
    elif(inp==2): content = GetNewsApi(getIds(dic)[1])
    elif(inp==3): content = GetNewsApi(getIds(dic)[2])
    elif(inp==4): content = GetNewsApi(getIds(dic)[3])
    elif(inp==5): content = GetNewsApi(getIds(dic)[4])


    return content






dic=SearchGame()


for x in dic:
    print("--------------------------")
    print("News Title : ", x)
    print("Url : ", dic[x])
    print("--------------------------")
    print()