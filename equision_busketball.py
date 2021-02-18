import numpy as np
from scipy.optimize import linprog

C = np.array([-192,-190,-188,-186,-185,-180,-178,-178])
A_ub = np.array([[0,0,0,0,0,-1,-1,-1],[1,0,0,0,0,1,0,0],[0,0,0,1,0,1,0,0],[0,1,0,0,0,0,0,1]])
B_ub = np.array([-1,1,1,1])
A_eq = np.array([[1,1,1,1,1,1,1,1],[1,1,0,0,0,0,0,0]])
B_eq = np.array([5,1])
r = linprog(C, A_ub, B_ub, A_eq, B_eq, bounds=(0,None),integer=true)
print(r)