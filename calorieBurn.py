# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math


def met(age, hr, rhr):

    mhr = 0
    mvo2 = 0
    cvo2 = 0
    vo2 = 0
    metval = 0

    mhr = 220-(0.85*age)
    mvo2 = 15*(mhr/rhr)
    vo2 = (((hr/mhr*100)-37)/0.64)*mvo2/100

    metval = vo2/3.5

    return metval


def bmr(age, weight, height, gender):

    bmrval = 0

    # weight in kg, height in cm, age in years
    if gender == "Male":
        bmrval = (10 * weight) + (6.25 * height) - (5 * age) + 5
    elif gender == "Female":
        bmrval = (10 * weight) + (6.25 * height) - (5 * age) - 161

    return bmrval


page = 0
pweight = 0
pheight = 0
pGender = ""
phr = 0
prhr = 0
time = 0

x = met(page, phr, prhr)
y = bmr(page, pweight, pheight, pGender)

# time in hours
calorie = y*x*time/24

