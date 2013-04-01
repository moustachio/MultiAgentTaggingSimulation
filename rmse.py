import math

def rmse(x,y):
	lenX = len(x)
	lenY = len(y)
	dif = lenX - lenY
	n=float(lenX)
	if dif<0:
		x+=[0]*dif
		n=float(lenY)
	elif dif>0:
		y+=[0]*dif
	se = 0
	for i,j in zip(x,y): 
		se += ((i-j)**2)
	rmse = math.sqrt(se/n)
	return rmse


empirical = [int(line.strip().split('\t')[1]) for line in open('C:/Users/jlorince/Dropbox/Research/PROJECTS/Tagging/OLD/crawlerAnalysisV2/data/generalData/annotationsPerTag')]
null = [44.34860660399451]*747275
improved = [int(line.strip().split('\t')[1]) for line in open('C:/Users/jlorince/Dropbox/Research/PROJECTS/Tagging/MultiAgentTaggingSimulation/data/annotationsPerTag_2013-03-26.122247').read().strip().split('\n')]
basic = [int(line.strip().split('\t')[1]) for line in open('C:/Users/jlorince/Dropbox/Research/PROJECTS/Tagging/MultiAgentTaggingSimulation/data/annotationsPerTag_2013-03-27.124725').read().strip().split('\n')]

nullVsEmp = rmse(null,empirical)
basicVsEmp = rmse(basic,empirical)
impVsEmp = rmse(improved,empirical)
print 'Null vs. empirical: '+str(nullVsEmp)
print '--------------------'
print 'Basic vs. empirical: '+str(basicVsEmp)
print '----> '+str(100*(1 - basicVsEmp/nullVsEmp))+' percent improvement over null model'
print '--------------------'
print 'Improved vs. empirical: '+str(impVsEmp)
print '----> '+str(100*(1 - impVsEmp/nullVsEmp))+' percent improvement over null model'
