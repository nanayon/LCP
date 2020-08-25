import re
import csv

class FileOP():
    def __init__(self, filename):
        self.lines = None
        self.newline = []
        with open(filename, 'r') as f:
            self.lines = f.readlines()

        # self.dele_op()
        # self.mtx_op()
        self.dip_op()
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

    '''删除第三个数字'''
    def mtx_op(self):
        for each_line in self.lines[0: ]:
            line = re.search('\d+\s+\d+', each_line).group(0)
            a, b = (int(i) for i in line.split())
            self.newline.append([a, b]) 

    '''处理DIP文件'''
    def dip_op(self):
        id_dic = dict()
        pid = 1
        for each_line in self.lines[0: ]:
            line = re.search('DIP-([0-9]+)[\w:_|]+[\s]+DIP-([0-9]+)[\w:_|]+', each_line)
            if line == None:
                continue
            
            a = line.group(1)
            if a in id_dic.keys():
                pass
            else:
                id_dic[a] = pid
                pid += 1
                
            b = line.group(2)
            if b in id_dic.keys():
                pass
            else:
                id_dic[b] = pid
                pid += 1
                
            self.newline.append([id_dic[a], id_dic[b]])
            
if __name__ == '__main__':
    filename = './dataset/DIP/Mmusc20160114CR.txt'
    fileop = FileOP(filename)
