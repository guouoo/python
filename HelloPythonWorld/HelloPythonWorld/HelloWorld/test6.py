'''
Created on Dec 28, 2015

@author: tguo
'''


# coding=UTF-8

import matplotlib.pyplot as plt

line1, = plt.plot([1,2,3], label="Line 1", linestyle='--')
line2, = plt.plot([3,2,1], label="Line 2", linewidth=4)
line3, = plt.plot([3,3,1], label="Line 3", linewidth=2)

# Create a legend for the first line.
first_legend = plt.legend(handles=[line1], loc=1)

# Add the legend manually to the current Axes.
ax = plt.gca().add_artist(first_legend)

# Create another legend for the second line.
plt.legend(handles=[line2], loc=4)
plt.legend(handles=[line3], loc=2)

plt.show()