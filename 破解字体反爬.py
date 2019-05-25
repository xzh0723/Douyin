

from urllib.request import urlretrieve
from fontTools.ttLib import TTFont
import re
from scrapy import Selector
import requests

# 百度字体编辑器打开提前下载好的字体文件，得出以下字典
num_dict = {
    'num_': '1', 'num_1': '0', 'num_2': '3', 'num_3': '2', 'num_4': '4', 'num_5': '5', 'num_6': '6', 'num_7': '9',
    'num_8': '7', 'num_9': '8'
}

# 获取cmap映射
font_url = 'https://s3.pstatp.com/ies/resource/falcon/douyin_falcon/static/font/iconfont_9eb9a50.woff'
urlretrieve(font_url, 'douyin.woff')
font = TTFont('douyin.woff')
cmap = font.getBestCmap()
print(cmap)
font_dict = {}
for k, v in cmap.items():
    key = "&#x{:x}".format(k)
    value = v
    font_dict[key] = value
print(font_dict)

url = 'https://www.iesdouyin.com/share/user/96804266953?u_code=14d3hl0m2&utm_campaign=client_share&app=aweme&utm_medium=ios&tt_from=copy&utm_source=copy'

headers = {
    'accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': '_ga=GA1.2.1915370291.1558628984; _gid=GA1.2.831588782.1558628984',
    'referer': 'https://www.iesdouyin.com/share/user/96804266953?u_code=14d3hl0m2&utm_campaign=client_share&app=aweme&utm_medium=ios&tt_from=copy&utm_source=copy',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Mobile Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

r = requests.get(url, headers=headers)
# print(r.text)
dytk = re.search("dytk: '(.*?)'", r.text, re.S).group(1)
print(dytk)

# 昵称
selector = Selector(text=r.text)
nickname = selector.css('.nickname::text').extract_first()
print(nickname)

# ID
id_ = re.findall('<i class="icon iconfont "> (.*?); </i>', r.text, re.S)
print(id_)
real_id = ''
for num in id_:
    if num in list(font_dict.keys()):
        real_num = num_dict[font_dict[num]]
        real_id += real_num
    else:
        real_id += num
print(real_id)

# 签名
signature = selector.css('.signature::text').extract_first()
print(signature)

# 关注
focus = re.findall('<i class="icon iconfont follow-num"> (.*?); </i>', re.search('<span class="focus block">(.*?)</span>', r.text, re.S).group(1), re.S)
print(focus)
real_focus_num = ''
for num in focus:
    if num in list(font_dict.keys()):
        real_num = num_dict[font_dict[num]]
        real_focus_num += real_num
    else:
        real_focus_num += num
print(real_focus_num)

# 粉丝
real_follower_num = re.search('<span class="follower block">(.*?)</span>', r.text, re.S).group(1).replace('<i class="icon iconfont follow-num"> ', '').replace('; </i>', '').replace('<span class="num">', '').strip()
print(real_follower_num)
follower = re.findall('<i class="icon iconfont follow-num"> (.*?); </i>', re.search('<span class="follower block">(.*?)</span>', r.text, re.S).group(1), re.S)
print(follower)
for num in follower:
    if num in list(font_dict.keys()):
        real_num = num_dict[font_dict[num]]
        real_follower_num = re.sub(num, real_num, real_follower_num)
print(real_follower_num)

# 点赞
real_like_num = re.search('<span class="liked-num block">(.*?)</span>', r.text, re.S).group(1).replace('<i class="icon iconfont follow-num"> ', '').replace('; </i>', '').replace('<span class="num">', '').strip()
print(real_like_num)
liked = re.findall('<i class="icon iconfont follow-num"> (.*?); </i>', re.search('<span class="liked-num block">(.*?)</span>', r.text, re.S).group(1), re.S)
print(liked)
for num in liked:
    if num in list(font_dict.keys()):
        real_num = num_dict[font_dict[num]]
        real_like_num = re.sub(num, real_num, real_like_num)
print(real_like_num)

# 作品
videos_num = re.search('作品<span class="num">(.*?)</span>', r.text, re.S).group(1).replace('<i class="icon iconfont tab-num"> ', '').replace('; </i>', '').strip()
print(videos_num)
videos = re.findall('<i class="icon iconfont tab-num"> (.*?); </i>', re.search('作品<span class="num">(.*?)</span>', r.text, re.S).group(1), re.S)
print(videos)
for num in videos:
    if num in list(font_dict.keys()):
        real_num = num_dict[font_dict[num]]
        videos_num = re.sub(num, real_num, videos_num)
print(videos_num)

# 喜欢
likes_num = re.search('喜欢<span class="num">(.*?)</span>', r.text, re.S).group(1).replace('<i class="icon iconfont tab-num"> ', '').replace('; </i>', '').strip()
print(videos_num)
likes = re.findall('<i class="icon iconfont tab-num"> (.*?); </i>', re.search('喜欢<span class="num">(.*?)</span>', r.text, re.S).group(1), re.S)
print(likes)
for num in likes:
    if num in list(font_dict.keys()):
        real_num = num_dict[font_dict[num]]
        likes_num = re.sub(num, real_num, likes_num)
print(likes_num)
