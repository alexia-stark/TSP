import pygame
import random
import copy
import math

def generate_random_sol(points) -> list:
    """
    We generate a random spanning tree 
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
    solution.append(points[start])
    return solution

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
    return total

def generate_modified_solution(solution) -> list: #we do a 2-opt improvement
    """
    Given a solution, we generate a new one trying to make a 2-opt improvement
    :param solution: list of points, the given solution
    :return ew_sol: list of points, the new solution
    """
    new_sol =copy.copy(solution)
    p1 = random.randrange(1, len(new_sol) - 2)
    p2 = random.randrange(p1+1, len(new_sol)-1)
    p2+=1
    new_sol[p1:p2] = reversed(new_sol[p1:p2]) # invert all the numbers in between - try to fix a crossover of roads
    return new_sol

def Acceptance_function(solution, new_solution, T) -> list:
    """
    Given an existing solution and a newly generated one, this function determines
    using the simulated annealying method wether to change the solution or to ignore the new one
    :param T: the given temperature
    :param solution: list of tuples, the given order of the cities
    :param new_solution: list of tuples, the new order of the cities
    :return: list, the kept solution
    """
    initial_TSP = calculate_TSP_tour_cost(solution)
    new_TSP = calculate_TSP_tour_cost(new_solution)

    if new_TSP < initial_TSP:
        return (new_solution,T)
    else:
        delta = new_TSP - initial_TSP
        probability =  math.exp( - delta/ T)
        r = random.uniform(0,1)
        if r < probability :
            return (new_solution, T)# we change it 
        else:
            return (solution,T)

def simulated_annealing(screen,points, Temperature, alfa):
    sol = generate_random_sol(points)
    current_cost = calculate_TSP_tour_cost(sol)

    the_solution = sol

    font = pygame.font.SysFont("Arial", 50)
    iteration = 0
    while Temperature > 0.01 :
        new_sol = generate_modified_solution(the_solution)
        (the_solution, Temperature) = Acceptance_function(the_solution, new_sol, Temperature)
        iteration +=1
        if iteration == 3000:
            draw_solution(screen, the_solution)
            iteration = 0
            txt = font.render(f"Cost: {current_cost} | Temp: {int(Temperature)}", True, (255, 255, 255))
            screen.blit(txt, (20, 20))
            pygame.display.flip()

        current_cost = calculate_TSP_tour_cost(the_solution)
        Temperature = Temperature * alfa
        
def draw_solution(surface, solution: list):
 
    surface.fill("black") 
    for i in range (0, len(solution)-1):
        pygame.draw.line(surface, (255,255,255), solution[i], solution[i+1])

    for sol in solution:
        pygame.draw.circle(surface, (255,0,0), (sol[0], sol[1]), 5.0)   
    
    pygame.display.flip()

def sim_an_main(points, maxX, maxY, temp, alfa):
    pygame.init()
    pygame.display.set_caption("Simulated Annealing - TSP")
    
    screen = pygame.display.set_mode((maxX + 10, maxY + 10))
    
    final_solution = simulated_annealing(screen, points, temp, alfa) 
    print("Algorithm finished. Close the window to return to console.")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Opțional: Poți permite închiderea și cu tasta ESC
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        pygame.display.flip()

    pygame.quit()
