from gensim.models import Doc2Vec
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
import numpy
from  sklearn.model_selection import train_test_split
# classifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
# random
import random
from sklearn import svm
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

class LabeledLineSentence(object):
    def __init__(self, sources):
        self.sources = sources
        
        flipped = {}
        
        # make sure that keys are unique
        for key, value in sources.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                raise Exception('Non-unique prefix encountered')
    
    def __iter__(self):
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    yield LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])
    
    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    self.sentences.append(LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
        return self.sentences
    
    def sentences_perm(self):
        shuffled = list(self.sentences)
        random.shuffle(shuffled)
        return shuffled

if __name__ == "__main__":
	sources = {"stemmed_JOY_Phrases.txt":"Joy" , "stemmed_ANGER_Phrases.txt":"Anger" , "stemmed_SURPRISE_Phrases.txt" : "Surprise", "stemmed_FEAR_Phrases.txt" :"Fear" , "stemmed_SADNESS_Phrases.txt" : "Sadness" }
	#sentences = LabeledLineSentence(sources)
	#model = Doc2Vec(min_count=1, window=10, size=100, sample=1e-4, negative=5, workers=7)
	#model.build_vocab(sentences.to_array())
	# for epoch in range(10):
		# model.train(sentences.sentences_perm(), total_examples = model.corpus_count, epochs = model.iter)
	#model.save("TrainedModel.pkl")
	model = Doc2Vec.load("TrainedModel.pkl")
	print model.most_similar('anger')
	#print model.docvecs.doctags
	print model.docvecs["Joy_87"]
	print model.corpus_count
	total = model.corpus_count
	train_arrays = numpy.zeros((total, 100))
	train_labels = numpy.zeros(total)
	dict = {"Anger" :858,	"Fear" : 865, "Joy":845 ,"Sadness" : 805, "Surprise":912 } 
	k =0
	l = 0
	for i,m in dict.items():
		for j in range(m):
			train_arrays[l] = model.docvecs[i+"_" + str(j)]
			train_labels[l] = k
			l+=1
		k+=1
	print set(train_labels)
	print train_arrays
	X = train_arrays
	Y = train_labels
	X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
	#classifier = LinearSVC( random_state = 0)
	#classifier = LogisticRegression()
	#classifier = svm.SVC(kernel = "rbf")
	classifier = LinearDiscriminantAnalysis()
	classifier.fit(X_train, y_train)
	print classifier.score(X_test, y_test)