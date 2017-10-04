import pickle
from sklearn.lda import LDA
from sklearn.model_selection import train_test_split
import random

def loadXY():
	zippedXY = pickle.load(open("../Vectorizer/zippedXY.p","rb"))
	random.shuffle(zippedXY)
	X,Y = zip(*zippedXY)
	return X,Y



if __name__ == "__main__":

	X,Y = loadXY()
	print "X and Y loaded"
	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.80, random_state=0)
	print Y
	lda_model = LDA()
	lda_model.fit(X_train,Y_train)
	predictedY = lda_model.predict(X_test)
	for tt in range(len(Y_test)):
		print "Actual:",Y_test[tt],"  Predicted:",predictedY[tt]
	accuracy = lda_model.score(X_test,Y_test)
	print accuracy
