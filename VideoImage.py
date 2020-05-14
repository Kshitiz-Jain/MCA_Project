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
import cv2

# os.remove('./output.avi')

from PIL import Image, ImageFont, ImageDraw

def text_wrap(text, font, max_width):
	lines = []
	if font.getsize(text)[0] <= max_width:
		lines.append(text) 
	else:
		words = text.split(' ')  
		i = 0
		while i < len(words):
			line = ''         
			while i < len(words) and font.getsize(line + words[i])[0] <= max_width:                
				line = line + words[i] + " "
				i += 1
			if not line:
				line = words[i]
				i += 1
			lines.append(line)    
	return lines

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
ingredients = f[0].split('\n')#
ingredients = sorted(ingredients)
while("" in ingredients) : 
	ingredients.remove("") 
# ingredients = ingredients[:4]
print(ingredients)

links = []
for keyword in ingredients:
	print(keyword)
	links.append(get_image_links(keyword))# + " hd"
print(links)

for i in range(len(links)):
	download_images(links[i], i)


count = 0
for mytext in ingredients:
	language = 'en'
	myobj = gTTS(text=mytext, lang=language, slow=False)
	myobj.save("welcome_1.mp3")
	os.system("mpg321 welcome_1.mp3")
	os.system('ffmpeg -i "welcome_1.mp3" -acodec copy "welcome_1a.mp3')
	os.system('ffmpeg -i welcome_1a.mp3 -af "adelay=1000|1000" welcome11.mp3')
	os.system('ffmpeg -i "welcome11.mp3" -acodec copy "welcome11a.mp3')
	os.system('ffmpeg -i welcome11a.mp3 -af "apad=pad_dur=1" welcome1.mp3')
	os.system('ffmpeg -i welcome1.mp3 -codec:a libmp3lame -b:a 32k welcome1a.mp3')
	# os.system('ffmpeg -i "welcome1.mp3" -acodec copy "welcome1a.mp3')
	os.remove("welcome_1.mp3")
	os.remove("welcome11.mp3")
	os.remove("welcome_1a.mp3")
	os.remove("welcome11a.mp3")
	img = cv2.imread('./IngredientImages/image{i}.jpg'.format(i=count), cv2.IMREAD_UNCHANGED)
	resized = cv2.resize(img, (720,720), interpolation = cv2.INTER_AREA)
	cv2.imwrite('./IngredientImages/image{i}.jpg'.format(i=count), resized)

	img = Image.open('./IngredientImages/image{i}.jpg'.format(i=count))
	image_size = img.size
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype('arial.ttf', size=50, encoding="unic")

	text = mytext
	lines = text_wrap(text, font, image_size[0])
	line_height = font.getsize('hg')[1]
	x = 10
	if(len(lines)==1):
		y = 650
	elif (len(lines) == 2):
		y = 495
	elif(len(lines) == 3):
		y = 450
	elif(len(lines)==4):
		y = 405
	for line in lines:
		draw.text((x-1, y-1), line, font=font, fill='black')
		draw.text((x+1, y-1), line, font=font, fill='black')
		draw.text((x-1, y+1), line, font=font, fill='black')
		draw.text((x+1, y+1), line, font=font, fill='black')
		draw.text((x, y), line, fill='white', font=font)
		y = y + line_height
	img.save('./IngredientImages/image{i}.jpg'.format(i=count))#, optimize=True)



	os.system('ffmpeg -loop 1 -y -i ./IngredientImages/image{i}.jpg -i welcome1a.mp3 -shortest -acodec copy -vcodec mjpeg ./IngredientVideos/result{i}.avi'.format(i=count))
	# os.system('ffmpeg -i ./IngredientImages/image{i}.jpg -i welcome1.mp3 -c:a aac -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" ./IngredientVideos/final{i}.mp4'.format(i=count))
	os.remove("welcome1.mp3")
	os.remove("welcome1a.mp3")
	count+=1




videos = glob.glob("./IngredientVideos/*.avi")

with open('./myfilelist.txt','a+') as wf:
		wf.writelines(['#This is a comment','\n'])
for i in videos:
	with open('./myfilelist.txt','a+') as wf:
		i = i.replace('\\', '/')
		wf.writelines(['file ',i,'\n'])


os.system('ffmpeg -f concat -safe 0 -i myfilelist.txt -c copy output.avi')

# for i in glob.glob("./IngredientVideos/*.avi"):
    # os.remove(i)
# for i in glob.glob("./IngredientImages/*.jpg"):
    # os.remove(i)

os.remove('./myfilelist.txt')

#https://mail.python.org/pipermail/image-sig/2009-May/005681.html
#https://haptik.ai/tech/putting-text-on-images-using-python-part2/