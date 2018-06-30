# -*- coding: utf-8 -*-

import pandas as pd
import Tkinter
import tkFileDialog
import matplotlib.pyplot as plt
import math


def quit(root):
    root.destroy()


def acquire_file():
    root = Tkinter.Tk()
    filename = tkFileDialog.askopenfilename(parent=root, title='Open file to PROCESS')
    fdata = pd.read_csv(filename)
    quit(root)
    return fdata


def getdisp(gender, height, axis):
    # gender as a string, height in cm
    change = []
    gtemp = []
    atemp = []
    velocity = []

    for i in range(0, len(gx), 1):
        gmag = math.sqrt(gx[i] * gx[i] + gy[i] * gy[i] + gz[i] * gz[i])
        amag = math.sqrt(ax[i] * ax[i] + ay[i] * ay[i] + az[i] * az[i])
        gtemp.append(gmag)
        atemp.append(amag)

    if gender == "Male":
        forearm = (height + 254.03)/17.45
    elif gender == "Female":
        forearm = (height - 32.16)/5.66

    radius = forearm + (1.3*forearm)

    print forearm

    for i in range(1, len(gtemp), 1):
        velocity.append(gtemp[i]*radius/100)
        change.append(gtemp[i-1]*radius/100*0.05 + 0.5*atemp[i]*0.05*0.05)

    return change


data = acquire_file()
ax = data.iloc[:,0]
ay = data.iloc[:,1]
az = data.iloc[:,2]
gx = data.iloc[:,3]
gy = data.iloc[:,4]
gz = data.iloc[:,5]

rate = getdisp("Male", 176, gz)

plt.figure("Velocity")
plt.plot(rate)
plt.show()
