# Quadratic Programming (QP) Solver using Gurobi

This repository contains a Python implementation for solving Quadratic Programming (QP) problems with binary variables and linear constraints using the Gurobi optimizer. The project focuses on solving QP problems from the QPLIB library and compares two linearization techniques: **Glover** and **Glover-Woolsey**.

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Functions](#functions)
5. [Results and Analysis](#results-and-analysis)
6. [Conclusion](#conclusion)
7. [License](#license)

---

## Introduction

Quadratic Programming (QP) problems are optimization problems where the objective function is quadratic, and the constraints are linear. This repository focuses on solving QP problems with binary variables using the Gurobi optimizer. Two linearization techniques are implemented and compared:
1. **Glover's Linearization**
2. **Glover-Woolsey Linearization**

The project reads QP problems from the QPLIB library, solves them using both techniques, and analyzes the results in terms of computational time, solution quality, and bounds provided by the Linear Programming (LP) relaxation.

---

## Installation

To use this repository, you need to have Gurobi installed. Follow these steps:

1. **Install Gurobi**:
   - Download and install Gurobi from the [official website](https://www.gurobi.com/).
   - Obtain a license (free academic licenses are available).

2. **Install Python Dependencies**:
   - Ensure you have Python 3.x installed.
   - Install the required Python packages:
     ```bash
     pip install numpy pandas gurobipy
     ```

3. **Set Up Gurobi in Python**:
   - Navigate to the Gurobi installation directory and run:
     ```bash
     cd gurobi811\win64
     python setup.py install
     ```

---

## Usage

The repository contains a Python script that reads QP problems from the QPLIB library, solves them using Gurobi, and compares the two linearization techniques. The main steps are:

1. **Read the QP Problem**:
   - The function `readaQP` reads the problem data from a `.qplib` file.

2. **Solve the QP Problem**:
   - The function `solve_QP_gurobi` solves the QP problem directly using Gurobi.
   - The function `solve_Glover_Woolsey_gurobi` solves the problem using the Glover-Woolsey linearization.
   - The function `solve_Glover_gurobi` solves the problem using Glover's linearization.

3. **Analyze the Results**:
   - The results are saved in CSV files (`export_dataframe_G.csv` and `export_dataframe_GW.csv`) for further analysis.

### Example

To solve a specific QP problem, you can use the following code:

```python
name, typee, sense, n, m, Q0, b0, q0, A0, ccl, ccu = readaQP('QPLIB_0067')
result_GW = solve_Glover_Woolsey_gurobi(name, typee, sense, n, m, Q0, b0, q0, A0, ccl, ccu)
result_G = solve_Glover_gurobi(name, typee, sense, n, m, Q0, b0, q0, A0, ccl, ccu)
```

## Functions

### 1. `readaQP(nameproblem)`
- **Input**: The name of the QP problem (e.g., `QPLIB_0067`).
- **Output**: Problem data including the objective function, constraints, and variable bounds.

### 2. `solve_QP_gurobi(name, typee, sense, n, m, Q0, b0, q0, A0, ccl, ccu)`
- **Input**: Problem data.
- **Output**: Solves the QP problem directly using Gurobi and returns the solution.

### 3. `solve_Glover_Woolsey_gurobi(name, typee, sense, n, m, Q0, b0, q0, A0, ccl, ccu)`
- **Input**: Problem data.
- **Output**: Solves the QP problem using the Glover-Woolsey linearization and returns the solution.

### 4. `solve_Glover_gurobi(name, typee, sense, n, m, Q0, b0, q0, A0, ccl, ccu)`
- **Input**: Problem data.
- **Output**: Solves the QP problem using Glover's linearization and returns the solution.

---

## Results and Analysis

The repository includes an analysis of the results obtained from solving 20 selected QP problems. Key findings include:

### Quality of Bounds:
- The **Glover-Woolsey method** generally provides better bounds from the LP relaxation compared to Glover's method.
- However, **Glover's method** often finds better integer solutions within the time limit.

### Computational Time:
- The computational time increases with the number of binary variables and constraints.
- **Glover's method** is faster due to fewer additional constraints.

### Optimality:
- Only a few instances could be solved to optimality within 10 minutes using either method.
- The maximum problem size that could be solved to optimality within the time limit was **220 binary variables and 121 constraints**.

### Advantages and Disadvantages:
- **Glover-Woolsey**:
  - *Advantages*: Provides better bounds.
  - *Disadvantages*: Requires more computational resources.
- **Glover**:
  - *Advantages*: Faster and more scalable.
  - *Disadvantages*: May provide weaker bounds.

---

## Conclusion

Based on the analysis:
- **Glover's linearization** is recommended for larger problems due to its computational efficiency and ability to find good solutions quickly.
- For smaller problems where bound quality is critical, **Glover-Woolsey** may be preferred.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

For any questions or issues, please open an issue in the repository or contact the author.
