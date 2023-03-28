import random
import time
import os


ticks_all_day = 300
hunger_decrease_per_tick = 0.7
hunger_decrease_per_tick_sleep_time = 0.3
energy_decrease_per_tick = 0.5
get_energy_from_sleep = 1
get_energy_from_food = 1 + energy_decrease_per_tick
get_hunger_from_food = 10 + hunger_decrease_per_tick

stats = {"idle": 0, "sleeping": 1, "eating": 2}


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

    def eat(self):
        self.status = stats["eating"]
        self.time_for_change_status = 10  # TODO : not hardcode

    def sleep(self):
        self.status = stats["sleeping"]
        self.time_for_change_status = 100  # TODO : not hardcode

    def idle(self):
        self.status = stats["idle"]
        self.time_for_change_status = 0

    def decrease_hunger(self):
        if self.hunger >= 0:
            self.hunger -= hunger_decrease_per_tick
        else:
            self.hunger = 0
            # TODO: not hardcode
            self.decrease_energy(3*energy_decrease_per_tick)

    def decrease_hunger_when_sleep(self):
        if self.hunger <= 20:
            self.idle()
        else:
            self.hunger -= hunger_decrease_per_tick_sleep_time

    def decrease_energy(self, n=energy_decrease_per_tick):
        if self.energy - energy_decrease_per_tick <= 0:
            # TODO: decrease helth
            self.energy = 0
        else:
            self.energy -= n

    def increase_hunger(self):
        if self.hunger + get_hunger_from_food >= self.max_hunger:
            self.hunger = self.max_hunger
            self.idle()
        else:
            self.hunger += get_hunger_from_food

    def increase_energy_from_sleep(self):
        if self.energy + get_energy_from_sleep >= self.max_energy:
            self.energy = self.max_energy
        else:
            self.energy += get_energy_from_sleep

    def increase_energy_from_food(self):
        if self.energy + get_energy_from_food >= self.max_energy:
            self.energy = self.max_energy
        else:
            self.energy += get_energy_from_food

    def decrease_status_time(self):
        self.time_for_change_status -= 1

    def __str__(self):
        return f"Status: {self.status}\nTime for change status:{self.time_for_change_status}\nHonger: {round(self.hunger , 2 )}\nEnergy: {round(self.energy , 2)}\nHealth: {self.health}"


npc1 = NPC()
NPCs = [npc1]


def main():
    # check status
    for npc in NPCs:
        # TODO: helth check and increase
        if npc.status != 0 and npc.time_for_change_status != 0:
            npc.decrease_status_time()
            if npc.time_for_change_status == 0:
                npc.idle()

        if npc.status == 1:  # sleeping
            npc.decrease_hunger_when_sleep()
            npc.increase_energy_from_sleep()
        else:
            npc.decrease_hunger()
            npc.decrease_energy()
            if npc.status == 2:  # eating
                npc.increase_energy_from_food()
                npc.increase_hunger()
            elif npc.status == 0:  # idle
                if npc.hunger < 20:  # TODO: not hardcode
                    npc.eat()
                elif npc.energy < 20:  # TODO: not hardcode
                    npc.sleep()


while 1:
    for tick in range(ticks_all_day):
        time.sleep(0.1)
        os.system("clear")
        print(npc1)
        main()
# TODO round
