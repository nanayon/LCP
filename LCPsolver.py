from adjSet import adjSet as Graph
from FileProcess import FilePro
import random

class LCPsolver:
    def __init__(self, G):
        self.__G = G
        self.__visited = [False] * (self.__G.get_adjlen() + 1)
        self.__record = [0] * (G.V + 1)
        self.__record2 = [0] * (G.V + 1)
        self.__path = []
        self.__stvcounter = 0

    '''深度优先找到一个初始路径'''
    def dfs(self, v):
        self.__visited[v] = True
        
        if v not in self.__path:
            self.__path.append(v)
        
        if len(self.__path) >= self.__G.V*0.5 and self.__G.has_edge(self.__path[-1], self.__path[0]):
            print("找到一个初始圈")
            return True
        
        next_v_list = []
        for w in self.__G.adj(v):
            if not self.__visited[w]:
                next_v_list.append(w)

        next_v = 0
        if len(next_v_list) != 0:
            next_v = random.choice(next_v_list)
        
        if next_v != 0:         #有未被访问的邻接点
            self.dfs(next_v)
        else:
            self.__record[self.__path[-1]] += 1
            self.__rotation()     
        return False

    def __rotation(self):
        rttv_list = []                              #选择转置结点
        for w in self.__G.adj(self.__path[-1]):     #找末端节点的邻居节点
            if self.__visited[w]:
                rttv_list.append(w)
        
        # 还要检查一下是否能进行旋转变换
        if not rttv_list:
            return False
        
        rttv = 0
        #选具体的端点,选出一个就好
        #如果有可到达的端点，直接选这个可到达的，否则选record次数最小的
        for w in rttv_list:   
            i = self.__path.index(w) + 1                    #现在是尾端点节点候选，就是当前w在path中的邻居结点
            if not self.__unreachable(self.__path[i]):      #检测新的尾端点是否可到达，检测到可达顶点就跳出
                rttv = self.__path[i]
                break
            
        # 如果没有可达顶点,我觉得应该退回上一步，换策略
        # 那么就只好将不可达的顶点作为结束顶点，然后祈祷一下，在经过为数不多的转置后能够重新出现可达顶点   
        if not rttv:
            min_record = 3
            min_v = 0
            for w in rttv_list:   #应该是检测在path中w的邻居结点
                i = self.__path.index(w)+1
                if self.__record[self.__path[i]] <= min_record:
                    min_record = self.__record[self.__path[i]]
                    min_v = self.__path[i]
            rttv = min_v
            if min_record >= 3 and self.__stvcounter <= 3:
               self.__stvcounter += 1
               rttv = self.__path[0] #stv
        
        if not rttv:
            if self.__G.has_edge(self.__path[-1], self.__path[0]):
                print("找到一个初始圈")
                return True
            else:
                self.__rotation2()
                '''
                print(self.__G.degree(self.__path[-1]), '=end')
                print(self.__G.adj(self.__path[-1]))
                print(self.__G.degree(self.__path[0]), '=stv')
                print(self.__G.adj(self.__path[0]))'''
                return False
        
        #旋转变换
        i = self.__path.index(rttv)    #现在是尾端点节点候选
        j = len(self.__path) - 1   
        while(i < j):
            temp = self.__path[i] 
            self.__path[i] = self.__path[j]
            self.__path[j] = temp
            i = i + 1
            j = j - 1
        if self.dfs(self.__path[-1]):
            return True
        
    #将初始路径转换为初始圈
    def __rotation2(self):
        self.__stvcounter += 1
        print(self.__path)
        rttv_list = []                              
        for w in self.__G.adj(self.__path[-1]):     #找末端节点的邻居节点
            if self.__visited[w]:
                rttv_list.append(w)
        di_index = len(rttv_list)   
        for w in self.__G.adj(self.__path[0]):
            if self.__visited[w]:
                rttv_list.append(w)
        # print(rttv_list)

        dic_v = dict()
        for w in rttv_list[0: di_index]:  
            i = self.__path.index(w) + 1                    # 现在是尾端点节点候选，就是当前w在path中的邻居结点
            dic_v[self.__path[i]] = True                    # 现在找的是end端的
        for w in rttv_list[di_index:]:                      # start端
            i = self.__path.index(w) - 1
            dic_v[self.__path[i]] = False
                
        rttv = 0
        max_d = 0
        flag = True                         #如果度最大点是尾端结点
        for w in dic_v.keys():
            if self.__record2[w] < 2 and self.__G.degree(w) > max_d:
                max_d = self.__G.degree(w)
                rttv = w
        print(rttv,'= rttv')
        print(self.__G.degree(rttv), '= degree')
        
        if rttv == 0:
            print("可能要换or减点")
            return False
        
        self.__record2[rttv] += 1

        #旋转变换
        if dic_v[rttv]:
            i = self.__path.index(rttv)    #现在是尾端点节点候选
            #print(i)
            j = len(self.__path) - 1   
            #print(j)                     
        else:
            i = 0
            j = self.__path.index(rttv)
            pass
        while(i < j):
            temp = self.__path[i] 
            self.__path[i] = self.__path[j]
            self.__path[j] = temp
            i = i + 1
            j = j - 1
        if self.__G.has_edge(self.__path[-1], self.__path[0]):
            print("找到一个初始圈")
            return True      
        elif self.__stvcounter >= 100:
            return False
        else:
            self.__rotation2()
            #print("没有找到初始圈，可能要回退了")
            return False

        
    def is_hamilton(self, path):
        i = 0
        end = True
        while(i < len(path)-1):
            if not self.__G.has_edge(path[i], path[i+1]):
                print("%d-X-%d" %(path[i], path[i+1]))
                end = False
            i = i + 1
        if end:
            if self.__G.has_edge(path[0],path[-1]):
                   print("成功了！")
            else:
                   print("只能找到路径")
        return end

            
    """检测不可达顶点"""
    def __unreachable(self, v):
        for w in self.__G.adj(v):
            if not self.__visited[w]:
                return False
        return True
    
    def result(self):
        #print(self.__G.get_all_v())
        #print(len(self.__G.get_all_v()))
        print(self.__path)
        print(len(self.__path))
        #self.is_hamilton(self.__a)
        self.is_hamilton(self.__path)

        
if __name__ == '__main__':
    filename = './dataset/pre_dataset/homer_pre.csv'
    root = 13
    graph = Graph(filename)
    fp = FilePro(graph, filename, root)
    fp.tarjan(root, 0)
    fp.comp_divis()
    lcpsol = LCPsolver(graph)
    lcpsol.dfs(64)
    lcpsol.result()