from matplotlib import pyplot as plt
import numpy as np
import csv
import math
import matplotlib.animation as animation

fname="ExampleData/air_halfatm.csv"
print(fname)
Time=[]
s1=[]
s2=[]
derivative=[]
rise=-999
atime=-999
rise_counter= 0
tolerance = 1e-1
dTau = 0
with open(fname, 'r') as fp:
    plotter=csv.reader(fp,delimiter=',')
    for i in range (0,16):
        next(plotter)
    for cols in plotter:
        if float(cols[0]) > -80 and float(cols[0])<80:
            Time.append(float(cols[0]))
            s1.append(float(cols[1]))
            s2.append(float(cols[2]))
            #print(cols[0],cols[1],cols[2])
fig,axs=plt.subplots(1,2)
line0 = axs[0].plot(Time[0],s1[0],'.',mfc='orange',mec='orange')[0]
line1 = axs[0].plot(Time[0],s2[0],'.',mfc='blue',mec='blue')[0]
line2 = axs[1].plot(s1[0],s2[0],'.',mfc='magenta',mec='magenta')[0]

axs[0].set(xlim=[-80,80],ylim=[-1.5,3.0])
axs[1].set(xlim=[-1.5,1],ylim=[0,3.0])

for i in range(0,len(s1)-1):
    dS = s1[i+1] - s1[i]
    dT = Time[i+1] - Time[i]
    dSdT = dS/dT
    if dSdT < tolerance and abs(Time[i]-dTau) > 4:
        rise_counter+=1
        dTau = Time[i]

def update(frame):
    line0.set_xdata(Time[:frame])
    line0.set_ydata(s1[:frame])
    line1.set_xdata(Time[:frame])
    line1.set_ydata(s2[:frame])
    line2.set_xdata(s1[:frame])
    line2.set_ydata(s2[:frame])
    return(line0,line1,line2)
print(rise_counter)
ani=animation.FuncAnimation(fig=fig, func=update, frames=len(s1), interval=1)
plt.show()

            
