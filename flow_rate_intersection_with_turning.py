# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 20:56:48 2023

@author: ASUS
"""

import random

class car:
    def __init__(self, position, velocity, road):
        self.position = position
        self.velocity = velocity
        self.road = road

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.position < other.position


class road:
    def __init__(self,car_positions,car_velocities,time):
        self.car_positions = car_positions
        self.car_velocities = car_velocities
        self.time = time


def initialize(num_cars,road_len):
    n_car = 0
    n_car_max = num_cars

    position_list_1 = list()
    position_list_2 = list()
    info_1 = list()
    info_2 = list()

    while n_car < n_car_max:

        random_position = random.randint(0,road_len-1)
        random_road = random.randint(1,2)

        if random_road == 1:
            if random_position not in position_list_1:
                car_info = car(random_position,random.randint(1,5),1)
                info_1.append(car_info)
                position_list_1.append(random_position)
                n_car += 1
        if random_road == 2:
            if random_position not in position_list_2:
                car_info = car(random_position,random.randint(1,5),2)
                info_2.append(car_info)
                position_list_2.append(random_position)
                n_car += 1

    info_1 = sorted(info_1)
    info_2 = sorted(info_2)

    return info_1,info_2


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


def simulate(car_num,road_len,itr):

    v_max = 5
    t = 0
    t_max = itr
    past_cars = 0

    cars_1 , cars_2 = initialize(car_num,road_len)
  
    while t < t_max:
    
        #first road has pirority
        remove_1 = list()
    
        for car_index_1 in range(len(cars_1)):
            #sets the velocity, position and next position of cars
            vehicle_pos = cars_1[car_index_1].position
            vehicle_v = cars_1[car_index_1].velocity
            if car_index_1 + 1 == len(cars_1):
                vehicle_pos_next = cars_1[0].position
            else:
                vehicle_pos_next = cars_1[car_index_1 + 1].position
        
            #move vehicles
            vehicle_v = acceleration(vehicle_v, vehicle_pos_next, vehicle_pos, v_max, road_len)
            vehicle_v = random_deccel(vehicle_v)
            vehicle_v = deceleration(vehicle_v, vehicle_pos_next, vehicle_pos, v_max, road_len)
            
            turning_decision = 0
            
            #at intersection 
            if vehicle_pos < road_len/2:
                if vehicle_pos + vehicle_v >= road_len/2:
        
                    car_on_intersection = False
        
                    for element in cars_2:
                        if element.position == road_len/2:
                            car_on_intersection = True
                            break
                    
                    if car_on_intersection == True:
                        vehicle_v = (road_len/2 - vehicle_pos) - 1
            
                    if car_on_intersection == False:
                        
                        turning_decision = random.randint(0,1)
                    
                        if turning_decision == 1:
                            
                            vehicle_v = vehicle_v - (road_len/2 - vehicle_pos)
                            vehicle_pos = road_len/2
                            remove_1.append(car_index_1)
                            car_pos_temp = car(vehicle_pos,vehicle_v,2)
                            cars_2.append(car_pos_temp)
                            cars_2 = sorted(cars_2)
                            
                            #finds car in new road
                            index = 0
                            for thing in cars_2:
                                if thing.position == road_len/2:
                                    break
                                index += 1
                            
                            vehicle_pos = cars_2[index].position
                            vehicle_v = cars_2[index].velocity
                            
                            if index + 1 == len(cars_2):
                                vehicle_pos_next = cars_2[0].position
                            else:
                                vehicle_pos_next = cars_2[index + 1].position
                             
                            #change velocity once again wrt to road 2
                            vehicle_v = acceleration(vehicle_v, vehicle_pos_next, vehicle_pos, v_max, road_len)
                            vehicle_v = random_deccel(vehicle_v)
                            vehicle_v = deceleration(vehicle_v, vehicle_pos_next, vehicle_pos, v_max, road_len)
                            
                            #move
                            vehicle_pos = vehicle_pos + vehicle_v
                            cars_2[index].position = vehicle_pos
                            cars_2[index].velocity = vehicle_v
        
            #else just move
            if turning_decision == 0:
                if (vehicle_pos + vehicle_v) >= road_len:
                    past_cars += 1
                vehicle_pos = (vehicle_pos + vehicle_v)%road_len
                cars_1[car_index_1].position = vehicle_pos
                cars_1[car_index_1].velocity = vehicle_v
    
        for element in remove_1:
            cars_1.pop(element)
    
        #move cars on 2nd road
        remove_2 = list()
        
        for car_index_2 in range(len(cars_2)):
            #sets the velocity, position and next position of cars
            vehicle_pos = cars_2[car_index_2].position
            vehicle_v = cars_2[car_index_2].velocity
            if car_index_2 + 1 == len(cars_2):
                vehicle_pos_next = cars_2[0].position
            else:
                vehicle_pos_next = cars_2[car_index_2 + 1].position
        
            #move vehicles
            vehicle_v = acceleration(vehicle_v, vehicle_pos_next, vehicle_pos, v_max, road_len)
            vehicle_v = random_deccel(vehicle_v)
            vehicle_v = deceleration(vehicle_v, vehicle_pos_next, vehicle_pos, v_max, road_len)
            
            turning_decision = 0
            
            if vehicle_pos < road_len/2:
                if vehicle_pos + vehicle_v >= road_len/2:
        
                    car_on_intersection = False
        
                    for element in cars_1:
                        if element.position == road_len/2:
                            car_on_intersection = True
                            break
                    
                    if car_on_intersection == True:
                        vehicle_v = (road_len/2 - vehicle_pos) - 1
            
                    if car_on_intersection == False:
                        
                        turning_decision = random.randint(0,1)
                    
                        if turning_decision == 1:
                            
                            vehicle_v = vehicle_v - (road_len/2 - vehicle_pos)
                            vehicle_pos = road_len/2
                            remove_2.append(car_index_2)
                            car_pos_temp = car(vehicle_pos,vehicle_v,2)
                            cars_1.append(car_pos_temp)
                            cars_1 = sorted(cars_1)
                            
                            #finds car in new road
                            index = 0
                            for thing in cars_1:
                                if thing.position == road_len/2:
                                    break
                                index += 1
                            
                            vehicle_pos = cars_1[index].position
                            vehicle_v = cars_1[index].velocity
                            
                            if index + 1 == len(cars_1):
                                vehicle_pos_next = cars_1[0].position
                            else:
                                vehicle_pos_next = cars_1[index + 1].position
                             
                            #change velocity once again wrt to road 1
                            vehicle_v = acceleration(vehicle_v, vehicle_pos_next, vehicle_pos, v_max, road_len)
                            vehicle_v = random_deccel(vehicle_v)
                            vehicle_v = deceleration(vehicle_v, vehicle_pos_next, vehicle_pos, v_max, road_len)
                            
                            #move
                            vehicle_pos = vehicle_pos + vehicle_v
                            cars_1[index].position = vehicle_pos
                            cars_1[index].velocity = vehicle_v
    
            if turning_decision == 0:
                if (vehicle_pos + vehicle_v) >= road_len:
                    past_cars += 1
                vehicle_pos = (vehicle_pos + vehicle_v)%road_len
                cars_2[car_index_2].position = vehicle_pos
                cars_2[car_index_2].velocity = vehicle_v
    
        for element in remove_2:
            cars_2.pop(element)
        
        t += 1
     
    flow_rate = past_cars/t_max
    car_density = car_num/(road_len*2)
    
    return flow_rate,car_density