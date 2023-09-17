#!/bin/python3

'''Download videos form Youtube v0.1
by:Ahmed Hossam
ahmedhosam.dev@gmail.com
'''

import telebot
from telebot import types
from Download_From_Youtube import Youtube_video
from Download_Playlist import Youtube_Playliat
from pytube.exceptions import VideoUnavailable
from userInfo import User
from decouple import config


# Setup
BOT_TOKEN = config('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
userCount = 0


######### Code ######### 

# /help -> get all commands
@bot.message_handler(["help"])
def help(message):
    bot.send_message(message.chat.id, "Hi, for now you can just send Youtube video url.\nCommands:\n\t - None")

# /start -> Hi, How can i help you today?
@bot.message_handler(["start"])
def start(message):
    try:
        newUser = User(message.from_user.id, message.chat.id, userCount + 1)
        # newUser.saveToFile()
    except Exception as e:
        print(f"Error: {e}")

    bot.send_message(message.chat.id, "Hi, how can i help you today?\n\n/help to get all commands")
    


# Get URL from user and send it to get info function to send data
@bot.message_handler(func=lambda message: True)
def url(message):


    # Check if the url is from Youtube
    if message.text.startswith(('https://www.youtube.com', 'https://youtu.be', 'https://youtube.com')):

        # Check if the url is a video or a list
        if message.text.startswith(('https://www.youtube.com/playlist', 'https://www.youtube.com/watch', 'https://youtu.be/playlist', 'https://youtu.be/watch', 'https://youtube.com/playlist', 'https://youtube.com/watch')):
            
            #! -----> Play list: send a zip file have all videso 

            yp = Youtube_Playliat(message.text)
            bot.send_message(message.chat.id, yp.getTitle())
            
            for video in yp.videos():
                try:
                    global ytb
                    ytb = Youtube_video(video)
                    ifVideo(message)
                except VideoUnavailable as v:
                    bot.send_message(message.chat.id, f"Video {video} is unavaialable: {v}")


        # Youtube video
        else:
            try:
                global yt
                yt = Youtube_video(message.text)
                bot.send_message(message.chat.id, "wait while getting video resolution..")
                ifVideo(message)
            except Exception as e:
                bot.send_message(message.chat.id, f"Error! {e}.")

# Donload Video when user pres resolution button 
@bot.callback_query_handler(lambda call: True)
def download_video_callback(call):
    bot.answer_callback_query(call.id, "Downloading")
    bot.send_message(call.message.chat.id, "Wait while sending...")

    try:
        bot.send_document(call.message.chat.id, yt.bufferStream(call.data), visible_file_name=f"{yt.getTitle()}.mp4", caption=f"{yt.getTitle()}", timeout=30*60)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Error while sending: {e}")
##### محتاجين نعمل تسجيل دخول

# video
def ifVideo(message):

    markup = types.InlineKeyboardMarkup()

    res = yt.getVideoRes()
    for i in res.keys():
        button = types.InlineKeyboardButton(f"{res[i][1]} | {yt.getFileSize(i)}", callback_data=str(i))
        markup.add(button)

    bot.send_photo(message.chat.id, message.text, reply_markup=markup)



print("Run..")
bot.polling()
print("\nStoped")


