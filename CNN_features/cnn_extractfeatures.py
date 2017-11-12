import pickle
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import random
from matplotlib import pyplot as plt
import numpy as np

def loadXY():
	zippedXY = pickle.load(open("../Vectorizer/zippedXY_wff_1k.p","rb"))
	random.shuffle(zippedXY)
	X,Y = zip(*zippedXY)
	return X,Y

if __name__ == "__main__":

	X,Y = loadXY()
	print "X and Y loaded"
	
	print np.array(X).shape
	cnn_X = []
	gap = 8
	sentence = 0
	for xx in X:
		print "Current Sentence : ",sentence
		newfeature = []
		newf = 408
		startindex = 0
		for f in range(newf):
			endindex = startindex + gap
			#print "StartIndex :",startindex,"  Endindex:",endindex
			curr_window = xx[startindex:endindex].count(1)
			newfeature.append(curr_window)
			startindex = startindex + gap/2
		cnn_X.append(newfeature)
		sentence += 1
	zippedXY = zip(cnn_X,Y)
	pickle.dump(zippedXY,open("zippedXY_cnn_wff_1k.p","wb"))
		#print "New Feature = ",newfeature
		#break
	