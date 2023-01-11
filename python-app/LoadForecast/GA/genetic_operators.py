import random
import numpy as np

def crossover_func(parents, offspring_size, ga_instance):
    offspring = []
    idx = 0
    random_parents=[]
    random_parent=[]

    if ga_instance.generations_completed in [600, 800]:
        for i_chromosome in range(int(len(parents))):
            for i_gene in range(len(parents[i_chromosome])):
                random_parent.append(np.random.choice(ga_instance.gene_space[i_gene]))
            random_parents.append(random_parent.copy())
            random_parent=[]

    while len(offspring)!= offspring_size[0]:
        parent1 = parents[idx % parents.shape[0], :].copy()
        if ga_instance.generations_completed!=500 and ga_instance.generations_completed!=800:
            parent2 = parents[(idx + 1) % parents.shape[0], :].copy()
        else:
            parent2=random_parents[idx].copy()
        child1=[]
        child2=[]
        lista=[]
        for i in range(len(parent1)):
            if parent1[i]<parent2[i]:
                lista=list(np.arange(parent1[i],parent2[i],(ga_instance.gene_space[i][1]-ga_instance.gene_space[i][0])))
            elif parent1[i]>=parent2[i]:
                lista=list(np.arange(parent2[i],parent1[i],(ga_instance.gene_space[i][1]-ga_instance.gene_space[i][0])))

            if len(lista)<2:
                child1.append(np.random.choice(ga_instance.gene_space[i]))
                child2.append(np.random.choice(ga_instance.gene_space[i]))
            else:
                child1.append(np.random.choice(lista[:len(lista)//2],size=int(len(lista) > 0))[0])
                child2.append(np.random.choice(lista[len(lista)//2:],size=int(len(lista) > 0))[0])


        offspring.append(child1.copy())
        if len(offspring)<offspring_size[0]:
            offspring.append(child2.copy())
        
        idx += 1

    return np.array(offspring)

def mutation_func(offspring, ga_instance):

    for chromosome_idx in range(offspring.shape[0]):
        if(random.random() < ga_instance.mutation_probability):
            random_gene_idx = np.random.choice(range(offspring.shape[1]))

            offspring[chromosome_idx, random_gene_idx] = np.random.choice(ga_instance.gene_space[random_gene_idx])
        
    if ga_instance.mutation_probability < 0.5:
        ga_instance.mutation_probability+=0.05
        
    return offspring

def parent_selection_func(fitness, num_parents, ga_instance):

    fitness_sorted = sorted(range(len(fitness)), key=lambda k: fitness[k], reverse=True)
    retVal= np.empty((len(fitness), ga_instance.population.shape[1]))
    parents = np.empty((num_parents, ga_instance.population.shape[1]))
    probability_distribution=[]
   
    for parent_num in range(len(fitness)):
        retVal[parent_num, :] = ga_instance.population[fitness_sorted[parent_num], :].copy()
        probability_distribution.append(10/fitness[parent_num])

    probability_distribution.sort(reverse=True)
    
    retVal = random.choices(retVal.copy(), weights=probability_distribution, k=num_parents) 

    for parent_num in range(num_parents):
        parents[parent_num, :] = retVal[parent_num].copy()

    return parents, fitness_sorted[:num_parents]