from math import inf
import numpy as np
import matplotlib.pyplot as plt

def notation():
    a = np.array([0,1,2,3,4,5,6,7])
    print(a, a.shape)
    a2d = np.matrix('0 1 2 3; 4 5 6 7')
    print(a2d, a2d.shape)
    a3d = np.array([np.matrix('1 2; 3 4'), np.matrix('4 5; 6 7')])
    print(a3d, a3d.shape)

def rank():
    A = np.eye(4)
    print(np.linalg.matrix_rank(A))
    A[-1,-1] = 0.
    print(np.linalg.matrix_rank(A))
    A = np.ones((4,))
    print(np.linalg.matrix_rank(A))
    A = np.zeros((4,))
    print(np.linalg.matrix_rank(A))

def vecnorm():
    a = np.array([[-3],[4]])
    print(np.linalg.norm(a, 1))
    print(np.linalg.norm(a, 2))
    print(np.linalg.norm(a, inf))

def matnorm():
    A = np.array([[-2,-2],[2,2]])
    print(np.linalg.norm(A, 'fro'))

def matprops():
    A = np.array([[2,1],[1,2]])
    print(np.trace(A))
    print(np.linalg.det(A))
    print(np.linalg.matrix_rank(A))
    print(np.linalg.cond(A))

def plotX():
    X = np.array([ [-1, -1], [0, 2], [2, 0], [3, 3] ])
    m = np.mean(X, axis = 0)
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    plt.grid(True)
    plt.axis([-2,4,-2,4])
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.plot(X[:,0], X[:,1], 'o')
    plt.plot(m[0], m[1],"x")
    plt.show()
    plt.savefig("plotX.eps")

def sumSlices():
    X = np.array([ [-1, -1], [0, 2], [2, 0], [3, 3] ])
    N,D = X.shape
    ones = np.ones((N,))
    first = np.matmul(ones, X)
    ones_prime = np.ones((D,))
    seccond = np.matmul(X,np.transpose(ones_prime))
    print(first)
    print(seccond)
    third = np.matmul(ones, np.matmul(X, ones_prime))
    print(third)
    print(first/N)
    print(third/(N*D))

def scaling():
    X = np.array([ [-1, -1], [0, 2], [2, 0], [3, 3] ])
    N,D = X.shape
    s_row = np.identity(N)/2
    s_col = np.identity(D)/2
    print(np.matmul(s_row,X))
    print(np.matmul(X,s_col))

def sum_scatter():
    X = np.transpose(np.array([ [-1, -1], [0, 2], [2, 0], [3, 3] ]))
    sq_mat = np.matmul(np.transpose(X),X)
    print(sq_mat)
    N,D = X.shape
    j_n = np.ones((N,N))
    c_n = np.identity(N)-(j_n/N)
    print(np.matmul(np.transpose(X),np.matmul(c_n,X)))

