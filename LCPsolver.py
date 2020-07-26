from adjSet import adjSet as Graph

class LCPsolver:
    def __init__(self, G):
        self.__G = G
        self.__visited = False * (self.__G.get_adjlen() + 1)

    def __dfs(self, v):
        self.__visited[v] = True
        if v not in self.__path:
            self.__path.append(v)
        if len(self.__path) == self.__G.V and self.__path[-1] in self.__G.adj(self.__path[0]):
            print("已找到哈密尔顿圈")
            return True
        
        end = True
        for w in self.__G.adj(v):
            if not self.__visited[w]:   #如果还存在没有访问过的
                end = False
                break
        if end:
            self.__record[v] = self.__record[v] + 1     # 作为不可扩展的尾端结点，record+1
            #print(v)
            #print(self.__record[v])
            return False
        
        #要改
        for w in self.__G.adj(v):
            if not self.__visited[w]:
                next_v = w
        #print(self.__G.adj(v), file = self.fo)
        
        for w in self.__G.adj(v):    
            if not self.__visited[w]:
                #如果不是不可到达的顶点
                #if not self.__unreachable(w):
                    #选择领域中度最小的点加入路径
                if self.__G.degree(w) < self.__G.degree(next_v):
                    next_v = w
        if self.__greedy(next_v):
            return True

        if len(self.__path) != self.__G.V or self.__path[-1] not in self.__G.adj(self.__path[0]):
            self.__rotation_trans()
        
        return False
        
    def __rotation(self):
        v = 0
        max_degree = 0
        for w in self.__G.adj(self.__path[-1]):
            if self.__visited[w]:
                if self.__G.V - self.__path.index(w) != 1:   #这里需不需要检测不可达？
                    if self.__G.degree(w) > max_degree:
                        max_degree = self.__G.degree(w)
                        v = w
        # 还要检查一下是否能进行旋转变换
        # 转置     
        if v == 0:
            print("在第二阶段退出")
            return False
        
        i = self.__path.index(v)+1
        j = self.__G.V
        while(i < j):
            temp = self.__path[i] 
            self.__path[i] = self.__path[j]
            self.__path[j] = temp
            i = i + 1
            j = j - 1
        
if '__name__' == '__main__':
    filename = './dataset/pre_dataset/huck_pre.csv'
    graph = Graph(filename)