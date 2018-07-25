import realtimelrc
import vlc
from time import sleep
import pylyrics
from os.path import basename
import os
import sys

OFFSET = 0 #263
os.system('clear')
#for i in range(14):
#    print('')
filepath = input('''Standby. Drag n' drop to play >''')

##UNIX specific
filepath = filepath.strip()
filepath = filepath.replace('\\', '')
filepath = filepath.replace('\ ', ' ')

keyword = basename(filepath)
new_search = pylyrics.NeteaseSearch(keyword = keyword)



songID = new_search.get_song_ID()

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#print(new_search.get_song_url(encryptedID))
print('Searching lyrics for {}...'.format(keyword))
#with open('./fripSide - Run into the light.lrc','r') as lrcfile:
lrctext = new_search.lrc()

song = vlc.MediaPlayer(filepath)
song.play()
os.system('clear')
#for i in range(14):
#    print('')
lyrics = realtimelrc.RTLyrics(lrctext)
sleep(2)
for i in range(10000):
    sleep(0.1)
    ts = vlc.libvlc_media_player_get_time(song)
    #print(ts, end = ' ')
    output = lyrics.current_lyrics(ts + OFFSET)
    ts=str(ts)
    ts=ts.center(8)
    #output=output.center(60)
    sys.stdout.write(' Timestamp: ' + ts +'ms  '+ output + '\r')
    sys.stdout.flush()
    #print(lyrics.current_lyrics(ts + OFFSET), end = '')
    