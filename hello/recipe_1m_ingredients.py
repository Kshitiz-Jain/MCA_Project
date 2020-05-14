import pickle
file = open('allingrs_count.pkl','rb')
s = pickle.load(file)
file.close()
for i in s:
    print(i)
