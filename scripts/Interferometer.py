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
TimeLimits=[-25,25]
centre=[-0.25,1.25]
refcoord=[-0.25,2.5]
refcoord1=[-0.25,0.1]
phasor=[]

with open(fname, 'r') as fp:
    plotter=csv.reader(fp,delimiter=',')
    for i in range (0,16):
        next(plotter)
    for cols in plotter:
        if float(cols[0]) >TimeLimits[0] and float(cols[0])<TimeLimits[1]:
            Time.append(float(cols[0]))
            s1.append(float(cols[1]))
            s2.append(float(cols[2]))
            #print(cols[0],cols[1],cols[2])
fig,axs=plt.subplots(1,2)
line0 = axs[0].plot(Time[0],s1[0],'.',mfc='orange',mec='orange')[0]
line1 = axs[0].plot(Time[0],s2[0],'.',mfc='blue',mec='blue')[0]
line2 = axs[1].plot(s1[0],s2[0],'.',mfc='magenta',mec='magenta')[0]

axs[0].set(xlim=[TimeLimits[0],TimeLimits[1]], ylim=[-1.5,3.0])
axs[1].set(xlim=[-1.5,1],ylim=[0,3.0])
axs[0].set_xlabel("Time")
axs[0].set_ylabel("Signal Amplitude (V)")

axs[1].set_xlabel("Signal Amplitude (V)")
axs[1].set_ylabel("Signal Amplitude (V)")

for i in range(0,len(s1)-1):
    dS = s1[i+1] - s1[i]
    dT = Time[i+1] - Time[i]
    
    dSdT = dS/dT
    if dSdT < tolerance and abs(Time[i]-dTau) > 5:
        rise_counter+=1
        dTau = Time[i]
rotP =0
mult=True
for i in range (0, len(s1)):
    if s1[i] <  centre[0]:
     dotproduct = ((s1[i]-centre[0])*(refcoord[0]-centre[0]))+((s2[i]-centre[1])*(refcoord[1]-centre[1]))
     amp = math.hypot((s1[i]-centre[0]), (s2[i]-centre[1]))*math.hypot((refcoord[0]-centre[0]),(refcoord[1]-centre[1]))
     theta =math.acos(dotproduct/amp)*180/math.pi+180*rotP
 
    elif s1[i] >  centre[0]:
        dotproduct = ((s1[i]-centre[0])*(refcoord[0]-centre[0]))+((s2[i]-centre[1])*(refcoord[1]-centre[1]))
        amp = math.hypot((s1[i]-centre[0]), (s2[i]-centre[1]))*math.hypot((refcoord[0]-centre[0]),(refcoord[1]-centre[1]))     
        theta =rotP*180+math.acos(dotproduct/amp)*180/math.pi
        if mult:
            rotP=rotP+1
            mult=False
    phasor.append(theta/360)

phase_count =-10
aPhase=[]
Peak=False
ocu=0
for p in range (0,len(phasor)):
    if phasor[p] > phase_count:
        phase_count = phasor[p]
        ocu=0
        Peak=False
    if phasor[p]<phase_count and not Peak:
        if ocu ==0:
            aPhase.append(phase_count)
            Peak = True
        ocu=1
        phase_count=phasor[p]
print(aPhase)        
def update(frame):
    line0.set_xdata(Time[:frame])
    line0.set_ydata(s1[:frame])
    line1.set_xdata(Time[:frame])
    line1.set_ydata(s2[:frame])
    line2.set_xdata(s1[:frame])
    line2.set_ydata(s2[:frame])
    return(line0,line1,line2)
print("From waves-forms: ",rise_counter," From phasors: ", len(aPhase))
ani=animation.FuncAnimation(fig=fig, func=update, frames=len(s1), interval=5,repeat=False)
fig2,axs =plt.subplots()
axs.plot(Time,phasor,color='blue')
axs.set_xlabel("Time")
axs.set_ylabel("Occurance of Full rotations")
plt.show()

            
