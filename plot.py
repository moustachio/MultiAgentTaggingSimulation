"""
Generates frequency distribution plots for all the measures from the 'basicStats' script
"""
import matplotlib
matplotlib.use('Agg') # use plotting backend
from matplotlib import pyplot
import os
import numpy
import operator

rawDataDir = '/home/jared/Dropbox/Research/PROJECTS/Tagging/SIM/V3/rawData'
#rawDataDir = '/Users/AxelStreichen/Dropbox/Research/PROJECTS/Tagging/SIM/V3/rawData'
unique = set([fi.strip().split('_')[1] for fi in os.listdir('data') if fi[0]!='.'])

# Load parameter values from disk, and store in dictionary
paramKey = {}
for date in unique:
    paramKey[date]= {}
    f = open(rawDataDir+'/'+date+'.params')
    for line in f:
        line = line.strip().split('\t')
        paramKey[date][line[0]]=line[1]
    f.close()




names = {'bin':'Uniform heuristic','top5':'Top-five heuristic','norm':'Normalized heuristic','top5normed':'Normalized Top5 Heuristic'}
#col = {0.1:(1,0,0),0.2:(0,1,0),0.3:(0,0,0.1724),0.4:(1,0.1034,0.7241),0.5:(1,0.8276,0),0.6:(0,0.3448,0),0.7:(0.5172,0.5172,1),0.8:(0.6207,0.3103,0.2759),0.9:(0,1,0.7586),0.95:'black',1.0:(1,1,0)}
#col={'1':(1,0,0),'5':(0,1,0),'10':(0,0,0.1724),'20':(1,0.1034,0.7241)}
truDist = [int(line.strip().split('\t')[1]) for line in open('/home/jared//Dropbox/Research/PROJECTS/Tagging/crawlerAnalysisV2/data/generalData/annotationsPerTag')]
#truDist = [int(line.strip().split('\t')[1]) for line in open('/Users/AxelStreichen/Dropbox/Research/PROJECTS/Tagging/crawlerAnalysisV2/data/generalData/annotationsPerTag')]
allPcopy = [float(paramKey[i]['pCopy']) for i in paramKey]
#allMem = [paramKey[i]['memory'] for i in paramKey]
allEx = [paramKey[i]['ex'] for i in paramKey]
fig = pyplot.figure()
for ex in allEx:
    ax = pyplot.subplot(1,1,1)
    for t in paramKey:
        if paramKey[t]['ex'] == ex:
            print ex
            x = []
            fi = open('data/annotationsPerTag'+'_'+t)
            for line in fi:
                x.append(float(line.strip().split('\t')[1]))
            fi.close()
            print len(x)
            ax.plot(x,label=ex)
ax.plot(truDist,c='blue',lw=2)

pyplot.yscale('log')
pyplot.xscale('log')
pyplot.xlim(0,10**7)
pyplot.ylim(0,10**6)
pyplot.ylabel('count')
pyplot.xlabel('rank')
pyplot.title('P=0.6, pTop=0.95')
handles, labels = ax.get_legend_handles_labels()
hl = sorted(zip(handles,map(float,labels)),key=operator.itemgetter(1),reverse=True)
handles2,labels2 = zip(*hl)
pyplot.legend(handles2,['exp='+str(float(i)) for i in labels2],loc='best')
fig.savefig('pCopy0.6_pTop0.95_varyEx.pdf')
