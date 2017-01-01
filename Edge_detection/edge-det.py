# -*- coding: utf-8 -*-
import numpy as np
from scipy import misc
from scipy import ndimage
import PIL #for preview
import os;
path = os.getcwd() #root directory

im = ndimage.imread(str(path)+"\img\example.jpg") #image to np.array

#getting image parameters
parameters = str(im.shape).replace(",", "")
h = parameters.split(" ", 2)[0]
h = int(h[1:])
w = parameters.split(" ", 2)[1]
w = int(w.replace(")", ""))
print 'width: ' + str(w),'height: ' + str(h)
# rgb to grayscale
print 'Converting to grayscale'
for i in range(1,h):
	for j in range(1,w):
		r,g,b = im[i,j]
		gray = r*0.299+g*0.587+b*0.114
		im[i,j] = [gray,gray,gray] # f(x,y) - grayscale image
# 1) blurring S(x,y) = G(x,y)*f(x,y)
print 'Blurring'
S = ndimage.gaussian_filter(im, sigma=2) # S(x,y) - smoothed image
# 2) compute gradient
print 'Computing gradient'
Gx = np.zeros([w,h,1])
Gy = np.zeros([w,h,1])
G = np.zeros([w,h,1])
theta = np.zeros([w,h,1])
k = 0
for y in range(1,h-1):
	for x in range(1,w-1):
		try:
			Gx[x,y] =(int(S[x,y+1,1]) - int(S[x,y,1]) + int(S[x+1,y+1,1]) - int(S[x+1,y,1]))/2
			Gy[x,y] =(int(S[x,y,1]) - int(S[x+1,y,1]) + int(S[x,y+1,1]) - int(S[x+1,y+1,1]))/2
			G[x,y] = np.sqrt(pow(int(Gx[x,y]),2) + pow(int(Gy[x,y]),2))
			theta[x,y] = np.arctan(pow(int(Gy[x,y]),2)/pow(int(Gx[x,y]),2))
		except:
			k = k+1
		shape = Gx.shape
		#Gy[x,y] =(S[x,y,1] - S[x+1,y,1] + S[x,y+1,1] - S[x+1,y+1,1])/2
# preview
print shape
print 'out of bounds ' + str(k) + ' times'
img = PIL.Image.fromarray(S, 'RGB')
img.save(str(path)+'\img\preview.png')