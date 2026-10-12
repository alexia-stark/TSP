from algorithms.tsp_genetic_recombinations import genetic_main
from algorithms.tsp_hill_climbing import hill_main
from algorithms.TSP_simulated_annealing import sim_an_main
from algorithms.tsp_tabu_search import tabu_main
from algorithms.tsp_ant_colony import ants_colony_main
from utils.manage_file import Manage_File

def help():
    print("--------------------------- tsp <file_name> <algo> -------------------------------------")
    print("<file_name> must be one of the followings: ")
    print_files_in_data_folder()
    print("--------------- <algo>----------------")
    print("You can choose between: ")
    print("<algo> =  sim_an -> simulated annealing")
    print("<algo> = hill_climbing")
    print("<algo> = genetic -> genetic recombinations algorithms")
    print("<algo> = tabu_search")
    print("<algo> = ant_colony")
    print("------------------------------------quit-------------------------------------------")

def print_files_in_data_folder():
    file_manager =  Manage_File()
    all_files = file_manager.get_files()
    for file in all_files:
        print(file)

def handle_tsp(filename, algo):
    
    file  = Manage_File(filename)
    try:
        (points, maxX, maxY) = file.read_file_and_create_points()
        match algo:
            case 'sim_an':
                Temp = input("Choose the temperature (recommended 5000.0): ")
                alfa = input("Choose degrading rate (recommended 0.99999): ")
                Temp = float(Temp)
                alfa = float(alfa)
                sim_an_main(points, maxX, maxY, Temp, alfa)
            case 'hill_climbing':
                repet = input("Choose how many times you want to repet the algorithm (recommended 20): ")
                repet = int(repet)
                hill_main(points,maxX, maxY, repet)
            case 'genetic':
                initial_population = input("Choose the number of the initialpopulation (recommended 500): ")
                nr_of_generations = input("Choose how many generations you want(recommended 1000): ")
                initial_population = int (initial_population)
                nr_of_generations = int (nr_of_generations)
                genetic_main(points, maxX, maxY, initial_population, nr_of_generations)
            case 'tabu_search':
                nr_iterations = input ("Choose number of iterations (recommended 500): ")
                print("You will now have to choose an interval [st,dr] fo the tabu tenure. ")
                st_tabu_tenure = input ("Choose st_tabu_tenure (recommended 7): ")
                dr_tabu_tenure = input ("Choose dr_tabu_tenure (recommended 12): ")
                st_tabu_tenure = int (st_tabu_tenure)
                dr_tabu_tenure = int (dr_tabu_tenure)                
                nr_iterations = int (nr_iterations)
                tabu_main(points, maxX, maxY, nr_iterations, st_tabu_tenure, dr_tabu_tenure)
            case 'ant_colony':
                iterations = input ("Choose number of iterations (recommended 200): ")
                ants = input("Choose the number of ants (recommended = nr of cities): ")
                alfa = input("Choose alfa value (recommended 1): ")
                beta = input("Choose beta value (recommended 3): ")
                evaporation_rate = input("Choose evaporation rate (recommended 0.5): ")
                Q = input ("Choose the value of Q (recommended 100): ")
                ants_colony_main(points, maxX, maxY,int(iterations), int(ants), int(alfa), int(beta), float(evaporation_rate), int(Q) )
            case _:
                print("The <algo> paramter does not have a valid input.")
    except NameError:
        print("The filename is invalid. Please select a file that exists.")

def console():
    print("Anytime you are confused, enter help. ")
    while True: 
        choice  = input(">> ")
        command =  choice.split()
        match command[0]:
            case 'help':
                help()
            case 'tsp':
                handle_tsp(command[1], command[2])
            case 'quit': 
                break
            case _:
                print("That was not a valid option.")



