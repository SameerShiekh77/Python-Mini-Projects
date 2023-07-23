import requests


for episode_number in range(1, 31):
    if episode_number < 10:
        link = f'http://video.watcho.pk/stream/videosection/tvserials/FaroukOmar/FaroukOmar-Ep0{episode_number}.mp4'
        file_name = "FaroukOmar-Ep0"+str(episode_number)+".mp4"  
    else:
        link = f'http://video.watcho.pk/stream/videosection/tvserials/FaroukOmar/FaroukOmar-Ep{episode_number}.mp4'
        file_name = "FaroukOmar-Ep"+str(episode_number)+".mp4"  
    
 
 
    print ("Downloading file:%s"%file_name)
 
    #create response object
    r = requests.get(link, stream = True)
 
    #download started
    with open(file_name, 'wb') as f:
      for chunk in r.iter_content(chunk_size = 1024*1024):
        if chunk:
          f.write(chunk)
 
    print ("%s downloaded!\n"%file_name)
 
