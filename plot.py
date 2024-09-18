# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 04:11:50 2023

@author: ASUS
"""

import flow_rate_intersection_with_turning as flow
import matplotlib.pyplot as plt

list_flow = list()
car_density_list = list()


i = 1
i_max = 999

for _ in range(1):
    while i < i_max:
        flow_rate,car_density = flow.simulate(i,500,2500)
        list_flow.append(flow_rate)
        car_density_list.append(car_density)
        i += 5


plt.style.use('seaborn-whitegrid')
fig = plt.figure()
axes = fig.add_subplot(111)
axes.set_title('Car Density vs Flow Rate(intersection with turning)')
axes.set_xlabel('Car Density')
axes.set_ylabel('Flow Rate')

axes.scatter(car_density_list,list_flow,marker='x',color='#0C7489')
plt.savefig('Car Density vs Flow Rate(intersection with turning)',dpi=200)
plt.show()