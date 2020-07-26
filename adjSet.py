class adjSet():
    def __init__(self, filename):
        lines = None
        with open(filename, 'r') as f:
            lines = f.readlines()
        if not lines:
            raise ValueError('Expected something from input file!')
        
        #self.__V, self.__E = (int(i) for i in lines[0].split(' '))
        self.__V = int(lines[0])
        self.__E = 0
        self.__edgelist = []    #记录所有的边
        self.__vset = set(range(1, self.__V+1))
        self.__adj = [set() for _ in range(self.__V+1)]
        for each_line in lines[1:]:
            a, b = (int(i) for i in each_line.split(','))
            if a == b:
                continue
            if b in self.__adj[a]:
                continue
            self.__adj[a].add(b)
            self.__adj[b].add(a)
            self.__E += 1
            self.__edgelist.append([a, b])
        print(self.__E,"=E")

    # 记录真实的顶点数
    @property
    def V(self):
        return self.__V
    
    def get_all_v(self):
        return self.__vset
    
    @property
    def E(self):
        return self.__E
    
    def get_all_edge(self):
        return self.__edgelist
    
    '''返回邻接表大小的长度，而不是点的个数'''
    def get_adjlen(self):
        return len(self.__adj)

    
    #这里adj是一个点,和它的一条连边
    def add_vertex(self, v, adj_v):
        self.__adj.append(set())
        if (v == len(self.__adj) - 1):
            self.__adj[v].add(adj_v)
            self.__adj[adj_v].add(v)
            self.__V += 1
            self.__vset.add(v)
            self.__E += 1
            self.__edgelist.append([v, adj_v])

    
    def add_edge(self, v, u):
        if (not self.has_edge(u, v)):
            self.__adj[v].add(u)
            self.__adj[u].add(v)
            self.__E += 1
            self.__edgelist.append([u, v])
        
    #判断两顶点间是否有边存在
    def has_edge(self, v, w):
        return w in self.__adj[v]
    
    #返回所有邻接结点
    def adj(self, v):
        return self.__adj[v]
        
    def degree(self, v):
        return len(self.adj(v))
    
    #删除边
    def remove_edge(self, v, w):
        if w in self.__adj[v]:
            self.__adj[v].remove(w)
        if v in self.__adj[w]:
            self.__adj[w].remove(v)
        if [w, v] in self.__edgelist:
            self.__edgelist.remove([w, v])
            self.__E -= 1
        else:
            self.__edgelist.remove([v, w])
            self.__E -= 1

    #删除点,并删除与所有这个点相邻的边
    def remove_vertex(self, v):
        if v in self.__vset:
            self.__vset.discard(v)
            self.V -= 1
        for w in list(self.__adj[v]):
            self.__adj[v].remove(w)
            self.__adj[w].remove(v)
            self.__E -= 1
            if [w, v] in self.__edgelist:
                self.__edgelist.remove([w, v])
            else:
                self.__edgelist.remove([v, w])
    
    #将其他点的边转接到点v上，然后删除list_v中的点
    def merge_vertex(self, v, list_v):
        for w in list_v:
            for u in self.__adj[w]:
                if u not in self.__adj[v] and u not in list_v and u != v:
                    self.__adj[v].add(u)         #向v的邻域添加点
                    self.__adj[u].add(v)
            self.remove_vertex(w)               #删除点w和与之关联的边
    
    def __str__(self):
        res = ['V = {}, E = {}'.format(self.__V, self.__E)]
        for v in range(1, self.__V + 1):
            res.append('{}: {}'.format(v, ' '.join(str(w) for w in self.__adj[v])))
        return '\n'.join(res)
            
    def __repr__(self):
        return self.__str__()
    
if __name__ == '__main__':
    filename = './dataset/pre_dataset/test.csv'
    adj_list = adjSet(filename)
    print(adj_list)