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
