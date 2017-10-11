from gensim.models import Doc2Vec
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
import numpy
from  sklearn.model_selection import train_test_split
# classifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
# random
import matplotlib.pyplot as plt
import random
import pickle
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

def countNumberOfLines (filename) :
	file  = open (filename , "r")
	data = file.readlines ()
	print len (data)
	return len (data)
	
if __name__ == "__main__":
	# sources = {"stemmed_JOY_Phrases.txt":"Joy" , "stemmed_ANGER_Phrases.txt":"Anger" , "stemmed_SURPRISE_Phrases.txt" : "Surprise", "stemmed_FEAR_Phrases.txt" :"Fear" , "stemmed_SADNESS_Phrases.txt" : "Sadness" }
	sources = {"Anger_10k.txt": "Anger" , "Fear_10k.txt":"Fear" , "Joy_10k.txt": "Joy" , "Sadness_10k.txt" : "Sadness" , "Surprise_10k.txt" : "Surprise" }
	sentences = LabeledLineSentence(sources)
	
	count = [1,5,10]
	sizes = [100, 500, 1000]
	grid = []
	grid.append(count)
	grid.append(sizes)
	bestc = 0.0
	bestacc = 0.0
	bests = 0.0
	accuracies = []
	parameters =[]
	for p in range(3):
		for q in range(3):
			print grid[0][p]
			model = Doc2Vec(min_count=int (grid[0][p]), window=10, size=int(grid[1][q]), sample=1e-4, negative=5, workers=7)
			#print model
			model.build_vocab(sentences.to_array())
			for epoch in range(10):
				model.train(sentences.sentences_perm(), total_examples = model.corpus_count, epochs = model.iter)
			total = model.corpus_count
			train_arrays = numpy.zeros((total, grid[1][q]))
			train_labels = numpy.zeros(total)
			dict = {"Anger":8000 , "Fear":8000 , "Joy":8000 , "Sadness":8000 , "Surprise":8000 }
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
			X_train = X[:6000]
			X_test = X[6000:8000]
			y_train = Y[:6000]
			y_test = Y[6000:8000]
			classifier = LinearDiscriminantAnalysis()
			classifier.fit(X_train, y_train)
			print classifier
			acc = classifier.score(X_test, y_test)
			print acc
			accuracies.append(acc)
			parameters.append (str(grid[0][p])+"," + str(grid[1][q]) )
			if bestacc < acc :
				model.save("BestLDA.pkl")
				bestc = grid[0][p]
				bests = grid[1][q]
				bestacc = acc
				
				
	print bestc, bests
	D ={}
	for i in range (9):
		D[parameters[i]] = int (acc[i])
	plt.plot(range(len(D)), D.values())#, align='center'
	plt.xticks(range(len(D)), D.keys())
	plt.ylabel("Accuracies")
	plt.xlabel("mincount, size")
	plt.title("LDA Grid Search for Doc2Vec")
	plt.savefig("LDA_gridSearch.png")
	plt.show()
	#model = Doc2Vec.load("TrainedModel_10k_1_1000.pkl")
	#print model.most_similar('anger')
	#print model.docvecs.doctags
	#print model.docvecs["Joy_87"]
	#print model.corpus_count
	
	
	# dict = {"Anger" : countNumberOfLines("stemmed_ANGER_Phrases.txt") ,	"Fear" : countNumberOfLines ("stemmed_FEAR_Phrases.txt"),"Joy": countNumberOfLines("stemmed_JOY_Phrases.txt") , "Sadness" : countNumberOfLines ("stemmed_SADNESS_Phrases.txt"), "Surprise":countNumberOfLines("stemmed_SURPRISe_Phrases.txt") } 
	
	# file = open("train_arrays.pkl", "wb")
	# pickle.dump(X,file)
	# file.close()
	# X = pickle.load("train_arrays.pkl","rb")
	# file = open("train_labels.pkl", "wb")
	# pickle.dump(Y,file)
	# file.close()
	# Y = pickle.load("train_labels.pkl","rb")
	#X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
	#classifier = LinearSVC( random_state = 4)
	#classifier = LogisticRegression()
	#classifier = svm.SVC(kernel = "linear")
	#classifier = svm.SVC(kernel="linear")
	#classifier = LinearDiscriminantAnalysis()
	#classifier.fit(X_train, y_train)
	#print classifier, classifier.score(X_test, y_test)