import pickle
file = open('captions (1).pickle','rb')
captions = pickle.load(file)
file.close()
words_index = captions[3]
file = open('example_captions.txt','r')
file2 = open('example_captions_processed.txt','w')
words = set()
overlap = set()
for i in file:
    s = i.split()
    new_list = []
    for j in s:
        found = False
        if j in words_index.keys():
            new_list.append(j)
            continue
        for k in range(3,len(j)):
            word_part = j[:k]
            if word_part in words_index.keys():
                found = True
        if found:
            new_list.append(j)
    sent = ""
    for j in new_list:
        sent = sent+j+" "
    file2.write(sent+"\n")
file.close()
file2.close()
