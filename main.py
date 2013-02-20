"""
Core simulation code
"""
from cts import *
import time


# Set fixed parameters
staticParams = {'users':318415,'items':3262724,'vocabSize':747275}
userAnnoDist = [int(i.strip().split('\t')[1]) for i in open('/home/jared/Dropbox/Research/PROJECTS/Tagging/crawlerAnalysisV2/data/generalData/annotationsPerUser').read().strip().split('\n')]
itemAnnoDist = [int(i.strip().split('\t')[1]) for i in open('/home/jared/Dropbox/Research/PROJECTS/Tagging/crawlerAnalysisV2/data/generalData/annotationsPerItem').read().strip().split('\n')]
    
for ex in (1.5,2,2.5,3):#(500,1000,5000,10000):
    print ex
    ctsObject = CTS(nUsers=staticParams['users'],nItems=staticParams['items'],vocabSize=staticParams['vocabSize'],pTop=0.95,pCopy=0.6,record=True,ex=ex)
    itemsToTag = []
    for iid,count in enumerate(itemAnnoDist):
        itemsToTag += count*[iid]
    usersToTag = []
    for uid,count in enumerate(userAnnoDist):
        usersToTag += count*[uid]
    random.shuffle(itemsToTag)
    random.shuffle(usersToTag)
    for user,item in zip(usersToTag,itemsToTag):
        ctsObject.tagItem(user,item)
    ctsObject.cleanup()
#    out=open('tagViewCounts.pCopy0.5.pTop0.95','w')
#    for i in xrange(ctsObject.nUsers):
#        out.write(str(i)+'\t'+str(userAnnoDist[i])+'\t'+str(len(ctsObject.users[i]))+'\n')
    
    


