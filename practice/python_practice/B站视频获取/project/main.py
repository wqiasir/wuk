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
    }
    resp=requests.get(url,headers=headers)
    return resp
#获取视频音频下载链接
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

    video_address=fr'project\viau_get\video\{name}.mp4'
    audio_address=fr'project\viau_get\audio\{name}.mp3'
    if select=="是":
        download_address = input("请输入音频保存的目录（没有目录则默认）：")
        if download_address=='':
            download_address=fr"project\viau_get\audio\{name}.mp3"
        savefile(audio_url,download_address)
        return
    download_address=input("请输入最终视频保存的目录（没有目录则默认）：")

    if download_address!="":
        download_address = fr"{download_address}\{name}.mp4"
    else :
        download_address = fr"project\viau_get\result\{name}.mp4"
    save(video_url,audio_url,video_address,audio_address)
    compose(video_address,audio_address,download_address)

if __name__=='__main__':
    query()
