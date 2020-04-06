import pickle
import cv2
def show_image(image):
    cv2.imshow('',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
inst = []
file = open('recipefile.txt','r')
for i in file:
    inst.append(i[1:-2].split('.'))
#print(inst[1])
file.close()
file = open('recipenamefile.txt','r')
dish_list = []
for i in file:
    dish_list.append(i[:-1])
file.close()
#print(dish_list[0])
recipes = {}
for i in range(len(dish_list)):
    recipes[dish_list[i]] = inst[i]
file = open('d8.pkl','rb')
d5 = pickle.load(file)
file.close()
image_inst = []
for k in d5.keys():
    name = k.split('/')[-1][:-4]
    r = recipes[name]
    images = d5[k]
    core = images[1:-1]
    for j in range(min(len(r),len(core))):
        t = (r[j],core[j])
        image_inst.append(t)
        print(r[j])
        show_image(core[j])
file = open('image_inst_pairs.pkl','wb')
pickle.dump(image_inst,file)
file.close()
    
