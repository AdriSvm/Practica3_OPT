import random
import numpy as np
from matplotlib import pyplot as plt
from model import Capa


class OP_Problema:
    def __init__(self,nrows:int=None,ncols:int=None,nobstacles:int=0,pos_obstacles:list=[]):
        """
        Object Programming oriented implementation of a basic avalanche.
        We create a main layer where the avalanche initiates in a fixed or random point and where you can
        see the evolution of it.
        We made two similiar implementations:
            -First one incorporates a layer of obstacles which can be natural stuff like rocks or big trees,
             but also made to implement avalanche protections. We consider that these obstacles stop completely
             the avalanche. This one can be called through .evolve() method.
            -In the second implementation we add a third layer of snow. This layer it's made of floats which
             reflects how much snow there's in the mountain. As we're modeling a constant slope, it's made like
             a gradient, in the top we have a lot of snow and very little in the bottom. This implementation
             can be called through the evolve_prop method. The snow gains power with the snow it encounters
             but, it also divides its power proportionally to the three cels below.
        Numpy is compulsory and a random seed.
        The layers are created through a model called Capa which retains all the information about them
        """
        self._nrows = nrows if nrows else 50
        self._ncols = ncols if ncols else 50
        random.seed(2224)
        #capa principal
        self._matriu = Capa(nrow=nrows,ncol=ncols,init_value=0.0)
        # capa obstacles
        self._cobstacles = Capa(nrow=nrows,ncol=ncols,init_value=0)
        self._cneu = self.gen_snow_layer()
        if len(pos_obstacles) == nobstacles:
            for i in pos_obstacles:
                self._cobstacles.gen_layer_values(i[0],i[1],i[2],i[2],1)
        else:
            self._cobstacles.gen_random_layers(nobstacles,value=1)

    def evolve(self) -> np.array:
        """
        Main method which creates the first implementation of the avalanche, the start is randomly created
        """
        els = []
        els.append((random.randint(0,self._matriu.shape()[0]-1),random.randint(0,self._matriu.shape()[1]-1)))
        print(els)
        while len(els) > 0:
            print(els)
            nucli = els.pop()
            if self._matriu.Capa[nucli[0]][nucli[1]] == 0:
                for i,val in enumerate(self.vicinity(self._matriu,nucli[0],nucli[1],self._cobstacles)):
                    self._matriu.change_value(nrow=nucli[0],ncol=nucli[1],value=1)
                    if val == 0:
                        els.append((nucli[0]+1,nucli[1]+i-1))

        return self._matriu.Capa, self._cobstacles.Capa

    def evolve_prop(self,init_row:int,init_col:int) -> np.array:
        """
        Second implementation of the avalanche, here we consider the third layer of snow
        init_row and init_col precises where the avalanche starts.
        """
        self._matriu.change_value(init_row,init_col,self._cneu.Capa[init_row,init_col])
        print(self._matriu.Capa[init_row,init_col])
        for i in range(init_row,self._nrows):
            for x,val in enumerate(self._matriu.Capa[i]):
                print(val) if val != 0 else None
                if val > 0.4: #IMPORTANT LINE, Changing the 0.4 value, we can adjust how much snow we consider to still evolve the avalanche
                    veins = self.vicinity(self._matriu,i,x,self._cobstacles)
                    veins_neu = self.get_snow_neighbours(i,x) # Nova capa de quantitat de neu per cada casella
                    num_dif_de_zero = sum(1 for elem in veins if elem == 0)
                    veins = tuple(float((val / num_dif_de_zero) + veins_neu[o]) if veins[o] == 0 else 0 for o in range(len(veins)))
                    for m,val in enumerate(veins):
                        if val != 0:
                            self._matriu.gen_one_value(i+1,x+m-1,val)

        return self._matriu.Capa,self._cobstacles.Capa, self._cneu.Capa

    def get_snow_neighbours(self,nrow,ncol):
        """
        Vicinity function of the snow layer
        """
        if nrow == self._matriu.shape()[0] - 1:
            return (0,0,0)
        elif ncol == 0:
            return (0,self._cneu.Capa[nrow+1,ncol],self._cneu.Capa[nrow+1,ncol+1])
        elif ncol == self._ncols-1:
            return (self._cneu.Capa[nrow + 1, ncol - 1], self._cneu.Capa[nrow + 1, ncol], 0)
        else:
            return (self._cneu.Capa[nrow + 1, ncol - 1], self._cneu.Capa[nrow + 1, ncol],self._cneu.Capa[nrow+1,ncol+1])

    def gen_snow_layer(self):
        """
        Method which creates the snow layer with the gradient method, we consider that the start of the layer is the
        top of the mountain, so there's more snow and as we go down the mountain, the quantity of snow decreases.
        """
        snow = np.zeros((int(self._nrows),int(self._ncols)))
        for i in range(self._nrows):
            alt_rel = int(self._nrows*0.95) -i
            nieve = alt_rel / (self._nrows - 1)  # calcular la cantidad de nieve en función de la altura
            snow[i, :] = nieve  # asignar la cantidad de nieve a todas las columnas en la fila i
        return Capa(0, 0, 0, snow)


    @staticmethod
    def vicinity(matriu,fila,columna, matriu_obstacles):
        """
        The main vicinity function of the main layer
        """
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


#Creation of the main object for the modeling of the avalanche
#Here we consider a layer of 220*220 and 10 obstacles, we can also precise the position of the obstacles
proba = OP_Problema(220,220,10)

#You can call the first implementation with the next line:
#res,obst = proba.evolve()

# And the second implementation is called through the next line, we specify the position of the start of the avalanche
res,obst,neu = proba.evolve_prop(1,100)

#Then we plot the simulation results
fig, ax = plt.subplots()


ax.imshow(res, cmap='viridis')


plt.show()

fig, ax = plt.subplots()

ax.imshow(obst, cmap='binary')


plt.show()


fig, ax = plt.subplots()


ax.imshow(neu, cmap='viridis')


plt.show()