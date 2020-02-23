import json
import re
import random
import glob
urlfile = open("recipelinkfile.txt", "r").read()
paths = (glob.glob("allphotos/*.jpg"))
paths.sort()
print(paths[:20])
print (len(paths))

urls = urlfile.split("\n")[:-1]
ids = {}
for element in urls:
	start = [i.start() for i in re.finditer("\/", element)]
	# print(str(element[start[4]+1:start[5]]))
	ids[str(element[start[4]+1:start[5]])] = str(element[start[3]+1:start[4]])

finallist = []
for i in range(len(paths)):
	dic = {}
	start = [j.start() for j in re.finditer("\/", paths[i])]
	dic["id"] = ids[paths[i][start[0]+1:-4]]
	dic1 = {}
	dic1["id"] = paths[i][10:]
	l = []
	l.append(dic1)
	dic["images"] = l
	finallist.append(dic)
# print (finallist)

with open("layer2.json", "w") as f:
	json.dump(finallist, f)
