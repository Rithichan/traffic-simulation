# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:11:37 2023

@author: ASUS
"""

import random
import simulate_2nd_road as sim
import numpy as np
from scipy.stats import sem

class car:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.position < other.position


def initialize(num_cars,road_len):
    n_car = 0
    n_car_max = num_cars

    position_list = list()
    info = list()

    while n_car < n_car_max:
        random_position = random.randint(0,road_len - 1)
        if random_position not in position_list:
            car_info = car(random_position,random.randint(1,5))
            info.append(car_info)
            position_list.append(random_position)
            n_car += 1
    info = sorted(info)
    return info
        

def acceleration(vehicle_v,vehicle_pos_next,vehicle_pos,v_max,road_len):
    if vehicle_v < v_max:
        if ((vehicle_pos_next - vehicle_pos) + road_len)%road_len > vehicle_v + 1:
            vehicle_v = vehicle_v + 1
            return vehicle_v
    vehicle_v = vehicle_v
    return vehicle_v

def deceleration(vehicle_v,vehicle_pos_next,vehicle_pos,v_max,road_len):
    if ((vehicle_pos_next - vehicle_pos) + road_len)%road_len <= vehicle_v:
        vehicle_v = ((vehicle_pos_next - vehicle_pos) + road_len)%road_len - 1
        return vehicle_v
    vehicle_v = vehicle_v
    return vehicle_v

def random_deccel(vehicle_v):
    if vehicle_v < 1: #if change to <= 1 basically no traffic jams occur
        return vehicle_v
    cope = random.uniform(0,1)
    if cope < 0.3:
        return vehicle_v - 1
    else:
        return vehicle_v

def flow_rate(thing,road_len):
    
    car_num = 0
    car_on_other_road = 0
    
    for _ in range(thing):
        cope = random.randint(0,1)
        if cope == 0:
            if car_num >= road_len:
                car_on_other_road += 1
            else: 
                car_num += 1
        if cope == 1:
            if car_on_other_road >= road_len:
                car_num += 1
            else:
                car_on_other_road += 1

    cars = initialize(car_num,road_len)
    v_max = 5
    t = 0
    t_max = 3500
    past_cars = 0
    wait_time = 0

    second_road,flow_rate_2 = sim.simulate_road(car_on_other_road,road_len)

    while t<t_max:

        for car_index in range(len(cars)):
            #sets the velocity, position and next position of cars
            vehicle_pos = cars[car_index].position
            vehicle_v = cars[car_index].velocity

            if car_index + 1 == len(cars):
                vehicle_pos_next = cars[0].position
            else:
                vehicle_pos_next = cars[car_index + 1].position

            #move vehicles
            vehicle_v = acceleration(vehicle_v, vehicle_pos_next, vehicle_pos, v_max, road_len)
            vehicle_v = deceleration(vehicle_v, vehicle_pos_next, vehicle_pos, v_max, road_len)
            vehicle_v = random_deccel(vehicle_v)

            #intersection
            if vehicle_pos < road_len/2:
                if vehicle_pos + vehicle_v >= road_len/2:


                    #info of 2nd road
                    second_road_present = second_road[t]
                    car_postions_present = np.array(second_road_present.car_positions)

                    second_road_future = second_road[t+1]
                    car_positions_future = np.array(second_road_future.car_positions)
                    
                    check_1 = np.where(car_postions_present < road_len/2)
                    check_1 = check_1[0]
                    
                    will_cross = False
                    
                    if road_len/2 in car_positions_future:
                        will_cross = True

                    for element in check_1:
                        if car_positions_future[element] >= road_len/2:
                            will_cross = True
                            break

                    if will_cross == True:
                        vehicle_v = (road_len/2 - vehicle_pos) - 1

                if (vehicle_pos + vehicle_v) >= road_len:
                    past_cars += 1
                
            if vehicle_pos == (road_len/2 - 1):
                if vehicle_v == 0:
                    wait_time += 1

            vehicle_pos = (vehicle_pos + vehicle_v)%road_len
            cars[car_index].position = vehicle_pos
            cars[car_index].velocity = vehicle_v

        t += 1

    car_density = thing/(2*road_len)
    flow_rate_1 = past_cars/t_max
    flow_rate_total = flow_rate_1 + flow_rate_2

    return flow_rate_total,car_density
    
