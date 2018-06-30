# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import Tkinter
import tkFileDialog
import math
import sys

from matplotlib.pyplot import plot, scatter, show
from numpy import NaN, Inf, arange, isscalar, asarray, array


def quit(root):
    root.destroy()


def acquire_file() :
    root = Tkinter.Tk()
    filename = tkFileDialog.askopenfilename(parent=root,title='Open file to PROCESS')
    fdata = pd.read_csv(filename)
    quit(root)
    return fdata


def peakdet(v, delta, x=None):

    maxtab = []
    mintab = []

    if x is None:
        x = arange(len(v))

    v = asarray(v)

    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')

    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')

    if delta <= 0:
        sys.exit('Input argument delta must be positive')

    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN

    lookformax = True

    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]

        if lookformax:
            if this < mx - delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn + delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)


angleX = angleY = angleZ = accAngleX = accAngleY = accAngleZ = 0
listX = []
listY = []
listZ = []
max = []
min = []
rep = []
repDev = []
sum = 0
sumDev = 0
sample = 0
sampleAvg = 0
repDel = []

data = acquire_file()
ax = data.iloc[:,0]
ay = data.iloc[:,1]
az = data.iloc[:,2]
gx = data.iloc[:,3]
gy = data.iloc[:,4]
gz = data.iloc[:,5]

# complementary filter

for i in range(0, len(ax), 1):
    angleX = angleX + math.degrees(gx[i] * 0.04347826086)
    angleY = angleY + math.degrees(gy[i] * 0.04347826086)
    angleZ = angleZ + math.degrees(gz[i] * 0.04347826086)

    accAngleX = math.degrees(math.atan2(ay[i], az[i]))
    accAngleY = math.degrees(math.atan2(az[i], ax[i]))
    accAngleZ = math.degrees(math.atan2(-ay[i], ax[i]))

    angleX = 0.98 * angleX + 0.02 * accAngleX
    angleY = 0.98 * angleY + 0.02 * accAngleY
    angleZ = 0.98 * angleZ + 0.02 * accAngleZ

    listX.append(angleX)
    listY.append(angleY)
    listZ.append(angleZ)

# add code to find axis with max height

max, min = peakdet(listZ,.3)

print max
print min

# remove small variations
# calculate rom

if len(max) != len(min):
    for i in range(0, len(max) - 1, 1):
        sample = sample + abs(max[i][0] - min[i][0])
    sampleAvg = sample / (len(max) - 1)

    for i in range(0, len(max) - 1, 1):
        if abs(max[i][0] - min[i][0]) > sampleAvg/2:
            rom = abs(max[i][1] - min[i][1])
            rep.append(rom)
else:
    for i in range(0, len(max), 1):
        sample = sample + abs(max[i][0] - min[i][0])
    sampleAvg = sample / len(max)

    for i in range(0, len(max), 1):
        if abs(max[i][0] - min[i][0]) > sampleAvg/2:
            rom = abs(max[i][1] - min[i][1])
            rep.append(rom)

for j in range(0, len(rep), 1):
    sum = sum + abs(rep[j])

avgROM = sum/(len(rep))
sum = 0

for m in range(0, len(rep), 1):
    if rep[m] < avgROM*0.4:
        repDel.append(rep[m])


if len(repDel)>0:
    for i in range(0, len(repDel), 1):
        rep.remove(repDel[i])
    for j in range(0, len(rep), 1):
        sum = sum + abs(rep[j])
    avgROM = sum / (len(rep))

for r in range(0, len(rep), 1):
    repDev.append(abs((rep[r] - avgROM))/avgROM*100)

for s in range(0, len(repDev), 1):
    sumDev = sumDev + repDev[s]

avgCon = 100 - (sumDev/(len(rep)))

print "RepCount: "
print len(rep)
print "AvgCon: "
print avgCon


plot(listZ)
scatter(array(max)[:,0], array(max)[:,1], color='blue')
scatter(array(min)[:,0], array(min)[:,1], color='red')
show()

# plotting sensor fused data on all axis

plt.figure("Angle X")
plt.plot(listX)
plt.figure("Angle Y")
plt.plot(listY)
plt.figure("Angle Z")
plt.plot(listZ)

plt.show()

# plotting raw sensor data

# plt.figure("x axis acc")
# plt.plot(ax)
# plt.figure("y axis acc")
# plt.plot(ay)
# plt.figure("z axis acc")
# plt.plot(az)
#
# plt.figure("x axis gyro")
# plt.plot(gx)
# plt.figure("y axis gyro")
# plt.plot(gy)
# plt.figure("z axis gyro")
# plt.plot(gz)
#
# plt.show()
