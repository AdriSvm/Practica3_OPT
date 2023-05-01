import random
import numpy as np
from matplotlib import pyplot as plt
from model import Capa

np.set_printoptions(threshold=600)

class OP_Problema:
    def __init__(self,nrows:int=None,ncols:int=None,nobstacles:int=0,pos_obstacles:list=[]):
        self._nrows = nrows if nrows else 50
        self._ncols = ncols if ncols else 50
        random.seed(2224)
        #capa principal
        self._matriu = Capa(nrow=nrows,ncol=ncols,init_value=0.0)
        # capa obstacles
        self._cobstacles = Capa(nrow=nrows,ncol=ncols,init_value=0)
        self._cneu = self.gen_snow_layer()
        self._capes = []
        if len(pos_obstacles) == nobstacles:
            for i in pos_obstacles:
                self._cobstacles.gen_layer_values(i[0],i[1],i[2],i[2],1)
        else:
            self._cobstacles.gen_random_layers(nobstacles,value=1)

    def afegir_capa(self,init_value):

        c = Capa(nrow=self._nrows,ncol=self._ncols,init_value=init_value)

    def evolve(self) -> np.array:
        els = []
        els.append((random.randint(0,self._matriu.shape()[0]-1),random.randint(0,self._matriu.shape()[1]-1)))
        print(els)
        while len(els) > 0:
            print(els)
            nucli = els.pop()
            if self._matriu.Capa[nucli[0]][nucli[1]] == 0:
                for i,val in enumerate(self.vicinity30(self._matriu,nucli[0],nucli[1],self._cobstacles)):
                    self._matriu.change_value(nrow=nucli[0],ncol=nucli[1],value=1)
                    if val == 0:
                        els.append((nucli[0]+1,nucli[1]+i-1))

        return self._matriu.Capa, self._cobstacles.Capa

    def evolve_prop(self,init_row:int,init_col:int) -> np.array:
        self._matriu.change_value(init_row,init_col,self._cneu.Capa[init_row,init_col])
        print(self._matriu.Capa[init_row,init_col])
        for i in range(init_row,self._nrows):
            for x,val in enumerate(self._matriu.Capa[i]):
                print(val) if val != 0 else None
                if val > 0.05:
                    veins = self.vicinity30(self._matriu,i,x,self._cobstacles)
                    veins_neu = self.get_snow_neighbours(i,x) # Crear nova capa de quantitat de neu per cada casella
                    print("veins_init",veins)
                    num_dif_de_zero = sum(1 for elem in veins if elem == 0)
                    veins = tuple(float((val / num_dif_de_zero) + veins_neu[o]) if veins[o] == 0 else 0 for o in range(len(veins)))
                    print("veins",veins, "caselles", i+1,i+1,x-1,x-2)
                    for m,val in enumerate(veins):
                        if val != 0:
                            self._matriu.gen_one_value(i+1,x+m-1,val)
                    #self._matriu.gen_values(i+1,i+1,x-1,x+2,veins)
                    #self._matriu.Capa[i+1,x-1:x+2] = veins

        return self._matriu.Capa,self._cobstacles.Capa, self._cneu.Capa

    def get_snow_neighbours(self,nrow,ncol):
        if nrow == self._matriu.shape()[0] - 1:
            return (0,0,0)
        elif ncol == 0:
            return (0,self._cneu.Capa[nrow+1,ncol],self._cneu.Capa[nrow+1,ncol+1])
        elif ncol == self._ncols-1:
            return (self._cneu.Capa[nrow + 1, ncol - 1], self._cneu.Capa[nrow + 1, ncol], 0)
        else:
            return (self._cneu.Capa[nrow + 1, ncol - 1], self._cneu.Capa[nrow + 1, ncol],self._cneu.Capa[nrow+1,ncol+1])
    def gen_snow_layer(self):
        inc = 0.6
        snow = np.zeros((int(self._nrows),int(self._ncols)))
        for i in range(self._nrows):
            alt_rel = int(self._nrows*0.95) -i
            for j in range(self._ncols):
                distancia_al_centro = abs(j - (self._ncols - 1) / 2)
                ancho_mitad = self._ncols / 2
                factor_anchura = np.exp(-distancia_al_centro ** 2 / (2 * (ancho_mitad * inc) ** 2))
                nieve = alt_rel * factor_anchura
                snow[i, j] = max(nieve, 0)
        return Capa(0,0,0,snow)


    @staticmethod
    def vicinity30(matriu,fila,columna, matriu_obstacles):
        print(fila,columna)
        # 0: pot propagar, 1: no pot propagar
        if fila == matriu.shape()[0]-1:
            return (1,1,1)
        elif columna == 0:
            esq,mig,dret = 1,1,1
            if matriu_obstacles.Capa[fila+1][columna] == 0:
                mig = 0
            if matriu_obstacles.Capa[fila+1][columna+1] == 0:
                dret = 0
            return (esq,mig,dret)

        elif columna == matriu.shape()[1]-1:
            esq, mig, dret = 1, 1, 1
            if matriu_obstacles.Capa[fila + 1][columna] == 0:
                mig = 0
            if matriu_obstacles.Capa[fila + 1][columna - 1] == 0:
                esq = 0
            return (esq, mig, dret)

        else:
            esq, mig, dret = 1, 1, 1
            if matriu_obstacles.Capa[fila + 1][columna - 1] == 0:
                esq = 0
            if matriu_obstacles.Capa[fila + 1][columna] == 0:
                mig = 0
            if matriu_obstacles.Capa[fila + 1][columna + 1] == 0:
                dret = 0
            return (esq, mig, dret)


proba = OP_Problema(220,220,10)
res,obst,neu = proba.evolve_prop(40,120)
print(res,obst,sep='\n\n\n')

fig, ax = plt.subplots()

# Mostramos la matriz como una imagen en blanco y negro
ax.imshow(res, cmap='viridis')


# Mostramos el gráfico
plt.show()

fig, ax = plt.subplots()

# Mostramos la matriz como una imagen en blanco y negro
ax.imshow(obst, cmap='binary')


# Mostramos el gráfico
plt.show()


fig, ax = plt.subplots()

# Mostramos la matriz como una imagen en blanco y negro
ax.imshow(neu, cmap='viridis')


# Mostramos el gráfico
plt.show()