import pickle
import re
def determine(ing_list):
	non_ = ['chicken','beef','fish','mutton','meat','turkey','ribs','spareribs','bacon','ham','lamb','eggs','bison','mussels','crabs','oysters','pork','loin','buffalo','rack','clams','crabmeat','bonelespork','salmon','quartchicken','quartturkey','boneleschuck','bone','catfish','filletcatfish','caviar','crab','prawn','prawns','salami','pepperoni','yolk','shrimp','shrimps']
	non_ = set(non_)
	for i in ing_list:
		if i in non_:
			return False
	return True
file = open('ingredientsnew.txt','r')
wfile = open('ingr_parsed.txt','w')
veg = 0
nonveg = 0
cur_veg = True
cur_ingr = []
for i in file:
	print(i,cur_ingr)
	i = re.sub(',',' ',i)
	wfile.write(i+'\n'+str(cur_ingr)+'\n')
	if '[' in i and len(cur_ingr)>0:
		index = i.index('[')
		vn = determine(cur_ingr)
		if vn:
			veg += 1
			#print(cur_ingr)
		else:
			nonveg += 1
		cur_ingr = i[index+1:].split()
	elif ']' in i:
		index = i.index(']')
		temp = i[:index].split()
		for j in temp:
			cur_ingr.append(j)
	else:
		#cur_ingr.append(i)
		temp = i.split()
		for j in temp:
			cur_ingr.append(j)

	#print(temp)
print(veg,nonveg)