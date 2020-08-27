from adjSet import adjSet as Graph
import re
import csv
from collections import Counter

class FilePro():
    def __init__(self, G, cname, root):
        self.__G = G
        self.__pre_csvname = re.search(r'\.[\w\s+/_]*', cname).group() + '_pre.csv'
        self.__csvname = cname
        self.__initV = self.__G.V
        #print(self.__initV,'initV')
        #self.del_leaf()
        print(self.__G.get_adjlen(), 'adjlen')
        '''tarjan'''
        print(self.__G.V)
        self.__dfn, self.__low = [0]*(self.__G.V+1), [0]*(self.__G.V+1)
        self.__index, self.__root = 0, root
        self.__ans = set()                      #保存割点结果
        self.__root_subtree = []                #分割后新生成的点作为该连通片的root结点
        self.__component = dict()               #连通分量信息
        self.__adjlen = self.__G.get_adjlen()
        self.__comp_count = 0 
        '''print(self.__dfn)
        print(self.__low)'''
        # print(self.__G.get_all_edge)
        # print(self.__G.get_all_edge())
    
    '''删除叶子结点，并将结果保存至preXXX.csv中'''
    def del_leaf(self):
        count = 0
        flag = False
        while not flag:
            flag = True
            for v in range(1, self.__initV+1):
                if self.__G.degree(v) <= 1:
                    self.__G.remove_vertex(v)
                    count += 1
                    flag = False
        print(count, '= counter')
        with open(self.__pre_csvname, 'w', newline='') as sf:
            self.svwriter = csv.writer(sf)
            #self.svwriter.writerow([self.__G.V - count])
            self.svwriter.writerows(self.__G.get_all_edge())
 
    '''trajan算法找割点，并分割图'''
    def tarjan(self, v, f):
        print(v)
        self.__index += 1   #记录访问次序
        self.__dfn[v] = self.__low[v] = self.__index
        child = 0
        if f == self.__root and self.__index > 2:   #root要单独处理，除了第一个遍历的子节点外
           self.__root_subtree.append(v)            #其他子树的根节点加入数组中
           #这里要不要生成新的结点
            
        for u in list(self.__G.adj(v)):
            child += 1
            if not self.__dfn[u]:
                self.tarjan(u, v)
                self.__low[v] = min(self.__low[v], self.__low[u])
                if v != self.__root and self.__low[u] >= self.__dfn[v]:
                    self.__ans.add(v)                              #ans中存储的是原图中的割点
                    self.__G.add_vertex(self.__G.get_adjlen(), u)  #添加结点, 新节点的序号是原结点数＋1，并在新节点和u之间连边（确定新节点与子树的连接关系）
                    print(self.__G.get_adjlen()-1, '是新添加的结点')
                    self.__G.remove_edge(v, u)                     #断开原来的连接
                    # print(u)
                    self.__component[self.__adjlen] = v
                    self.__adjlen += 1
                if v == self.__root and child >= 2:
                    self.__ans.add(v)                              #如果根节点是割点，加入ans
                    # print(v,"......")
            else:
                self.__low[v] = min(self.__low[v], self.__dfn[u])
        print(self.__ans)
        print(self.__root_subtree)
        # print(self.__component.keys())
        # 分割图
        # self.comp_divis()
    '''找连通分量'''
    def comp_dfs0(self):
        print(self.__G.get_adjlen(), 'adjlen')
        for i in range(1, self.__G.get_adjlen()):
            pass
        pass
        
    #从某个结点开始进行深度遍历
    def comp_dfs(self, v, u, comp_vis, comp_root): 
        for w in list(self.__G.adj(v)):
            if not comp_vis[w]:
                if w in self.__ans: #这里为何要移动？
                    self.__ans.remove(w)
                comp_vis[w] = 1
                if self.__G.has_edge(w, u):         #换边
                    self.__G.remove_edge(w, u)
                    self.__G.add_edge(w, comp_root)
                self.__comp_count += 1
                self.comp_dfs(w, u, comp_vis, comp_root)
            
    # 判断anser中剩下的结点是否在一个联通分片里
    def comp_dfs2(self, v, comp_vis): 
        for w in list(self.__G.adj(v)):
            if not comp_vis[w]:
                if w in self.__ans:
                    self.__ans.remove(w)
                comp_vis[w] = 1
                self.__comp_count += 1
                self.comp_dfs2(w, comp_vis)
    
    '''根据割点分裂图'''
    def comp_divis(self):
        if len(self.__ans) == 0:
            print("该图没有割点")
            return False
        print(self.__root_subtree, ':subtree_root')        #打印子树的根节点
        print(self.__ans, '~')
        
        #先处理root点，因为之前他没得断开
        for v in self.__root_subtree:
            self.__G.add_vertex(self.__G.get_adjlen(), v)  #添加结点, 并在新节点和u之间连边（确定新节点与子树的连接关系）
            self.__G.remove_edge(v, self.__root)           #断开原来的连接
            self.__component[self.__adjlen] = self.__root
            self.__adjlen += 1
        
        print(self.__component.keys())                          #打印连通分支的根节点
        comp_vis = [0] * ((max(self.__component.keys())) + 1)   #寻找遍历连通分支用，并增加和断开一些连边
        for v in self.__component.keys():
            comp_vis[v] = 1
            self.__comp_count = 1
            u = self.__component[v]     #u应该是之前连接的割点
            comp_root = v
            self.comp_dfs(v, u, comp_vis, comp_root)    
            self.__component[v] = self.__comp_count
        
        #判断ans中剩下的结点是否在一个连通片
        '''
        v = self.__ans.pop()
        print(v)
        comp_vis[v] = 1
        self.__comp_count = 1
        self.comp_dfs2(v, comp_vis)
        
        if len(self.__ans) == 0:
            self.__component[v] = self.__comp_count
            print("剩下的点构成一个连通片")
        '''
        return True
    
    '''返回最大连通片的根节点'''
    def comp_max(self):
        max_k = 1
        for k, v in self.__component.items():
            if v == max(self.__component.values()):
                max_k = k
        print(max_k, "max_comp")
        return max_k

    '''处理三角形'''
    def tri_pre(self):
        pass
    
    def show_information(self):
        print(self.__ans)
        print(self.__component)
        #print(self.__G.V, '=V')
        #print(len(self.__G.get_all_v()))
        #print(self.__G.E, '=E')
        #print(self.__G.get_all_edge())
        #print(len(self.__G.get_all_edge()))
        #print(self.__dfn)
        #print(self.__low)

    
if __name__ == '__main__':
    filename = './dataset/pre_dataset/test.csv'
    '''
    csvname = re.search(r'\.[\w\s+/_]*', filename).group() + '_pre.csv'
    print(csvname)
    '''
    root = 6
    graph = Graph(filename)
    fp = FilePro(graph, filename, root)
    fp.tarjan(root, 0)
    
    fp.comp_divis()
    
    fp.show_information()
    fp.comp_max()
    
    