#!/bin/python3

# Donwload Playlist form Youtube #

from pytube import Playlist

class Youtube_Playliat:
    def __init__(self, __url: str) -> str:
        self.__playlist = Playlist(
            __url)
        
    # Get title
    def getTitle(self):
        return self.__playlist.title
    
    # Get all videos form playlist
    def videos(self):
        videos = list()
        for i in self.__playlist:
            videos.append(i)

        return videos

    
    
    
if __name__ == '__main__':
    yp = Youtube_Playliat('https://youtube.com/playlist?list=PLi4D6ypXyLFAjfw3WrIXr8TwUSIvuuW1Z')

    print(yp.getTitle())
    yp.downloadVideo()
        
    