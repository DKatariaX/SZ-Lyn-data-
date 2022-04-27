# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 00:43:19 2022

@author: Dhairya
"""

import matplotlib.pyplot as plt
import numpy as np
import csv
from astropy.timeseries import LombScargle
from scipy.interpolate import interp1d
rel_targ = []
rel_ch1B = []
rel_ch2B = []
B_V = []
jd_targ_B = []
jd_bv = []
jd_ch = []
targ_B=[]
mag_error_B=[]
rel_ch1V = []
rel_ch2V = []
targ_V = []
jd_targ_V= []
mag_error_V= []
B_V_error=[]
with open('ben_data_V.csv', 'r', newline='') as databen:
    reader = csv.reader(databen)
    # skip header
    next(reader)
    for row in reader:
        
        targ_V.append(float(row[21]))
        jd_targ_V.append(float(row[0]))
        mag_error_V.append(float(row[29]))
        rel_ch1V.append(float(row[22]))
        rel_ch2V.append(float(row[23]))

with open('ben_data_B.csv', 'r', newline='') as databen:
    reader = csv.reader(databen)
    # skip header
    next(reader)
    for row in reader:
        targ_B.append(float(row[24]))
        jd_targ_B.append(float(row[0]))
        mag_error_B.append(float(row[35]))
        # if float(row[17]) > float(-2.5) and float(row[17]) < float(-1):
        #     rel_targ.append(float(row[17]))
        if float(row[28]) > float(0) and float(row[28]) < float(0.7):
            B_V.append(float(row[28]))
            jd_bv.append(float(row[0]))
            B_V_error.append(float(row[29]))
        rel_ch1B.append(float(row[25]))
        rel_ch2B.append(float(row[26]))
        #jd_ch.append(float(row[0]))
# x2 =  np.arange(0,180,1)
# x1 = np.arange(0,186,1)
# # x = np.arange(0,188,1)


print(len(B_V))
fig, ax = plt.subplots(1, 2, figsize=(9, 4))



# plt.axvline(55,c='black')
# plt.axvline(85,c='black')
# plt.scatter(x1,rel_ch1)
# plt.scatter(x1,rel_ch2)
ax[0].set(xlabel = 'time (JD)', ylabel='B mag', title='B magnitude variation')
ax[0].errorbar(jd_targ_B, targ_B,mag_error_B,ecolor='gray', capsize=0,fmt='.k')

# ax[2].set(xlabel = 'time (JD)', ylabel='B-V color')
# ax[2].errorbar(jd_bv,B_V,fmt='.k')

ax[1].set(xlabel = 'time (JD)', ylabel='V mag', title='V magnitude variation')
ax[1].errorbar(jd_targ_V,targ_V,mag_error_V,ecolor='gray', capsize=0,fmt='.k')

#B mag
ls = LombScargle(jd_targ_B, targ_B,mag_error_B)
frequency , power = ls.autopower()
period_days = 1/frequency
period_hours = period_days*24
best_period  = period_days[np.argmax(power)]
abs_mag = -2.81*np.log10(best_period)-1.43
phase_B = (jd_targ_B / best_period) % 1

print('total observation window (days)', np.round(max(jd_targ_B)-min(jd_targ_B),2))
print("Best period: {0:.2f} hours".format(24 * best_period))
print("Best period: {0:.2f} days".format(best_period))
print("mean abs mag", np.round(abs_mag,2) )

fig, ax = plt.subplots(1, 2, figsize=(9, 4))
plt.suptitle('Lomb-Scargle periodgram using B mag data')
ax[0].set(xlim=(0, 10), ylim=(0, 1),xlabel='Period (hours)', 
          ylabel='Lomb-Scargle Power',
          title='Lomb-Scargle  Periodogram')

ax[0].plot(period_hours, power, '-k')
ax[1].errorbar(phase_B, targ_B,mag_error_B,
               fmt='.k', ecolor='gray', capsize=0)
ax[1].set(xlabel='phase',ylabel='B magnitude',title='Phased Data')
ax[1].invert_yaxis()

#### Vmag
ls = LombScargle(jd_targ_V, targ_V, mag_error_V)
frequency , power = ls.autopower()
period_days = 1/frequency
period_hours = period_days*24
best_period  = period_days[np.argmax(power)]
abs_mag = -2.81*np.log10(best_period)-1.43
phase_V = (jd_targ_V / best_period) % 1


fig, ax = plt.subplots(1, 2, figsize=(9, 4))
plt.suptitle('Lomb-Scargle periodgram using V mag data')
ax[0].set(xlim=(0, 10), ylim=(0, 1),xlabel='Period (hours)', 
          ylabel='Lomb-Scargle Power',
          title='Lomb-Scargle Periodogram')

ax[0].plot(period_hours, power, '-k')
ax[1].errorbar(phase_V, targ_V,mag_error_V,
               fmt='.k', ecolor='gray', capsize=0)
ax[1].set(xlabel='phase',ylabel='V magnitude',title='Phased Data')
ax[1].invert_yaxis()

#### B-V


ls = LombScargle(jd_bv, B_V,B_V_error)
frequency , power = ls.autopower()

period_days = 1/frequency
period_hours = period_days*24
best_period  = period_days[np.argmax(power)]
abs_mag = -2.81*np.log10(best_period)-1.43
phase_B_V = (jd_bv / best_period) % 1

fig, ax = plt.subplots(1, 2, figsize=(9, 4))
plt.suptitle('Lomb-Scargle periodgram using B-V data')
ax[0].set(xlim=(0, 10), ylim=(0, 1),xlabel='Period (hours)', 
          ylabel='Lomb-Scargle Power',
          title='Lomb-Scargle  Periodogram')

ax[0].plot(period_hours, power, '-k')
ax[1].errorbar(phase_B_V, B_V,B_V_error,
                fmt='.k', ecolor='gray', capsize=0)
ax[1].set(xlabel='phase',ylabel='B-V index',title='Phased Data')
ax[1].invert_yaxis()

fig, ax = plt.subplots(1, 2, figsize=(9, 4))
ax[0].errorbar(phase_V, targ_V,mag_error_V,
               fmt='.g', ecolor='gray', capsize=0,label='V phase progression')
ax[0].errorbar(phase_B, targ_B,mag_error_B,
              fmt='.b', ecolor='gray', capsize=0,label='B phase progression')
ax[1].errorbar(phase_B_V, B_V,B_V_error,
              fmt='.k', ecolor='gray', capsize=0,label='B_V phase progression')
ax[0].set(ylabel='Magnitude',
xlabel='phase')
ax[1].set(ylabel='Magnitude',
xlabel='phase')
ax[0].legend(loc='lower left')
ax[1].legend(loc='lower left')
# interp=interp1d(targ_V,targ_B[:181])
# print(interp)
# plt.figure()

# plt.plot(targ_V, interp)
