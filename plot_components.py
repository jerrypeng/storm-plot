#7::EvenScheduler:spout_head:2:test1-1-1417657508:0
from pylab import *
import matplotlib.pyplot as plt
import sys

throughput_dict=dict()
time_dict=dict()
file = open(sys.argv[1], "r")
for line in file.readlines():
    data = line.strip().split(":")
    time = data[0]
    sched_type = data[1]
    component = data[2]
    topology = data[4]
    throughput = data[5]
    
    if(int(throughput) < 0):
         throughput = 0

    element_id = component
   # print "{"+element_id+"}-->["+time+", "+throughput+"]"
    if ((element_id in throughput_dict) == False):
        throughput_dict[element_id]=[]
    if ((element_id in time_dict) == False):
        time_dict[element_id]=[]
    throughput_dict[element_id].append(int(throughput))
    time_dict[element_id].append(int(time))
file.close()	
for key in throughput_dict:
    print "{"+key+"}-->"
    print str(throughput_dict[key])
    print str(time_dict[key])
    print "\n"

    line1=plt.plot(time_dict[key], throughput_dict[key], label=key)
plt.xlabel("Time (s)")
plt.ylabel("Throughput-Tuples/10sec")
plt.grid()
#plt.legend([line1,line2], ["line1","line2"])
plt.legend()
plt.show()

