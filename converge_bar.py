import os
from os import listdir
import re
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import sys


START1=400
END1=500
START2=1000
END2=1100


throughput_dict=dict()
data_points = dict()
convergence=dict()
time_dict=dict()
files = []
def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

def mean(data):
    a = np.array(data)
    return np.mean(a)

def stdev(data):
    a=np.array(data)
    return np.std(a)

def getData(filename):
	file = open(filename, "r")
	p = dict();
	a = dict();
	throughput_dict[filename] = dict()
	for line in file.readlines():
		data = line.strip().split(":")
	   
		time = data[0]
		sched_type = data[1]
		topology = data[3]
		throughput = data[4]
		element_id = sched_type		

		if ((str(element_id+":"+filename) in data_points) == False):
			data_points[element_id+":"+filename]=[]
			time_dict[element_id+":"+filename]=[]

		data_points[element_id+":"+filename].append(int(throughput))
		time_dict[element_id+":"+filename].append(int(time))
		
		if (int(time) > START1 and int(time)<END1):
		    if ((element_id in p) == False):
		        p[element_id]=[]
		    p[element_id].append(int(throughput))
		elif(int(time) >START2 and int(time)<END2):
		    if ((element_id in a) == False):
		        a[element_id]=[]
		    a[element_id].append(int(throughput))
	
	for key, values in p.iteritems():
		print "->" + key
		average_throughput_before_rebalance = mean(p[key])
		average_throughput_after_rebalance = mean(a[key])
		
		throughput_dict[filename][key] = (average_throughput_before_rebalance, average_throughput_after_rebalance)
	file.close() 

def findConvergence2(data, time, convergedThroughput):
	print "convergedThroughput: "+str(convergedThroughput)
	window_size = 6;
	start_time=600
	window=[]
	convergedTime=0
	zero=0;
	for index in range(0, len(data)): 
		#print "time: "+str(time[index])
		if(time[index] >=600):
			if(data[index] <= 0):
				zero=zero+10
		
	
	return zero

def findConvergence(data, time, convergedThroughput):
	print "convergedThroughput: "+str(convergedThroughput)
	window_size = 6;
	start_time=600
	window=[]
	convergedTime=0
	
	for index in range(0, len(data)): 
		#print "time: "+str(time[index])
		if(time[index] >=600):
			if(len(window)>=window_size):
				window.pop(0)
			window.append(data[index])
			
			closeness = float((abs(mean(window)-convergedThroughput) *1.0))/float(convergedThroughput)
			print "point: "+str(data[index])+" Index: "+str(index) + " time: "+str(time[index]) +" window: "+str(window)
			print closeness
			if(closeness < 0.05 and len(window)>= window_size):
				convergedTime = time[index-window_size]
				break;
		
	if(convergedTime==0 or start_time > convergedTime):
		print "ERROR"
		sys.exit(-1)
	return convergedTime-start_time
	

for dirname, dirnames, filenames in os.walk('.'):
    # print path to all subdirectories first.
    for filename in filenames:
		print filename
		
		getData(filename)
#print "time_dict: "+str(time_dict)
convergence_time = dict()
convergence_compare= dict()

for filename, value in throughput_dict.iteritems():
	for typeSched, d in value.iteritems():
		print "/** Convergence "+typeSched+"_"+filename+" **/"
		converge = findConvergence(data_points[typeSched+":"+filename], time_dict[typeSched+":"+filename], throughput_dict[filename][typeSched][1]);
		print typeSched+"_"+filename+": "+ str(converge)
		if((filename in convergence_time)==False):
			convergence_time[filename]=dict()
		convergence_time[filename][typeSched] = converge
		
		

print "/***********************/"
print "/***********************/"
print convergence_time
print "/***********************/"
print "/***********************/"
schedNames=[]
N=len(convergence_time)

for filename, values in convergence_time.iteritems():
	files.append(filename)
	for type_sched, convergence_time in values.iteritems():
		if((type_sched in convergence_compare)==False):
			convergence_compare[type_sched]=[]
		convergence_compare[type_sched].append(convergence_time)
		if((type_sched in schedNames) == False):
			schedNames.append(type_sched);
		
print "N: "+str(N)
print "convergence_compare: "+str(convergence_compare)
ind = np.arange(N)  # the x locations for the groups 
print "ind: "+str(ind)
width = 0.4       # the width of the bars
fig, ax = plt.subplots()
i=0;
rects = []
for key, values in convergence_compare.iteritems():
	rects1 = ax.bar(ind+i, values, width/1.5, color=cm.jet(2.5*i/(N-1)))
	i=i+0.25
	#autolabel(rects1)
	rects.append(rects1[0])

# add some text for labels, title and axes ticks
ax.set_ylabel('Convergence Time (Secs)')
ax.set_title('Convergence Time Comparison')
ax.set_xticks(ind+width)
print "files: "+str(files)
ax.set_xticklabels( files )

ax.legend( rects, schedNames,loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)


#autolabel(rects1)
#autolabel(rects2)

plt.show()






#ax.set_xticks(ind+width)
plt.show()









