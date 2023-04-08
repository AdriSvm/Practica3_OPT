import random
import numpy as np
from matplotlib import pyplot as plt

np.set_printoptions(threshold=600)


class Problema:
    def __init__(self,nrows:int=None,nobstacles:int=0):
        if nrows:
            self._nrows = nrows
        else:
            self._nrows = 50
        random.seed(2223)
        #capa principal
        self._matriu = np.array([[0 for _ in range(self._nrows)] for _ in range(self._nrows)])
        # capa obstacles
        self._cobstacles = np.array([[0 for _ in range(self._nrows)] for _ in range(self._nrows)])
        for _ in range(nobstacles):
            a = random.randint(0,self._cobstacles.shape[1]-1)
            b = random.randint(a,self._cobstacles.shape[1]-1)

            pared = (random.randint(0,self._cobstacles.shape[0]-1) ,random.randrange(0,self._cobstacles.shape[1]-1))
            self._cobstacles[pared[0]][a:b] = 1

    def evolve(self) -> np.array:
        els = []
        els.append((random.randint(0,self._matriu.shape[0]-1),random.randint(0,self._matriu.shape[1]-1)))
        while len(els) > 0:
            print(els)
            nucli = els.pop()
            if self._matriu[nucli[0]][nucli[1]] == 0:
                for i,val in enumerate(Problema.vicinity30(self._matriu,nucli[0],nucli[1],self._cobstacles)):
                    self._matriu[nucli[0]][nucli[1]] = 1
                    if val == 0:
                        els.append((nucli[0]+1,nucli[1]+i-1))

        return self._matriu, self._cobstacles

    '''    @staticmethod
    def evolve(fila):
        nueva_fila = []
        for i in range(len(fila)):
            nueva_celda = Problema.nucleo30(Problema.vicinity30(fila, i))
            nueva_fila.append(nueva_celda)
        return np.array([[nueva_fila]])'''

    @staticmethod
    def vicinity30(matriu,fila,columna, matriu_obstacles):
        print(fila,columna)
        if str(type(matriu)) != "<class 'numpy.ndarray'>" or type(fila) != int or type(columna) != int:
            raise Exception("Vicinity function only callable with a numpy one-row object")
        # 0: pot propagar, 1: no pot propagar
        if fila == matriu.shape[0]-1:
            return (1,1,1)
        elif columna == 0:
            esq,mig,dret = 1,1,1
            if matriu_obstacles[fila+1][columna] == 0:
                mig = 0
            if matriu_obstacles[fila+1][columna+1] == 0:
                dret = 0
            return (esq,mig,dret)

        elif columna == matriu.shape[1]-1:
            esq, mig, dret = 1, 1, 1
            if matriu_obstacles[fila + 1][columna] == 0:
                mig = 0
            if matriu_obstacles[fila + 1][columna - 1] == 0:
                esq = 0
            return (esq, mig, dret)

        else:
            esq, mig, dret = 1, 1, 1
            if matriu_obstacles[fila + 1][columna - 1] == 0:
                esq = 0
            if matriu_obstacles[fila + 1][columna] == 0:
                mig = 0
            if matriu_obstacles[fila + 1][columna + 1] == 0:
                dret = 0
            return (esq, mig, dret)


proba = Problema(220,10)
res,obst = proba.evolve()
print(res,obst,sep='\n\n\n')

fig, ax = plt.subplots()

# Mostramos la matriz como una imagen en blanco y negro
ax.imshow(res, cmap='binary')


# Mostramos el gráfico
plt.show()

fig, ax = plt.subplots()

# Mostramos la matriz como una imagen en blanco y negro
ax.imshow(obst, cmap='binary')


# Mostramos el gráfico
plt.show()