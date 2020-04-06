import pickle
import nltk
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
def window(instruction,subtitle_window):
    c = 0
    s = 0
    for i in instruction:
        if i.lower() in stop:
            s+=1
            continue
        for j in subtitle_window:
            if j.lower() in stop:
                continue
            if i in j.lower() or j in i.lower():
                #print(i.lower(),j.lower())
                c+=1
                break
    return c/(len(instruction)-s)
def match(recipe,sub):
    pairs = []
    p1 = 0
    p2 = 0
    while p1<len(recipe) and p2<len(sub):
        temp = recipe[p1].split()
        win = sub[p2:min(p2+len(temp)+2,len(sub))]
        if len(temp)==0 or len(win)==0:
            p1+=1
            p2+=1
            continue
        val = window(temp,win)
        #print(recipe[p1],win,val)
        if val>0.3:
            print(recipe[p1],win,val)
            pairs.append([recipe[p1],win])
            p1+=1
            p2+=1
        else:
            p2+=1
    return pairs
file = open('instr.pickle','rb')
instr = pickle.load(file)
file.close()
#print(instr[0])
file = open('instr_name.pickle','rb')
instr_name = pickle.load(file)
file.close()
inst_name = []
for i in instr_name:
    inst_name.append(i.split('/')[-1][:-4])
file = open('recipenamefile.txt','r')
dish_list = []
for i in file:
    dish_list.append(i[:-1])
file.close()
inst = []
file = open('recipefile.txt','r')
for i in file:
    inst.append(i[1:-2].split('.'))
#print(inst[1])
file.close()
d_sub = {}
for i in range(len(inst_name)):
    temp = instr[i]
    s = ""
    for j in temp:
        s = s+" "+j
    s = s.split()
    for j in s:
        if len(j)==0:
            s.remove(j)
    d_sub[inst_name[i]] = s
#print(d_sub)
d_recipe = {}
for i in range(len(dish_list)):
    d_recipe[dish_list[i]] = inst[i]
k = list(d_sub.keys())[0]
match(d_recipe[k],d_sub[k])
