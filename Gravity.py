import math as math
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import random
import sys as sys
import imageio

def startProgress(title):
	global xpro
	xpro=0
	print("         ____________________")
	sys.stdout.write("Progress:")
	sys.stdout.flush()

def progress(x):
	global xpro
	sys.stdout.write("#" * (int(x * 20 // 100 - xpro)))
	sys.stdout.flush()
	xpro = x * 20 // 100

def endProgress():
	global xpro
	sys.stdout.write("#" * int(20 - xpro) + "\n")
	sys.stdout.flush()

def dist(x1,x2,y1,y2):
	return (x1-x2)**2+(y1-y2)**2

def gravity(dots,k,t,a):
	dots1 = dots.copy()
	dots2 = dots1.copy()
	dots3 = dots2.copy()
	dots4 = dots3.copy()
	deltax=[0]*len(dots)
	deltay=[0]*len(dots)
	startProgress("Progress")
	k1 = k
	kwargs={ 'duration': 0.04 }
	with imageio.get_writer('Gravity.gif', mode='I', **kwargs ) as writer:
		timer = 0
		while k1>=1:
			progress(100 * (128-k1) / 128)
			plt.style.use('dark_background')
			plt.title('Gravity Simulation')
			plt.xlabel('First Axis')
			plt.ylabel('Second Axis')
			plt.axis('off')
			plt.xlim(0, 1)
			plt.ylim(0, 1)
			plt.text(0.27, -0.05, 'Timelapse acceleration: 1e+'+str(64.0*k/k1),fontsize=10)
			plt.plot([dots4[0],dots3[0]],[dots4[1],dots3[1]],c=(1.0,1.0,0.8,0.25),lw=0.5)
			plt.plot([dots3[0],dots2[0]],[dots3[1],dots2[1]],c=(1.0,1.0,0.8,0.5),lw=1.0)
			plt.plot([dots2[0],dots1[0]],[dots2[1],dots1[1]],c=(1.0,1.0,0.8,0.75),lw=1.5)
			plt.plot([dots1[0],dots[0]],[dots1[1],dots[1]],c=(1.0,1.0,0.8,1.0),lw=2.0)
			plt.plot(dots[0],dots[1],'w.',mec=(1.0,1.0,0.8),mew=1.0,ms=6.0)
			plt.savefig('temp.png')
			plt.close()
			image = imageio.imread('temp.png')
			writer.append_data(image)
			dots4 = dots3.copy()
			dots3 = dots2.copy()
			dots2 = dots1.copy()
			dots1 = dots.copy()
			for i in range(0,len(dots)):
				corr = (0.5+dist(dots[0][:],dots[0][i],dots[1][:],dots[1][i]))
				corr = corr**k1
				deltax[i] = a*(np.sum(dots[0][:]/corr)/np.sum(1/corr)-dots[0][i])+(1-a)*deltax[i]
				deltay[i] = a*(np.sum(dots[1][:]/corr)/np.sum(1/corr)-dots[1][i])+(1-a)*deltay[i]
				dots[0][i] = dots[0][i]+deltax[i]
				dots[1][i] = dots[1][i]+deltay[i]
			if (max(deltax)<0.005 and max(deltay)<0.005 and min(deltax)>-0.005  and min(deltay)>-0.005):
				if (timer<25):
					timer = timer+1
				else:
					k1=k1/2
					timer = 0
			else:
				timer = 0
	endProgress()

def GO():
	dots=[]
	for i in range(0,100):
		dots.append([random.random(),random.random()])
	dots=pd.DataFrame(dots)
	print("=== Simulating gravitational force ===")
	a=gravity(dots,128,100,0.05)

GO()
