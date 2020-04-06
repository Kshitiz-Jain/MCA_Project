from gtts import gTTS
import os
import os
import json
import time
import logging
import urllib.request
import urllib.error
from urllib.parse import urlparse, quote
import numpy as np
import glob
from multiprocessing import Pool
from user_agent import generate_user_agent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



def get_image_links(main_keyword, num_requested = 1):
	number_of_scrolls = int(num_requested / 400) + 1 
	img_urls = []
	driver = webdriver.Firefox()
	search_query = quote(main_keyword)
	url = "https://www.google.com/search?q="+search_query+"&source=lnms&tbm=isch"
	driver.get(url)
	thumbs = driver.find_elements_by_xpath('//a[@class="wXeWr islib nfEiy mM5pbd"]')
	count = 0
	while count<len(thumbs) and len(img_urls)<1:
		try:
			thumbs[count].click()
			time.sleep(1)
		except e:
			print("Error clicking one thumbnail")

		url_elements = driver.find_elements_by_xpath('//img[@class="n3VNCb"]')
		for url_element in url_elements:
			try:
				url = url_element.get_attribute('src')
			except e:
				print("Error getting one url")

			if url.startswith('http') and not url.startswith('https://encrypted-tbn0.gstatic.com'):
				img_urls.append(url)
				print("Found image url: " + url)
		count = count+1
	driver.quit()
	return img_urls[0]


def download_images(link, count):
	headers = {}
	try:
		o = urlparse(link)
		ref = o.scheme + '://' + o.hostname
		ua = generate_user_agent()
		headers['User-Agent'] = ua
		headers['referer'] = ref
		print('\n{0}\n{1}\n{2}'.format(link.strip(), ref, ua))
		req = urllib.request.Request(link.strip(), headers = headers)
		response = urllib.request.urlopen(req)
		data = response.read()
		file_path = './IngredientImages/' + 'image{0}.jpg'.format(count)
		with open(file_path,'wb') as wf:
			wf.write(data)
	except urllib.error.URLError as e:
		print('URLError')
	except urllib.error.HTTPError as e:
		print('HTTPError')
	except Exception as e:
		print('Unexpected Error')

f = open("ingredientsnew.txt", "r")
f = f.read()
f = f.replace("]","")
f = f.split("[")
f = list(filter(None, f))
ingredients = f[0].split('\n')[:3]
ingredients = sorted(ingredients)
print(ingredients)

links = []
for keyword in ingredients:
	print(keyword)
	links.append(get_image_links(keyword))
print(links)

for i in range(len(links)):
	download_images(links[i], i)


count = 0
for mytext in ingredients:
	language = 'en'
	myobj = gTTS(text=mytext, lang=language, slow=False)
	myobj.save("welcome_1.mp3")
	os.system("mpg321 welcome_1.mp3")
	os.system('ffmpeg -i welcome_1.mp3 -af "adelay=1000|1000" welcome11.mp3')
	os.system('ffmpeg -i welcome11.mp3 -af "apad=pad_dur=1" welcome1.mp3')
	os.remove("welcome_1.mp3")
	os.remove("welcome11.mp3")
	os.system('ffmpeg -i ./IngredientImages/image{i}.jpg -i welcome1.mp3 -c:a aac -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" ./IngredientVideos/final{i}.mp4'.format(i=count))
	os.remove("welcome1.mp3")
	count+=1


for i in glob.glob("./IngredientImages/*.jpg"):
    os.remove(i)

videos = glob.glob("./IngredientVideos/*.mp4")


for i in videos:
	with open('./myfilelist.txt','a+') as wf:
		i = i.replace('\\', '/')
		wf.writelines(['file ',i,'\n'])


os.system('ffmpeg -f concat -safe 0 -i myfilelist.txt -filter_complex \"[0:v]setpts=PTS-STARTPTS[v0]; [0:a]asetpts=PTS-STARTPTS[a0]; [1:v]setpts=PTS-STARTPTS[v1]; [1:a]asetpts=PTS-STARTPTS[a1]; [2:v]setpts=PTS-STARTPTS[v2]; [2:a]asetpts=PTS-STARTPTS[a2]; [v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]\" -map \"[v]\" -map \"[a]\" -c:v copy output.mp4')

for i in glob.glob("./IngredientVideos/*.mp4"):
    os.remove(i)

os.remove('./myfilelist.txt')