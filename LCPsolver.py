from adjSet import adjSet as Graph
from FileProcess import FilePro
import random
from goto import with_goto

class LCPsolver:
    def __init__(self, G):
        self.__G = G
        self.__visited = [False] * (self.__G.get_adjlen() + 1)
        self.__comp_vist = [False] * (self.__G.get_adjlen() + 1)
        self.__ep_vist = [False] * (self.__G.get_adjlen() + 1)
        self.__ep_father = [0] * (self.__G.get_adjlen() + 1)
        self.__record = [0] * (G.V + 1)
        self.__record2 = [0] * (G.V + 1)
        self.__path = []
        self.__path2 = []
        self.__insert_path = []
        self.__comp_v = set()
        self.__stvcounter = 0
        self.__a = 1 #控制长度的参数
        self.__cycle = set()
        self.__remain = set()
        
    def reset(self):
        self.__visited = [False] * (self.__G.get_adjlen() + 1)
        self.__record = [1] * (self.__G.V + 1)
        self.__record2 = [0] * (self.__G.V + 1)
        self.__path = []
        self.__stvcounter = 0

    def set_a(self, value):
        self.__a = value
        
    '''深度优先找到一个初始路径'''
    def dfs(self, v):
        self.__visited[v] = True
        
        if v not in self.__path:
            self.__path.append(v)
        
        if len(self.__path) >= self.__G.get_adjlen() * self.__a and self.__G.has_edge(self.__path[-1], self.__path[0]):
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
            
        if self.__G.has_edge(self.__path[-1], self.__path[0]):
            return True
        
        return False
    
    '''获取连通片内的所有点'''
    def comp_dfs(self, v):
        self.__comp_vist[v] = True
        self.__comp_v.add(v)
        for w in self.__G.adj(v):
            if not self.__comp_vist[w]:
                self.comp_dfs(w)
    
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
    
    '''按度的大小排列'''
    def __sort_degree(self):
        dic = {}
        for i in range(1, self.__G.V):
            dic[i] = self.__G.degree(i)
        list_v = sorted(dic.items(), key = lambda kv:kv[1], reverse = True)
            
        return list_v
    '''想办法转置度最大的结点到首末端'''
    '''把剩下的结点转化为圈'''
    
    '''扩展圈'''
    def extend_circle(self):
        self.__cycle = set(self.__path)
        self.__remain = set(self.__comp_v) - self.__cycle
        self.__path2 = self.__path[:]
        st = set()
        end = set()
        for i in range(0, len(self.__path)):
            print(i, ' = i ********')
            print(self.__path[i],' = path[i]')
            flag = False
            epath = []
            st = self.__G.adj(self.__path[i]) & self.__remain
            
            if i != len(self.__path) - 1:
                end = self.__G.adj(self.__path[i+1]) & self.__remain
            else:
                end = self.__G.adj(self.__path[0]) & self.__remain
                
            if(len(st)==0 or len(end)==0):
                print("nonono")
                continue
            else:
                print(st, "=st")
                print(end, "=end")
                v = 0
                counter = 0
                list_ev = []
                for w in st:
                    if flag:
                        print("跳出循环")
                        break
                    for u in end:
                        if w != u:
                            self.__ep_vist = self.__visited[:]
                            self.__ep_father = [0] * (self.__G.get_adjlen() + 1)
                            counter = self.__ep_dfs(w, u, self.__path[i])
                            print(counter,'=counter')
                            if counter != 0:
                                print('扩展了%d个点' %(counter))
                                flag = True
                                break
                        else:
                            list_ev.append(w)   
                
                if counter == 0 and len(list_ev) != 0:
                    v = 0
                    for j in list_ev:
                        if j not in self.__cycle:
                            v = j
                            break
                    if v != 0:
                        self.__visited[v] = True
                        self.__remain.discard(v)
                        self.__cycle.add(v)
                        self.__path2.insert(self.__path2.index(self.__path[i])+1, v)
                        counter = 1
                        print(v, '=v,扩展了1个点')        
            
    def __ep_dfs(self, w, u, stv):
        self.__ep_vist[w] = True
        counter = 0
        epath = []
        for v in self.__G.adj(w):
            if self.__ep_vist[v]:   
                continue
            self.__ep_father[v] = w    
            
            if u == v:
                self.__visited[u] = True
                self.__cycle.add(u)
                self.__remain.discard(u)
                counter += 1
                epath.append(u)
                m = self.__ep_father[u]
                while(m != 0):
                    epath.append(m)
                    self.__visited[m] = True
                    self.__cycle.add(m)
                    self.__remain.discard(m)
                    m = self.__ep_father[m]
                    counter += 1
                if counter != 0:
                    epath.reverse()
                    print(epath)
                    x = 1
                    for i in epath:
                        self.__path2.insert(self.__path2.index(stv)+x, i)
                        x += 1
                    #print(counter, '=counter')
                return counter
            
            if not self.__ep_vist[v]:
               counter = self.__ep_dfs(v, u, stv)
               #print(counter, '===counter')
               return counter
        return counter
    
    def __find_path(self, w, u, epath):
        self.__visted[w] = True
        if w not in epath:
            epath.append(w)
        if u in epath:
            #要记录一下
            return True
        
        next_v_list = []
        for x in self.__G.adj(w):
            if not self.__visited[w]:
                next_v_list.append(w)
        
        next_v = 0
        if len(next_v_list) != 0:
            next_v = random.choice(next_v_list)
        
        if next_v !=0:
            self.__find_path(next_v, u)

        return False
            
    '''用BFS搜索v和w之间有没有可以扩展的路径'''
    def __bfs(self, v, w):
        pass
    
    '''用DFS搜索v和w之间有没有可以扩展的路径'''
    def __dfs(self, v, w):
        lenv = 0
        for u in self.__G.adj(v):
            if not self.__visited[u]:
                self.__visited[u] = True
                self.__insert_path.append(u)                    
                if self.__G.has_edge(u, w): 
                    print("great@_@")
                    print(self.__insert_path, '=ipath')
                    return
                self.__dfs(u, w)

    #将初始路径转换为初始圈
    def __rotation2(self):
        self.__stvcounter += 1
        #print(self.__path)
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
 
        if rttv == 0:
            return False
        
        self.__record2[rttv] += 1

        #旋转变换
        if dic_v[rttv]:
            i = self.__path.index(rttv)    #现在是尾端点节点候选
            j = len(self.__path) - 1   
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
        print(self.__path2)
        print(len(self.__path2))
        #print(self.__extend_circle())
        #self.is_hamilton(self.__a)
        #self.is_hamilton(self.__path2)
        setp = set()
        for i in range(0, len(self.__visited)):
            if self.__visited[i] == True:
                setp.add(i)
        print(setp - set(self.__path))
                
        
if __name__ == '__main__':
    filename = './dataset/pre_dataset/football_pre.csv'
    root = 8
    counter = 1
    a = 1   #参数
    graph = Graph(filename)
    fp = FilePro(graph, filename, root)
    '''
    fp.find_comp()          #找连通分片
    root = fp.fcomp_max()   #找最大连通分片根节点
    fp.set_root(root)       #设置新的根节点
    '''
    fp.tarjan(root, 0)
    fp.comp_divis()
    comp_root = fp.comp_max()
    
    lcpsol = LCPsolver(graph)
    lcpsol.comp_dfs(comp_root)
    flag = lcpsol.dfs(comp_root)
    while not flag and counter <= 90:
        for i in range(0, 10):
            lcpsol.reset()
            flag = lcpsol.dfs(comp_root)
            counter += 1
        a -= 0.1
        lcpsol.set_a(a)
        
    print(a)
    print(flag)
    print(counter)
    
    lcpsol.extend_circle()
    print(comp_root,'232')
    lcpsol.result()
    