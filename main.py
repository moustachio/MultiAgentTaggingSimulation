"""
Core simulation code
"""
from cts import *
import time


# Set fixed parameters
staticParams = {'users':318415,'items':3262724,'vocabSize':747275}
#userAnnoDist = [int(i.strip().split('\t')[1]) for i in open('D:/Dropbox/Research/PROJECTS/Tagging/OLD/crawlerAnalysisV2/data/generalData/annotationsPerUser').read().strip().split('\n')]
#itemAnnoDist = [int(i.strip().split('\t')[1]) for i in open('D:/Dropbox/Research/PROJECTS/Tagging/OLD/crawlerAnalysisV2/data/generalData/annotationsPerItem').read().strip().split('\n')]
userAnnoDist = [int(i.strip().split('\t')[1]) for i in open('C:/Users/jlorince/Dropbox/Research/PROJECTS/Tagging/OLD/crawlerAnalysisV2/data/generalData/annotationsPerUser').read().strip().split('\n')]
itemAnnoDist = [int(i.strip().split('\t')[1]) for i in open('C:/Users/jlorince/Dropbox/Research/PROJECTS/Tagging/OLD/crawlerAnalysisV2/data/generalData/annotationsPerItem').read().strip().split('\n')]
	

ctsObject = CTS(nUsers=staticParams['users'],nItems=staticParams['items'],vocabSize=staticParams['vocabSize'],pTop=0.0,pCopy=0.6,record=True)
itemsToTag = []
for iid,count in enumerate(itemAnnoDist):
	itemsToTag += count*[iid]
usersToTag = []
for uid,count in enumerate(userAnnoDist):
	usersToTag += count*[uid]
random.shuffle(itemsToTag)
random.shuffle(usersToTag)
count=0
start = time.time()
for user,item in zip(usersToTag,itemsToTag):
	if count%100000==0 and count>0:
		print count
		print (time.time()-start)/60
	ctsObject.tagItem(user,item)
	count += 1
ctsObject.cleanup()
