# Python 2.7.12
# Written by Trevor McGuire
# GitHub: onzie9

from bs4 import BeautifulSoup
import requests
import re
import time
from torrequest import TorRequest
import numpy as np
from copy import deepcopy
import urllib
# These first three lines are just setting up how I want my data to be written.  They are set to amend currently because
# the code scrapes in segments, so the resulting file gets written to multiple times.
#ingredients_file = open("ingredients_file.txt", "a+")
recipelinkfile = open("recipelinkfile.txt", "a+")
videolinkfile = open("videolink.txt", "a+")
ingrfile =open("ingredients.txt","a+")
recipenamefile = open("recipenamefile.txt","a+")
recipefile = open("recipefile.txt","a+")
notincludedvideofile = open("notincludedvideofile.txt", "a+")
#no_recipe = open("no_recipes.txt", "a+")
equalsigns = "======================================="
kk = 588#181
for j in np.arange(0, 19997, 12):
	for i in range(kk + j, kk + j + 12):  # The 241927 is just the last place I scraped.  The unique recipes
												  # were really sparse out this far.
		#try:
		r = requests.get("http://allrecipes.com/video/" + str(i))
		soup = BeautifulSoup(r.text, "html.parser")  # First download the code for the individual recipe.
		videolink =deepcopy(r)
		#mother = soup.find("ul", {"id": "lst_ingredients_1"}).parent
		#children = str(mother.findAll("span", {"itemprop": "ingredients"}))
		#children = re.sub(r'<.+?>', '', children)
		#children = re.sub(", ([0-9])", "\n \\1", children)

		type = str(soup.find("a", {"data-click-id": "recipe breadcrumb 3"}))
		type = re.sub(r'<.+?>', '', type)
		type = type.strip()
		print(r.url.split("/")[-2])
		print(r.url)
		recipetype = str(soup.find("a", {"class": "btns-one-large"}))
		if(recipetype.find("href=\"https://www.allrecipes.com/recipe/")!=-1):
			recipetype = (recipetype.split("href=\"")[1]).split(">")[0][:-1]
			print(recipetype)
			# videolinkfile.write(r.url + "\n")
			# recipelinkfile.write(recipetype + "\n")
			r = requests.get(recipetype)
			#soup = BeautifulSoup(r.text, "html.parser")
			#soup.clear(                            )
			soup.clear()
			rt = r.text
			with TorRequest(proxy_port=9050, ctrl_port=9051, password=None) as tr:
				tr.reset_identity()
			soup = BeautifulSoup(re.sub("<!--|-->","", rt), "html.parser")
			# recipenamefile.write(r.url.split("/")[-2] + "\n")
			mother = soup.find("ul", {"id": "lst_ingredients_1"})
			count = 0
			while mother is None and count<5:
				print("Yo")
				count = count + 1
				r1 = requests.get(recipetype)
				soup.clear()
				rt1 = r1.text
				with TorRequest(proxy_port=9050, ctrl_port=9051, password=None) as tr:
					tr.reset_identity()
				soup = BeautifulSoup(re.sub("<!--|-->","", rt1), "html.parser")
				mother = soup.find("ul", {"id": "lst_ingredients_1"})

			if mother is not None:
				mother = mother.parent
				children = str(mother.findAll("label", {"ng-class": "{true: 'checkList__item'}[true]"}))
				children = re.sub(r'<.+?>', '', children)
				children = str(children)
				children = re.sub("\n", '', children)
				children = re.sub(", ([0-9])", "\n \\1", children)
				#print ("HERE")
				print(children)
				ingrfile.write(children+"\n")
				videolinkfile.write(videolink.url + "\n")
				recipelinkfile.write(recipetype + "\n")
				recipenamefile.write(r.url.split("/")[-2] + "\n")

				mother = soup.find("div", {"class": "hero-photo__wrap"})
				children = str((mother.findAll("img", {"class": "rec-photo"})))
				imglink = (children.split("src=\"")[1]).split("/>")[0][:-1]
				print(imglink)
				filename = str("allphotos/" + r.url.split("/")[-2] + ".jpg")
				urllib.request.urlretrieve(imglink, filename)


				mother = soup.find("ol", {"class": "list-numbers recipe-directions__list"})
				children = str(mother.findAll("span", {"class": "recipe-directions__list--item"}))
				children = re.sub(r'<.+?>', '', children)
				children = str(children)
				children = re.sub("\n", '', children)
				children = re.sub("                            ,", '', children)
				children = re.sub("                            ", '', children)
				recipefile.write(children + "\n")
				print(children)

			else:
				notincludedvideofile.write(videolink.url + "\n")
			# 	mother = soup.find("span", {"class": "ingredients-item-name"})
			# 	if mother is not None:
			# 		mother = mother.parent
			# 		print ("HERE1")
			# 		print (mother)
			# 		children = str(mother.findAll("label", {"ng-class": "{true: 'checkList__item'}[true]"}))
			# 		children = re.sub(r'<.+?>', '', children)
			# 		children = str(children)
			# 		children = re.sub("\n", '', children)
			# 		children = re.sub(", ([0-9])", "\n \\1", children)
			# 		print ("HERE2")
			# 		print(children)
			# 		ingrfile.write(children+"\n")
			# 		videolinkfile.write(r.url + "\n")
			# 		recipelinkfile.write(recipetype + "\n")
			# 		recipenamefile.write(r.url.split("/")[-2] + "\n")

			# mother = soup.find("ul", {"class": "ingredients-section"}).parent
			# children = str(mother.findAll("input", {"ng-class": "{true: 'checkList__item'}[true]"}))
			# children = re.sub(r'<.+?>', '', children)
			# children = str(children)
			# children = re.sub("\n", '', children)
			# children = re.sub(", ([0-9])", "\n \\1", children)


			# print(children)
			# ingrfile.write(children+"\n")
			print(i)
		with TorRequest(proxy_port=9050, ctrl_port=9051, password=None) as tr:
			tr.reset_identity()
		# if (type == "Desserts" or type == "Appetizer and Snacks" or type == "Salad" or type == "Breakfast and Brunch" or type == "Side Dish" or type == "Drinks" or type =="Bread"):
		#                 # This writes the recipe to a specific file.
		#     #ingredients_file.write("\n" + equalsigns + "\n" + r.url.split("/")[-2] + "\n" + str(i) + " " + type +
		#     #                       "\n" + children)
		#     namefile.write(r.url + "\n")
		# else:
		#     #ingredients_file.write("\n" + equalsigns + "\n" + r.url.split("/")[-2] + "\n" + str(i) + " main" + "\n"
		#     #                       + children)
		#     namefile.write(r.url + "\n")
		#except:
			#no_recipe.write(str(i) + ", ")  # There are thousands of recipe numbers that aren't used.
		#    print("no recipe for some reason")
		#print(str(i))
		time.sleep(1.7)  # This is needed to prevent getting banned.
	# This is the only line that is related to Tor.  In order to make Tor work, you need this line of code, and you also
	#  have to modify the torrc.txt file.  In that file, you need to uncomment the "controlport 9051" line, and then
	# uncomment the "hashed control password" line.  You also have to paste in a hash of your own password.  Get the
	# hash with 'tor --hash-password <mypassword>'.
	with TorRequest(proxy_port=9050, ctrl_port=9051, password=None) as tr:
		tr.reset_identity()
