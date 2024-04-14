import requests, re
import pandas as pd
from bs4 import BeautifulSoup as bs


data = pd.read_excel('watcho.xlsx')
links = data['link']


for index,link in enumerate(links):
    #create response object
    r = requests.get(link, stream = True)
    html_content = r.content
    website_html_content = bs(html_content, 'html.parser')
   # Find the button element
    button = website_html_content.find('button', class_='fbdownload')
    if button:
        # Get the onclick attribute value
        onclick_value = button.get('onclick')
        # Use regular expressions to extract the URL from the onclick value
        url_match = re.search(r"window\.open\('([^']+)", onclick_value)
        if url_match:
            download_url = url_match.group(1)
            r = requests.get(download_url, stream = True)
            file_name = data['name'][index] + '.mp4'

            #download started
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size = 1024*1024):
                    if chunk:
                        f.write(chunk)

            print ("%s downloaded!\n"%file_name)
            
print("Done")
