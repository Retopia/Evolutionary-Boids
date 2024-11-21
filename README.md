# Evolutionary-Boids
![Project View](https://i.imgur.com/NT5HmgM.png)
This is my first major project in Python and was inspired by the work of Professor Daniel Shiffman.
The graphics of this project is done with Pygame, and the UI elements are done using [Pygame_gui](https://github.com/MyreMylar/pygame_gui)

## Project Explanation

This project uses Genetic Algorithms in order to evolve the boids to become better at surviving in their environment, the genes every boid has are:
1. The maximum speed of the Boid (0.5, 3)
2. Attraction/Repulsion towards food (-2, 2)
3. Attraction/Repulsion towards poison (-2, 2)
4. Attraction/Repulsion towards another Boid (-2, 0)
5. Perception radius towards food (maximum speed * 2, 100)
6. Perception radius towards poison (maximum speed * 2, 100)
7. Perception radius towards another Boid (maximum speed * 2, 100)

This project relies heavily on the theory of Steering Force developed by Craig Reynolds in his research paper on boids. Essentially, there are 3 main steering forces (for food, poison, and towards another boid) and they are added onto the boid after being multiplied by their respective DNA value (genes 2, 3, and 4). The use of Genetic Algorithm helps fine-tune the values. For example, a boid sees a food right next to a poison. If its repulsion towards the poison is too high, it will not be able to reach the food. If it is attracted to the poison, it will simply die after eating it.

![Debug View](https://i.imgur.com/BCLZJf2.png)

The debug function of the program draws 3 circles, with the green representing the food perception radius, the red representing the poison perception radius, and the white representing the perception radius towards another boid.

I might come back to this project in the future to make all of the DNA ranges and values customizable.

## Installing the Required Dependencies (Requires Python 3):
`pip install pygame`  
`pip install pygame_gui`  

To run the program, simply download the project files into a folder after installing the required dependencies.
Then run `python main.py`
