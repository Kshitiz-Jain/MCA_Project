import pickle
file = open('ingr.pkl','rb')
ingr = pickle.load(file)
print(ingr)
file.close()
