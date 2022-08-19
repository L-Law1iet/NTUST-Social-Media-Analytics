import networkx as nx
import csv
import math
import numpy as np
import matplotlib.pyplot as plt

#讀取資料
Data1 = open("data_train_edge.csv")
#第一列跳過
next(Data1, None)
Graphtype = nx.DiGraph()
G = nx.read_edgelist(Data1,delimiter=",",create_using=Graphtype,nodetype=int)
#threshold根據pair間的平均Link Prediction值來調整
CNo_threshold = 2        #common out neighbors
CNi_threshold = 2        #common in neighbors
JCo_threshold = 0.021    #jaccard coefficient(以common out neighbors計)
JCi_threshold = 0.037    #jaccard coefficient(以common in neighbors計)
ADo_threshold = 0.311    #Adamic-Adar(以common out neighbors計)
ADi_threshold = 0.371    #Adamic-Adar(以common in neighbors計)
PA_threshold = 2625      #preferential attachment

#計算pair間common out(in) neighbors的方法
def common_out_neighbors(g, i, j):
    return set(g.successors(i)).intersection(g.successors(j))

def common_in_neighbors(g, i, j):
    return set(g.predecessors(i)).intersection(g.predecessors(j))

num = -1
with open("predict.csv") as predict:
        #第一列跳過
        rows = csv.reader(predict)
        next(rows, None)
        with open("ans_example.csv",'a+',newline='') as answer:
                w = csv.writer(answer)
                w.writerow(["predict_nodepair_id","ans"])
                for row in rows:
                        vote = 0
                        num = num + 1
                        node0 = int(row[0])
                        node1 = int(row[1])
                        try:
                                #下列計算node0,node1的各個Link Prediction值
                                #如果Link Prediction值有半數超過threshold就認定有hidden edge
                                cno = len(common_out_neighbors(G,node0,node1))
                                cni = len(common_in_neighbors(G,node0,node1))
                                union_size = len(set(G[node0]) | set(G[node1]))
                                jco = cno/union_size
                                jci = cni/union_size
                                ado = sum(1 / math.log(G.degree(w)) for w in common_out_neighbors(G, node0, node1))
                                adi = sum(1 / math.log(G.degree(w)) for w in common_in_neighbors(G, node0, node1))
                                pa = G.degree(node0) * G.degree(node1)
                                if cno>=CNo_threshold:
                                        vote = vote + 1
                                if cni>=CNi_threshold:
                                        vote = vote + 1
                                if jco>=JCo_threshold:
                                        vote = vote + 1
                                if jci>=JCi_threshold:
                                        vote = vote + 1
                                if ado>=ADo_threshold:
                                        vote = vote + 1
                                if adi>=ADi_threshold:
                                        vote = vote + 1
                                if pa>=PA_threshold:
                                        vote = vote + 1
                                if vote>=4:
                                        w.writerow([num,'1'])
                                else:
                                        w.writerow([num,'0'])
                        except:
                                w.writerow([num,'0'])

#算每個pair間的平均preferential attachment
# pa = 0
# count = 0
# for i in range(0,1003):
#         for t in range(0,1003):
#                 try:
#                         pa = pa + G.degree(i) * G.degree(t)
#                         count = count + 1
#                 except:
#                         pass
# print(pa/count) #答案為1749.9422300843505

#算每個pair間的平均Adamic-Adar
# ad = 0.0
# count = 0
# for i in range(0,1003):
#         for t in range(0,1003):
#                 try:
#                         ad = ad + sum(1 / math.log(G.degree(w)) for w in common_in_neighbors(G, i, t))
#                         count = count + 1
#                 except:
#                         pass
# print(ad/count) #答案為out:0.20722406899356252，in:0.24751035558514717


# #算每個pair間的平均common neighbor
# count = 0
# S = 0
# for i in range(0,1003):
#         for t in range(0,1003):
#                 try:
#                         S = S + len(common_in_neighbors(G, i, t))
#                         count = count + 1
#                 except:
#                         pass
# print(S/count) #答案為out:0.9613292015339514，in:1.1924151371063185

#算每個pair間的平均jaccard coefficient
# count = 0
# S = 0
# for i in range(0,1003):
#         for t in range(0,1003):
#                 try:
#                         union_size = len(set(G[i]) | set(G[t]))
#                         S = S + (len(common_out_neighbors(G, i, t))/union_size)
#                         count = count + 1
#                 except:
#                         pass
# print(S/count) #答案為out:0.014157726085440503，in:0.02435783330635175

