import random
import datetime
import numpy
from collections import OrderedDict as od

"""
'C'ollabortive 'T'agging 'S'ystem class. Current version only uses the "top-five" heuristic
"""

class CTS(object):

    def __init__(self,nUsers,nItems,pCopy,pTop=0.0,vocabSize=747275, memory=0, ex=numpy.e, recs = 5,record=False):
        # Starting user dictionary
        # users maintain ordered dictionary of tags encountered
        self.users = {u:od() for u in xrange(nUsers)}
        # Starting item-annotation structure
        # stores all annotations in one structure, top tags in another
        self.items = {i:{'anno':{},'top':{}} for i in xrange(nItems)}
        # Generate CTS ID
        initTime = str(datetime.datetime.now())
        self.id = initTime[:initTime.find('.')].replace(' ','.').replace(':','')
        # Set up data files
        if record:
            # open annotations file
            self.anno = open('rawData/'+self.id+'.anno','w')
            # write all parameters of interest to file
            params = open('rawData/'+self.id+'.params','w')
            params.write('nUsers\t'+str(nUsers)+'\n' +
                        'nItems\t'+str(nItems)+'\n' +
                        'pCopy\t'+str(pCopy) + '\n' +
                        'nRecs\t'+str(recs) +'\n' +
                        'pTop\t'+str(pTop) + '\n' +
                        'memory\t'+str(memory) + '\n' +
                        'ex\t'+str(ex)
                        )
            params.close()
        # set all global attributes
        self.record = record # record data? yes or no
        self.recs = recs # number of top displayed recommended tags
        self.vocabSize = vocabSize # total number of possible tags
        self.nItems = nItems # total number of items to be tagged
        self.pCopy = pCopy # aka "P" ; probability of using the top-five heuristic
        self.pTop = pTop # aka "Q" ; probability of drawing tag from "memory" of tags, with Pr proporitonal to number of times seen
        self.userMemory = memory # number of unique tags users maintain in memory (if a user hasn't seen a tag in a long time, he "forgets" it)
        self.ex = ex # exponent for adjusting observed tag frequencies
        #self.mode = mode # simulation mode; we're only useing top5 for nows
        #self.topTags=topTags # number of well-known popular tags (DEPRECATED)
        
    # given a user, item, and timestep, generates annotation from that user for that item
    def tagItem(self,user,item): 
        
        # Copy or not?
        flip = random.random()
        if (flip < self.pCopy) and (self.items[item]['anno']): # copy = True
            copy = True
        else:
            copy = False

        # If we're copying, pick one of top-five tags at random, otherwise engage in novel tagging behavior
        if copy: 
            tag = random.choice(self.items[item]['top'].keys())
        else:
            tag = self.newtag(user,item)
        
        for t in self.items[item]['top']:
			self.users[user][t] = self.users[user].get(t,0)+1

		# NOT USING MEMORY FOR NOW
		# Add all tags we see among the recommendations to memory, using ordered dictionary to keep most recently seen tags at the end of the distribution.
        #for t in sorted(self.items[item]['top'],key=self.items[item]['top'].get): # sort by frequency so the more common tags take precedence
        #    # pop out count for current tag, add 1, and put at the end of memory
        #    count = self.users[user].pop(t,0)+1 
        #    self.users[user][t] = count
            
        # If this overloads out memory, throw out the oldest tags in memory, oldest first
        #overload = len(self.users[user]) - self.userMemory
        #if overload > 0:
        #    for t in self.users[user].keys()[:overload]:
        #        del self.users[user][t]     

        # update annotation count
        count = self.items[item]['anno'].get(tag,0)+1
        self.items[item]['anno'][tag] = count
        
        # this block updates the top 5 tags for the item
        if self.items[item]['top']:
            minTop = min(self.items[item]['top'].values())
        else:
            minTop = 0
        if count >= minTop:
            self.items[item]['top'][tag] = count                        
            if (count > minTop) and (len(self.items[item]['top'])>self.recs):
                for tag in [t for t in self.items[item]['top'] if self.items[item]['top'][t]==minTop]:
                    del self.items[item]['top'][tag]

        # write annotation record to file
        if self.record:
            self.anno.write(str(user)+','+str(item)+','+str(tag)+'\n')
            
    # novel tagging behavior
    def newtag(self,user,item):
        flip = random.random()
        # With probability pTop, pick tag that you've seen before with probability proportional to how many times you've seen it (while tagging)
        # NOW EXPONENTIALLY SCALED, TO MORE STRONGLY PREFER MOST SEEN TAGS
        if flip < self.pTop and self.users[user]:
            expFreq = [i**self.ex for i in self.users[user].values()]
            #total = float(sum(self.users[user].values()))  
            total = float(sum(expFreq))
            #return self.users[user].keys()[numpy.array([self.users[user][i]/total for i in self.users[user]]).cumsum().searchsorted(numpy.random.sample(1))[0]]
            return self.users[user].keys()[numpy.array([i/total for i in expFreq]).cumsum().searchsorted(numpy.random.sample(1))[0]]
        # otherwise (or if you haven't seen any tags yet)
        else:
            return random.randint(1,self.vocabSize)
    
    # Close file when we're done.
    def cleanup(self):
        if self.record:
            self.anno.close()
            
