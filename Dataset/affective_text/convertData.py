def readFile():
	emot = open("affectivetext_test.emotions.gold","rb").readlines()
	sent = open("affectivetext_test.xml","rb").readlines()
	sent = sent[1:len(sent)-1]
	return sent,emot

if __name__ == "__main__":

	angerfile = open("ANGER_Phrases.txt","a")
	fearfile = open("FEAR_Phrases.txt","a")
	joyfile = open("JOY_Phrases.txt","a")
	sadnessfile = open("SADNESS_Phrases.txt","a")
	surprisefile = open("SURPRISE_Phrases.txt","a")
	sent,emot = readFile()
	for ii in range(len(emot)):
		# extracting sentences from xml
		startindex = sent[ii].index(">") + 1
		endindex = sent[ii].index("/") - 1
		sent[ii] = sent[ii][startindex:endindex] +"\n"
		splitted = emot[ii].split()
		sid = splitted[0]
		anger,fear,joy,sadness,surprise = splitted[1],splitted[3],splitted[4],splitted[5],splitted[6]
		values = [anger,fear,joy,sadness,surprise]
		emotions = ["anger","fear","joy","sadness","surprise"]
		maxval = max(values)
		index = values.index(maxval)
		if index == 0: # anger
			angerfile.write(sent[ii])
		if index == 1:
			fearfile.write(sent[ii])
		if index == 2:
			joyfile.write(sent[ii])
		if index == 3:
			sadnessfile.write(sent[ii])
		if index == 4:
			surprisefile.write(sent[ii])
	angerfile.close()
	fearfile.close()
	joyfile.close()
	sadnessfile.close()
	surprisefile.close()
		
