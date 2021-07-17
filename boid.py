import pygame as pg
import math
import random

class Boid():
    
    def __init__(self, x, y, r, rootWidth, rootHeight, dna=None):
        # Handles the physics logic
        self.acceleration = pg.Vector2(0, 0);
        self.velocity = pg.Vector2(0, -2);
        self.r = r;
        self.maxforce = 0.1;
        self.position = pg.Vector2(x, y)
        self.health = 0.6
        
        self.rootWidth = rootWidth
        self.rootHeight = rootHeight
        # Points of the triangle, later scaled and translated to proper location
        self.points = ((-0.5, -0.866), (-0.5, 0.866), (2.0, 0.0))
        
        self.dna = []
        
        if dna == None:
            # Genetics
            # Max Speed
            self.dna.append(random.uniform(0.5, 3.0))
            self.maxspeed = self.dna[0]
            # Food Force
            self.dna.append(random.uniform(-2, 2))
            # Poison Force
            self.dna.append(random.uniform(-2, 2))
            # Boid Force
            self.dna.append(random.uniform(-2, 0))
            # Food Perception Radius
            self.dna.append(random.uniform(self.maxspeed * 2, 100))
            # Poison Perception Radius
            self.dna.append(random.uniform(self.maxspeed * 2, 100))
            # Boid Perception Radius
            self.dna.append(random.uniform(self.maxspeed * 2, 100))
        else:
            # Slightly mutate the dna that is received
            self.dna.append(self.mutate(dna[0], 0.50, 0.5, 0.5, 3))
            self.maxspeed = dna[0]
            self.dna.append(self.mutate(dna[1], 0.10, 0.25, -2, 2))
            self.dna.append(self.mutate(dna[2], 0.10, 0.25, -2, 2))
            self.dna.append(self.mutate(dna[3], 0.10, 0.25, -2, 0))
            # self.dna.append(-2)
            self.dna.append(self.mutate(dna[4], 0.10, 20, self.maxspeed * 2, 100))
            self.dna.append(self.mutate(dna[5], 0.10, 20, self.maxspeed * 2, 100))
            self.dna.append(self.mutate(dna[6], 0.10, 20, self.maxspeed * 2, 100))
        
    # Mutates a gene and makes sure it doesn't go below or above min/max value
    def mutate(self, current, rate, amount, minValue, maxValue):
        if random.random() < rate:
            current += random.uniform(-amount, amount)
        
        if current < minValue:
            current = minValue
        
        if current > maxValue:
            current = maxValue
            
        return current
            
    
    def clone(self):
        return Boid(self.position.x, self.position.y, self.r, self.rootWidth, self.rootHeight, self.dna)
        
    # Update location
    def update(self):
        self.points = ((-0.5, -0.866), (-0.5, 0.866), (2.0, 0.0))
        # Update velocity
        self.velocity += self.acceleration
        
        #  Limit speed
        if self.velocity.magnitude() > self.maxspeed:
            self.velocity = self.velocity.normalize() * self.maxspeed
            
        self.points = self.rotate_triangle(self.position, self.r, (self.velocity + self.position))
            
        self.position += self.velocity
        
        # Reset acceleration to 0 each cycle
        self.acceleration *= 0
        
    def applyForce(self, force):
        self.acceleration += force;
        
    # Handles the 3 main steering factors for boids
    def behaviors(self, foods, poisons, boids):        
        foodSteer = self.eat(foods, 0.2)
        poisonSteer = self.eat(poisons, -0.5)
        boidSteer = self.eat(boids, 0.0)
        
        foodSteer *= self.dna[1]
        poisonSteer *= self.dna[2]
        boidSteer *= self.dna[3]
        
        self.applyForce(foodSteer)
        self.applyForce(poisonSteer)
        self.applyForce(boidSteer)
        
    # A method that calculates a steering force towards a target
    # steer = desired minus velocity
    def seek(self, target):        
        desired = target.position - self.position # A vector pointing from the location to the target

        # Scale to maximum speed
        if desired.x != 0 and desired.y != 0:
            desired = desired.normalize() * self.maxspeed;
    
        # Steering = Desired minus velocity
        steer = desired - self.velocity;
        
        # Limit to maximum steering force
        if steer.magnitude() > self.maxforce and steer.x != 0 and steer.y != 0:
            steer = steer.normalize() * self.maxforce
    
        return steer
        
    # Distance formula implementation
    def distance(self, ax, ay, bx, by):
        return math.sqrt(((bx - ax)**2) + ((by - ay)**2))
        
    # Sorts by closest, does the eating as well
    def eat(self, edibles, weight):
        record = math.inf
        closest = None
        for i in range(len(edibles)):
            d = self.distance(self.position.x, self.position.y, edibles[i].position[0], edibles[i].position[1])
            
            # Not combining the if statements so it's clearer to read
            if d < record:
                # If you're a food and you're within the detection range
                if weight > 0 and d < self.dna[4]:
                    closest = edibles[i]
                    record = d
                
                # If you're a poison and you're within the detection range
                if weight < 0 and d < self.dna[5]:
                    closest = edibles[i]
                    record = d
                    
                # If you're a boid and you're within the detection range
                # And you're not me
                if weight == 0 and d < self.dna[6] and edibles[i] != self:
                    closest = edibles[i]
                    record = d
                
        if record < self.r and weight != 0:
            edibles.remove(closest)
            self.health += weight
            
            if self.health > 1:
                self.health = 1
                
        if closest != None:
            return self.seek(closest)
        else:
            return pg.Vector2(0, 0)
        
    # Function provided by Daniel Shiffman in JavaScript
    # Makes boids who go out of bounds go back in bounds
    def boundaries(self, d):
        desired = None

        if self.position.x < d:
            desired = pg.Vector2(self.maxspeed, self.velocity.y)
        elif self.position.x > self.rootWidth - d:
            desired = pg.Vector2(-self.maxspeed, self.velocity.y)

        if self.position.y < d:
            desired = pg.Vector2(self.velocity.x, self.maxspeed)
        elif self.position.y > self.rootHeight - d:
            desired = pg.Vector2(self.velocity.x, -self.maxspeed)

        if desired != None:
            desired = desired.normalize() * self.maxspeed
            steer = desired - self.velocity
            
            if steer.magnitude() > self.maxforce:
                steer = steer.normalize() * self.maxforce
            self.applyForce(steer);
        
    # Taken from StackOverFlow, calculates the rotation of a triangle
    # using rotation matrices
    def rotate_triangle(self, center, scale, mouse_pos):
        dx = mouse_pos[0] - center[0]
        dy = mouse_pos[1] - center[1]
        len = math.sqrt(dx*dx + dy*dy)
        dx, dy = (dx*scale/len, dy*scale/len) if len > 0 else (1, 0)
    
        pts = [(-0.5, -0.866), (-0.5, 0.866), (2.0, 0.0)]
        pts = [(center[0] + p[0]*dx + p[1]*dy, center[1] + p[0]*dy - p[1]*dx) for p in self.points]
        return pts
            