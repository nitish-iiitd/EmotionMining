from nltk.stem import *
from nltk.stem.porter import *
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import nltk

def extractN(filename,n=None):
	lines = open("../Dataset/we_feel_fine/Phrases/"+filename,"rb").readlines()
	if n==None :
		return lines
	return lines[:n]

def stemmingAndStopwords(sentences):
	importantwords = {}
	importantwords["JJ"],importantwords["RB"],importantwords["VB"] = [],[],[]
	stop_words = set(stopwords.words('english'))
	stemmed = []
	stemmer = PorterStemmer()
	for sent in sentences:
		#print "before=",sent
		word_tokens = word_tokenize(sent)
		postags =  nltk.pos_tag(word_tokens)
		for pt in postags:
			#print pt[0]
			try:
				importantwords[str(pt[1])] += [str(pt[0])]
			except KeyError:
				pass
		stemmed_sent = [stemmer.stem(word) for word in word_tokens]
		filtered_sentence = [w for w in stemmed_sent if not w in stop_words]
		filtered_sentence = " ".join(filtered_sentence)
		stemmed.append(filtered_sentence)
	#print "importantwords=",importantwords
	return stemmed,importantwords

if __name__ == "__main__":
	
	files = ["ANGER_Phrases.txt","FEAR_Phrases.txt","JOY_Phrases.txt","SADNESS_Phrases.txt","SURPRISE_Phrases.txt"]
	for f in files:
		sentences = extractN(f, 100)
		processed = list()
		for line in sentences:
			for c in string.punctuation:
				line = line.replace(c, "")
				line.lower()
			processed.append(line)
		stemmed_sentence,importantwords = stemmingAndStopwords(processed)
		for key in importantwords.keys():
			list_exist = importantwords.get(key)
			list_duplicate_remove = list(set(list_exist))
			importantwords[key] = list_duplicate_remove
		print "importantwords=",importantwords
		
		print "without removing duplicates: ", len(stemmed_sentence)
		# Removing duplicates
		stemmed_unique = list(set(stemmed_sentence))
		print "after removing duplicates: ", stemmed_unique
		print("writing to file....  ", f)
		of = open("stemmed_"+f, "wb")
		for sent in stemmed_unique:
			of.write(sent+"\n")
		of.close()
		
		#print "stemmed set:", stemmed_unique
