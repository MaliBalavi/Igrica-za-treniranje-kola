import pygame
import sys
import numpy as np
import random
import time
import math
import pickle
import os

class Line:
    def __init__(self, x1, y1, x2, y2):
        # Line defined by two points (x1, y1) and (x2, y2)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.turned=True
        
    def draw(self, surface,color):
        # This method would draw the line on a given surface (e.g., using Pygame)
        if self.turned:
            pygame.draw.line(surface,color, (self.x1, self.y1), (self.x2, self.y2))
    
    def is_intersecting(self, other_line):
        """Check if this line intersects with another line."""
        def ccw(A, B, C):
            """Check if the points A, B, C are counterclockwise."""
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        # Points of the two lines
        A = (self.x1, self.y1)
        B = (self.x2, self.y2)
        C = (other_line.x1, other_line.y1)
        D = (other_line.x2, other_line.y2)

        # Check if the line segments AB and CD intersect
        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


class Level:
    def __init__(self, walls,checkpoints,BACKGROUND_COLOR = ([0,0,0]), prop=(1000,1000),FPS=60,g=9.81,location=(100,100,0.5*math.pi)):
        # walls should be a list of Line objects
        self.walls = walls
        self.checkpoints=checkpoints
        self.BACKGROUND_COLOR=BACKGROUND_COLOR
        self.proportions=prop
        self.FPS=FPS
        self.g=g
        self.location=location

    def add_wall(self, x1, y1, x2, y2):
        # Adds a wall (line) to the track
        self.walls.append(Line(x1, y1, x2, y2))
        
    def draw(self, surface):
        surface.fill(self.BACKGROUND_COLOR)
        # Draw all walls of the track
        for wall in self.walls:
            wall.draw(surface,([255,255,255]))
        for checkpoint in self.checkpoints:
            checkpoint.draw(surface,([0,255,0]))
            
    def checkall(self):
        return all(not cek.turned for cek in self.checkpoints)

class Car:
    # Constructor method to initialize attributesFlevel
    def __init__(self, mass, length, width, color,pull,ni=5,location=(100,100,0.5*math.pi),k=5):
        self.mass=mass
        self.length=length
        self.width=width
        self.pull=pull
        self.ori=location[2]
        self.ni=ni
        self.bni=ni
        self.k=k
        self.ax=0
        self.ay=0
        
        self.x=location[0]
        self.y=location[1]
        
        
        self.vx=0
        self.vy=0
        self.rfx=0
        self.rfy=0
        
        self.color=color
    def tostart(self,location):
        self.x=location[0]
        self.y=location[1]
        self.ori=location[2]
    def Ori(self):
        self.ori = (self.ori + 2 * math.pi) % (2 * math.pi)
        return self.ori
    # Method to display information
    # def show(self, screen):
    #     pygame.draw.rect(screen, self.color, [self.x, self.y,self.width,self.length])
    def show(self, screen):
        cos_ori = math.cos(self.ori)
        sin_ori = math.sin(self.ori)
        half_width = self.length / 2
        half_length = self.width / 2
        corners = [
            (-half_width, -half_length),  # Top-left
            (half_width, -half_length),   # Top-right
            (half_width, half_length),    # Bottom-right
            (-half_width, half_length)    # Bottom-left
        ]
        rotated_corners = [
            (
                self.x + x * cos_ori - y * sin_ori,
                self.y + x * sin_ori + y * cos_ori
            )
            for x, y in corners
        ]
        pygame.draw.polygon(screen, self.color, rotated_corners)
            # Highlight the front of the car
        front_center_x = self.x + half_length * cos_ori
        front_center_y = self.y + half_length * sin_ori

        # Draw a small triangle at the front to indicate the car's direction
        front_triangle = [
            (
                front_center_x + half_width * 0.5 * sin_ori,
                front_center_y - half_width * 0.5 * cos_ori
            ),
            (
                front_center_x - half_width * 0.5 * sin_ori,
                front_center_y + half_width * 0.5 * cos_ori
            ),
            (
                front_center_x + half_length * 0.5 * cos_ori,
                front_center_y + half_length * 0.5 * sin_ori
            )
        ]
        pygame.draw.polygon(screen, (255, 0, 0), front_triangle)  # Red triangle for the front indicator
        



    def ac(self,FPS):
        self.ax=(self.rfx/self.mass)/FPS
        self.vx+=self.ax
        self.ay=(self.rfy/self.mass)/FPS
        self.vy+=self.ay
    def step(self,FPS):
        self.x+=self.vx/FPS
        self.y+=self.vy/FPS
    def gas(self):
        self.rfx+=self.pull*math.cos(self.ori)
        self.rfy+=self.pull*math.sin(self.ori)
    # def brake(self)
    #     self.ni=self.ni
    def friction(self,g):

        velocity_magnitude = math.sqrt(self.vx**2 + self.vy**2)

        if(velocity_magnitude!=0):
            self.rfx-=(self.mass*g)*self.ni*(self.vx/velocity_magnitude)
            self.rfy-=(self.mass*g)*self.ni*(self.vy/velocity_magnitude)
    def brake(self):
        self.ni=self.k*self.bni
    def steerleft(self):
        self.ori-=0.07
    def steerright(self):
        self.ori+=0.07
        
        
    
        
        
        
        
        
        
    def wallinter(self, lines):
        """Check if any line of the car intersects with given lines."""
        cos_ori = math.cos(self.ori)
        sin_ori = math.sin(self.ori)
        half_width = self.length / 2
        half_length = self.width / 2

        # Calculate the four corners of the car
        corners = [
            (-half_width, -half_length),  # Top-left
            (half_width, -half_length),   # Top-right
            (half_width, half_length),    # Bottom-right
            (-half_width, half_length)    # Bottom-left
        ]
        transformed_corners = [
            (
                self.x + x * cos_ori - y * sin_ori,
                self.y + x * sin_ori + y * cos_ori
            )
            for x, y in corners
        ]

        # Create car edges (lines connecting the corners)
        carlines = [
            Line(transformed_corners[i][0], transformed_corners[i][1],
                transformed_corners[(i + 1) % 4][0], transformed_corners[(i + 1) % 4][1])
            for i in range(4)
        ]

        # Check for intersections between car edges and the given lines
        for carline in carlines:
            for line in lines:
                if carline.is_intersecting(line):
                    return True

        return False
    
    def checkinter(self, lines):
        """Check if any line of the car intersects with given lines."""
        cos_ori = math.cos(self.ori)
        sin_ori = math.sin(self.ori)
        half_width = self.length / 2
        half_length = self.width / 2

        # Calculate the four corners of the car
        corners = [
            (-half_width, -half_length),  # Top-left
            (half_width, -half_length),   # Top-right
            (half_width, half_length),    # Bottom-right
            (-half_width, half_length)    # Bottom-left
        ]
        transformed_corners = [
            (
                self.x + x * cos_ori - y * sin_ori,
                self.y + x * sin_ori + y * cos_ori
            )
            for x, y in corners
        ]

        # Create car edges (lines connecting the corners)
        carlines = [
            Line(transformed_corners[i][0], transformed_corners[i][1],
                transformed_corners[(i + 1) % 4][0], transformed_corners[(i + 1) % 4][1])
            for i in range(4)
        ]

        # Check for intersections between car edges and the given lines
        for carline in carlines:
            for line in lines:
                if carline.is_intersecting(line):
                    if(line.turned):
                        line.turned=False
                        return True

        return False
    
    
        
        
