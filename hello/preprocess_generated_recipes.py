import pickle
from nltk import word_tokenize
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

def read_file():
    data = []
    f = open("NLP-Assignment-5/data.txt","rb")
    data = f.read().decode()
    return data
def clean_text(text):
    temp = text.strip()
    temp = re.sub('[<>"*]','',temp)
    temp = re.sub('/',' ',temp)
    return temp
def rem_sp_char(word):
    temp = re.sub('[\!\@\#\$\%\^\&\*\(\)\{\}\:\[\]\<\>\?\|\,\_\;\=]','',word)
    temp = re.sub('--+','',temp)
    temp = re.sub('\.\.+','',temp)
    temp = re.sub('\-','',temp)
    if temp == '.' or temp == '-':
        return ''
    return temp
def preprocess(text):
    temp = clean_text(text)
    temp = word_tokenize(temp)
    stop_words = set(stopwords.words('english'))
    filter_temp = []
    for i in temp:
        if i not in stop_words:
            filter_temp.append(i)
    final_temp = []
    for i in filter_temp:
        word = i.lower()
        if len(word)!=0:
            final_temp.append(word)
    return final_temp
def get_words(text):
    sentences = text.split('\n')
    d = {}
    index = 0
    for j in sentences:
        s = parse_sentence(j)
        for i in s:
            if i not in d.keys():
                #print(i,' yes')
                d[i] = index
                index += 1
            else:
                #print(i,d[i])
                pass
    return d
def parse_sentence(text):
    l = preprocess(text)
    s = ""
    for i in l:
        r = rem_sp_char(i)
        if not(len(r) == 0 or (len(r)==1 and r[0] in '!@#$%^&*)(":;<>,.?/\|')):
            if r[0] == "'":
                s = s+r+" "
            elif r[-1] == '.':
                r = r[:len(r)-1]
                s = s+r+" "
            else:
                s = s+r+" "
    return s
file = open('captions.pickle','rb')
existing = pickle.load(file)
index_words = existing[2]
words_index = existing[3]
file.close()
file = open('recipes.pkl','rb')
generated = pickle.load(file)
file.close()
processed = {}
pt = 0
for i in generated.keys():
    recipe = generated[i]
    recipe = recipe.split('\n')
    temp = []
    for j in recipe:
        temp.append(parse_sentence(j))
    if pt<5:
        print(temp)
    pt+=1
    processed[i] = temp
file = open('processed_recipes.pkl','wb')
pickle.dump(processed,file)
file.close()
