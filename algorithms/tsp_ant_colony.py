import pygame
import random
import copy
import math

def edge_length(a,b)-> float:
    """
    We calculate d(a,b)
    :param a: tuple(int,int), a point
    :param b: tuple(int,int), a point
    :return L: float, the length
    """
    L = (a[0] - b[0]) ** 2 + (a[1]-b[1]) ** 2
    return round(L ** 0.5)

def create_pheromon_matrix_edges(points, initialp):
    edges = []
    for i in range(0, len(points)):
        edgei = []
        for j in range(0, len(points)):
            edgei.append(initialp)
        edges.append(edgei)
    return edges

def create_length_matrix_edge(points):
    edges = []
    for i in range(0, len(points)):
        edgei = []
        for j in range(0, len(points)):
            length = edge_length(points[i], points[j])
            edgei.append(length)
        edges.append(edgei)
    return edges   
       
def generate_random_sol(points, start) -> list:
    """
    We generate a random spanning tree 
    :return:sol, list of points
    """
    solution = []
    solution.append(start)
    
    frec = {}
    for i in range (0, len(points)):
        frec[i] = 0
    frec[start] = 1  # used point

    for i in range (0 , len(points) -  1):
        while True:
            p = random.randrange(0,len(points))
            if frec[p] == 0:
                frec[p] = 1
                solution.append(p)
                break
    solution.append(start)
    return solution

def calculate_TSP_tour_cost(points, solution) -> int : 
    """
    We calculate the cost of the given TSP tour
    :param solution: list of tuples, list of points
    :return:int, the TSP tour cost
    """
    total = 0
    for i in range (0, len(solution)-1):
        total += edge_length(points[solution[i]],points[solution[i+1]])
    return total

def generate_initial_roads(points, ants: int)->list:
    ants_road = []
    start = 0
    for ant in range(0, ants):
        if start == len(points):
            start = 0
        ants_road.append(generate_random_sol(points, start))
        start += 1
    return ants_road

def is_in_solution(road,i,j):
    for city in range(0, len(road)-1):
        if (road[city] == i and road[city+1] == j) or (road[city] == j and road[city+1] == i):
            return True
    return False

def update_pheromons(pheromon_edges, evaporation_rate, Q, roads_cost, ants_roads):
    for i in range (0, len(pheromon_edges)):
        for j in range (0, len(pheromon_edges)):
            pheromon_edges[i][j] = (1 - evaporation_rate) * pheromon_edges[i][j]
            for a in range (0, len(roads_cost)):
                if is_in_solution(ants_roads[a],i,j) == True:
                    pheromon_edges[i][j]+= Q / roads_cost[a]
    return pheromon_edges

def choose_next_city(city, pheromon_edges, length_edges, alfa, beta, visited):
    probability = {}
    sum_probabilities = 0
    for j in range (0, len(length_edges)):
        if visited[j] == False:
            probability[j] = pheromon_edges[city][j]**alfa * ( 1/max(1e-10, length_edges[city][j]) )**beta
            sum_probabilities += probability[j]
    
    r = random.uniform(0,sum_probabilities)
    j = 0
    while r >= 0 and j < len(length_edges):
        if j in probability:
            r -= probability[j]
        j = j + 1
    return j - 1

def generate_new_road(start_city, pheromon_edges, length_edges, alfa, beta):
    new_sol = []
    visited = []
    for i in range (0, len(length_edges)):
        visited.append(False)
    city = start_city
    for i in range (0, len(length_edges) - 1 ):
        new_sol.append(city)
        visited[city] = True
        next_city = choose_next_city(city, pheromon_edges, length_edges, alfa, beta, visited)
        city = next_city

    new_sol.append(city)
    new_sol.append(start_city)
    return new_sol


def ant_colony(surface, points, interations, ants, alfa, beta, evaporation_rate,  Q):

    font = pygame.font.SysFont("Arial", 50)

    ants_roads = generate_initial_roads(points, ants)
    pheromon_edges = create_pheromon_matrix_edges(points, 0.5)
    length_edges = create_length_matrix_edge(points)
    best_cost =  float('INF')
    best_solution = None
    it = 2
    while it <= interations:
        roads_cost = []
        for ant in range (0, ants):
            roads_cost.append(calculate_TSP_tour_cost(points, ants_roads[ant]))
            if best_cost > roads_cost[ant]:
                    best_cost = roads_cost[ant]
                    best_solution = ants_roads[ant]
                    draw_solution(surface, points, best_solution)
                    txt = font.render(f"Iteration: {it} | Cost: {best_cost}", True, (255, 255, 255))
                    surface.blit(txt, (20, 20))
                    pygame.display.flip()
        pheromon_edges = update_pheromons(pheromon_edges, evaporation_rate, Q, roads_cost, ants_roads)
        start = 0
        for ant in range(0, ants):
            if start == len(points):
                start = 0
            ants_roads[ant] = generate_new_road(start, pheromon_edges, length_edges, alfa, beta)
            start += 1
        it += 1
    return (best_cost, best_solution)


def draw_solution(surface, points, solution: list):
    surface.fill("black") 
    # Desenăm liniile
    for i in range(0, len(solution) - 1):
        pygame.draw.line(surface, (255, 255, 255), points[solution[i]], points[solution[i+1]], 2)

    # Desenăm orașele
    for sol in solution:
        # sol este un indice, deci points[sol] este (x, y)
        pygame.draw.circle(surface, (255, 0, 0), points[sol], 5)
    
    pygame.display.flip()
def ants_colony_main(points, maxX, maxY,interations, ants, alfa, beta, evaporation_rate,  Q):
    pygame.init()
    pygame.display.set_caption("Ant colony - TSP")
    
    screen = pygame.display.set_mode((maxX + 10, maxY + 10))
    
    (best_cost, final_solution) = ant_colony(screen, points, interations, ants, alfa, beta, evaporation_rate,  Q)
    print(best_cost)
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