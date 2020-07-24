import re
import csv

class FileOP():
    def __init__(self, filename):
        self.lines = None
        self.newline = []
        with open(filename, 'r') as f:
            self.lines = f.readlines()
        
        self.dele_op()
        print(self.newline)

        self.csvname = re.search(r'\.[\w\s+/_]*', filename).group() + '.csv'
        print(self.csvname)
        with open(self.csvname, 'w', newline='') as sf:
            self.svwriter = csv.writer(sf)
            self.svwriter.writerows(self.newline)
    
    '''删除文件中字母e'''
    def dele_op(self):
        for each_line in self.lines[0: ]:
            line = re.search('[^e](.*)', each_line).group(0)
            a, b = (int(i) for i in line.split())
            self.newline.append([a, b])     
             
    '''处理.mtx文件'''
    def mtx_op(self):
        pass
    
    '''处理.gml文件'''
    def gml_op(self):
        pass
    
    
if __name__ == '__main__':
    filename = './dataset/DIMACS/huck'
    fileop = FileOP(filename)
