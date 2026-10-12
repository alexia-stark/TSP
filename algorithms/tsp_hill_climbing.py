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

def generate_all_neighbours(solution) -> list: #we do a 2-opt improvement
    """
    Given a solution, we generate all the neighbours of this solution.
    A neighbour is obtaine dby swapping 2 points in the solution. 
    :param solution: list of points, the given solution
    :return ew_sol: list of points, the new solution
    """
    neighbours = []
    neighbours_costs = []
    for i in range (1, len(solution) - 2):
        for j in range (i+1, len(solution) - 1):
            new_sol = copy.copy(solution)
            new_sol[i:j+1] = reversed(new_sol[i:j+1] )
            neighbours.append(new_sol)
            neighbours_costs.append(calculate_TSP_tour_cost(new_sol))

    return get_best_neighbour(neighbours, neighbours_costs)

def get_best_neighbour(neighbours, neighbours_costs):
    """
    Given the neighbours = the new TSP Tours and their TSP Tour costs, this function
    returns the best one and its cost.
    :param neighbours: list of lists of points
    :param neighbours_costs: list of ints
    :return (best, minim): tuple, the best neighbour and its cost
    """
    minim = neighbours_costs[0]
    best = neighbours[0]

    for i in range (1, len(neighbours)):
        if neighbours_costs[i] < minim :
            minim = neighbours_costs[i]
            best = neighbours[i]

    return (best,minim)

def hill_climbing(screen, points, index):

    start_sol = generate_random_sol(points)
    current_sol = start_sol
    best_cost = calculate_TSP_tour_cost(current_sol)
    ok = True

    font = pygame.font.SysFont("Ariel", 50)
    while ok == True:
        ok = False
        (best_neighbour, bn_cost) = generate_all_neighbours(current_sol)
        
        if bn_cost < best_cost:
            best_cost = bn_cost
            current_sol = best_neighbour
            draw_solution(screen, current_sol)
            ok = True

            text = font.render(f"Current iteration: {index} | Best cost: {best_cost} ",True, (255, 255, 255))
            screen.blit(text, (20, 20))
            pygame.display.flip()
    return (best_cost, current_sol)

def draw_solution(surface, solution: list):
 
    surface.fill("black") 
    for i in range (0, len(solution)-1):
        pygame.draw.line(surface, (255,255,255), solution[i], solution[i+1])

    for sol in solution:
        pygame.draw.circle(surface, (255,0,0), (sol[0], sol[1]), 5.0)  
    pygame.display.flip()

def hill_main(points, maxX, maxY, repeat):
    pygame.init()
    pygame.display.set_caption("Hill climbing - TSP")

    font = pygame.font.SysFont("Ariel", 50)

    screen = pygame.display.set_mode((maxX + 10, maxY + 10))
    
    best_cost = float ('inf')
    best_solution = []
    used = 1
    while used <= repeat:
        (cost, TSP_Tour) = hill_climbing(screen, points, used)
        if best_cost > cost:
            best_cost = cost
            best_solution = TSP_Tour
        used+=1
    
    draw_solution(screen, best_solution)
    text = font.render(f"Overall best: {best_cost} ",True, (255, 255, 255))
    screen.blit(text, (20, 20))
    pygame.display.flip()
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