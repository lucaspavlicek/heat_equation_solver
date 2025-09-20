from js import sendArray, colormap, pixelSize, resultdone, window
import os
import numpy as np
from scipy.linalg import block_diag
import matplotlib.pyplot as plt
import matplotlib.animation as animation

colortable = np.array(colormap.to_py(), dtype=np.uint8)
pixelsize = pixelSize

def temptorgb(temp):
    rgb = [-1, -1, -1]
    for i in range(100):
        if colortable[i, 3] == temp:
            rgb = colortable[i, :3]
    return rgb[0], rgb[1], rgb[2]

def rgbtotemp(r, g, b):
    temp = -1
    for i in range(100):
        if list(colortable[i, :3]) == [r, g, b]:
            if temp > -1:
                print('Duplicate found')
            temp = colortable[i, 3]
    return temp

def processcolor(arr, i):
    return arr[i::32].reshape((64*pixelsize, 64))[::8].reshape(-1)

def getarray(jsproxyarray):

    fullarray = np.array(jsproxyarray.to_py(), dtype=np.uint8)
    rs = processcolor(fullarray, 0)
    gs = processcolor(fullarray, 1)
    bs = processcolor(fullarray, 2)


    temps = []
    for r, g, b in zip(rs, gs, bs):
        temps.append(rgbtotemp(r, g, b))
    
    return np.reshape(temps, (int(np.sqrt(len(temps))), int(np.sqrt(len(temps)))))

# generates a matrix that acts like a Laplacian in 2D (for Crank-Nicholson)
def makeLaplacian(gridsize):
    I = np.identity(gridsize)
    T = -4 * I
    for i in range(gridsize - 1):
        T[i, i + 1] = 1
        T[i + 1, i] = 1
    
    TT = block_diag(*([T]*gridsize)) 
    uI = block_diag(*([I]*gridsize)) 
    uI = np.hstack((np.zeros((uI.shape[0], gridsize)), uI[:,:-gridsize]))
    lI = block_diag(*([I]*gridsize)) 
    lI = np.hstack((lI[:,gridsize:],np.zeros((lI.shape[0], gridsize))))

    return TT + uI + lI

# generates a matrix that acts as a centered difference 2nd derivative (for LOD)
def makeD2(gridsize):
    I = np.identity(gridsize)
    d2 = -2 * I
    for i in range(gridsize - 1):
        d2[i, i + 1] = 1
        d2[i + 1, i] = 1
        
    return d2

# Crank-Nicholson
def crank(Ui, gridsize, iterations, deltat):
    laplacian = makeLaplacian(gridsize)
    
    U = np.zeros((iterations, gridsize, gridsize))
    U[0] = Ui
    Uvectors = np.zeros((iterations, gridsize ** 2))
    Uvectors[0] = (Ui.T).ravel()

    A = np.identity(gridsize ** 2) - (deltat/2)*laplacian
    for i in range(iterations - 1):
        b = (np.identity(gridsize ** 2) + (deltat/2)*laplacian).dot(Uvectors[i])
        Uvectors[i + 1] = np.linalg.solve(A, b)
        U[i + 1] = (Uvectors[i + 1].reshape(gridsize, gridsize)).T
    
    return U
    
# LOD
def LOD(Ui, gridsize, iterations, deltat):
    I = np.identity(gridsize)
    D2 = makeD2(gridsize)
    
    U = np.zeros((iterations, gridsize, gridsize))
    U[0] = Ui
    
    A = I - (deltat/2)*D2
    for i in range(iterations - 1):
        # x direction
        Ustar = np.zeros((gridsize,gridsize))
        for j in range(gridsize):
            b = (I + (deltat/2)*D2).dot(U[i, j])
            Ustar[j] = np.linalg.solve(A, b)
        
        #y direction
        for j in range(gridsize):
            b = (I + (deltat/2)*D2).dot(Ustar[:, j])
            U[i + 1, :, j] = np.linalg.solve(A, b)
        
    return U

# ADI
def ADI(Ui, gridsize, iterations, deltat):
    I = np.identity(gridsize)
    D2 = makeD2(gridsize)
    
    U = np.zeros((iterations, gridsize, gridsize))
    U[0] = Ui
    
    A = I - (deltat/2)*D2
    for i in range(iterations - 1):
        #x direction
        Ustar = np.zeros((gridsize,gridsize))
        Ustarstar = np.zeros((gridsize,gridsize))
        for j in range(gridsize):
            b = (I + (deltat/2)*D2).dot(U[i, :, j])
            Ustar[j] = np.linalg.solve(A, b)
        
        Ustar = Ustar.T 
        #y direction
        for j in range(gridsize):
            b = (I + (deltat/2)*D2).dot(Ustar[j])
            Ustarstar[:, j] = np.linalg.solve(A, b)
            
        U[i + 1] = Ustarstar.T
    return U

def makegif(U):
    # below is some fun plotting code I took from:
    # https://levelup.gitconnected.com/solving-2d-heat-equation-numerically-using-python-3334004aa01a
    def plotheatmap(u_k, k):
        # Clear the current plot figure
        plt.clf()

        plt.title(f"Temperature at t = {k} unit time")
        plt.xlabel("x")
        plt.ylabel("y")

        # This is to plot u_k (u at time-step k)
        plt.pcolormesh(u_k, cmap=plt.cm.jet, vmin=0, vmax=100)
        plt.colorbar()

        return plt

    # Also part of borrowed code
    # I will plot my ADI solution, but I promise all the methods appear pretty much the same.
    def animate(k):
        plotheatmap(U[k], k)

    anim = animation.FuncAnimation(plt.figure(), animate, interval=1, frames=len(U), repeat=False)
    anim.save("heat_equation_solution.gif")

    return
    

def main(event):
    Ui = getarray(sendArray())
    Gridsize = len(Ui)
    Iterations = 300
    Deltat = 1

    Uadi = LOD(Ui, Gridsize, Iterations, Deltat)
    jsUadi = Uadi.astype(np.uint8).tolist()

    window.U = jsUadi
    window.resultdone = True
    print("done")



