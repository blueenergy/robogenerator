'''
    int N; // number of vertices
    int delta[]; // deltas of vertices
    int neg[], pos[]; // unbalanced vertices
    int arcs[][]; // adjacency matrix, counts arcs between vertices
    Vector label[][]; // vectors of labels of arcs (for each vertex pair) 
    int f[][]; // repeated arcs in CPT
    float c[][]; // costs of cheapest arcs or paths
    String cheapestLabel[][]; // labels of cheapest arcs
    boolean defined[][]; // whether path cost is defined between vertices
    int path[][]; // spanning tree of the graph
    float basicCost; // total cost of traversing each arc once
'''
class CPP(object):

    def __init__(self,vertices):
        
        if int(vertices) <= 0 :
            raise Exception,"Graph is empty"
        self.N = vertices
        self.delta = [0]*self.N
        self.defined = [[False for i in range(self.N)] for j in range(self.N)]
        self.label = [['' for i in range(self.N)] for j in range(self.N)]
        self.c = [[ 0 for i in range(self.N)] for j in range(self.N)]
        self.f = [[ 0 for i in range(self.N)] for j in range(self.N)]
        self.arcs = [[ 0 for i in range(self.N)] for j in range(self.N)]
        self.cheapestLabel = [[ ' ' for i in range(self.N)] for j in range(self.N)]
        self.path = [[ 0 for i in range(self.N)] for j in range(self.N)]


        self.basicCost = 0;

    
    def solve(self):
        self.leastCostPaths()
        self.checkValid()
        self.findUnbalanced()
        self.findFeasible()
        while(self.improvements()):
            pass
            
        


    
    def addArc(self,lab, u, v, cost):
        if not self.defined[u][v]:
            self.label[u][v] = ''
        self.label[u][v] =lab 
        self.basicCost += cost
        if not self.defined[u][v] or self.c[u][v] > cost:
            self.c[u][v] = cost
            self.cheapestLabel[u][v] = lab
            self.defined[u][v] = True
            self.path[u][v] = v
        
        self.arcs[u][v] +=1
        self.delta[u] += 1
        self.delta[v] -=1
        return self
    
    def leastCostPaths(self):
        for k in range(self.N):
            for i in range(self.N):
                if self.defined[i][k]:
                    for j in range(self.N):
                        if self.defined[k][j] and (not self.defined[i][j] or self.c[i][j] > (self.c[i][k]+self.c[k][j])):
     
                            self.path[i][j] = self.path[i][k]
                            self.c[i][j] = self.c[i][k]+self.c[k][j]
                            self.defined[i][j] = True
                            if i == j and self.c[i][j] < 0:
                                return #stop on negative cycle
                        
    def checkValid(self):
        for i in range(self.N):
            for j in range(self.N):
                if not self.defined[i][j]:
                    print 'arc from %s to %s is not defined' %(i,j)
                    raise Exception,"Graph is not strongly connected"
                if self.c[i][i] < 0:
                    raise Exception, "Graph has a negative cycle"
        
        
    def cost(self):
        return self.basicCost+self.phi()
    
    def phi(self):
        phi = 0;
        for i in range(self.N):
            for j in range(self.N):
                phi += self.c[i][j]*self.f[i][j];
        return phi;
    
    def findUnbalanced(self):
        nn = 0
        np = 0 #number of vertices of negative/positive delta
        
        for i in range(self.N):
            if self.delta[i] < 0:
                nn+=1
            elif self.delta[i] > 0:
                np+=1
            
        self.neg = [0] * nn
        self.pos = [0] * np
        nn = np = 0
        '''initialise sets'''
        for i in range(self.N): 
            if self.delta[i] < 0:
                self.neg[nn] = i
                nn+=1
            elif self.delta[i] > 0:
                self.pos[np] = i
                np+=1
    
    

    
    def findFeasible(self):
        ''' delete next 3 lines to be faster, but non-reentrant'''

        delta = [0]*self.N
        for i in range(self.N):
            delta[i] = self.delta[i]
        
        for u in range(len(self.neg)):
            i = self.neg[u]
            for v in range(len(self.neg)):
                j = self.pos[v]
                self.f[i][j] = -delta[i] if -delta[i] < delta[j] else delta[j]
                delta[i] += self.f[i][j]
                delta[j] -= self.f[i][j]
            
        
    
    
    def improvements(self):
        residual = CPP(self.N) 
        for u in range(len(self.neg)):
            i = self.neg[u]
            for v in range(len(self.pos)):
                j = self.pos[v]
                residual.addArc(None, i, j, self.c[i][j]);
                if self.f[i][j] != 0:
                    residual.addArc(None, j, i, -self.c[i][j])
            
        '''find a negative cycle'''
        residual.leastCostPaths(); 
        for i in range(self.N): 
            '''cancel the cycle (if any)'''
            if residual.c[i][i] < 0: 
                k= 0
                kunset = True
                u = i
                '''// find k to cancel'''
                while u != i :
                    v = residual.path[u][i];
                    if residual.c[u][v] < 0 and (kunset or k > self.f[v][u]):
                        k = self.f[v][u]
                        kunset = False
                    u=v
                    
                #cancel k along the cycle
                u = i
                while u!=i:
                    v = residual.path[u][i]
                    if residual.c[u][v] < 0:
                        self.f[v][u] -= k
                    else:
                        self.f[u][v] += k;
                 
                return True# have another go
            
        return False# no improvements found
    
    


    def findPath(self,from_node,f):

        for i in  range(self.N):
            if( f[from_node][i] > 0 ):
                return i;
        return None
    

    def printCPT(self,startVertex):
        v = startVertex;
        


        f = [[ 0 for i in range(self.N)] for j in range(self.N)]
        arcs = [[ 0 for i in range(self.N)] for j in range(self.N)]
        for i in range(self.N):
            for j in range(self.N):
                arcs[i][j] = self.arcs[i][j];
                f[i][j] = self.f[i][j];
            
        
        while( True ):
            u = v
            v = self.findPath(u, f)
            if v: 
                #remove path
                f[u][v] = f[u][v]-1
                #break down path into its arcs
                p = self.path[u][v]
                while u!=v:
                    u=p
                    print self.cheapestLabel[u][p]
                    print "Take arc" + self.cheapestLabel[u][p]+" from "+str(u)+" to "+str(p)
                    p = self.path[u][v]


                
            else:
                bridgeVertex = self.path[u][startVertex]
                if arcs[u][bridgeVertex] == 0:
                    '''finished if bridge already used'''
                    break
                v = bridgeVertex
                '''// find an unused arc, using bridge last'''
                for i in range(self.N): 
                    if i != bridgeVertex and arcs[u][i] > 0:
                        v = i
                        break
                '''decrement count of parallel arcs'''
                arcs[u][v] =  arcs[u][v] - 1
                '''use each arc label in turn'''
                #print arcs[u][v]
                print '***'
                print self.label[u][v]
                print "Take arc "+self.label[u][v]\
                    +" from "+str(u)+" to "+str(v)
            
        
    

                    
if __name__=='__main__':
    G = CPP(4)
    G.addArc("aa", 0, 1, 1)
    G.addArc("bb", 0, 2, 1)
    G.addArc("cc", 1, 2, 1)
    G.addArc("dd", 1, 3, 1)
    G.addArc("ee", 2, 3, 1)
    G.addArc("ff", 3, 0, 1)
    
    G.solve()
    G.printCPT(0)
    
    
