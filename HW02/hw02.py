import networkx as nx
import csv
from networkx.algorithms import community

#讀取資料
Data1 = open("train.csv")
#第一列跳過
next(Data1, None)
Graphtype = nx.Graph()
G = nx.read_edgelist(Data1,delimiter=",",create_using=Graphtype,nodetype=int)

#使用Louvain演算法計算Community,並存到名為partition的dictionary
partition = community.louvain_communities(G,seed=1,resolution=0.3) #0.5 0.4 0.77666 0.3 0.76666

num = -1
same = 0
with open("test.csv") as predict:
        #第一列跳過
        rows = csv.reader(predict)
        next(rows, None)
        with open("ans.csv",'a+',newline='') as answer:
                w = csv.writer(answer)
                w.writerow(["Id","Category"])
                for row in rows:
                        num = num + 1
                        node0 = int(row[1])
                        node1 = int(row[2])
                        for i in range(0,len(partition)):
                            if node0 in partition[i] and node1 in partition[i]:
                                same = 1
                            else:
                                pass
                        if same == 1:
                            w.writerow([num,'1'])
                        else:
                            w.writerow([num,'0'])
                        same = 0
                        #判斷兩個node的community是否相同