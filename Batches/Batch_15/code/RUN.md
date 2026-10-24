# How to Run the Code

## Requirements
* Python 3.8+
* `matplotlib` (for generating benchmark plots)

```bash
pip install matplotlib
```

## Running the Components

### 1. Run the Main Solution (Branch & Bound)
```bash
python code/main_solution.py
```
Finds the exact optimal VM packing for the Batch 15 instance $[9, 8, 7, 6, 5, 4, 3, 2]$ with capacity $C = 16$.

### 2. Run Heuristics & Segment Tree (5k Servers)
```bash
python code/heuristics.py
```
Runs First-Fit Decreasing, demonstrates the Segment Tree for 5,000 servers, and prints the FFD counterexample.

### 3. Run Rejected Alternative (Pure Backtracking)
```bash
python code/rejected_alternative.py
```
Runs pure exhaustive search without lower bounding, demonstrating node explosion.

### 4. Run Changed Requirement (2D Vector Packing + Anti-Affinity)
```bash
python code/changed_requirement.py
```
Consolidates VMs requiring both vCPUs and RAM with microservice anti-affinity constraints.

### 5. Reproduce Timing Benchmarks & Generate Plots
```bash
python code/generate_inputs.py
```
Generates random test instances of sizes $N \in [6, 8, 10, 12, 14, 16]$, runs timing comparisons, and saves `results/timing.csv` and `results/timing_plot.png`.
