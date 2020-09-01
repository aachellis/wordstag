import nltk
import numpy as np 
import operator
import re
from textblob import TextBlob
from collections import Counter
import modules.creating_ngrams as cn
import modules.word_context as wc
ngram_categorization_model = cn.get_ngrams_occurance()
word_context_profile = wc.get_word_context_profile()

def ngram_frequency(word):
	"""Creating a ngram frequecy profile of a specific word consists of 300 entries"""
	word = word.lower()
	word = re.sub(r'[^A-Za-z. ]','',word)
	ngram_statistics = {}
	ngram_categorization_model_keys = []
	ngram_categorization_model_occurances = []
	res = [0 for _ in range(0,300)]
	for ituple in ngram_categorization_model:
		ngram_categorization_model_keys.append(ituple[0])
		ngram_categorization_model_occurances.append(int(ituple[1]))
	for grams in range(2,6):
		for i in range(len(word)-grams+1):
			seq = word[i:i+grams]
			if seq not in ngram_statistics.keys():
				ngram_statistics.update({seq:1})
			else:
				ngram_occurances = ngram_statistics[seq]
				ngram_statistics.update({seq:ngram_occurances+1})
	ngram_frequency_keys = ngram_statistics.keys()
	ngram_frequency_occurances = list(ngram_statistics.values())
	for index, val in enumerate(ngram_categorization_model_keys):
		for index1, val1 in enumerate(ngram_frequency_keys):
			if val == val1:
				res[index] = ngram_categorization_model_occurances[index]*ngram_frequency_occurances[index1]
	return res

def is_english(word):
	"""Look up in the English Dictionary to know if that word exist in it"""
	with open("ENG_DICT.txt", "r", encoding = "utf-8") as f:
		wordlist = [line.split("\n")[0] for line in f]
	if word in wordlist:
		return 1
	return 0

def is_hindi(word):
	"""Look up in the Hindi Dictionary to know if that word exist in it"""
	wordlist = []
	with open("HINDI_DICT.txt", "r", encoding = "utf-8") as f:
		for line in f:
			line = re.sub(r'[^A-Za-z.;]','',line)
			line = line.lower()
			list1 = line.split(";")
			for element in list1:
				if element != '':
					wordlist.append(element)
	if word in list(wordlist):
		return 1
	return 0

def is_abbr(word):
	"""Look up in the Abbreviation Dictionary to know if that word is an abbreviation"""
	with open("ABBR_DICT.txt", "r", encoding = "utf-8") as f:
		wordlist = [line.split("\n")[0] for line in f]
	if word.upper() in wordlist:
		return 1
	return 0

def med(correct_word, word):
	"""Calculating the Minimum Edit Distance so that we know how much spelling mistake has been done while writing the word (Helpful if the word doesn't exist in the dictonary"""
	t = np.zeros((len(correct_word), len(word)))
	for i in range(len(word)):
		t[0][i] = i
	for i in range(len(correct_word)):
		t[i][0] = i
	for i in range(1, len(correct_word)):
		for j in range(1, len(word)):
			if correct_word[i-1] == word[j-1]:
				t[i][j] = t[i-1][j-1]
			else:
				t[i][j] = min(t[i-1][j-1],t[i][j-1],t[i-1][j])+1
	return t[len(correct_word)-1,len(word)-1]

def med_in_english(word):
	"""Minimum edit distance if that word was to be a English Word"""
	return int(med(TextBlob(word).correct(), word))

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('HINDI_DICT.txt', encoding = "utf-8").read()))

def P(word, N=sum(WORDS.values())): 
    """Probability of `word`."""
    return WORDS[word] / N

def correction(word): 
    """Most probable spelling correction for word."""
    return max(candidates(word), key=P)

def candidates(word): 
    """Generate possible spelling corrections for word."""
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    """The subset of `words` that appear in the dictionary of WORDS."""
    return set(w for w in words if w in WORDS)

def edits1(word):
    """All edits that are one edit away from `word`."""
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    """All edits that are two edits away from `word`."""
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def med_in_hindi(word):
	"""Minimum edit distance if that word was to be a Hindi Word"""
	return int(med(correction(word),word))

def get_word_context(word):
	"""Get word context profile for that word"""
	for content, profile in word_context_profile:
		if word == content:
			return profile 
	return 0

def creating_feature_vector():
	"""To arrange and getting a resulting Feature Vector of the Corpus"""
	wordlist = []
	label = ""
	fw = open("feature_vector.txt", "w+", encoding = "utf-8")
	with open("D:\\Python_Prac\\wordstag\\modules\\HI_EN_TRAIN.txt", "r", encoding = "utf-8") as f:
		for line in f:
			wordlist.append(line)
		for index, line in enumerate(wordlist):
			if line == "\n":
				continue
			context = line.split("\t")
			label = context[1]
			feature_vector = label+" "
			ngram_vector = ngram_frequency(str(context[0]))
			for vector in ngram_vector:
				feature_vector += str(vector)+" "
			feature_vector += str(is_english(context[0]))+" "
			feature_vector += str(is_hindi(context[0]))+" "
			feature_vector += str(is_abbr(context[0]))+" "
			feature_vector += str(med_in_english(context[0]))+" "
			feature_vector += str(med_in_hindi(context[0]))+" "
			before = [0,0,0]
			after = [0,0,0]
			for i in range(3):
				if (index-i) < 0 or (index-i+1) > len(wordlist)-1:
					continue
				before[2-i] = get_word_context(wordlist[index-i+1].split("\t")[0])
			for i in range(3):
				if (index+i+1) > len(wordlist)-1:
					continue
				after[2-i] = get_word_context(wordlist[index+i+1].split("\t")[0])
			for i in before:
				feature_vector += str(i)+" "
			for i in after:
				feature_vector += str(i)+" "
			feature_vector += "\n"
			fw.write(feature_vector)
			print("Proceeding..."+str(index+1)+" of 16683")

	fw.close()

if __name__ == '__main__':
	creating_feature_vector()
