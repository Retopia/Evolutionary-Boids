import sys
import random
import pygame_gui
import pygame as pg
import pygame.gfxdraw

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

    currentSimulSpeed = 1
    maxSimulSpeed = 4

    # Distance from edge of simulation
    # Forces boids to go back in the boundaries of the simulation
    boundaryDistance = 40

    # Variable for showing debug or not
    debug = False

    screen = pg.display.set_mode((rootWidth, rootHeight))

    # Initialize the UI Manager
    manager = pygame_gui.UIManager((rootWidth, rootHeight), "theme.json")
    clock = pg.time.Clock()

    pg.display.set_caption(
        'Evolutionary Boids - Inspired by Professor Daniel Shiffman - Created By Preston Tang in July 2021')

    # Initializing the UI
    sliderDesc = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(40, 545, 70, 28),
                                             text="Speed: 1",
                                             manager=manager)
    sliderLeft = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(10, 545, 25, 28),
                                              text="-",
                                              manager=manager)
    sliderRight = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(115, 545, 25, 28),
                                              text="+",
                                              manager=manager)
    toggleDebug = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(155, 545, 115, 28),
                                              text="Toggle Debug",
                                              manager=manager)

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
        # Required for the UI Manager
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                done = True

            # Event for UI
            if event.type == pygame.USEREVENT:
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        # Left slider button pressed
                        if event.ui_element == sliderLeft:
                            if currentSimulSpeed > 1:
                                currentSimulSpeed -= 1
                                sliderDesc.set_text("Speed: " + str(currentSimulSpeed))
                        # Right slider button pressed
                        if event.ui_element == sliderRight:
                            if currentSimulSpeed < maxSimulSpeed:
                                currentSimulSpeed += 1
                                sliderDesc.set_text("Speed: " + str(currentSimulSpeed))

                        # Toggle debug pressed
                        if event.ui_element == toggleDebug:
                            debug = not debug

            manager.process_events(event)

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

        # Updates time variable for UI and also control animation fps
        time_delta = clock.tick(60 * currentSimulSpeed) / 1000.0

        # Update UI Manager
        manager.update(time_delta)
        manager.draw_ui(screen)

        # Drawing the boids
        for boid in boids:
            # pg.draw.circle(screen, (pg.Color(255, 0, 0).lerp((0, 255, 0), boid.health)), boid.position, boid.r)
            pg.gfxdraw.aapolygon(screen, boid.points, (pg.Color(255, 0, 0).lerp((0, 255, 0), boid.health)))
            pg.gfxdraw.filled_polygon(screen, boid.points, (pg.Color(255, 0, 0).lerp((0, 255, 0), boid.health)))

            # Debugging shapes
            if debug:
                pg.gfxdraw.aacircle(screen, round(boid.position.x), round(boid.position.y), round(boid.dna[4]), (0, 255, 0))
                pg.gfxdraw.circle(screen, round(boid.position.x), round(boid.position.y), round(boid.dna[4]), (0, 255, 0))

                pg.gfxdraw.aacircle(screen, round(boid.position.x), round(boid.position.y), round(boid.dna[5]), (255, 0, 0))
                pg.gfxdraw.circle(screen, round(boid.position.x), round(boid.position.y), round(boid.dna[5]), (255, 0, 0))

                pg.gfxdraw.aacircle(screen, round(boid.position.x), round(boid.position.y), round(boid.dna[6]),
                                    (255, 255, 255))
                pg.gfxdraw.circle(screen, round(boid.position.x), round(boid.position.y), round(boid.dna[6]),
                                  (255, 255, 255))

        # Drawing the food
        for food in foods:
            pg.draw.circle(screen, (0, 255, 0), food.position, food.r)

        # Drawing the poison
        for poison in poisons:
            pg.draw.circle(screen, (255, 0, 0), poison.position, poison.r)

        # Draw the border
        pg.draw.rect(screen, (80, 80, 80),
                     pg.Rect(boundaryDistance, boundaryDistance
                             , gameWidth - boundaryDistance * 2,
                             gameHeight - boundaryDistance * 2), 2)

        # Runs at 60 fps * slider value
        pg.display.update()


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()
