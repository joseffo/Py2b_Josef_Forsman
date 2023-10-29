# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 17:40:54 2023

@author: JFORSMAN
"""

import numpy as np
import random

class Person:
    def __init__(self):
        self.recover_prob = 0.2
        self.die_prob = 0.05
        self.init_sick_prob = 0.1
        self.recovered = False
        self.dead = False
        self.sick = False
        self.infect_others_prob = 0.05
        self.average_meetups = 10
        self.days_sick = 0
        self.vaccinated = False
        
        self.init_sick_or_not()
        
    def init_sick_or_not(self):
        """When created each person starts as either sick or healthy"""
        prob = random.random()
        if prob <= self.init_sick_prob:
            # This should yield that about 10% of the people created are sick, the rest healthy
            self.sick = True
        else:
            self.sick = False
    
    def day_passes(self, population, init_scenario):
        """This method describes what happends to each person each day"""
        
        # If the person is sick it might infect others
        if self.sick == True:
            self.days_sick += 1
            if init_scenario == False:
                self.infect_others(population)
        
        # Will person recover?
        prob = random.random()
        if prob <= self.recover_prob and self.sick == True:
            # Person has rehabilitated and is now healthy!
            self.sick = False
            self.recovered = True 
        
        # If person is still sick they might die
        prob = random.random()
        if prob <= self.die_prob and self.sick == True:
            self.dead = True
            self.sick = False

    def infect_others(self, population):
        person_encounters = []
        person_encounters = random.sample(range(population.size), self.average_meetups)
        for person_id in person_encounters:
            prob_infect = random.random()
            # \ can be used to continnue on next row
            if self.infect_others_prob >= prob_infect and \
                population[person_id].dead != True and \
                population[person_id].recovered !=True and \
                population[person_id].vaccinated == False:
                    
                population[person_id].sick = True

class Village:
    def __init__(self, init_population_size):
        self.population = np.empty(init_population_size, Person)
        self.generate_inhabitants()
        self.init_vaccination = 0.2*init_population_size
        self.vaccination_started = False
        self.daily_vaccination_threshold = 0.04*init_population_size
    
    def generate_inhabitants(self):
        """Generates the population"""
        for i in range(self.population.size):
            self.population[i] = Person()
        
    def advance_days(self, init_scenario = False):
        """Counts the status of the citizens in the community"""
        people_sick = 0
        people_recovered = 0
        people_dead = 0
        people_vaccinated = 0
        for person in self.population:# Looping over all persons and summing up number of _sick, _recovered and _dead
            if person.sick == True:
                people_sick += 1
            elif person.recovered == True:
                people_recovered += 1
            elif person.dead == True:
                people_dead += 1
            elif person.vaccinated == True:
                people_vaccinated += 1
            
            person.day_passes(self.population, init_scenario)
        if people_sick >= self.init_vaccination and self.vaccination_started == False:
            self.vaccination_started = True
            print(f"At the end of the day {people_sick} have become sick and a vaccination process has been initiated!")
        if self.vaccination_started == True:
            self.vaccinate_population()
        

        return people_sick, people_recovered, people_dead, people_vaccinated
    
    def vaccinate_population(self):
        people_vaccinated_today = 0
        for person in self.population:# Looping over all persons and vaccinating until threshold is reached
            if people_vaccinated_today == self.daily_vaccination_threshold:# might not always happen (if much of the population is vaccinated already)
                #print(f"Today {people_vaccinated_today} were vaccinated")
                break
            elif person.dead == False and person.sick == False and person.vaccinated == False:
                person.vaccinated = True#self.population[person].vaccinated = True - No! person is not a number in a list
                people_vaccinated_today += 1
                
        
        pass
    
    def start_simulation(self):
        """This function controls the simulation and what happends in a day"""
        current_day = 0
        people_sick, people_recovered, people_dead, people_vaccinated = self.advance_days(init_scenario = True)
        while people_sick != 0:
            print(f"By day {current_day} {people_sick} people are sick, {people_dead} are dead, {people_recovered} has recovered and {people_vaccinated} has been vaccinated")
            current_day += 1
            people_sick, people_recovered, people_dead, people_vaccinated = self.advance_days()
        
        population_sickdays = [x.days_sick for x in self.population] #list of every persons number of sickdays
        people_unaffected = self.population.size - (people_sick + people_recovered + people_dead)
        print(f"\nBy day {current_day} {people_sick} people are sick, {people_dead} are dead and {people_recovered} has recovered. {people_unaffected} people were never in contact with the virus")
        print("The village has recovered and the virus is eliminated!")
        print(f"The longest time an individual was sick is: {max(population_sickdays)} days")

        
def main():
    pop_size = 1000
    village = Village(pop_size)
    village.start_simulation()

main()