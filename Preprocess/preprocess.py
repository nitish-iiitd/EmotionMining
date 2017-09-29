from nltk.stem import *
from nltk.stem.porter import *
from nltk import word_tokenize
from nltk.corpus import stopwords

def extractN(filename,n=None):
	lines = open("../Dataset/we_feel_fine/Phrases/"+filename,"rb").readlines()
	if n==None :
		return lines
	return lines[:n]

def stemmingAndStopwords(sentences):
	stop_words = set(stopwords.words('english'))
	stemmed = []
	stemmer = PorterStemmer()
	for sent in sentences:
		stemmed_sent = [stemmer.stem(sent) for word in sent]
		word_tokens = word_tokenize(sent)
		filtered_sentence = [w for w in word_tokens if not w in stop_words]
		filtered_sentence = " ".join(filtered_sentence)
		stemmed.append(filtered_sentence)
	return stemmed

if __name__ == "__main__":
	files = ["ANGER_Phrases.txt","FEAR_Phrases.txt","JOY_Phrases.txt","SADNESS_Phrases.txt","SURPRISE_Phrases.txt"]
	for f in files:
		sentences = extractN(f,1000)
		stemmed_sentence = stemmingAndStopwords(sentences)
		of = open("stemmed_"+f,"a")
		#total_sentences = len(stemmed_sentence)
		for sent in stemmed_sentence:
			of.write(sent+"\n")
		of.close()
		#print "stemmedsentence:",stemmed_sentence
