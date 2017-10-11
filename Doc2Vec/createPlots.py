import matplotlib.pyplot as plt
def plot_graph (D, filename,e):
	plt.plot(range(len(D)), D.values())#, align='center'
	plt.xticks(range(len(D)), D.keys())
	plt.ylabel("Accuracies")
	plt.xlabel("mincount, size")
	plt.title(filename)
	plt.savefig(e+"_Accuracies.png")
	plt.show()
	
if __name__ == "__main__":
	D = {"1,100":0.58, "4,200":0.665, "1,1000":0.63 }
	plot_graph ( D, "SVM Doc2Vec Model on WeFeelFine Dataset 10k", "SVMWff")
	
#Logistic 0.61, 0.663, 0.6
#lda 	D = {"1,100":0.6, "4,200":0.668, "1,1000":0.8005 }
#SVM D = {"1,100":0.58, "4,200":0.665, "1,1000":0.63 }