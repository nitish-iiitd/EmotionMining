from nltk.stem import *
from nltk.stem.porter import *
from nltk import word_tokenize
from nltk.corpus import stopwords
import string

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
        sentences = extractN(f, 1000)
        processed = list()
        for line in sentences:
            # print(line)
            for c in string.punctuation:
                line = line.replace(c, "")
                line.lower()
            processed.append(line)
            # print(line)
        stemmed_sentence = stemmingAndStopwords(processed)
        print "without removing duplicates: ", len(stemmed_sentence)
        # Removing duplicates
        stemmed_unique = list(set(stemmed_sentence))
        print "after removing duplicates: ", len(stemmed_unique)
        print("writing to file....  ", f)
        of = open("stemmed_"+f, "a")
        for sent in stemmed_unique:
            of.write(sent+"\n")
        of.close()
        print "stemmed set:", stemmed_unique
