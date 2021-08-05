import sys
import random
import pygame as pg
import pygame.gfxdraw
from pygame_widgets.toggle import Toggle
from pygame_widgets.textbox import TextBox
from pygame_widgets.slider import Slider

from boid import Boid
from edible import Edible

def main():
    rootWidth = 800
    rootHeight = 600
    
    # Size of the simulation area
    # 100 pixels for the controls
    gameWidth = 800
    gameHeight = 550
    
    foodCount = 30
    poisonCount = 10
    foodRadius = 3
    poisonRadius = 3
    boidCount = 10
    boidRadius = 8
    
    # Distance from edge of simulation
    # Forces boids to go back in the boundaries of the simulation
    boundaryDistance = 40
    
    screen = pg.display.set_mode((rootWidth, rootHeight))
    clock = pg.time.Clock()
    
    pg.display.set_caption('Evolutionary Boids - Inspired by Professor Daniel Shiffman - Created By Preston Tang in July 2021')
    
    # Initializing the UI
    slider = Slider(screen, 120, 545, 100, 20, min=1, max=3, step=1, initial=1)
    output = TextBox(screen, 10, 545, 90, 20, fontSize=18, borderColour=(40, 40, 40))
    toggle = Toggle(screen, 360, 545, 20, 20)
    debug = TextBox(screen, 250, 545, 90, 20, fontSize=18, borderColour=(40, 40, 40))
    
    done = False
    
    boids = []
    foods = []
    poisons = []
    
    # Initializing the food, poison, and boids
    for i in range(foodCount):
        x = random.randint(foodRadius + boundaryDistance, gameWidth - (foodRadius + boundaryDistance))
        y = random.randint(foodRadius + boundaryDistance, gameHeight - (foodRadius + boundaryDistance))
        foods.append(Edible(x, y, foodRadius))
        
    for i in range(poisonCount):
        x = random.randint(poisonRadius + boundaryDistance, gameWidth - (poisonRadius + boundaryDistance))
        y = random.randint(poisonRadius + boundaryDistance, gameHeight - (poisonRadius + boundaryDistance))
        poisons.append(Edible(x, y, poisonRadius))
    
    for i in range(boidCount):
        x = random.randint(boidRadius, gameWidth - boidRadius)
        y = random.randint(boidRadius, gameHeight - boidRadius)
        
        boids.append(Boid(x, y, boidRadius, gameWidth, gameHeight))
        
    # Game loop
    while not done:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                done = True
                
        # Spawns in food
        if random.random() <= 0.08:
            x = random.randint(foodRadius + boundaryDistance, gameWidth - (foodRadius + boundaryDistance))
            y = random.randint(foodRadius + boundaryDistance, gameHeight - (foodRadius + boundaryDistance))
            foods.append(Edible(x, y, foodRadius))
            
        # Spawns in poison
        if len(poisons) < poisonCount or (random.random() <= 0.01 and len(poisons) < poisonCount * 2):
            x = random.randint(poisonRadius + boundaryDistance, gameWidth - (poisonRadius + boundaryDistance))
            y = random.randint(poisonRadius + boundaryDistance, gameHeight - (poisonRadius + boundaryDistance))
            poisons.append(Edible(x, y, poisonRadius))
        
        # Moving the boids
        for boid in boids[:]:
            boid.boundaries(boundaryDistance)
            boid.behaviors(foods, poisons, boids)
            boid.update()
            
            boid.health -= 0.002
            
            # It's dead so remove
            if boid.health < 0:
                boids.remove(boid)
                
                # Also add a piece of food where it died
                # Helps with evolution also it makes logical sense
                x = boid.position.x
                y = boid.position.y
                foods.append(Edible(x, y, foodRadius))
                
        # X% chance of boids cloning
        # for boid in boids[:]:
        #     if random.random() <= 0.001 and len(boids) < boidCount * 3:
        #         boids.append(boid.clone())
                
        # Clone if health > 80%
        for boid in boids[:]:
            if boid.health >= 0.8:
                # Asexual reproduction uses energy
                boid.health /= 2
                boids.append(boid.clone())
                
        # Repopulate world if everyone died (Essentially a reset)
        if len(boids) == 0:
            for i in range(boidCount):
                x = random.randint(boidRadius, gameWidth - boidRadius)
                y = random.randint(boidRadius, gameHeight - boidRadius)
                boids.append(Boid(x, y, boidRadius, gameWidth, gameHeight))
                
        # Technically also resets the screen
        screen.fill((40, 40, 40))
        
        # Drawing the UI elements
        slider.listen(events)
        slider.draw()
        
        toggle.listen(events)
        toggle.draw()

        output.setText("Speed: " + str(slider.getValue()) + "x")
        output.draw()
        
        debug.setText("Debug: " + str(toggle.getValue()))
        debug.draw()
        
        # Drawing the boids
        for boid in boids:
            # pg.draw.circle(screen, (pg.Color(255, 0, 0).lerp((0, 255, 0), boid.health)), boid.position, boid.r)
            pg.gfxdraw.aapolygon(screen, boid.points, (pg.Color(255, 0, 0).lerp((0, 255, 0), boid.health)))
            pg.gfxdraw.filled_polygon(screen, boid.points, (pg.Color(255, 0, 0).lerp((0, 255, 0), boid.health)))
            
            # Debugging shapes
            if toggle.getValue() == True:
                pg.gfxdraw.aacircle(screen, round(boid.position.x), round(boid.position.y), round(boid.dna[4]), (0, 255, 0))
                pg.gfxdraw.circle(screen, round(boid.position.x), round(boid.position.y), round(boid.dna[4]), (0, 255, 0))
                
                pg.gfxdraw.aacircle(screen, round(boid.position.x), round(boid.position.y), round(boid.dna[5]), (255, 0, 0))
                pg.gfxdraw.circle(screen, round(boid.position.x), round(boid.position.y), round(boid.dna[5]), (255, 0, 0))
                
                pg.gfxdraw.aacircle(screen, round(boid.position.x), round(boid.position.y), round(boid.dna[6]), (255, 255, 255))
                pg.gfxdraw.circle(screen, round(boid.position.x), round(boid.position.y), round(boid.dna[6]), (255, 255, 255))
        
        # Drawing the food
        for food in foods:
            pg.draw.circle(screen, ((0, 255, 0)), food.position, food.r)
            
        # Drawing the poison
        for poison in poisons:
            pg.draw.circle(screen, ((255, 0, 0)), poison.position, poison.r)
            
        # Draw the border
        pg.draw.rect(screen, (80, 80, 80), 
                     pg.Rect(boundaryDistance, boundaryDistance
                             , gameWidth - boundaryDistance * 2,
                             gameHeight - boundaryDistance * 2), 2)

        # Runs at 60 fps * slider value
        pg.display.update()
        clock.tick(60 * slider.getValue())


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()