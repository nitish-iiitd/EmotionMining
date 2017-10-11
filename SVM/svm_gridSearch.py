import pickle
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
import random
import matplotlib.pyplot as plt

def loadXY():
    zippedXY = pickle.load(open("../Vectorizer/zippedXY_wff_10k.p", "rb"))
    random.shuffle(zippedXY)
    X,Y = zip(*zippedXY)
    return X,Y

if __name__ == "__main__":

    X, Y = loadXY()
    print "X and Y loaded"
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.80, random_state=0)
    X, X_test, Y, Y_test = train_test_split(X, Y, test_size=0.2, train_size=0.8)
    X_train, X_cv, Y_train, Y_cv = train_test_split(X, Y, test_size=0.25, train_size=0.75)
    print Y

    # Tuning of parameters using validation dataset

    penalty = ['l1', 'l2']
    C = [0.5, 1.0, 20]
    loss = ['hinge', 'squared_hinge']
    res = ['', 0, 0, 0]
    xaxis = []
    xticks = []
    yaxis = []
    for a in penalty:
        for c in C:
            for l in loss:
                try:
                    svm_model = LinearSVC(random_state=0, penalty=a, loss=l, C=c)
                    svm_model.fit(X_train, Y_train)
                    predictedY = svm_model.predict(X_cv)
                    # for tt in range(len(Y_test)):
                    # print "Actual:",Y_test[tt],"  Predicted:",predictedY[tt]
                    accuracy_val = svm_model.score(X_cv, Y_cv)
                    print "penalty, c, loss:", a, c, l, "  accuracy:", accuracy_val
                    par = []
                    par.append(a)
                    par.append(c)
                    par.append(l)
                    xaxis.append(len(xticks))
                    xticks.append(str(par))
                    yaxis.append(accuracy_val)

                    if (res[3] <= accuracy_val):
                        res[0] = a
                        res[1] = c
                        res[2] = l
                        res[3] = accuracy_val

                except ValueError:
                     print "value error comes"

    # creating and saving the plot
    plt.xticks(xaxis, xticks, rotation=90)
    plt.plot(xaxis, yaxis)
    plt.tight_layout()
    plt.show()
    # plt.savefig("plot2b_svm.png")


    # Test data
    svc_model = LinearSVC(random_state=0, penalty=res[0], loss=res[2], C=res[1])
    svc_model.fit(X_train, Y_train)
    predictedY = svc_model.predict(X_test)
    accuracy_test = svc_model.score(X_test, Y_test)
    print "accuracy after test data:", accuracy_test
    # svm_model = LinearSVC(random_state=0)
    # svm_model.fit(X_train,Y_train)
    # predictedY = svm_model.predict(X_test)
    # for tt in range(len(Y_test)):
    #     print "Actual:",Y_test[tt],"  Predicted:",predictedY[tt]
    # accuracy = svm_model.score(X_test,Y_test)
    # print accuracy
