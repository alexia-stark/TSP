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

def generate_all_neighbours(solution, tabu_list, overall_best_score) -> list: #we do a 2-opt improvement
    """
    Given a solution, we generate all the neighbours of this solution.
    A neighbour is obtaine dby swapping 2 points in the solution. 
    :param solution: list of points, the given solution
    :return ew_sol: list of points, the new solution
    """
    neighbours = []
    neighbours_costs = []
    neighbours_i_j = []
    for i in range (1, len(solution) - 2):
        for j in range (i+1, len(solution) - 1):
            new_sol = copy.copy(solution)
            new_sol[i:j+1] = reversed(new_sol[i:j+1] )
            neighbours.append(new_sol)
            neighbours_i_j.append((i,j))
            neighbours_costs.append(calculate_TSP_tour_cost(new_sol))

    return get_best_neighbour(neighbours, neighbours_costs, neighbours_i_j, tabu_list, overall_best_score)

def get_best_neighbour(neighbours, neighbours_costs, neighbours_i_j, tabu_list, overall_best_score):
    """
    Given the neighbours = the new TSP Tours and their TSP Tour costs, this function
    returns the best one and its cost.
    :param neighbours: list of lists of points
    :param neighbours_costs: list of ints
    :return (best, minim): tuple, the best neighbour and its cost
    """
    minim = float('inf')
    best = None
    i_j = None
    for i in range (0, len(neighbours)):
        if neighbours_costs[i] < minim:
            if aspiration(neighbours_i_j[i], neighbours_costs[i], tabu_list, overall_best_score):
                minim = neighbours_costs[i]
                best = neighbours[i]
                i_j = neighbours_i_j[i]

    return (best, minim, i_j)

def aspiration(candidate, candidate_cost, tabu_list, overall_best_cost):
    if candidate not in tabu_list.keys() or tabu_list[candidate] == 0:
        return True

    if candidate_cost < overall_best_cost:
        return True
    # it is in the tabu list and it is forbidden   
    return False

def modify_tabu_list (candidate, tabu_list, st_tabu_tenure, dr_tabu_tenure):
    to_be_deleted_key = []
    for key,value in tabu_list.items():
        tabu_list[key] = value - 1
        if tabu_list[key] == 0:
            to_be_deleted_key.append(key)
    
    for element in to_be_deleted_key:
        del tabu_list[element]

    if candidate not in tabu_list.keys():
        tabu_list[candidate] = random.randint(st_tabu_tenure, dr_tabu_tenure)

def tabu_search(screen, points, index, st_tabu_tenure, dr_tabu_tenure):

    start_sol = generate_random_sol(points)
    current_sol = start_sol
    best_cost = calculate_TSP_tour_cost(current_sol)

    ok = True
    tabu_list = {}
    font = pygame.font.SysFont("Ariel", 50)
    for i in range (0, index):
        (best_neighbour, bn_cost,i_j) = generate_all_neighbours(current_sol, tabu_list, best_cost)
        if i_j != None:
            modify_tabu_list(i_j, tabu_list, st_tabu_tenure, dr_tabu_tenure)
        if bn_cost < best_cost:
            best_cost = bn_cost
        current_sol = best_neighbour
        if i % 20 == 0:
            draw_solution(screen, current_sol)
            text = font.render(f"Current iteration: {i} | Current_cost: {bn_cost} | Best cost: {best_cost} ",True, (255, 255, 255))
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

def tabu_main(points, maxX, maxY, nr_iterations, st_tabu_tenure,dr_tabu_tenure):
    pygame.init()
    pygame.display.set_caption("Hill climbing - TSP")

    font = pygame.font.SysFont("Ariel", 50)

    screen = pygame.display.set_mode((maxX + 10, maxY + 10))
    
    (best_score, best_config) = tabu_search(screen, points, nr_iterations, st_tabu_tenure, dr_tabu_tenure)
    
    draw_solution(screen, best_config)
    text = font.render(f"Overall best: {best_score} ",True, (255, 255, 255))
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