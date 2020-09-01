import re
import operator
def get_word_context_profile():
	with open("D:\\Python_Prac\\wordstag\\modules\\HI_EN_TRAIN.txt", "r", encoding = "utf-8") as f:
		word_frequency = {}
		wordlist = []
		for line in f:
			line = line.lower()
			line = line.split("\t")[0]
			line = re.sub(r'[^A-Za-z]','',line)
			wordlist.append(line)
	
	for word in wordlist:
		if word not in word_frequency.keys():
			word_frequency.update({word:1})
		else:
			word_occurance = word_frequency[word]
			word_frequency.update({word:word_occurance+1})
	word_frequency_sorted = sorted(
			word_frequency.items(),
			key = operator.itemgetter(1),
			reverse = True
		)[1:501]
	return word_frequency_sorted
