import random
import datetime
import numpy
import weighted_choice
from collections import OrderedDict as od

"""
'C'ollabortive 'T'agging 'S'ystem class. Current version only uses the "top-five" heuristic
"""

class CTS(object):

	def __init__(self,nUsers,nItems,pCopy,pTop,vocabSize=747275,recs = 5,record=False, memory=100):
		# Starting user dictionary
		self.users = {u:od() for u in xrange(nUsers)}
		"""
		Original version without ordered dict:
		self.users = {u:{} for u in xrange(nUsers)}
		"""
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
						'memory\t'+str(memory)
						)
			params.close()
		# set all global attributes
		self.record = record # record data? yes or no
		self.recs = recs # number of top displayed recommended tags
		self.vocabSize = vocabSize # total number of possible tags
		self.nItems = nItems # total number of items to be tagged
		self.pCopy = pCopy # aka "P" ; probability of using the top-five heuristic
		self.pTop = pTop # aka "Q" ; probability of drawing tag from "memory" of tags, with Pr proporitonal to number of times seen
		self.memory = memory # Number of unique tags a user can remember
		
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
			tag = self.newtag(self.users[user])
		
		for t in self.items[item]['top']:
			self.users[user][t] = self.users[user].get(t,0)+1

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
	def newtag(self,dist):
		if dist:
			flip = random.random()
			if flip < self.pTop:
				return weighted_choice.weighted_choice(dist)
		# otherwise (or if you haven't seen any tags yet)
		return random.randint(1,self.vocabSize)
	
	# Close file when we're done.
	def cleanup(self):
		if self.record:
			self.anno.close()
			
