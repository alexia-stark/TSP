import pygame
import random

def edge_length(a,b)-> float:
    """
    We calculate d(a,b)
    :param a: tuple(int,int), a point
    :param b: tuple(int,int), a point
    :return L: float, the length
    """
    L = (a[0] - b[0]) ** 2 + (a[1]-b[1]) ** 2
    return round(L ** 0.5)

def calculate_TSP_tour_cost(solution) -> int : 
    """
    We calculate the cost of the given TSP tour
    :param solution: list of tuples, list of points
    :return:int, the TSP tour cost
    """
    total = 0
    for i in range (0, len(solution)-1):
        total += edge_length(solution[i],solution[i+1])
    # we also calculate  last city - first city distance because it has to return 
    total += edge_length(solution[len(solution)-1], solution[0])
    return total

def generate_random_sol(points) -> list:
    """
    We generate a random solution WITHOUT adding the first point also to the finish
    :return:sol, list of points
    """
    start = random.randrange(0,len(points))
    solution = []
    solution.append(points[start])
    
    frec = {}
    for i in range (0, len(points)):
        frec[i] = 0
    frec[start] = 1  # used point

    for i in range (0 , len(points) -  1):
        while True:
            p = random.randrange(0,len(points))
            if frec[p] == 0:
                frec[p] = 1
                solution.append(points[p])
                break
    return solution

def best_of_the_generation(generation:list)->tuple:
    """
    Given the generation, this function returns the cost and the index of the solution of the best tsp-route
    :param generation: list of lists of points
    :return(minim, best): tuple: (int, index)
    """
    minim = calculate_TSP_tour_cost(generation[0]) 
    best = 0 
    for i in range(0, len(generation)) :
        cost = calculate_TSP_tour_cost(generation[i])
        if cost < minim:
            minim = cost
            best = i

    return (minim, best)

def fitness_function( route:list, best_cost):
    """
    Given a route, we calculate its fitness function, being best_cost of the generation / cost_route
    :param route: list
    :param best_cost: the best cost of the generation 
    """
    return best_cost / calculate_TSP_tour_cost(route)

def create_initial_population(points, population_number:int ):
    """
    Given a number of routs of the 'population', we return a 
    list of that number of random routes as the initial population
    WITOUD ADDING the last point as the start point
    :param population_number: int
    :return initial_population: list of lists
    """
    initial_population = []
    for i in range(0, population_number):
        solution = generate_random_sol(points)
        initial_population.append(solution)
    return initial_population

def tournament_selection(population:list, best)-> list:
    """
    Given a number of possible routes, this function returns half of the population
    the routes: chooses 2 random routes, computes their distances then chooses  the smallest one.
    :param population: list of lists, the given routes
    :return survivors: list of lists, the 'winners' of the tournament
    """
    survivors = []
    random.shuffle(population)
    for i in range (0, len(population) // 2):
        j = random.randint(0, len(population)-2)
        k = random.randint(j+1, len(population)-1)
        if fitness_function(population[j], best) > fitness_function(population[k],best):
            survivors.append(population[j])
        else:
            survivors.append(population[k])
    return survivors

def crossover(parent_a, parent_b)-> list:
    """
    This function simulates a crossover of 2 lists into another list.
    :param parent_a: list
    :param parent_b: list
    :return offspring: list
    """
    offspring = []
    # we first choose what to take from parent a
    start = random.randint(0, len(parent_a)-4)
    finish = random.randint(start+4, len(parent_a)) # cat mai departati 
    from_parent_a = parent_a[start:finish]
    from_parent_b = list([b for b in parent_b if b not in from_parent_a] )
    for i in range (0, len(parent_a)):
            if i >= start and i < finish: # we take from a 
                offspring.append(from_parent_a[0])
                from_parent_a.pop(0)
            else:
                offspring.append(from_parent_b[0])
                from_parent_b.pop(0)
    return offspring

def create_new_generation(old_generation:list)-> list :
    """
    Given the list of existing routes/survivors, this function returns a new list constaining a
    completely new generation of routes, with the same number of routes but resulted
    from the crossover of the survivors.
    For each pair of parents, we generate 4 children 
    :param old_generation: list of lists
    :return new_gen: list of lists
    """
    new_gen = []
    random.shuffle(old_generation)
    midway =  len(old_generation) // 2
    for i in range (0, midway):
        for j in range(0,2):
            offspring = crossover( old_generation[i], old_generation[i+ midway])
            new_gen.append(offspring)
            offspring = crossover( old_generation[i+midway], old_generation[i])
            new_gen.append(offspring)
            
    return new_gen

def mutation(new_generation :list, TheBest, mutation_rate)->list:
    """
    This function manages mutations. 3% of the new_generation will suffer mutations
    Inversion mutation is used
    Elitism will be used - the best won't mutate
    :param new_generation: ist of routes
    :return new_generation: list of routes, the mutated generation
    """
    elite = list (new_generation[TheBest])
    for k in range (0, len(new_generation)): 
            if k!= TheBest and  random.randint(0, 1000) < 10 * mutation_rate: #<3.5% 
                i = random.randint(0, len(new_generation[k])- 2)
                j = random.randint(i+1, len(new_generation[k]))
                new_generation[k][i:j] = reversed(new_generation[k][i:j])  
    new_generation[0] = elite
    return new_generation

def genetic_recombination(points, surface, nr_initial, nr_of_generations):

    font = pygame.font.SysFont("Ariel", 50)

    initial_population = create_initial_population(points, nr_initial)
    old_generation = initial_population

    (best_cost, index_sol) = best_of_the_generation(old_generation)
    print(best_cost)
    no_change_gen = 0
    last_best_cost = best_cost
    for i in range (nr_of_generations):

        survivors = tournament_selection(old_generation, best_cost)
        new_generation = create_new_generation(survivors)
        (best_cost, index_sol) = best_of_the_generation(new_generation)

        if no_change_gen >= 500:
            new_generation = mutation(new_generation, index_sol, 10) # we aplly elitism 
        else:
            new_generation = mutation(new_generation, index_sol, 3) # we aplly elitism 

        (best_cost, index_sol) = best_of_the_generation(new_generation)

        if best_cost == last_best_cost:
            no_change_gen += 1
        else:
            no_change_gen = 0 
        print(best_cost)

        if i % 10 == 0:
            draw_solution(surface, new_generation[index_sol]+ [new_generation[index_sol][0]])
            text = font.render(f"Generation: {i} | Best cost :{best_cost}", True, (255,255,255))
            surface.blit(text,(20,20))
            pygame.display.flip()
    
        old_generation = new_generation
        last_best_cost = best_cost
    
def draw_solution(surface, solution: list):
 
    surface.fill("black") 
    for i in range (0, len(solution)-1):
        pygame.draw.line(surface, (255,255,255), solution[i], solution[i+1])

    for sol in solution:
        pygame.draw.circle(surface, (255,0,0), (sol[0], sol[1]), 5.0)   
    pygame.display.flip()

def genetic_main(points, maxX, maxY, initial_population, nr_of_generations):
    pygame.init()
    pygame.display.set_caption("Gentic recombination- TSP")
    
    screen = pygame.display.set_mode((maxX + 10, maxY + 10))
    
    final_solution = genetic_recombination(points, screen, initial_population, nr_of_generations) 
    print("Algorithm finished. Close the window to return to console.")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        pygame.display.flip()

    pygame.quit()
