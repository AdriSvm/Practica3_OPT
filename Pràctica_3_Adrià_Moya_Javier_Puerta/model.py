import numpy as np, random
class Capa():
    def __init__(self, nrow:int,ncol:int,init_value:[int,float,str,bool],matrix=None):
        """
        Layer implementation in an Object Programming oriented way, to make easier the creation of new layers and its
        modifications.
        The layer can be created through 2 methods:
            -Specificating the nrows, ncols, and the init value of the layer or through a matrix created before
        Then you can see a few method to make easier the modifications of the layer
        """
        if matrix is not None:
            self.Capa=matrix
            self.nrows = self.shape()[0]
            self.ncols = self.shape()[0]
        else:
            self.Capa = np.array([[init_value for _ in range(ncol)] for _ in range(nrow)]) # Main object with the layer
            self.nrows = nrow
            self.ncols = ncol

    def change_value(self,nrow:int,ncol:int,value):
        """
        Change the value of a specific [nrow,ncol] cel with a value
        """
        try:
            self.Capa[nrow,ncol] = value
            return True
        except:
            return False

    def gen_random_samples(self,n:int,value):
        """
        Generate random cels of the layer, to set random positions with a specific value
        """
        for _ in range(n):
            a = random.randint(0, self.nrows - 1)
            b = random.randint(a, self.ncols - 1)
            self.Capa[a,b] = value
        return self.Capa

    def gen_random_layers(self,n,value):
        """
        Generate n random layers modified to a value. We use this to create the obstacles
        """
        for _ in range(n):
            a = random.randint(0, self.shape()[1] - 1)
            b = random.randint(a, self.shape()[1] - 1)

            pared = (random.randint(0, self.shape()[0] - 1), random.randrange(0, self.shape()[1] - 1))
            self.Capa[pared[0]][a:b] = value
    def gen_one_value(self,nrow:int,ncol:int,value):
        """
        Set one specific value to a specific [nrow,ncol] cel
        """
        self.Capa[nrow,ncol] = value

    def gen_values(self,nrow_init:int,nrow_fin:int,ncol_init:int,ncol_fin:int,values):
        """
        Set a specific range of cels to a specific value (values)
        """
        self.Capa[nrow_init:nrow_fin+1,ncol_init:ncol_fin] = values

    def gen_layer_values(self,colinit:int,colfin:int,rowinit:int,rowfin:int,value):
        """
        Sane as gen_values, IDK why I reimplemented it
        I think at first I created one method for specific cel changing values and for a range of values and then
        I realised that it can be made with only one method.
        """
        self.Capa[rowinit:rowfin+1,colinit:colfin] = value

    def shape(self):
        """
        Easy use of .shape numpy.array method
        """
        sh = self.Capa.shape
        try:
            a = sh[1]
        except:
            a = 0
        return (sh[0],a)