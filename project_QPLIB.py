# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 10:02:50 2020

@author: esnil
"""


#> cd gurobi811\win64
#> python setup.py install

# the modules to use are loaded

import gurobipy as gp
import numpy as np
import pandas as pd

##############################################
# if I want to read a problem in .lp format
# The gurobi version is 811

#model = gp.read('QPLIB_0067.lp')
#model.optimize()

##############################################

# I read the database from where I have the information of all the problems 
# of the given page

datos = pd.read_csv('instancedata.csv')  

# filter the data of interest
datosA = datos[["name","objsense","nbinvars","nvars","ncons","probtype","solobjvalue"]].copy()
datosA = datosA.loc[datosA['probtype'] == "QBL"]

print(datosA.dtypes)

# I check if there is Nan
print("How much NaN: ",len(datosA[pd.isnull(datosA.solobjvalue)]))

# I fill the missing data with zeros
if len(datosA[pd.isnull(datosA.solobjvalue)]) > 0:
    datosA['solobjvalue'] = datosA['solobjvalue'].fillna(0)

# I order the data from smallest to largest number of binary variables
datosA = datosA.sort_values('nbinvars')

# total problem 
numproblem = len(datosA)

######################
#
#  Functions
#

'''
There are 4 functions called:
    
    - readaQP                      : read datos
    - solve_QP_gurob               : solve QP problem
    - solve_Glover_Woolsey_gurobi  : solve QP linealized with G-W method
    - solve_Glover_gurobi          : solve QP linealized with G method

The inputs of the functions solve_Glover_Woolsey_gurobi and solve_Glover_gurobi
    
    - name   : problem's name
    - typee  : Quadratic Binaray var and linear constraints (QBL)
    - sense  : Maximize or Minimize
    - n      : number of variables binary
    - m      : number of constraints linear
    - Q0     : Matrix orden n x n
    - b0     : array orden n x 1
    - q0     : constant
    - A0     : Matrix orden m x n
    - ccl    : array orden m x 1
    - ccu    : array orden m x 1

QP: 1/2 x^t Q0 x + b0^t x + q0

s.t. 

    ccl <= A0 x <= ccu 
    
    x is {0,1}
    

The outputs of the functions solve_Glover_Woolsey_gurobi and solve_Glover_gurobi

it's a dictionary, with the keys:
    - name      : problem's name
    - timeload  : time it takes to read the .qplib file
    - timerun   : time to solve el model
    - gapmip    : gap of solution
    - solobj    : the best integer solution found
    - solBound  : the best upper bound solution found
    - status    : if it is optimal (2)
    - solrelax  : bound provided by the Linear Programming relaxation

'''

def readaQP(nameproblem):
    
    name  = [] # problem name (character string)
    typee = [] # problem type (character string)
    sense = [] # one of the words minimize or maximize (character string)
    
    n = 0 # number of variables (integer)
    m = 0 # number of constraints (integer)
    
    # value of function objective
    
    nQ0 = 0                     # number of nonzeros (integer) in lower triangle of Q0
    Q0  = np.zeros((n,n))       # matrix Q
    
    nb0  = 0                    # default value (real) for entries in b0 
    nnb0 = 0                    # number of non-default linear coefficients in objective
    b0  = np.zeros(n)           # array b
    
    q0  = 0                     # constant part of the objective function
    
    # value of constrains
    
    nbi = 0                     # number of nonzeros (integer) in bi, summed over all i in M
    A0  = np.zeros((m,n))       # matrix A
    
    cinfmas   = 0               # value (real) for innity for constraint or variable bounds|anybound greater than or equal to this in, absolute value, is infnite
    
    cl  = 0                     # default value (real) for entries in cl
    ncl = 0                     # number of non-default entries (integer) in cl
    ccl = np.zeros(m)
    
    cu  = 0                     # default value (real) for entries in cu
    ncu = 0                     # number of non-default entries (integer) in cu
    ccu = np.zeros(m)
    
    ld  = 0                     # default value (real) for entries in l
    nld = 0                     # number of non-default entries (integer) in l
    l   = np.zeros(n)
    
    ud  = 0                     # default value (real) for entries in u
    nud = 0                     # number of non-default entries (integer) in u
    u   = np.zeros(n)
    
    filepath = 'qplib/'
    filepath += nameproblem
    filepath += '.qplib'
    
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
       
        name.append(line.strip())
        
        line = fp.readline()
        cnt += 1
        
        typee.append(line.strip())
    
        line = fp.readline()
        cnt += 1
        
        sense.append(line.split())
     
        line = fp.readline()
        cnt += 1
            
        n = int(line.split()[0])
        
        line = fp.readline()
        cnt += 1
      
        m = int(line.split()[0])
    
        line = fp.readline()
        cnt += 1
    
        nQ0  = int(line.split()[0])
        
        ### inicial
        
        Q0  = np.zeros((n,n))
        A0  = np.zeros((m,n))   
        b0  = np.zeros(n)
        ccl = np.zeros(m)
        ccu = np.zeros(m)
        l   = np.zeros(n)
        u   = np.zeros(n)
        
        
        if (n < 1000 and m < 5000):
        
            aux = 1
            print("Quadratic objective")
            while aux <= nQ0:
                line = fp.readline()
                term = line.split()
                cnt +=1
                aux +=1
                Q0[int(term[0])-1,int(term[1])-1] = float(term[2])
                #Q0[int(term[1])-1,int(term[0])-1] = float(term[2])
                
            # next row 
            line = fp.readline()
            cnt +=1
            
            nb0 = float(line.split()[0])
            
            # next row 
            line = fp.readline()
            cnt +=1
            
            nnb0 = int(line.split()[0])
            
            b0 = b0 + nb0
            
            if nnb0 > 0:
                print("linear objective")
                aux = 1
                while (aux <= nnb0):
                    line = fp.readline()
                    term = line.split()
                    cnt +=1
                    aux +=1
                    b0[int(term[0])-1] = float(term[1])
            
            # next row 
            line = fp.readline()
            cnt +=1
            
            q0 = float(line.split()[0])
           
            # next row 
            line = fp.readline()
            cnt +=1
            
            nbi = int(line.split()[0])
            
            aux = 1
            print("linear constraint")
            while(aux <= nbi):
                line = fp.readline()
                term = line.split()
                cnt +=1
                aux +=1
                A0[int(term[0])-1,int(term[1])-1] = float(term[2])
             
            # next row 
            line = fp.readline()
            cnt +=1   
            
            cinfmas   = float(line.split()[0])  
            
            line = fp.readline()
            cnt +=1    
            
            cl = float(line.split()[0])
            ccl = ccl + cl
            
            line = fp.readline()
            cnt +=1  
            
            ncl = int(line.split()[0])
            
            if ncl > 0:
                print("ncl > 0")
                aux = 1
                while (aux <= ncl):
                    line = fp.readline()
                    term = line.split()
                    cnt +=1
                    aux +=1
                    ccl[int(term[0])-1] = float(term[1])
                
            # next row 
            line = fp.readline()
            cnt +=1
            
            cu = float(line.split()[0])
            ccu = ccu + cu
            
            # next row 
            line = fp.readline()
            cnt +=1
            
            ncu = int(line.split()[0])
            
            if ncu > 0:
                print("ncu > 0")
                aux = 1
                while (aux <= ncu):
                    line = fp.readline()
                    term = line.split()
                    cnt +=1
                    aux +=1
                    ccu[int(term[0])-1] = float(term[1])
        
        return name,typee,sense,n,m,Q0,b0,q0,A0,ccl,ccu
        
    
# name,typee,sense,n,m,Q0,b0,q0,A0,ccl,ccu = readaQP('QPLIB_0067')    
    
def solve_QP_gurobi(name,typee,sense,n,m,Q0,b0,q0,A0,ccl,ccu):
    import numpy as np
    import scipy.sparse as sp
    import gurobipy as gp
    from gurobipy import GRB
    import time

    try:
        
        start_time = time.time()
        # Create a new model
        model = gp.Model(name[0])
    
        # Create variables.
        x = model.addVars(n, vtype=GRB.BINARY, name="x")
        
        model.update()
        # The objective is to minimize/maximize the total fixed and variable costs
        
        if 'minimize' == sense[0][0]:
            model.modelSense = GRB.MINIMIZE
        else:
            model.modelSense = GRB.MAXIMIZE
        model.update()
        
        # constraints
        model.addConstrs((gp.quicksum(A0[i][j]*x[j] for j in range(n)) <= ccu[i]) for i in range(m))
        model.addConstrs((gp.quicksum(A0[i][j]*x[j] for j in range(n)) >= ccl[i]) for i in range(m))
        model.update()
        
        # function objetive        
        model.setObjective(gp.quicksum(0.5*x[i]*Q0[i,j]*x[j] for i in range(n) for j in range(n)) + gp.quicksum(b0[j]*x[j] for j in range(n)) + q0)
        
        model.params.TimeLimit = 1000
        model.update()
        
        end_time = time.time() - start_time
        
        # Optimize.
        model.optimize()
        
        if model.status == GRB.OPTIMAL:
            time = model.Runtime
            gap = model.MIPGap
            solobj = model.objVal
        
        # print model in format .lp
        model.write('poolsearch.lp')
        
        assert model.status == GRB.OPTIMAL
    
    
    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError:
        print('Encountered an attribute error')
    
    if model.status == GRB.OPTIMAL:
        return np.array([solobj,time,gap,end_time])
    else:
        return -1


#solve_QP_gurobi(name,typee,sense,n,m,Q0,b0,q0,A0,ccl,ccu)


def solve_Glover_Woolsey_gurobi(name,typee,sense,n,m,Q0,b0,q0,A0,ccl,ccu):
    import numpy as np
    import scipy.sparse as sp
    import gurobipy as gp
    from gurobipy import GRB
    import time

    Q00 = Q0.transpose()

    try:
        
        start_time = time.time()
        # Create a new model
        model = gp.Model(name[0])
        
        # Create variables.
        x = model.addVars(n, vtype=GRB.BINARY, name="x")
        
        y = {}
        for i in range(n):
            for k in range(n):
                y[i,k] = model.addVar(lb=-GRB.INFINITY,ub=GRB.INFINITY,vtype=GRB.CONTINUOUS, name="y%s" % str([i,k]))
        
        model.update()
  
        if 'minimize' == sense[0][0]:
            model.modelSense = GRB.MINIMIZE
        else:
            model.modelSense = GRB.MAXIMIZE
        model.update()
    
        # const 1-4            
        model.addConstrs((y[i,j] <= x[i] for i in range(n) for j in range(n) if i<j))
        model.addConstrs((y[i,j] <= x[j] for i in range(n) for j in range(n) if i<j))
        model.addConstrs((y[i,j] >= x[i] + x[j] - 1 for i in range(n) for j in range(n) if i<j))
        model.addConstrs((y[i,j] >= 0.0 for i in range(n) for j in range(n) if i<j))
        model.update() 
            
        # constraints
        model.addConstrs((gp.quicksum(A0[i][j]*x[j] for j in range(n)) <= ccu[i]) for i in range(m))
        model.addConstrs((gp.quicksum(A0[i][j]*x[j] for j in range(n)) >= ccl[i]) for i in range(m))
        model.update()
        
        # function objetive        
        model.setObjective(gp.quicksum(0.5*Q00[i,j]*y[i,j] for i in range(n) for j in range(i+1,n)) + gp.quicksum(b0[j]*x[j] for j in range(n)) + q0)
        
        model.params.TimeLimit = 600
        model.update()
        
        end_time = time.time() - start_time
        
        # Optimize.
        model.optimize()
        
        # solve relax model
        r = model.relax()
        r.optimize()
        
        time     = model.Runtime
        gap      = model.MIPGap
        solobj   = model.objVal
        solBound = model.ObjBound
        status   = model.status
        solrelax = r.objval
        
        # print model in format .lp
        model.write('poolsearch_GW.lp')
                    
    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError:
        print('Encountered an attribute error')
    
    return {"name": name[0],"timeload": end_time,"timerun": time,"gapmip": gap,"solobj": solobj,"solBound": solBound,"status": status,"solrelax": solrelax}


#solve_Glover_Woolsey_gurobi(name,typee,sense,n,m,Q0,b0,q0,A0,ccl,ccu)

def solve_Glover_gurobi(name,typee,sense,n,m,Q0,b0,q0,A0,ccl,ccu):
    import numpy as np
    import scipy.sparse as sp
    import gurobipy as gp
    from gurobipy import GRB
    import time

    Q00 = 0.25*Q0
    Q00 = Q00 + Q00.transpose()

    Qmas = np.array([sum(max(0,Q00[i,j]) for j in range(n)) for i in range(n)])
    Qmenos = np.array([sum(min(0,Q00[i,j]) for j in range(n)) for i in range(n)])

    #Qmas     = np.array([sum(Q00[i,j] for i in range(n) if i!=j and Q00[i,j] > 0 ) for j in range(n)]) 
    #Qmenos   = np.array([sum(Q00[i,j] for i in range(n) if i!=j and Q00[i,j] < 0 ) for j in range(n)]) 

    try:
        start_time = time.time()
        # Create a new model
        model = gp.Model(name[0])
        
        # Create variables.
        x = model.addVars(n, vtype=GRB.BINARY, name="x")
        w = model.addVars(n, lb=-GRB.INFINITY,ub=GRB.INFINITY,vtype=GRB.CONTINUOUS, name="w")
        
        model.update()
  
        if 'minimize' == sense[0][0]:
            model.modelSense = GRB.MINIMIZE
        else:
            model.modelSense = GRB.MAXIMIZE
        model.update()
        
        if 'minimize' == sense[0][0]:
            model.addConstrs((w[i]>= Qmenos[i]*x[i] for i in range(n)))
            model.addConstrs((w[j]>= gp.quicksum(Q00[i,j]*x[i] for i in range(n)) - Qmas[j]*(1-x[j])  for j in range(n)))
        else:
            model.addConstrs((w[i]<= Qmas[i]*x[i] for i in range(n)))
            model.addConstrs((w[j]<= gp.quicksum(Q00[i,j]*x[i] for i in range(n)) - Qmenos[j]*(1-x[j])  for j in range(n)))
        model.update()

        # model.addConstrs((w[i]>= Qmenos[i]*x[i] for i in range(n)))
        # model.addConstrs((w[i]<= Qmas[i]*x[i] for i in range(n)))
        # model.update()
        
        # model.addConstrs((w[j]>= gp.quicksum(Q00[i,j]*x[i] for i in range(n) if i!=j) - Qmas[j]*(1-x[j])  for j in range(n)))
        # model.addConstrs((w[j]<= gp.quicksum(Q00[i,j]*x[i] for i in range(n) if i!=j) - Qmenos[j]*(1-x[j])  for j in range(n)))
        # model.update()

        # constraints
        model.addConstrs((gp.quicksum(A0[i][j]*x[j] for j in range(n)) <= ccu[i]) for i in range(m))
        model.addConstrs((gp.quicksum(A0[i][j]*x[j] for j in range(n)) >= ccl[i]) for i in range(m))
        model.update()
        
        # function objetive        
        model.setObjective(gp.quicksum(w[i] for i in range(n)) + gp.quicksum(b0[j]*x[j] for j in range(n)) + q0)
        
        model.params.TimeLimit = 600
        model.update()
        
        end_time = time.time() - start_time
        
        # Optimize.
        model.optimize()
        
        # solve relax model
        r = model.relax()
        r.optimize()
        
        time     = model.Runtime
        gap      = model.MIPGap
        solobj   = model.objVal
        solBound = model.ObjBound
        status   = model.status
        solrelax = r.objval
        
        # print model in format .lp
        model.write('poolsearch_G.lp')
        
    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError:
        print('Encountered an attribute error')
    
    return {"name": name[0],"timeload": end_time,"timerun": time,"gapmip": gap,"solobj": solobj,"solBound": solBound,"status": status,"solrelax": solrelax}
    
#solve_Glover_gurobi(name,typee,sense,n,m,Q0,b0,q0,A0,ccl,ccu)

dataGW = pd.DataFrame(columns=('name','timeload', 'timerun', 'gapmip', 'solobj','solBound','status','solrelax'))
dataG = pd.DataFrame(columns=('name','timeload', 'timerun', 'gapmip', 'solobj','solBound','status','solrelax'))

datos_select = ["QPLIB_3834","QPLIB_0633","QPLIB_0067","QPLIB_3762","QPLIB_2512",
"QPLIB_3714","QPLIB_10040","QPLIB_3402","QPLIB_10043",
"QPLIB_10054","QPLIB_3775","QPLIB_3883","QPLIB_3803",
"QPLIB_3815","QPLIB_2492","QPLIB_10057","QPLIB_3614",
"QPLIB_7144","QPLIB_3703","QPLIB_2357"]

for i in range(len(datos_select)):
    
    name,typee,sense,n,m,Q0,b0,q0,A0,ccl,ccu =  readaQP(datos_select[i])

    print(name[0])
    if Q0.any() != 0:
        
        GW = solve_Glover_Woolsey_gurobi(name,typee,sense,n,m,Q0,b0,q0,A0,ccl,ccu)
        
        print("")
        dataGW = dataGW.append(GW , ignore_index=True)
        G = solve_Glover_gurobi(name,typee,sense,n,m,Q0,b0,q0,A0,ccl,ccu)
        print("")
        dataG = dataG.append(G , ignore_index=True)
        
        dataG.to_csv ('export_dataframe_G.csv', index = False, header=True)
        dataGW.to_csv ('export_dataframe_GW.csv', index = False, header=True)

    del name,typee,sense,n,m,Q0,b0,q0,A0,ccl,ccu

'''
Analyse the instances describing their main features, with particular attention  
to the presence of binary variables and the diferent kind of linear constraints:
    
    resp: 
        - There are 91 problem type QBL, that is, they have quadratic function,
          linear constraints and binary variables.
        - The range of binary variables is from 50 to 8904.
        - 80% of the binary variables vary between 50 and 900.
        - 6 problems are maximization the rest is minimization
        
Analyse and compare the quality of the bound provided by the Linear Programming 
relaxation of the two Linearization Techniques.

    assumptions: We select 20 minimization problems in increasing order in the number of binary variables.
                 We run each instance with a maximum time limit of 600 seconds
     resp:
        - In most of the time the quality of the bounds offered by the relaxed
          linearization method of Glover is worse than that offered by Glover_Woolsey
        - However, the upper bound offered by the Glover method at the end of 600 seconds
          is most of the time better than those of Glover_Woolsey.

Analyse the variation of the computational time necessary to solve the in-
stances in function of the number of binary variables.

    resp:
        - It is evident that the computational time grows as the number of binary
          variables grows, however, the computational time is also affected by the 
          number of linear constraints. The method that offers the fastest solutions
          is that of Glover, this is because it does not generate as many additional 
          restrictions as in Glover_Woolsey.
        
Determine the maximum dimension of the instances that can be solved to proven
optimality within a computing time of 10 minutes.

    resp:
        - Using Glover: out of 20 instances, only 4 reached the optimal solution 
          in less than 10 minutes
        - Using Glover_Woolsey: out of 20 instances, only 4 reached the optimal solution 
          in less than 10 minutes
        - the maximum dimension of the instances in both is 220 var binary and 121 contraints
        - Note: In some cases, it is observed in the method of Glover, 
          that despite not satisfying the optimality criteria, the best known 
          integer solution coincides with the optimal solution of the problem.
        
Discuss the advantages and the disadvantages of the two linearization teachniques.

    resp:
        disadvantages Glover_Woolsey
        - the size of the reformulation increases quadratically
        - this linearization doubles the number of additional constraints added.
          This drawback could be problematic in the case when the
          size of original QP becomes very large
          
        advantages Glover_Woolsey
        - The big advantage of this new linearization is that the variable  
          need not anymore be declared as binary
        
        disadvantages Glover
        - requires a linear number of additional variables and constraints
        
        advenatgaes GLover
        - This technique yields a much smaller number of additional constraints

        
Discuss the results as you were in machine learning data center to convince the
management to adopt one or the other linearization technique.

    resp:
        - Since in the problem QPLIB_7144 when using the method of Glover
          the computation time was 10 times faster than that of Glover_Woolsey,
          I recommend using the Glover method, no matter that the upper bound
          of method relaxed is worse, in most of the times, it is possible to 
          reach the optimal solution of the problem, even without reaching 
          satisfy gap tolerance.
        
'''

dataG_size = pd.DataFrame(columns=('name','timeload', 'timerun', 'gapmip', 'solobj','solBound','status','solrelax'))

for i in range(len(datosA)):
    
    name,typee,sense,n,m,Q0,b0,q0,A0,ccl,ccu =  readaQP(datosA.iloc[i][0])

    print(name[0])
    if Q0.any() != 0:
        
        #GW = solve_Glover_Woolsey_gurobi(name,typee,sense,n,m,Q0,b0,q0,A0,ccl,ccu)
        
        #print("")
        #dataGW = dataGW.append(GW , ignore_index=True)
        G = solve_Glover_gurobi(name,typee,sense,n,m,Q0,b0,q0,A0,ccl,ccu)
        #print("")
        dataG_size = dataG_size.append(G , ignore_index=True)
        
        #dataGW.to_csv ('export_dataframe_GW.csv', index = False, header=True)
        dataG_size.to_csv ('export_dataframe_G_size.csv', index = False, header=True)
        

    del name,typee,sense,n,m,Q0,b0,q0,A0,ccl,ccu
