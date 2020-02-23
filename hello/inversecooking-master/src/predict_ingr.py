import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import numpy as np
import os
from build_vocab import Vocabulary
from args import get_parser
import pickle
from model import get_model
from torchvision import transforms
from utils.output_utils import prepare_output
from PIL import Image
import time

data_dir = '../data'

ingrs_vocab = pickle.load(open(os.path.join(data_dir,'recipe1m_vocab_ingrs.pkl'),'rb'))
ingrs_vocab = [min(w,key=len) if not isinstance(w,str) else w for w in ingrs_vocab.idx2word.values()]
vocab = pickle.load(open(os.path.join(data_dir, 'recipe1m_vocab_toks.pkl'),'rb')).idx2word
pickle.dump(ingrs_vocab, open('../data/ingr_vocab.pkl','wb'))
pickle.dump(vocab, open('../data/instr_vocab.pkl','wb'))
ingrs_vocab = pickle.load(open(os.path.join(data_dir, 'ingr_vocab.pkl'),'rb'))
vocab = pickle.load(open(os.path.join(data_dir, 'instr_vocab.pkl'),'rb'))
ingr_vocab_size = len(ingrs_vocab)
instrs_vocab_size = len(vocab)
output_dim = instrs_vocab_size
print(ingr_vocab_size)
print(instrs_vocab_size)
kk = 'cuda'
device = torch.device(kk)
t= time.time()
import sys
sys.argv = ['']
del sys
args = get_parser()
args.maxseqlen = 15
args.ingr_only = False
model = get_model(args,ingr_vocab_size,instrs_vocab_size)
model.load_state_dict(torch.load('../checkpoints/inversecooking/im2ingr/checkpoints/modelbest.ckpt', map_location = None))
model.to(device)
model.eval()
model.ingrs_only = False
model.recipe_only = False

transf_list_batch = []
transf_list_batch.append(transforms.ToTensor())
transf_list_batch.append(transforms.Normalize((0.485, 0.456, 0.406),(0.229, 0.224, 0.225)))
to_input_transf = transforms.Compose(transf_list_batch)


greedy = [True, False, False, False]
beam = [-1, -1, -1, -1]
temperature = 1.0
numgens = len(greedy)

import requests
from io import BytesIO
import random
from collections import Counter


image_folder = os.path.join(data_dir, 'test')
demo_imgs = os.listdir(image_folder)
random.shuffle(demo_imgs)
#demo_urls = ['https://food.fnr.sndimg.com/content/dam/images/food/fullset/2013/12/9/0/FNK_Cheesecake_s4x3.jpg.rend.hgtvcom.826.620.suffix/1387411272847.jpeg'
demo_files =demo_imgs
for img_file in demo_files:
	image_path = os.path.join(image_folder, img_file)
	image = Image.open(image_path).convert('RGB')
	transf_list = []
	transf_list.append(transforms.Resize(256))
	transf_list.append(transforms.CenterCrop(224))
	transform = transforms.Compose(transf_list)
	image_transf = transform(image)
	image_tensor = to_input_transf(image_transf).unsqueeze(0).to(device)
	num_valid = 1
	numgens = 1
	for i in range(numgens):
		with torch.no_grad():
			outputs = model.sample(image_tensor, greedy=greedy[i],temperature=temperature, beam=beam[i], true_ingrs=None)
		ingr_ids = outputs['ingr_ids'].cpu().numpy()
		recipe_ids = outputs['recipe_ids'].cpu().numpy()
		outs, valid = prepare_output(recipe_ids[0], ingr_ids[0], ingrs_vocab, vocab)
		if True or valid['is_valid']:
			print ('RECIPE', num_valid)
			print("Image name",img_file)
			num_valid+=1
			BOLD = '\033[1m'
			END = '\033[0m'
			#print (BOLD + '\nTitle:' + END,outs['title'])
			print (BOLD + '\nIngredients:'+ END)
			print (', '.join(outs['ingrs']))
		print("Hello")
