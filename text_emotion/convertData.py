def readFile():
	sent = open("text_emotion.csv","rb").readlines()
	sent = sent[1:len(sent)]
	return sent

if __name__ == "__main__":

	angerfile = open("ANGER_Phrases.txt","a")
	fearfile = open("FEAR_Phrases.txt","a")
	joyfile = open("JOY_Phrases.txt","a")
	sadnessfile = open("SADNESS_Phrases.txt","a")
	surprisefile = open("SURPRISE_Phrases.txt","a")
	sent = readFile()
	
	for ii in range(len(sent)):
		splitted = sent[ii].replace("\"","").split(",")
		print "data:",splitted
		emotion = splitted[1]
		text = splitted[3]
		if emotion == "hate": # anger
			angerfile.write(text)
		if emotion == "worry":
			fearfile.write(text)
		if emotion == "happiness" or emotion == "enthusiasm":
			joyfile.write(text)
		if emotion == "sadness":
			sadnessfile.write(text)
		if emotion == "surprise":
			surprisefile.write(text)
	angerfile.close()
	fearfile.close()
	joyfile.close()
	sadnessfile.close()
	surprisefile.close()
		
