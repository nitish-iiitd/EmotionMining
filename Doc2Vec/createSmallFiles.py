file = open ("stemmed_ANGER_Phrases.txt", "r" )
data = file.readlines()
file.close()
from sklearn.utils import shuffle
data = shuffle(data, random_state = 42)
file = open ("Anger_14k.txt" , "w")
for i in range (14000):
	file.write (data[i])
file.close()