import json
import re
import random
import glob
import pickle
urlfile = open("recipelinkfile.txt", "r").read()
ingredientsfile = open("ingredientsnew.txt", "r").read()

urls = urlfile.split("\n")[:-1]
ids = []
for element in urls:
	start = [i.start() for i in re.finditer("\/", element)]
	ids.append(str(element[start[3]+1:start[4]]))

ingr = []
start = [i.start() for i in re.finditer("\[", ingredientsfile)]
end = [i.start() for i in re.finditer("\]", ingredientsfile)]

for i in range(len(start)):
	#print(ingredientsfile[start[i]:end[i]].replace("\n",";").split("[")[1].split(";"))
	ingr.append(ingredientsfile[start[i]:end[i]].replace("\n",";").split("[")[1].split(";"))

file = open('ingr.pkl','wb')
pickle.dump(ingr,file)
file.close()

finalingr = []
valids = []
for i in range(len(ingr)):
	lis = []
	val = []
	for j in range(len(ingr[i])):
		dic = {}
		dic["text"] = ingr[i][j]
		lis.append(dic)
		val.append(True)
	finalingr.append(lis)
	valids.append(val)
print (finalingr)

finallist = []
for i in range(len(finalingr)):
	dictionary = {}
	dictionary["ingredients"] = finalingr[i]
	dictionary["valid"] = valids[i]
	dictionary["id"] = ids[i]
	finallist.append(dictionary)

with open("det_ingrs.json", "w") as f:
	json.dump(finallist, f)