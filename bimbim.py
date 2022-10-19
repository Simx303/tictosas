from http import client
from traceback import print_tb
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import subprocess

# api = TikTokApi()
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('diss-16542-ce4a3b3ea8c5.json',scope)
client = gspread.authorize(creds)
sheet = client.open('TicTos').sheet1

api = "https://tiktok-downloader-download-videos-without-watermark1.p.rapidapi.com/media-info/"
reheaders = {
	"X-RapidAPI-Key": "0db409fb4dmshd417a3f9dbb2e69p1c2528jsn15a9cf81046f",
	"X-RapidAPI-Host": "tiktok-downloader-download-videos-without-watermark1.p.rapidapi.com"
}



def tick(vurl):
    print("vurl start")
    response = requests.request("GET", api, headers=reheaders, params={"link":vurl}).json()["result"]
    desc = response['aweme_detail']['desc']
    author = response['aweme_detail']['author']['unique_id']
    title = desc.split('#')[0]
    id = response['aweme_id']
    tags= []
    for n in desc.split('#')[1:]:
        tags.append(n.replace(" ",""))
    waturl = response['video']['url_list'][0]
    # print("URL: "+waturl)
    # print("AUTHOR: "+author)
    # print("TITLE: "+title)
    # print("TAGS: "+", ".join(tags))
    # print("THE TIC: https://www.tiktok.com/@{}/video/{}".format(author,id))
    sheet.insert_row(["https://www.tiktok.com/@{}/video/{}".format(author,id), waturl, author, title, ", ".join(tags)],2)

    r = requests.get(waturl).content
    with open(f"vids/"+author+".mp4", "wb+") as f:
        f.write(r)
    subprocess.call(['python','ytupld.py','--file=C:/Users/User/Desktop/Simx_Projekts/Python/tiktok-short/vids/{}.mp4'.format(author), '--title={}'.format(title+" @"+author), '--keywords="{}"'.format(", ".join(tags)), '--privacyStatus=private'], shell=True)
