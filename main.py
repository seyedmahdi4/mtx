import random
import time
import os
import math


ticks_all_day = 300
hunger_decrease_per_tick = 0.7
hunger_decrease_per_tick_sleep_time = 0.3
energy_decrease_per_tick = 0.5
get_energy_from_sleep = 1
get_energy_from_food = 1 + energy_decrease_per_tick
get_hunger_from_food = 10 + hunger_decrease_per_tick
time_for_eat = 10
sleep_time = 100
hunger_triger = 30
sleep_triger = 20


stats = {"idle": 0, "sleeping": 1, "eating": 2, "moving": 3}


def gen_map(x=10, y=10):
    world = []
    for i in range(x):
        a = []
        for j in range(y):
            a.append(".")
        world.append(a)
    return world


world = gen_map()

shop1 = [random.randint(0, 10), random.randint(0, 10)]
world[shop1[0]][shop1[1]] = "x"


class NPC:
    def __init__(self):
        #self.name = name
        self.health = 100
        self.max_health = 100  # TODO randomized
        self.energy = 100
        self.max_energy = 100  # TODO randomized
        self.hunger = 100
        self.max_hunger = 100  # TODO randomized
        self.status = stats["idle"]
        self.time_for_change_status = 0
        #TODO: not hardcode
        self.x = 1
        self.y = 1
        self.home = [1, 1]
        self.destination = None

    def eat(self):
        if self.x == shop1[0] and self.y == shop1[1]:
            self.status = stats["eating"]
            self.time_for_change_status = time_for_eat
        else:
            self.move_to(shop1)

    def sleep(self):
        if self.x == self.home[0] and self.y == self.home[1]:
            self.status = stats["sleeping"]
            self.time_for_change_status = sleep_time
        else:
            self.move_to(self.home)

    def move_to(self, xy):
        self.status = stats["moving"]
        self.destination = xy

    def idle(self):
        self.status = stats["idle"]
        self.time_for_change_status = 0

    def decrease_hunger(self):
        if self.hunger >= 0:
            self.hunger -= hunger_decrease_per_tick
        else:
            self.hunger = 0
            self.decrease_energy(3*energy_decrease_per_tick)

    def decrease_hunger_when_sleep(self):
        if self.hunger <= 20:  # TODO: not hardcode
            self.idle()
        else:
            self.hunger -= hunger_decrease_per_tick_sleep_time

    def decrease_energy(self, n=1):
        if self.energy - n * energy_decrease_per_tick <= 0:
            # TODO: decrease helth
            self.energy = 0
        else:
            self.energy -= n * energy_decrease_per_tick

    def increase_hunger(self):
        if self.hunger + get_hunger_from_food >= self.max_hunger:
            self.hunger = self.max_hunger
            if self.energy == self.max_energy:
                self.idle()
        else:
            self.hunger += get_hunger_from_food

    def increase_energy_from_sleep(self):
        if self.energy + get_energy_from_sleep >= self.max_energy:
            self.energy = self.max_energy
            self.idle()
        else:
            self.energy += get_energy_from_sleep

    def increase_energy_from_food(self):
        if self.energy + get_energy_from_food >= self.max_energy:
            self.energy = self.max_energy
            if self.hunger == self.max_hunger:
                self.idle()
        else:
            self.energy += get_energy_from_food

    def decrease_status_time(self):
        self.time_for_change_status -= 1
        if self.time_for_change_status == 0:
            self.idle()

    # def distance_to(self, other_x, other_y):
    #     dx = other_x - self.x
    #     dy = other_y - self.y
    #     distance = math.sqrt(dx**2 + dy**2)
    #     return distance
    # √(x^2 + y^2)

    def move(self):
        target_x, target_y = self.destination
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1
        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1

        if self.x == target_x and self.y == target_y:
            self.idle()

    def __str__(self):
        return f"Status: {self.status}\n\nX: {self.x}\nY: {self.y}\nTarget: {self.destination}\nTime for change status:{self.time_for_change_status}\nHonger: {round(self.hunger , 2 )}\nEnergy: {round(self.energy , 2)}\nHealth: {self.health}"


npc1 = NPC()
NPCs = [npc1]


def main():
    # check status
    for npc in NPCs:
        # TODO: helth check and increase

        if npc.status == 1:  # sleeping
            npc.decrease_status_time()
            npc.increase_energy_from_sleep()
            npc.decrease_hunger_when_sleep()
        else:
            npc.decrease_hunger()
            npc.decrease_energy()
            if npc.status == 2:  # eating
                npc.decrease_status_time()
                npc.increase_energy_from_food()
                npc.increase_hunger()
            elif npc.status == 3:  # moving
                npc.move()

            elif npc.status == 0:  # idle
                if npc.hunger < hunger_triger:
                    npc.eat()
                elif npc.energy < sleep_triger:
                    npc.sleep()


while 1:
    for tick in range(ticks_all_day):
        time.sleep(0.1)
        os.system("clear")
        print(npc1)
        main()