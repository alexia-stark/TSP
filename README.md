# TSP Solver - Berlin52 Dataset

A Python-based interactive application for solving the **Traveling Salesperson Problem (TSP)** on benchmark datasets (such as Berlin52) using various metaheuristic algorithms. The project features a Command Line Interface (CLI) and real-time route visualization powered by **Pygame**.

---

## Implemented Algorithms

- **Ant Colony Optimization (ACO)** (`tsp_ant_colony.py`): Simulates ant behavior using pheromone trails and edge lengths to discover optimal paths.
- **Genetic Algorithm with Recombinations** (`tsp_genetic_recombinations.py`): Uses tournament selection, custom 2-point crossover, 2-opt inversion mutation, and elitism across successive generations.
- **Hill Climbing** (`tsp_hill_climbing.py`): Iterative local search utilizing 2-opt edge swaps to find local minima over multiple random restarts.
- **Simulated Annealing** (`TSP_simulated_annealing.py`): Probabilistic technique that accepts worse intermediate solutions based on a cooling schedule to escape local minima.
- **Tabu Search** (`tsp_tabu_search.py`): Local search algorithm using a tabu list and tenure interval with an aspiration criterion to prevent cycling.

---

## Project Structure

```text
TSP_berlin52/
├── algorithms/                 # Metaheuristic implementations
│   ├── tsp_ant_colony.py
│   ├── tsp_genetic_recombinations.py
│   ├── tsp_hill_climbing.py
│   ├── TSP_simulated_annealing.py
│   └── tsp_tabu_search.py
├── data/                       # TSP dataset files (e.g., Berlin52)
├── ui/                         # User interface modules
│   └── console.py              # Interactive CLI command loop
├── utils/                      # File loading and utility functions
│   └── manage_file.py
├── main.py                     # Entry point
└── README.md

```

---

## Prerequisites and Installation

### Requirements

* Python 3.x
* `pygame` library

### Installation

1. Clone the repository:

```bash
git clone [https://github.com/alexia-stark/TSP.git](https://github.com/alexia-stark/TSP.git)
cd TSP

```

2. Install dependencies:

```bash
pip install pygame

```

---

## How to Run

Launch the interactive console application:

```bash
python main.py

```

### Console Commands

Once inside the application shell, the following commands are available:

* `help` - Display available dataset files and algorithm choices.
* `tsp <file_name> <algo>` - Run a specific algorithm on a chosen dataset.
* `quit` - Exit the application.

---

## Usage and Algorithm Parameters

When running a command like `tsp TSP_Berlin52.docx sim_an`, the console will prompt you to enter parameters. Below are the supported algorithm keys and their recommended configuration parameters:

| Algorithm Key | Algorithm Name | Parameters & Recommended Values |
| --- | --- | --- |
| `sim_an` | Simulated Annealing | • Initial Temperature (Recommended: `5000.0`)<br>

<br>• Degrading Rate / Alpha (Recommended: `0.99999`) |
| `hill_climbing` | Hill Climbing | • Restarts / Repetitions (Recommended: `20`) |
| `genetic` | Genetic Algorithm | • Initial Population (Recommended: `500`)<br>

<br>• Number of Generations (Recommended: `1000`) |
| `tabu_search` | Tabu Search | • Number of Iterations (Recommended: `500`)<br>

<br>• Tabu Tenure Lower Bound (Recommended: `7`)<br>

<br>• Tabu Tenure Upper Bound (Recommended: `12`) |
| `ant_colony` | Ant Colony Optimization | • Number of Iterations (Recommended: `200`)<br>

<br>• Number of Ants (Recommended: number of cities)<br>

<br>• Alpha / Pheromone importance (Recommended: `1`)<br>

<br>• Beta / Distance importance (Recommended: `3`)<br>

<br>• Evaporation Rate (Recommended: `0.5`)<br>

<br>• Q / Pheromone constant (Recommended: `100`) |

---

## Visualizations

When an algorithm runs, a Pygame window displays the live optimization process, showing current iterations, tour costs, and the rendered tour path.

| Hill Climbing | Simulated Annealing | Tabu Search |
| --- | --- | --- |
|  |  |  |

*(Close the Pygame visualization window or press `ESC` to return to the interactive console).*

---

## Code Documentation

Each algorithm module uses standard Python docstrings specifying parameter types and return values:

```python
def calculate_TSP_tour_cost(solution) -> int:
    """
    We calculate the cost of the given TSP tour
    :param solution: list of tuples, list of points
    :return: int, the TSP tour cost
    """

```

```

---

Dacă după salvare faci din nou `git add README.md`, `git commit -m "Fix README markdown"` și `git push origin main`, textul și imaginile se vor afișa corect pe GitHub. Verificați reîmprospătând pagina repozitoriului.

<Elicitations message="Ai nevoie de ajutor cu altceva?">
  <Elicitation label="Cum verific vizualizarea" query="Cum pot verifica cum arată README-ul direct în VS Code înainte de push?"/>
  <Elicitation label="Imaginile nu se încarcă" query="Ce fac dacă imaginile din tabelul de pe GitHub apar ca linkuri frânte?"/>
</Elicitations>
