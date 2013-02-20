"""
Script to generate sorted frequency distributions for a few basic measures from the folksonomy.
"""
import os

# Helper functions
def prepData(fi):
	return open('/home/jared/Dropbox/Research/PROJECTS/Tagging/SIM/V3/rawData/'+fi), {}
def sortSaveData(filename,timestamp):
	sortedFreqs = sorted(data.iteritems(), key=lambda x:x[1],reverse=True) 
	print len(sortedFreqs)
	out = open('data/'+filename+'_'+timestamp,'w')
	for i in sortedFreqs:
		out.write(i[0]+'\t'+str(i[1])+'\n')
	out.close()
		
paramFiles = [fi for fi in os.listdir('/home/jared/Dropbox/Research/PROJECTS/Tagging/SIM/V3/rawData') if '.params' in fi]
annoFiles = [fi for fi in os.listdir('/home/jared/Dropbox/Research/PROJECTS/Tagging/SIM/V3/rawData') if '.anno' in fi]

for fi in annoFiles:
    print fi
    timestamp = fi[:fi.find('.anno')]
    if 'annotationsPerTag_'+timestamp in os.listdir('data'):
	    continue
    if timestamp == '2013-02-06.121318':
        continue
    
    # Total number of annotations for each tag
    f, data = prepData(fi)
    for line in f:
        line = line.strip().split(',')
        tag = line[2]
        data[tag] = data.get(tag,0)+1
    f.close()
    sortSaveData('annotationsPerTag',timestamp)
