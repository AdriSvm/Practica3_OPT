import numpy as np, random
class Capa():
    def __init__(self, nrow:int,ncol:int,init_value:[int,float,str,bool],matrix=None):
        if matrix is not None:
            self.Capa=matrix
            self.nrows = self.shape()[0]
            self.ncols = self.shape()[0]
        else:
            self.Capa = np.array([[init_value for _ in range(ncol)] for _ in range(nrow)])
            self.nrows = nrow
            self.ncols = ncol

    def change_value(self,nrow:int,ncol:int,value):
        try:
            self.Capa[nrow,ncol] = value
            return True
        except:
            return False

    def gen_random_samples(self,n:int,value):
        for _ in range(n):
            a = random.randint(0, self.nrows - 1)
            b = random.randint(a, self.ncols - 1)
            self.Capa[a,b] = value
        return self.Capa

    def gen_random_layers(self,n,value):
        for _ in range(n):
            a = random.randint(0, self.shape()[1] - 1)
            b = random.randint(a, self.shape()[1] - 1)

            pared = (random.randint(0, self.shape()[0] - 1), random.randrange(0, self.shape()[1] - 1))
            self.Capa[pared[0]][a:b] = value
    def gen_one_value(self,nrow:int,ncol:int,value):
        self.Capa[nrow,ncol] = value

    def gen_values(self,nrow_init:int,nrow_fin:int,ncol_init:int,ncol_fin:int,values):
        self.Capa[nrow_init:nrow_fin+1,ncol_init:ncol_fin] = values

    def gen_layer_values(self,colinit:int,colfin:int,rowinit:int,rowfin:int,value):
        self.Capa[rowinit:rowfin+1,colinit:colfin] = value

    def shape(self):
        sh = self.Capa.shape
        try:
            a = sh[1]
        except:
            a = 0
        return (sh[0],a)