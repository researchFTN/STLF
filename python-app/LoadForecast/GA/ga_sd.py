import pygad
import numpy as np
import pandas as pd
import copy
from pathlib import Path
import sys
from sklearn.metrics import mean_absolute_percentage_error
from GA import genetic_operators
from FILTER import weather_filter
from FILTER import inertial_filter
from FILTER import initial_filter
from FILTER import deviation_filter
from FILTER import distance_filter
from MODEL import day
from DATA_MANIPULATION import write_read_file, converter
from FILTER import day_light_filter
from HELPER import DST
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)

initial_filter=initial_filter.InitialFilter()
weather_filter=weather_filter.WeatherFilter()
inertial_filter=inertial_filter.InertialFilter()
deviation_filter=deviation_filter.DeviationFilter()
distance_filter=distance_filter.DistanceFilter()
day_light_filter=day_light_filter.DayLightFilter()

num_genes = 14
sol_per_pop = 128
num_generations = 100
num_parents_mating = 64
pc=[1.0,1.14,0.10]
pc_load=0.014286
pc_temp=1
pc_h=0.014286
wc=0.002738 
pc_dl=0.05
load=[]

def fitness_func(solution, solution_idx):
  
    dataSet=[x for x in write_read_file.data_copy if x.start_date<F_day.start_date and x.part==F_day.part]
    data=[]
    day_type:int
    day_type=(F_day.start_date).weekday()

    if F_day.spec_day==True:
        day_type=6
    
    data=initial_filter.initial_filter(F_day, day_type, copy.deepcopy(dataSet))
    data=DST.get_all_hours(F_day, copy.deepcopy(data))
    data=weather_filter.weather_filter(F_day, copy.deepcopy(data), solution[0:3], pc)
    data=inertial_filter.inertial_filter(F_day, copy.deepcopy(data), solution[3], pc_load, pc_temp, pc_h, solution[4], solution[5], solution[6], solution[7])
    data=distance_filter.distance_filter(F_day, copy.deepcopy(data), wc)
    data=day_light_filter.day_light_filter(F_day, copy.deepcopy(data), pc_dl)

    for i_coef in range(0, len(data)):

        data[i_coef].coef=copy.deepcopy(((solution[8]*data[i_coef].weather_coef)+(solution[9]*data[i_coef].inertial_coef)+(solution[10]*data[i_coef].distance_coef)+(solution[13]*data[i_coef].day_light_coef))/(solution[8]+solution[9]+solution[10]+solution[13]))
     
    data.sort(key=lambda x: x.coef, reverse=False)

    data=deviation_filter.deviation_filter(data.copy(), solution[11], solution[12])
    
    forecast=[]
    elem=0

    for a in range(len(F_day.hours)):
        for b in range(len(data)):
            elem+=data[b].hours[a].load
        forecast.append(copy.copy(elem)/len(data))
        elem=0

    scoreAbs = mean_absolute_percentage_error(load, forecast)*100

    return 1.0/scoreAbs

def run_ga(f_day: day.Day):

    global F_day, load
    F_day=f_day
   
    for y in range(len(F_day.hours)):
        load.append(F_day.hours[y].load)

    ga_instance = pygad.GA(
        num_generations=num_generations,
        num_parents_mating=num_parents_mating,
        fitness_func=fitness_func,
        sol_per_pop=sol_per_pop,
        num_genes=num_genes,
        gene_space= [list(range(0, 100, 1)), list(range(0, 100, 1)), list(range(0, 100, 1)), list(range(1, 4, 1)), list(np.arange(0.1, 1, 0.01)), list(range(0, 100, 1)), list(range(0, 100,1)),list(range(0, 100, 1)),list(range(0, 100,1)), list(range(0, 100,1)), list(range(0, 100,1)), list(np.arange(1, 3, 0.1)), list(range(3,8,1)), list(range(0, 100, 1))],
        gene_type=float,
        parent_selection_type=genetic_operators.parent_selection_func,
        mutation_type=genetic_operators.mutation_func,
        mutation_probability=0.2,
        crossover_probability=0.2,
        crossover_type=genetic_operators.crossover_func
    )

    ga_instance.run()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Parameters of the best solution : {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
    print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))

    if ga_instance.best_solution_generation != -1:
        print("Best fitness value reached after {best_solution_generation} generations.".format(best_solution_generation=ga_instance.best_solution_generation))

    write_read_file.save_optimal_param(solution, F_day.start_date.strftime("%Y-%m-%d"), F_day.part)

    return solution