import networkx as nx
import csv
import math
import numpy as np
import matplotlib.pyplot as plt

#讀取資料
Data1 = open("traing.csv")
#第一列跳過
next(Data1, None)
Graphtype = nx.Graph()
G = nx.parse_edgelist(Data1,delimiter=",",create_using=Graphtype,nodetype=int)
# edges  = list(nx.non_edges(G))
# np.savetxt("numpy_test.csv", edges, delimiter =",",fmt ='% s')

#threshold根據pair間的平均Link Prediction值來調整
CN_threshold = 1        #common out neighbors
JC_threshold = 0.004 #4    #jaccard coefficient(以common out neighbors計)
AD_threshold = 0.015 #15  #Adamic-Adar(以common out neighbors計)
PA_threshold = 82    #82   #preferential attachment

# #計算pair間common out(in) neighbors的方法
def common_out_neighbors(g, i, j):
    return set(g.successors(i)).intersection(g.successors(j))

def common_in_neighbors(g, i, j):
    return set(g.predecessors(i)).intersection(g.predecessors(j))

num = -1
correct = 0
wrong = 0
with open("test.csv") as predict:
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
                        corr_ans = int(row[2])
                        try:
                                #下列計算node0,node1的各個Link Prediction值
                                #如果Link Prediction值有半數超過threshold就認定有hidden edge
                                cn = len(sorted(nx.common_neighbors(G, node0, node1)))
                                union_size = len(set(G[node0]) | set(G[node1]))
                                jc = cn/union_size
                                ad = sum(1 / math.log(G.degree(w)) for w in nx.common_neighbors(G, node0, node1))
                                pa = G.degree(node0) * G.degree(node1)
                                if cn>=CN_threshold:
                                        vote = vote + 1
                                if jc>=JC_threshold:
                                        vote = vote + 1
                                if ad>=AD_threshold:
                                        vote = vote + 1
                                if pa>=PA_threshold:
                                        vote = vote + 1
                                if vote>=1:
                                        w.writerow([num,'1'])
                                        if corr_ans == 1:
                                                correct = correct + 1
                                        else:
                                                wrong = wrong + 1
                                else:
                                        w.writerow([num,'0'])
                                        if corr_ans == 0:
                                                correct = correct + 1
                                        else:
                                                wrong = wrong + 1
                        except:
                                w.writerow([num,'0'])
                                if corr_ans == 0:
                                        correct = correct + 1
                                else:
                                        wrong = wrong + 1
print(correct)
print(wrong)

# #算每個pair間的平均preferential attachment
# pa = 0
# count = 0
# for i in range(0,7125):
#         for t in range(0,7125):
#                 try:
#                         pa = pa + G.degree(i) * G.degree(t)
#                         count = count + 1
#                 except:
#                         pass
# print(pa/count) #答案為82.7319068319549

# # 算每個pair間的平均Adamic-Adar
# ad = 0.0
# count = 0
# for i in range(0,7125):
#         for t in range(0,7125):
#                 try:
#                         ad = ad + sum(1 / math.log(G.degree(w)) for w in nx.common_neighbors(G, i, t))
#                         count = count + 1
#                 except:
#                         pass
# print(ad/count) #答案為out:0.015454849886297459


# #算每個pair間的平均common neighbor
# count = 0
# S = 0
# for i in range(0,7125):
#         for t in range(0,7125):
#                 try:
#                         S = S + len(sorted(nx.common_neighbors(G, i, t)))
#                         count = count + 1
#                 except:
#                         pass
# print(S/count) #答案為0.06747,S = 3426125

# # 算每個pair間的平均jaccard coefficient
# count = 0
# S = 0
# for i in range(0,7125):
#         for t in range(0,7125):
#                 try:
#                         union_size = len(set(G[i]) | set(G[t]))
#                         S = S + (len(sorted(nx.common_neighbors(G, i, t)))/union_size)
#                         count = count + 1
#                 except:
#                         pass
# print(S/count) #答案為0.00421482853041066

# S = 0
# K = 0
# for i in range(0,7125):
#         for t in range(0,7125):
#                 try:
#                         S = S + len(common_out_neighbors(G, i, t))
#                 except:
#                         pass
# print(S) #答案為out:1124451

# for o in range(0,7125):
#         for p in range(0,7125):
#                 try:
#                         K = K + len(common_in_neighbors(G, o, p))
#                 except:
#                         pass
# print(K) #答案為in:1587830
