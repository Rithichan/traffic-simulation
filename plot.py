# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 04:11:50 2023

@author: ASUS
"""

import traffic_light_flow as flow
import flow_rate_intersection_with_turning as no_light
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-whitegrid')
fig = plt.figure()
axes = fig.add_subplot(111)
axes.set_title('Light Duration vs Flow Rate')
axes.set_xlabel('Light Duration')
axes.set_ylabel('Flow Rate')

n = 20
n_max = 180

while n < n_max:

    list_flow = list()
    light_duration_list = list()
    
    i = 0
    i_max = 350
    
    for _ in range(1):
        while i < i_max:
    
            if i == 0:
                flow_rate, car_density = no_light.simulate(n, 100, 8000)
                list_flow.append(flow_rate)
                light_duration_list.append(i)
            else:
                flow_rate,car_density = flow.simulate(n,100,8000,i)
                list_flow.append(flow_rate)
                light_duration_list.append(i)
            i += 1

    axes.scatter(light_duration_list,list_flow,marker='x')

    n += 50

axes.legend(['ρ=0.1','ρ=0.35','ρ=0.6','ρ=0.85'])
plt.savefig('Light Duration vs Flow Rate Final',dpi=200)
plt.show()