# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.font_manager import FontProperties
a=[-0.100,2.697,3.153,4.058,1.477,0.273,2.221,3.784,4.923,7.230,10.926,11.193,10.029,10.285,12.715,15.998,14.815,17.554,18.076,14.659,17.013,19.615,19.168,17.882,20.899,25.280,25.706,28.541,29.214,31.391,36.293,39.578,41.979,37.002,38.890,37.046,39.956,44.522,48.816,51.791,54.992,51.605,51.632,55.325,57.646,56.505,49.154,50.518,53.269,50.797,54.035,58.053,58.089,56.502,56.356,54.220,55.275,54.172,53.983,47.855,46.166,44.474,53.082,61.703,66.890,65.999,65.387,66.749,74.309,77.704,82.964,89.935,88.863,87.429,96.089,99.037,89.391,95.402,104.819,114.066,116.354,113.090,111.101,101.719,102.006,109.011,112.075,115.023,106.060,98.723,105.874,94.833,84.015,83.831,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.358,84.174,81.905,90.212,87.193,85.338,90.123,97.855,97.183,94.602,99.117,99.804,101.129,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.937,87.749,84.714,84.962,82.381,82.199,90.568,93.259,101.419,104.161,101.020,108.552,111.698,110.278,116.389,102.422,111.910,119.342,119.586,122.375,116.437,117.341,117.207,113.444,112.822,125.366,124.162,132.396,138.767,141.287,147.887,148.122,139.730,147.148,141.717,136.580,146.649,150.808,147.883,153.176,160.358,156.702,141.126,144.446,141.766,136.531,144.801,144.305,148.844,145.519,143.142,143.142,142.900,146.237,146.859,149.370,157.367,155.673,162.093]
# print(len(a))
b=[0.000,2.489,1.425,0.387,-1.239,-0.240,1.580,2.390,2.651,3.455,4.339,5.020,3.720,6.331,6.526,7.374,4.590,5.273,4.245,3.714,5.480,4.969,5.089,7.122,7.862,10.486,12.020,14.672,14.484,16.059,18.429,18.458,17.485,17.771,18.418,21.891,20.789,22.956,22.982,24.347,27.015,28.082,27.078,29.531,31.817,32.327,30.607,34.574,37.036,34.823,37.723,41.320,41.352,40.212,43.341,41.381,42.349,41.620,42.749,37.057,35.760,33.278,35.911,39.851,41.547,40.683,40.156,37.672,36.410,41.064,41.770,44.336,47.627,52.044,55.008,54.487,44.128,44.332,51.349,53.904,53.359,54.487,55.952,59.625,58.543,58.294,58.219,59.069,55.672,51.010,53.217,47.007,38.256,42.700,45.503,40.327,29.286,24.973,33.365,26.806,22.482,15.861,19.218,17.115,9.215,16.210,22.439,25.577,22.606,18.271,19.183,23.779,24.051,24.212,23.948,26.740,24.518,13.857,13.630,17.186,13.758,13.797,14.171,17.716,15.294,14.249,16.488,21.777,21.250,19.743,21.512,21.455,21.584,14.057,15.867,12.150,7.024,-2.338,-9.274,-9.787,-4.422,-0.348,0.375,0.242,0.354,-3.085,-0.594,1.352,0.107,-0.202,-2.171,-6.015,-1.333,-3.487,-3.062,-1.363,-0.445,-2.711,-2.056,-3.638,-3.316,-5.221,-4.502,-1.714,-0.413,2.795,2.716,1.555,3.961,5.370,5.373,6.671,3.557,5.086,6.478,7.016,7.123,5.097,5.347,5.370,3.638,3.325,8.187,10.495,13.101,14.502,14.290,14.302,13.159,11.696,12.229,12.058,10.782,12.553,12.535,11.908,11.924,12.751,12.089,6.054,6.334,7.088,10.972,11.787,9.649,9.948,8.022,8.407,8.024,7.576,10.655,10.150,9.883,11.984,12.342,15.266]
x = np.linspace(0, 1, 216)
# y = np.sin(x)
y=a
# print(type(y))
z=b
# z = np.cos(x**2)
# print(z)


plt.figure(figsize=(8,4.5))
plt.plot(x,y,label="$Account$",color="red",linewidth=2)
# plt.plot(x,z,"--",label="$cos(x^2)$")
plt.plot(x,z,label="$Benchmark$",color="blue",linewidth=2)
plt.xlabel("$Date$")
plt.ylabel("$Return Rate(\%)$")
plt.title("$Cumulative  Return(\%)$")
# font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14) 
# plt.title(u'累计收益', fontproperties=font)
plt.ylim(-40,180)
plt.legend(('label1', 'label2'), 'upper left')
plt.show()