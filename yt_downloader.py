# importing modules
# by a-nonymou-s
import pytube 
from pytube import  YouTube
import bs4 as bs
import sys
import urllib.request
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
video_or_playlist = input("you want to download a video or a playlist ? \n") # requesting type from user
if video_or_playlist == 'video': # if statement (video)
    link = input("Please Enter The Video URL : \n") # requesting the video url
    video = YouTube(link) 
    print(f"The Video Title is : \n{video.title} \n") # printing the video title to the user
    print(f"The Video Description is : \n {video.description} \n") # printing the video description to the user
    print(f"The Video Views Number Are : \n {video.views} \n") # printing the number of views to the user
    print(f"The Video Rating is : \n {video.rating}\n") # printing the video rating to the user
    print(f"The Video Duration is : \n {video.length}\n") # printing the video duration to the user

    choice = input("This is your video ? [yes] or [no] ? \n") # asking the user about the video
    def finish(): # finish message function 
        print("Download Finished Successfully") # telling the user that the download has finished
    if choice == 'yes': # if statement about choice (his video)
        resolution = input("You Want The Lowest/Highest Resolution : \n") # asking user about resolution 
        if resolution == 'lowest': # if statement (lowest resolution)
            video.streams.get_lowest_resolution().download(output_path= "./video") # downloading the video
            video.register_on_complete_callback(finish()) # printing the finish message
        elif resolution == 'highest': # elif statement (highest resolution)
            video.streams.get_highest_resolution().download(output_path= "./video") # downloading the video
            video.register_on_complete_callback(finish()) # printing the finish message
        else : # else statement (resolution not found)
            print("Resolution Unavailable !\n")
    elif choice == 'no': # elif statement (not his video)
        print("Restart The Script And Enter A Valid URL ! \n")
    else : # else statement (choice not found)
        print("choice unavailable !\n")
if video_or_playlist == 'playlist': # if statement (playlist)
    class Page(QWebEnginePage):
        def __init__(self, url):
            self.app = QApplication(sys.argv)
            QWebEnginePage.__init__(self)
            self.html = ''
            self.loadFinished.connect(self._on_load_finished)
            self.load(QUrl(url))
            self.app.exec_()
    
        def _on_load_finished(self):
            self.html = self.toHtml(self.Callable)
            print('Load finished')
    
        def Callable(self, html_str):
            self.html = html_str
            self.app.quit()
    
    
    links = []
    
    
    def exact_link(link):
        vid_id = link.split('=')
        # print(vid_id)
        str = ""
        for i in vid_id[0:2]:
            str += i + "="
    
        str_new = str[0:len(str) - 1]
        index = str_new.find("&")
    
        new_link = "https://www.youtube.com" + str_new[0:index]
        return new_link
    
    
    url = input("enter a url : \n")
    # Scraping and extracting the video
    # links from the given playlist url
    page = Page(url)
    count = 0
    
    soup = bs.BeautifulSoup(page.html, 'html.parser')
    for link in soup.find_all('a', id='thumbnail'):
    
        # not using first link because it is
        # playlist link not particular video link
        if count == 0:
            count += 1
            continue
        else:
            try:
                # Prevents error for links with no href.
                vid_src = link['href']
                # print(vid_src)
                # keeping the format of link to be
                # given to pytube otherwise in some cases
                new_link = exact_link(vid_src)
    
                # error might occur due to this
                # print(new_link)
    
                # appending the link to the links array
                links.append(new_link)
            except Exception as exp:
                pass # No function necessary for invalid <a> tags.
    
    # print(links)
    
    # downloading each video from
    # the link in the links array
    for link in links:
        yt = pytube.YouTube(link)
    
        # Downloaded video will be the best quality video
        stream = yt.streams.filter(progressive=True,file_extension='mp4').order_by(
            'resolution').desc().first()
        try:
            stream.download(output_path="./playlist")
            # printing the links downloaded
            print("Downloaded: ", link)
        except:
            print('Some error in downloading: ', link)
