from skimage.measure import compare_ssim as ssim
import cv2
import os
import pickle
import imageio
#path change kar lena
# the folder should contain images of one video
file = open('fiveSeconds.pickle','rb')
d5 = pickle.load(file)
file.close()
file = open('twoSeconds.pickle','rb')
d2 = pickle.load(file)
file.close()
print("files loaded")
print(d5.keys())
dict5 = {}
for k in d5.keys():
    #name = 'turkey-brine'
    #dish = '/mntDrive/My Drive/MCA_P/newvideos/'+name+'.mp4'
    dish = k
    pics = []
    p2 = d2[dish]
    p5 = d5[dish]
    for i in range(len(p2)):
        pics.append([p2[i],i*2])
    for i in range(len(p5)):
        pics.append([p5[i],i*5])
    pics = sorted(pics,key = lambda k: k[1])
    print("extraction done")
    unique = {}
    #adjust this threshold
    threshold = 0.05
    for i in range(0,len(pics),5):
        for j in range(i+1,min(len(pics),i+20)):
            f1 = pics[i][0]
            f2 = pics[j][0]
            #print(f1,f2)
            #i1 = cv2.imread(f1,0)
            #i2 = cv2.imread(f2,0)
            i1 = cv2.resize(f1,(96,96))
            i2 = cv2.resize(f2,(96,96))
            val = ssim(i1,i2,multichannel=True)
            if i in unique.keys() and val > threshold:
                #print(i,j)
                unique[i].append(j)
            elif val > threshold:
                #print(i,j)
                unique[i] = [j]
    unique_images = []
    #os.rmdir('herb-roasted-pork')
    for i in unique.keys():
        unique_images.append(pics[i][0])
        #cv2.imwrite(path+str(i)+'.png',pics[i][0])
    dict5[k] = unique_images
    print(k)
file = open('d7.pkl','wb')
pickle.dump(dict5,file)
file.close()
            
            
