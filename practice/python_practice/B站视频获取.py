import requests
import re
import json
from jsonpath import jsonpath
from moviepy.video.io import ffmpeg_tools
#发起请求
def getresponse(url):
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
        "referer":"https://www.bilibili.com/",
        "cookie":"enable_web_push=DISABLE; rpdid=0zbfAI3gY3|1cVQodAUA|2V|3w1SEaKw; DedeUserID=3493104202025041; DedeUserID__ckMd5=702bdde23773028d; buvid_fp_plain=undefined; LIVE_BUVID=AUTO7817305463664915; is-2022-channel=1; CURRENT_QUALITY=80; enable_feed_channel=ENABLE; fingerprint=9bf446c544583c687402064749f20ef2; buvid_fp=9bf446c544583c687402064749f20ef2; header_theme_version=OPEN; theme-tip-show=SHOWED; theme-avatar-tip-show=SHOWED; buvid3=63F8EF95-20D7-E9B5-3A3D-61C34A1BF0BA16694infoc; b_nut=1755168316; _uuid=8FD4143D-9C25-76B3-82D10-3C4A92AFE9BD16637infoc; PVID=5; buvid4=DE37D0F8-5FAA-1BAA-E3F6-2D46D916AF0201027-024081409-Wps0OL9FICWhntUcrRinvsCfCz/kgNi+1QcucjtH1CLwvbDYFHt5LqSgy7oj6Qp7; SESSDATA=122946db%2C1772967688%2C3ad7e%2A91CjDf-z6W3AZrCyQv0UHCECZP9G97MZYrpv2pcE4ihnrRJhhvb5uhCGH6tThN2Rvt0RMSVnh6YWgzUjZDSWFwSGtXVlBFV0ZCUUx5YWpBSlNQMmtZdlZRZTZDYXFncHVnMWlqczBQcHYtSWI1VmczaU9VcTBtUEk4VHc4NGNveHRlR0U0YVViVGxRIIEC; bili_jct=144e6b5987aba4b9218a6a2e8a03eb4f; sid=51q9kx7o; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTc5MzA0NzgsImlhdCI6MTc1NzY3MTIxOCwicGx0IjotMX0.jWpK2JO2_77NY-9xHv_Pgtz9uglGEZIzJdHzCV00gSk; bili_ticket_expires=1757930418; bp_t_offset_3493104202025041=1111678866398642176; b_lsid=DD619BAE_1993D679B7B; home_feed_column=5; browser_resolution=1699-941; CURRENT_FNVAL=4048"
    }
    resp=requests.get(url,headers=headers)
    return resp
#解析请求到的网页，返回视频，音频链接,i表示画质，正着数0最高，倒着数-1最低
def handler(url):
    html = getresponse(url).text
    data = re.findall(r'"dash":(.*?),"support_formats":', html, re.S)[0]
    jsondata = json.loads(data)
    video_url = jsonpath(jsondata, "$.video..baseUrl")[0]
    audio_url = jsonpath(jsondata, "$.audio..baseUrl")[0]

    return video_url,audio_url
#保存二进制文件
def savefile(url,filename):
    content=getresponse(url).content
    with open(filename,'wb') as f:
        f.write(content)
#分别保存视频和音频
def save(video_url,audio_url,videofile,audiofile):
    savefile(video_url,videofile)
    savefile(audio_url,audiofile)
#合并视频和音频
def compose(video,audio,newfile):
    ffmpeg_tools.ffmpeg_merge_video_audio(video,audio,newfile)
#获取视频链接
def geturl():
    url = input("请输入要获取的是视频链接：")
    return url
#调用整合所有的函数
def query():
    url=geturl()
    video_url, audio_url = handler(url)
    name=input("请输入视频名称：")
    select = input("是否只下载音频：")

    video_address=fr'B站视频下载\viau_get\video\{name}.mp4'
    audio_address=fr'B站视频下载\viau_get\audio\{name}.mp3'
    if select=="是":
        download_address = input("请输入音频保存的目录（没有目录则默认）：")
        if download_address=='':
            download_address=fr"B站视频下载\viau_get\audio\{name}.mp3"
        savefile(audio_url,download_address)
        return
    download_address=input("请输入最终视频保存的目录（没有目录则默认）：")

    if download_address!="":
        download_address = fr"{download_address}\{name}.mp4"
    else :
        download_address = fr"B站视频下载\viau_get\result\{name}.mp4"
    save(video_url,audio_url,video_address,audio_address)
    compose(video_address,audio_address,download_address)

if __name__=='__main__':
    query()

