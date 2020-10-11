from adjSet import adjSet as Graph
from FileProcess import FilePro

'''获取每次的结果，装入circle_list中'''
def get_cir_list(filename):
    filename = './dataset/result/'+ fname +'.csv'
    lines = None
    with open(filename, 'r') as fcsv:
        lines = fcsv.readlines()
    
    # 获取全部(50)次运行结果
    circle_list = []    
    for i in range(0, 50):
        strc = str(lines[i].split(",")[2]).replace("[", "").replace("]", "").replace("\n", "")
        rlist = strc.split("  ")     #得到['1', '2', '3', ... , 'n'], 注意这里是有两个空格
        rlist = [int(rlist[i]) for i in range(0,len(rlist))]  #生成器写法换成(),但是获取其中的数据似乎还要一个函数？
        circle_list.append(rlist)
    return circle_list

'''每个顶点出现的次数'''
def count_frequency(circle_list, filename, graph, compv):
    
    dictv = dict()
    for v in compv:
        dictv[v] = 0;
    
    for clist in circle_list:
        for v in clist:
            dictv[v] += 1

    fcsv = open(filename, 'a')
    # fcsv.writelines([fname, '------------------Count the number of occurrences of each point------------------\n'])
    # fcsv.writelines([fname, 'id, degree, frequency\n'])
    # for item in dictv.items():
    #     fcsv.writelines([str(item[0]), ',', str(graph.degree(item[0])), ',', str(item[1]), '\n'])
    fcsv.close()

'''统计同一个圈中没有出现的顶点的序号和其度数'''
def count_unappear_vertex(circle_list, filename, graph, compv):
    
    fcsv = open(filename, 'a')
    # fcsv.writelines(['------------------Calculate points that do not appear in each run------------------\n'])
    # fcsv.writelines(['lenth, unappear_vertex(degree)\n'])
    
    for clist in circle_list:
        unappear_v_list = list(set(compv) - set(clist))
        s = str(len(clist)) + ','
        if len(unappear_v_list) == 0:
            s += 'null'
        else:
            for v in unappear_v_list:
               s += str(v) + '('+ str(graph.degree(v)) + ') '   
               
        s +='\n'
        
        print(s)
        fcsv.writelines([s])
    
    fcsv.close()

if __name__ == '__main__':
    fname_list = ['anna'] 
    # fname_list = ['adjnoun', 'lesmis', 'celegansneural', 'david', 'huck'] 

    for fname in fname_list:
        filename = './dataset/result/'+ fname +'.csv'
        graphname = './dataset/pre_dataset/'+ fname +'_pre.csv'
        
        # 获取图原始数据
        graph = Graph(graphname)

        # 获取circle_list
        circle_list = get_cir_list(filename)
                
        # 最大连通分量的所有点
        fp = FilePro(graph, filename, 18)
        compv = fp.get_max_component(18)  #返回最大连通片的所有顶点这个root值取不到就要改
        
        # 统计每个点在圈中出现的次数
        # count_frequency(circle_list, filename, graph, compv)
        
        # 统计同一个圈中没有出现的顶点的序号和其度数
        count_unappear_vertex(circle_list, filename, graph, compv)
        

        

        
        