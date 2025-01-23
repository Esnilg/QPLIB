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
8. [Aplicaciones de los Programas Binarios Cuadráticos (BQPs) en la Vida Real](#aplicaciones-de-los-programas-binarios-cuadráticos-(BQPs)-en-la-vida-real)

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

## Aplicaciones de los Programas Binarios Cuadráticos (BQPs) en la Vida Real

Los **Programas Binarios Cuadráticos (Binary Quadratic Programs, BQPs)** son un tipo de problema de optimización que combina variables binarias (0 o 1) con una función objetivo cuadrática y restricciones lineales. Estos modelos tienen una amplia gama de aplicaciones en la vida real, especialmente en áreas donde las decisiones son discretas y las interacciones entre variables son importantes. A continuación, se presentan algunas aplicaciones prácticas:

---

## 1. **Optimización de Portafolios Financieros**
- **Descripción**: En finanzas, los BQPs se utilizan para seleccionar una cartera de inversiones que maximice el rendimiento y minimice el riesgo, considerando interacciones entre activos.
- **Aplicación**: Decidir qué acciones incluir en un portafolio (1: incluir, 0: no incluir) y optimizar la combinación para maximizar el rendimiento esperado, sujeto a restricciones de riesgo y diversificación.
- **Ejemplo**: Seleccionar un subconjunto de acciones de un mercado para minimizar la varianza del portafolio (riesgo) mientras se maximiza la rentabilidad.

---

## 2. **Problemas de Asignación y Planificación**
- **Descripción**: Los BQPs son útiles para asignar recursos, tareas o personas de manera óptima.
- **Aplicación**:
  - **Asignación de tareas**: Asignar trabajadores a tareas específicas para minimizar costos o maximizar la eficiencia.
  - **Planificación de horarios**: Asignar turnos a empleados en hospitales, fábricas o servicios de transporte.
- **Ejemplo**: En una fábrica, decidir qué máquinas deben estar activas (1) o inactivas (0) para cumplir con la demanda de producción al menor costo.

---

## 3. **Diseño de Redes y Logística**
- **Descripción**: Los BQPs se utilizan para optimizar el diseño y la operación de redes de transporte, comunicación o suministro.
- **Aplicación**:
  - **Ubicación de instalaciones**: Decidir dónde construir almacenes o centros de distribución para minimizar costos de transporte.
  - **Ruteo de vehículos**: Planificar rutas para flotas de vehículos, considerando restricciones de capacidad y tiempo.
- **Ejemplo**: Determinar la ubicación óptima de centros de distribución para minimizar los costos de transporte y almacenamiento.

---

## 4. **Procesamiento de Señales y Machine Learning**
- **Descripción**: En el procesamiento de señales y el aprendizaje automático, los BQPs se utilizan para seleccionar características o agrupar datos.
- **Aplicación**:
  - **Selección de características**: Elegir un subconjunto óptimo de características para entrenar modelos de machine learning.
  - **Clustering binario**: Agrupar datos en categorías binarias para análisis de patrones.
- **Ejemplo**: En un sistema de reconocimiento de imágenes, seleccionar las características más relevantes para clasificar objetos.

---

## 5. **Diseño de Circuitos Electrónicos**
- **Descripción**: En ingeniería eléctrica, los BQPs se utilizan para optimizar el diseño de circuitos integrados y sistemas digitales.
- **Aplicación**:
  - **Minimización de componentes**: Decidir qué componentes incluir en un circuito para cumplir con las especificaciones técnicas al menor costo.
  - **Optimización de rutas**: Determinar la disposición óptima de conexiones en un chip.
- **Ejemplo**: Diseñar un circuito lógico que minimice el número de compuertas necesarias para realizar una función específica.

---

## 6. **Marketing y Publicidad**
- **Descripción**: Los BQPs ayudan a optimizar estrategias de marketing y publicidad.
- **Aplicación**:
  - **Selección de campañas**: Decidir qué campañas publicitarias ejecutar para maximizar el retorno de la inversión (ROI).
  - **Segmentación de clientes**: Identificar grupos de clientes para personalizar ofertas y promociones.
- **Ejemplo**: Seleccionar un subconjunto de clientes para enviarles una campaña promocional, maximizando las ventas esperadas.

---

## 7. **Problemas de Corte y Empaquetamiento**
- **Descripción**: En la industria manufacturera, los BQPs se utilizan para optimizar el corte de materiales y el empaquetamiento de productos.
- **Aplicación**:
  - **Corte de materiales**: Minimizar el desperdicio al cortar piezas de materiales como madera, metal o tela.
  - **Empaquetamiento**: Decidir cómo empaquetar productos en contenedores para minimizar el espacio utilizado.
- **Ejemplo**: Optimizar el corte de planchas de metal para producir piezas con el menor desperdicio posible.

---

## 8. **Problemas de Asignación en Energía**
- **Descripción**: En el sector energético, los BQPs se utilizan para optimizar la asignación de recursos y la gestión de redes.
- **Aplicación**:
  - **Distribución de energía**: Decidir qué fuentes de energía activar para satisfacer la demanda al menor costo.
  - **Gestión de redes eléctricas**: Optimizar la operación de redes eléctricas para minimizar pérdidas y maximizar la eficiencia.
- **Ejemplo**: Seleccionar qué generadores de energía activar en una red eléctrica para satisfacer la demanda con el menor costo operativo.

---

## 9. **Bioinformática y Genética**
- **Descripción**: En bioinformática, los BQPs se utilizan para analizar datos genéticos y optimizar procesos biológicos.
- **Aplicación**:
  - **Selección de genes**: Identificar genes asociados con enfermedades o características específicas.
  - **Diseño de fármacos**: Optimizar la selección de compuestos químicos para el desarrollo de nuevos medicamentos.
- **Ejemplo**: Seleccionar un subconjunto de genes que estén más relacionados con una enfermedad específica.

---

## 10. **Juegos y Teoría de Decisiones**
- **Descripción**: Los BQPs se utilizan en la teoría de juegos y la toma de decisiones estratégicas.
- **Aplicación**:
  - **Estrategias óptimas**: Encontrar la mejor estrategia en juegos de competencia o cooperación.
  - **Asignación de recursos en conflictos**: Decidir cómo asignar recursos limitados en situaciones de competencia.
- **Ejemplo**: Optimizar la estrategia de un equipo en un juego competitivo para maximizar las probabilidades de ganar.

---

## Conclusión

Los **Binary Quadratic Programs** son una herramienta poderosa para resolver problemas de optimización en una amplia variedad de campos. Su capacidad para modelar decisiones binarias y capturar interacciones entre variables los hace ideales para aplicaciones en finanzas, logística, ingeniería, marketing y más. Con el uso de solvers como Gurobi, es posible resolver problemas complejos de manera eficiente, lo que los convierte en una opción valiosa para la toma de decisiones en la vida real.

---

