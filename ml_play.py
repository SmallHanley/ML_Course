# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 04:31:09 2020

@author: Dining
"""
import pickle
import numpy as np
from os import path
import os 

class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0 #initialization
        self.car_pos = (0,0)
        self.feature = [0,0,0,0,0,0,0,0,0]
        
        with open(path.join(path.dirname(__file__), 'save', 'model.pickle'), 'rb') as file: self.model = pickle.load(file)
        pass
    
    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        def check_grid():
            self.car_pos = scene_info[self.player]
            if scene_info["status"] != "ALIVE":
                return "RESET"
        
            if len(self.car_pos) == 0:
                self.car_pos = (0,0)

            grid = set()
            for i in range(len(scene_info["cars_info"])): # for all cars information in scene of one frame
                car = scene_info["cars_info"][i]
                if car["id"]==self.player_no: #player's car information
                    self.car_vel = car["velocity"] 
                else: # computer's cars information
                    if self.car_pos[0] <= 65: # left bound 
                        grid.add(1)
                        grid.add(4)
                        grid.add(7)
                    elif self.car_pos[0] >= 565: # right bound
                        grid.add(3)
                        grid.add(6)
                        grid.add(9)

                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position

                    if x <= 40 and x >= -40 :      
                        if y > 0 and y < 300:
                            grid.add(2)
                            if y < 200:
                                grid.add(5) 
                        elif y < 0 and y > -200:
                            grid.add(8)
                    if x > -100 and x < -40 :
                        if y > 80 and y < 250:
                            grid.add(3)
                        elif y < -80 and y > -200:
                            grid.add(9)
                        elif y < 80 and y > -80:
                            grid.add(6)
                    if x < 100 and x > 40:
                        if y > 80 and y < 250:
                            grid.add(1)
                        elif y < -80 and y > -200:
                            grid.add(7)
                        elif y < 80 and y > -80:
                            grid.add(4)
#            print(grid)
            return move(grid = grid)
        
        def move(grid):

            grid_tolist = list(grid)
            grid_data = [0,0,0,0,0,0,0,0,0]
            for i in grid_tolist:
                grid_data[i-1] = 1 # change grid set into feature's data shape
            grid_data = np.array(grid_data).reshape(1,-1)
            self.feature = grid_data
            self.feature = np.array(self.feature)
            self.feature = self.feature.reshape((1,-1))
            y = self.model.predict(self.feature) 

            if y == 0:
                return ["SPEED"]
            if y == 1:
                return ["SPEED", "MOVE_LEFT"]
            if y == 2:
                return ["SPEED", "MOVE_RIGHT"]
            if y == 3:
                return ["BRAKE"]
            if y == 4:
                return ["BRAKE", "MOVE_LEFT"]
            if y == 5:
                return ["BRAKE", "MOVE_RIGHT"]
            if y == 6:
                return ["LEFT"]
            if y == 7:
                return ["RIGHT"]
        
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass
