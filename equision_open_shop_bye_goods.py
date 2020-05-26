# import numpy as np
# def solve():
#     while max(d[-1][:-1]) > 0:
#         jnum = np.argmax(d[-1][:-1]) #转入下标
#         inum = np.argmin(d[:-1, -1]/d[:-1, jnum])  #转出下标
#         s[inum] = jnum #更新基变量
#         d[inum] /= d[inum][jnum]
#         for i in range(bn):
#             if i != inum:
#                 d[i] -= d[i][jnum] * d[inum]
#
# def printSol():
#     for i in range(cn - 1):
#         print("x%d=%.2f" % (i,d[s.index(i)][-1] if i in s else 0))
#     print("objective is %.2f"%(-d[-1][-1]))
#
# d = np.loadtxt("files/data.txt", dtype=np.float)
# (bn,cn) = d.shape
# s = list(range(cn-bn,cn-1)) #基变量列表
# solve()
# printSol()
import numpy as np
from scipy.optimize import linprog

C = np.array([-65.5,-73,-30,-35.5,-33.5,-32,-79,-68.2,-93.5,-34,-16.3])
A_ub = np.array([[12.5,15,5,6.5,4.5,7,20,9.8,11.5,4,2.5],[1.5,-1.5,-0.5,0.5,1.5,0.5,-1.5,-2.5,-0.5,0.5,1.5]])
B_ub = np.array([5000, 0])
r = linprog(C, A_ub, B_ub, None, None, bounds=((10, None), (10, None), (10, None), (5, None), (5, None), (5, None), (5, None), (3, None), (3, None), (3, None), (3, None)))
print(r)









