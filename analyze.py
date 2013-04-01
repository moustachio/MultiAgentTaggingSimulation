"""
Script to generate sorted frequency distributions for a few basic measures from the folksonomy.
"""
import os

# Helper functions
def prepData(fi):
	return open('rawData/'+fi), {}
def sortSaveData(filename,timestamp):
	sortedFreqs = sorted(data.iteritems(), key=lambda x:x[1],reverse=True) 
	print len(sortedFreqs)
	out = open('data/'+filename+'_'+timestamp,'w')
	for i in sortedFreqs:
		out.write(i[0]+'\t'+str(i[1])+'\n')
	out.close()
		
paramFiles = [fi for fi in os.listdir('rawData') if '.params' in fi]
annoFiles = [fi for fi in os.listdir('rawData') if '.anno' in fi]

for fi in annoFiles:
	print fi
	timestamp = fi[:fi.find('.anno')]
	if 'annotationsPerTag_'+timestamp in os.listdir('data'):
		continue
	
	# Total number of annotations for each tag
	f, data = prepData(fi)
	count = 0
	for line in f:
		if count%100000==0:
			if count>0:
				print count
		line = line.strip().split(',')
		tag = line[2]
		data[tag] = data.get(tag,0)+1
		count += 1
	f.close()
	sortSaveData('annotationsPerTag',timestamp)
