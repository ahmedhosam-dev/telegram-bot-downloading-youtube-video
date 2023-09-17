#!/bin/python3

'''Download videos form Youtube v0.1
by:Ahmed Hossam
ahmedhosam.dev@gmail.com
'''

from pytube import YouTube
from io import BytesIO



class Youtube_video():
    def __init__(self, __url: str) -> str:
        self.__video = YouTube(__url)
        

    # Check video
    def checkAvailability(self):
        return self.__video.check_availability()
    
    # Get Url info title, thumbnail, quality 
    def getTitle(self):
        return self.__video.title
    
    def getThumbnailUrl(self):
        return self.__video.thumbnail_url
    

    # Get video res
    def getVideoRes(self):
        stream = self.__video.streams

        res = dict()
        
        for i in stream.filter(progressive=True): # !----> Should be faster  
            if i.mime_type != "video/webm":
                res[i.itag] = [i.mime_type, i.resolution]

        for j in stream.filter(only_audio=True):
            if j.mime_type != "audio/webm":
                res[j.itag] = [j.mime_type, f"Audio: {j.abr}"] # <-------

        return res
    
    # Get url to download from web
    def urlDownloader(self, itag: int) -> int:
        return self.__video.streams.get_by_itag(itag).url
    
    
    # Get file size
    def getFileSize(self, itag: int) -> int:
        file_size = self.__video.streams.get_by_itag(itag).filesize / 1024

        if file_size < 500: # -> kb
            return f"{int(file_size)}kb"
        elif file_size > 500: # -> mb
            return f"{int(file_size / 1024)}mb"
        else: # -> kb
            return f"{int(file_size)}kb"

    
    # Buffer stream
    def bufferStream(self, itag: int) -> int:
        buffer = BytesIO()
        vid = self.__video.streams.get_by_itag(itag)
        vid.stream_to_buffer(buffer)
        buffer.seek(0)

        return buffer
    
    # # Read buffer
    # def readBuffer(self, buffer):
    #     cont = buffer.read()
    #     buffer.close()
    #     return cont
        

    # Download the Video
    def downloadVideo(self, itag: int, path: str | None = None, filename: str | None = None) -> str:
        try:
            self.__video.streams.get_by_itag(itag=itag).download(path, filename)
        except NameError as n:
            print(n)
            
    

if __name__ == '__main__':
    pass
    