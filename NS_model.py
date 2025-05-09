# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 05:05:15 2023

@author: ASUS
"""

#import numpy as np
import random
#import matplotlib.pyplot as plt
#import time

class car:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.position < other.position


def initialize(num_cars):
    n_car = 0
    n_car_max = num_cars
    
    info = list()
    i = 0
    while n_car < n_car_max:
        thing = car(i,random.randint(1,5))
        i = i + random.randint(1,5)
        info.append(thing)
        n_car +=1
    return info

def acceleration(vehicle_v,vehicle_pos_next,vehicle_pos,v_max):
    if vehicle_v < v_max:
        if vehicle_pos_next - vehicle_pos > vehicle_v + 1:
            vehicle_v = vehicle_v + 1
            return vehicle_v
    vehicle_v = vehicle_v
    return vehicle_v

def deceleration(vehicle_v,vehicle_pos_next,vehicle_pos,v_max):
    if vehicle_pos_next - vehicle_pos <= vehicle_v:
        vehicle_v = (vehicle_pos_next - vehicle_pos) - 1
        return vehicle_v
    vehicle_v = vehicle_v
    return vehicle_v

def random_deccel(vehicle_v):
    if vehicle_v <= 1:
        return vehicle_v
    cope = random.uniform(0,1)
    if cope < 0.5:
        return vehicle_v - 1
    else:
        return vehicle_v

def flow_rate(v_max,num_cars):

    cars = initialize(num_cars)
    t = 0
    t_max = 100
    pass_cars = 0

    while t < t_max:
        list_of_car_positions = list()
        for car_index in range(len(cars)):
            #sets the velocity, position and next position of cars
            vehicle_pos = cars[car_index].position
            vehicle_v = cars[car_index].velocity
            if car_index + 1 == len(cars):
                vehicle_pos_next = cars[0].position
            else:
                vehicle_pos_next = cars[car_index + 1].position
            
            #conditions
            if vehicle_pos_next > vehicle_pos:
                vehicle_v = acceleration(vehicle_v, vehicle_pos_next, vehicle_pos,v_max)
                vehicle_v = deceleration(vehicle_v, vehicle_pos_next, vehicle_pos,v_max)
                vehicle_v = random_deccel(vehicle_v)
                vehicle_pos = vehicle_pos + vehicle_v
        
            if vehicle_pos_next < vehicle_pos:
                vehicle_v = vehicle_v + 1
                vehicle_v = random_deccel(vehicle_v)
                vehicle_pos = vehicle_pos + vehicle_v
        
            if vehicle_pos > 100:
                vehicle_pos = vehicle_pos%100
                vehicle_pos_next = cars[0].position
                if vehicle_pos_next > vehicle_pos:
                    vehicle_pos = vehicle_pos
                    pass_cars +=1
                if vehicle_pos_next < vehicle_pos:
                    vehicle_pos = 101
                cars[car_index].position = vehicle_pos
                cars[car_index].velocity = vehicle_v
                list_of_car_positions.append(vehicle_pos)
            else:
                cars[car_index].position = vehicle_pos
                cars[car_index].velocity = vehicle_v
                list_of_car_positions.append(vehicle_pos)
        cars = sorted(cars)
        t += 1
    
    flow_rate = pass_cars/t_max
    return flow_rate
