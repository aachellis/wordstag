import nltk
import numpy as np 
import operator
import re
def get_ngrams_occurance():
	res = []
	wordlist = []
	with open("D:\\Python_Prac\\wordstag\\modules\\HI_EN_TRAIN.txt", "r", encoding = "utf-8") as f:
		for line in f:
			line = line.lower()
			line = line.split("\t")[0]
			line = re.sub(r'[^A-Za-z. ]','',line)
			wordlist.append(line)
	ngram_statistics = {}
	for word in wordlist:
		for grams in range(2,6):
			for i in range(len(word)-grams+1):
				seq = word[i:i+grams]
				if seq not in ngram_statistics.keys():
					ngram_statistics.update({seq:1})
				else:
					ngram_occurances = ngram_statistics[seq]
					ngram_statistics.update({seq:ngram_occurances+1})
	ngram_statistics_sorted = sorted(
			ngram_statistics.items(),
			key = operator.itemgetter(1),
			reverse = True
		)[0:300]
	return ngram_statistics_sorted
