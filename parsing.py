import requests
import json
import csv
from bs4 import BeautifulSoup
try: 
    from BeautifulSoup import BeautifulSoup
   
except ImportError:
    from bs4 import BeautifulSoup
    
class track:  
    def __init__(self, title, album):  
        self.title = title  
        self.album = album

# set the path to the page of a playlist in spotify
page = requests.get('https://open.spotify.com/playlist/2750zhrggozc4qBtwURxEx?si=3kG7ezbrTYiEEEys7oQUXA')

soup = BeautifulSoup(page.content, 'html.parser')
jsonStr = ""
for p in soup.find_all('script'):
    if str(p).find("Spotify.Entity =") != -1:
        jsonStr = str(p)        
        break
#REmove useless content
jsonStr = jsonStr.replace("<script>", "")
jsonStr = jsonStr.replace("Spotify = {};", "")
jsonStr = jsonStr.replace("Spotify.Entity = ", "")
jsonStr = jsonStr.replace(";", "")
jsonStr = jsonStr.replace("</script>", "")

# creating list        
list = []  

parsed_json = (json.loads(jsonStr))
for x in parsed_json['tracks']["items"]:        
        if 'track' not in x:
            continue        
        if 'album' not in x["track"]:
            continue        
        if 'name' not in x["track"]["album"]:
            continue
        #f.write(str(x))
        album = x["track"]["album"]["name"]      
        
        if 'name' not in x["track"]:
            continue
        title = x["track"]["name"]
        list.append( track(title, album) ) 

with open('Playlist.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Title', 'Album'])
    for elt in list:
        filewriter.writerow([elt.title, elt.album])
    

