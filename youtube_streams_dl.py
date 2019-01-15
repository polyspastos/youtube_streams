# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from pytube import YouTube
from bs4 import BeautifulSoup as bs
from time import sleep

link = "https://www.youtube.com/results?search_query=kontrust"
# link = "https://www.youtube.com/results?search_query=javascript"
# link = "https://www.youtube.com/results?sp=EgYIBBABGAI%253D&search_query=puzs%C3%A9r"
# link = "https://www.youtube.com/results?search_query=hilltop+hoods"


proper_link = requests.get(link.replace(" ", "+"))
page = proper_link.text
soup = bs(page, 'html.parser')
videos = soup.findAll('a', attrs={'class': 'yt-uix-tile-link'})

videolist = []
for v in videos:
    link = 'https://www.youtube.com' + v['href']
    videolist.append(link)

# for vl in videolist:
#     print(vl)
# wait = input()

result_list = []


while len(result_list) < len(videolist):
    print(len(result_list))
    try:
        for vl in range(0, len(videolist)):
            print("{}.: ".format(vl+1), end='')
            if (("list" not in videolist[vl]) and ("user" not in videolist[vl]) and ("googlead" not in videolist[vl])):
                result = "{}".format(videolist[vl])
                yt = YouTube(result)
                print(yt.title)
                unique = ["PLAYLIST", "USER", "ADVERTISEMENT", "REGEXP", "EXCEPTION"]
                if (result not in result_list) or (result not in unique):
                    result_list.append(result)
            elif ("list" in videolist[vl]):
                print("--- This result is a playlist. ---")
                result_list.append("PLAYLIST")
            elif ("user" in videolist[vl]):
                print("--- This result is a user. ---")
                result_list.append("USER")
            elif ("googlead" in videolist[vl]):
                print("--- This result is an advertisement. ---")
                result_list.append("ADVERTISEMENT")
            elif ("regex" in videolist[vl]):
                print("--- Unhandled regexp pattern. ---")
                result_list.append("REGEXP")
    except Exception as e: #pytube.exceptions.RegexMatchError
        print(e)
        result_list.append("EXCEPTION")

required_stream_number = "0"
required_links = []
print("Please type the numbers of the streams you would like to download, press enter after each one, and type: \"end\" after the last one!")
print("Use \"all\" to download everything.")
while required_stream_number != "end":
    required_stream_number = input()
    if required_stream_number == "all":
        required_stream_number = "end"
        for i in range(0, len(result_list)):
            if result_list[i] != "--- PLAYLIST ---" or result_list[i] != "--- USER ---":
                required_links.append(result_list[i])
    if required_stream_number != "end":
        required_links.append(result_list[int(required_stream_number)-1])

for link in required_links:
    print(link)
wait2 = input()

for rsn in range(0, len(required_links)):
    required_result = required_links[rsn]
    print(required_result)
    if (required_result != "--- PLAYLIST ---") or (required_result != "--- USER ---"):
        try:
            yt_req = YouTube(required_result)
            print("Downloading", yt_req.title)
            stream = yt_req.streams.filter(only_audio=True).first() #.filter(only_audio=True)
            stream.download()
            print("Done!\n")
        except Exception as e:
            print(e)
            print("Result is not a link.\n")
