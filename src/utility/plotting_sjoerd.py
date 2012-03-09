
#       plotting.py
#       
#       To be merged with mwavepy
#		Functions to plot Smith charts of random transformations

'''
provides plotting functions, which dont belong to any class. 
'''
import pylab as plb
import numpy as npy
#from matplotlib.patches import Circle 	# for drawing smith chart
from matplotlib.lines import Line2D		# for drawing smith chart

ALMOST_ZER0 = 9.9999999999999995e-07	

def ztos(Z,Z0=1.0):
	return (Z-Z0)/(Z+Z0)
def stoz(S,Z0=1.0):
	return Z0*(1+S)/(1-S)
def identityTransform(S):
	return S

def smith(smithR=1,ax=None, chartColor='black', sTransform=identityTransform):
	'''
	plots the smith chart of a given radius
	takes:
		smithR - radius of smith chart
		ax - matplotlib.axes instance 
	'''
	##TODO: fix this function so it doesnt suck
	if ax == None:
		ax1 = plb.gca()
	else:
		ax1 = ax

	# contour holds matplotlib instances of: pathes.Circle, and lines.Line2D, which 
	# are the contours on the smith chart 
	contour = []
	
	# these are hard-coded on purpose,as they should always be present
	rHeavyList = [0,1]
	xHeavyList = [1,0,-1]
	zeroToInfinity = stoz(plb.linspace(-1,1,20))
	zeroToInfinity = npy.concatenate((zeroToInfinity[:-1],[1/ALMOST_ZER0]))
	infinityRound = npy.concatenate((-zeroToInfinity[:0:-1],zeroToInfinity))
	
		
	#TODO: fix this
	rLightList = npy.array([.2,.5,2,5])
	xLightList = npy.array([.2,.5,2,5])
	# these could be dynamically coded in the future, but work good'nuff for now 
# 	rLightList = plb.logspace(3,-5,9,base=.5)
# 	xLightList = plb.hstack([plb.logspace(2,-5,8,base=.5), -1*plb.logspace(2,-5,8,base=.5)]) 
# 	
# 	# cheap way to make a ok-looking smith chart at larger than 1 radii
# 	if smithR > 1:
# 		rMax = (1.+smithR)/(1.-smithR)
# 		rLightList = plb.hstack([ plb.linspace(0,rMax,11)  , rLightList ])

	def imaginaryCircle(realValue,lineWidth):
		unityCircle = ztos(realValue+npy.complex(ALMOST_ZER0,1)*infinityRound)
		unityCircle = sTransform(unityCircle)
		contour.append( Line2D( unityCircle.real, unityCircle.imag ,linewidth=lineWidth, color=chartColor) )
		
	def realBow(imaginaryValue,lineWidth):
		bow = ztos(npy.complex(0,imaginaryValue)+zeroToInfinity)
		bow = sTransform(bow)
		contour.append( Line2D( bow.real, bow.imag ,linewidth=lineWidth, color=chartColor) )
	def realBows(imaginaryValue,lineWidth):
		realBow(imaginaryValue,lineWidth)
		realBow(-imaginaryValue,lineWidth)
	
	# loops through Light and Heavy lists and draws circles using patches
	for r in rLightList:
		imaginaryCircle(r,.5)
	for x in xLightList:
		realBows(x,.5)
	for r in rHeavyList:
		imaginaryCircle(r,1)
	for x in xHeavyList:
		realBows(x,1)
	
	#draw x and y axis
# 	ax1.axhline(0, color='k')
# 	ax1.axvline(1, color='k')
	ax1.grid(0)
	#set axis limits
	ax1.axis('equal')
	ax1.axis(smithR*npy.array([-1.2, 1.2, -1.2, 1.2]))
	
	# loop though contours and draw them on the given axes
	for currentContour in contour:
		#ax1.add_patch(currentContour)
		ax1.add_line(currentContour)

def drawSParameter(complexData, sTransform=identityTransform,ax=None, chartColor='black',lineWidth=1.0):
	if ax == None:
		ax1 = plb.gca()
	else:
		ax1 = ax
	
	complexData = sTransform(complexData)
	curve = Line2D( complexData.real, complexData.imag ,linewidth=lineWidth, color=chartColor) 	
	ax1.add_line(curve)
			
if __name__ == '__main__':
	def shiftChart(S):
		return 0.2+S

	smith()
	smith(chartColor='red',sTransform=shiftChart)
	plb.show()