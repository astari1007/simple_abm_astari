#ASTARI RAIHANAH

#LAB 9b - Data and Programming for Public Policy I (Python Track)
#9b assignment:
#Create your own github repo
#Add a .py file
#Create a simple version of an agent based simulation, based on the code in the last lecture, and the github repo linked at the end
#1. Create an Agent class
#2. Create a World class
#3. Initialize the world
#4. Create a loop
#Ask each agent in sequence to find an empty patch
#Move the agent to the empty patch
#5. End
#Keep it simple (small grid, small number of agents, small number of loops), and utilize the code from the more complex example given in lecture.

# Part 1: Create an 'Agent' Class
class Agent:
    def __init__(self, id, x, y, color, same_preference):
        self.id = id
        self.x = x
        self.y = y
        self.color = color
        self.same_preference = same_preference

    def move(self, world):
        if not self.am_i_happy(world):
            new_x, new_y = world.find_vacant()
            if new_x is not None and new_y is not None:
                world.grid[self.y][self.x] = None
                self.x = new_x
                self.y = new_y
                world.grid[new_y][new_x] = self

    def am_i_happy(self, world):
        neighbors = self.locate_neighbors(world)
        same_count = sum(1 for neighbor in neighbors if neighbor and neighbor.color == self.color)
        return same_count >= self.same_preference

    def locate_neighbors(self, world):
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < world.width and 0 <= ny < world.height:
                    neighbors.append(world.grid[ny][nx])
        return neighbors


# Part 2: Create a 'World' Class
import random
import matplotlib.pyplot as plt
import numpy as np

class World:
    def __init__(self, width, height, num_agents, same_preference):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.agents = []
        self.same_preference = same_preference
        self.init_world(num_agents)

    def build_grid(self):
        return [[None for _ in range(self.width)] for _ in range(self.height)]

    def build_agents(self, num_agents):
        for i in range(num_agents):
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if self.grid[y][x] is None:
                    color = random.choice(['red', 'blue'])
                    agent = Agent(i, x, y, color, self.same_preference)
                    self.grid[y][x] = agent
                    self.agents.append(agent)
                    break

    def init_world(self, num_agents):
        self.grid = self.build_grid()
        self.build_agents(num_agents)

    def find_vacant(self):
        empty_patches = [(x, y) for x in range(self.width) for y in range(self.height) if self.grid[y][x] is None]
        return random.choice(empty_patches) if empty_patches else (None, None)

    def report_integration(self):
        self.display()

    def display(self):
        grid_colors = np.full((self.height, self.width), -1)
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x]:
                    grid_colors[y][x] = 1 if self.grid[y][x].color == 'red' else 0

        plt.imshow(grid_colors, cmap='bwr', interpolation='nearest')
        plt.title("Schelling Model")
        plt.show()

    def run(self):
        num_steps = 10
        for step in range(num_steps):
            for agent in self.agents:
                agent.move(self)
            self.report_integration()

# Part 3: Execute the Simulation
def main():
    width = 10
    height = 10
    num_agents = 25
    same_preference = 3

    world = World(width, height, num_agents, same_preference)
    world.run()

if __name__ == "__main__":
    main()
