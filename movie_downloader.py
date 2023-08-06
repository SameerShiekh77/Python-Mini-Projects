import requests
from bs4 import BeautifulSoup

url = 'http://cdn.watcho.pk/ds5/englishmoviesdub/B/Barbie.2023.Scr.Dual.mkv'
#create response object
r = requests.get(url, stream = True)
file_name = "Barbie +.mp4"  

#download started
with open(file_name, 'wb') as f:
    for chunk in r.iter_content(chunk_size = 1024*1024):
        if chunk:
            f.write(chunk)

print ("%s downloaded!\n"%file_name)
print ("All videos downloaded!")
