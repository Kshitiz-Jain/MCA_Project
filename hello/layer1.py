import json
import cv2
import re
import random
ingredientsfile = open("ingredients.txt", "r").read()
recipefile = open("recipefile.txt", "r").read()
titlefile = open("recipenamefile.txt", "r").read()
urlfile = open("recipelinkfile.txt", "r").read()

keys = ["ingredients", "url", "partition", "title", "id", "instructions"]

ingr = []
start = [i.start() for i in re.finditer("\[", ingredientsfile)]
end = [i.start() for i in re.finditer("\]", ingredientsfile)]

for i in range(len(start)):
	ingr.append(ingredientsfile[start[i]:end[i]].replace("\n",";").split("[")[1].split(";"))

recipefile = recipefile.replace("        Watch Now","")
recipefile = recipefile.replace(".,",".")
recipes = []
start = [i.start() for i in re.finditer("\[", recipefile)]
end = [i.start() for i in re.finditer("\]", recipefile)]

for i in range(len(start)):
	recipes.append(recipefile[start[i]:end[i]].split("[")[1].split("\n"))
# print (recipes)

titles = titlefile.split("\n")[:-1]
urls = urlfile.split("\n")[:-1]
ids = []
for element in urls:
	start = [i.start() for i in re.finditer("\/", element)]
	ids.append(str(element[start[3]+1:start[4]]))

finalingr = []
for i in range(len(ingr)):
	lis = []
	for j in range(len(ingr[i])):
		dic = {}
		dic["text"] = ingr[i][j]
		lis.append(dic)
	finalingr.append(lis)

finalrecipe = []
for i in range(len(recipes)):
	lis = []
	rec = recipes[i][0].split(".")
	for j in range(len(rec)-1):
		dic = {}
		dic["text"] = rec[j]
		lis.append(dic)
	finalrecipe.append(lis)


finallist = []
for i in range(len(finalrecipe)):
	dictionary = {}
	dictionary["ingredients"] = finalingr[i]
	dictionary["instructions"] = finalrecipe[i]
	dictionary["url"] = urls[i]
	dictionary["title"] = titles[i]
	dictionary["id"] = ids[i]
	x=random.randint(1,10)
	if x <= 7:
		dictionary["partition"] = "train"
		print(titles[i])
		im = cv2.imread("./allphotos/" + titles[i] + ".jpg")
		cv2.imwrite("./images/train/" + titles[i] + ".jpg", im)
	elif x==8 or x==9:
		dictionary["partition"] = "test"
		print(titles[i])
		im = cv2.imread("./allphotos/" + titles[i] + ".jpg")
		cv2.imwrite("./images/test/" + titles[i] + ".jpg", im)
	else:
		dictionary["partition"] = "val"
		print(titles[i])
		im = cv2.imread("./allphotos/" + titles[i] + ".jpg")
		cv2.imwrite("./images/val/" + titles[i] + ".jpg", im)
	finallist.append(dictionary)
print (finallist)

with open("layer1.json", "w") as f:
	json.dump(finallist, f)
