import numpy as np
import matplotlib.pyplot as plt
t=np.arange(-1,2,.01)
s=np.sin(2*np.pi*t)

# plt.plot(t,s)
# #drawathickredhlineaty=0thatspansthexrange
# l=plt.axhline(linewidth=4,color='r')
# plt.axis([-1,2,-1,2])
# plt.show()
# plt.close()
#
# #drawadefaulthlineaty=1thatspansthexrange
# plt.plot(t,s)
# l=plt.axhline(y=1,color='b')
# plt.axis([-1,2,-1,2])
# plt.show()
# plt.close()
#
# #drawathickbluevlineatx=0thatspanstheupperquadrantoftheyrange
# plt.plot(t,s)
# l=plt.axvline(x=0,ymin=0,linewidth=4,color='b')
# plt.axis([-1,2,-1,2])
# plt.show()
# plt.close()
#
# #drawadefaulthlineaty=.5thatspansthethemiddlehalfoftheaxes
# plt.plot(t,s)
# l=plt.axhline(y=.5,xmin=0.25,xmax=0.75)
# plt.axis([-1,2,-1,2])
# plt.show()
# plt.close()

plt.plot(t,s)
p=plt.axhspan(0.25,0.75,facecolor='0.5',alpha=0.5)
p=plt.axvspan(1.25,1.55,facecolor='g',alpha=0.5)
plt.axis([-1,2,-1,2])
plt.show()