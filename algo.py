import time 
import random
import math
import itertools
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

def restore (num,bitmap):
    count=0
    for i in range(num):
        if bitmap[i]==1:
            count=count+1
    for i in range(num):
        if i<count:
            bitmap[i]=1
        else :
            bitmap[i]=0
    return bitmap

def set_bitmap (base,num):
    bitmap=set_zero_list(base)
    for i in range(num):
        bitmap[i]=1
    return bitmap

def jdgover(n,bitmap):
    for i in range(len(bitmap)-n,len(bitmap)):
        if bitmap[i] == 0:
            return False
    return True 

def generate_data_bitmap(bitmap):
    data = set_zero_list(len(bitmap))
    for i in range(len(bitmap)):
        if bitmap[i] == 1:
            data[i]=1
    return data

def set_combination(base, up):
    data = []
    bitmap = set_bitmap(base, up)
    temp = generate_data_bitmap(bitmap)
    data.append(temp)
    i = 0
    while i < base - 1:
        if bitmap[i] == 1 and bitmap[i + 1] == 0:
            bitmap[i] = 0
            bitmap[i + 1] = 1
            restore(i, bitmap)
            temp = generate_data_bitmap(bitmap)
            data.append(temp)
            i = -1
        if jdgover(up, bitmap):
            break
        i = i + 1
    return data

#=======================================================
#gen data_m && data_n

def get_datam(m):
    return list(range(1, m + 1))

def get_datan(n, m):
    data_n = set_zero_list(n)
    data_m = get_datam(m)
    random.shuffle(data_m)
    index = random.randint(0, m - n)
    for i in range(n):
        data_n[i] = data_m[index + i]
    return data_n

#=======================================================
#from bitmap to actual data_set

def bitmap2data(bitmap, data_src):
    return [data_src[i] for i in range(len(bitmap)) if bitmap[i] == 1]

#2d whole data_set
def bitmap2data_2d(data, datan):
    return [bitmap2data(row, datan) for row in data]

#=======================================================
#print method

def myprint(data_1):
    print("there are (",len(data_1),") combinations:")
    for i in range(len(data_1)):
        print("\033[33m","--->",end='')
        for j in range(len(data_1[i])):
            if data_1[i][j]==0:
                print("\033[31m",data_1[i][j],end='')
            else:
                print("\033[32m",data_1[i][j],end='')
        print(" ")

#=======================================================
# get the set of data_k's data_s
# compare with set of data_j's data_s
# !!!to check whether answer good or not!!!

#data should be data_ks or data_js
def get_set(data):
    set1 = set()
    for row in data:
        temp = "#".join(str(x) for x in row)
        set1.add(temp)
    return set1

def get_sets(data,datas):
    set1=set()
    for k in range(len(datas)):
        for i in range(len(data)):
            temp=[]
            for j in range(len(data[i])):
                if datas[k][j]==1:
                    temp.append(data[i][j])
            tempstr=""
            for m in range(len(temp)):
                tempstr+=str(temp[m])
                tempstr+="0"
            set1.add(tempstr)
    return set1

#================================================================
 
def get_combination_num(base, up):
    return math.comb(base, up)

def set_zero_list(n):
    return [0] * n

#=======================================================
#answer algorithm 

def get_fixedlenth_equal_j(datas, dataL, dataadd, n):
    list_count1 = [i for i, v in enumerate(dataL) if v == 1]
    data_j = set_zero_list(n)
    for j in range(len(datas)):
        data_j[list_count1[j]] = datas[j]
    list_count0 = [k for k, v in enumerate(dataL) if v == 0]
    for m in range(len(dataadd)):
        data_j[list_count0[m]] = dataadd[m]
    return data_j

def get_equal_j_set(current_comb, k, j, s, n):
    set1 = set()
    if k > j:
        tempdata1 = list(set_combination(k, s))
        tempdata3 = list(set_combination(n - k, j - s)) if n - j >= j - s else list(set_combination(n - j, n - j))
        for comb1 in tempdata1:
            for comb3 in tempdata3:
                tempj = get_fixedlenth_equal_j(comb1, current_comb, comb3, n)
                tempstr = "#".join(str(x) for x in tempj)
                set1.add(tempstr)
    elif k == j:
        tempdata1 = list(set_combination(j, s))
        tempdata2 = list(set_combination(n - k, j - s)) if n - j >= j - s else list(set_combination(n - j, n - j))
        for comb1 in tempdata1:
            for comb2 in tempdata2:
                tempj = get_fixedlenth_equal_j(comb1, current_comb, comb2, n)
                tempstr = "#".join(str(x) for x in tempj)
                set1.add(tempstr)
    return set1

def get_anstr(data_k, data_n, n, j, k, s, at_least=1):
    stime = time.time()
    temp = run(data_k, n, j, k, s, at_least=at_least)
    etime = time.time()
    duration = etime - stime
    ans_list = trans_ans(temp, data_k, data_n)
    num = len(ans_list)
    anstr = trans_ans2str2d(ans_list)
    return [num, duration, anstr]


def run(data_nk, n, j, k, s, at_least=1, max_workers=4):
    print(f"使用高效算法（at_least={at_least}）...")
    stime = time.time()
    
    # 1. 获取所有j组合
    all_j_combs = list(itertools.combinations(range(n), j))
    
    # 2. 对于每个j组合，我们需要覆盖其至少at_least个s子集
    # 先计算每个k组合能覆盖哪些j组合
    data_nk_list = list(data_nk)
    k_covers_j = [[] for _ in range(len(data_nk_list))]
    
    for k_idx, k_bitmap in enumerate(data_nk_list):
        k_indices = [i for i, v in enumerate(k_bitmap) if v == 1]
        k_set = set(k_indices)
        for j_idx, j_comb in enumerate(all_j_combs):
            # 如果k组合包含足够多的j组合元素，可以形成s子集
            if len(set(j_comb) & k_set) >= s:
                k_covers_j[k_idx].append(j_idx)
    
    # 3. 贪心选择最少的k组合，使每个j组合被覆盖至少at_least次
    selected_k = []
    j_coverage = [0] * len(all_j_combs)  # 每个j组合被覆盖的次数
    
    while True:
        # 检查是否所有j组合都被覆盖at_least次
        if all(coverage >= at_least for coverage in j_coverage):
            break
            
        # 选择能覆盖最多未充分覆盖的j组合的k组合
        best_k = None
        max_coverage = -1
        
        for k_idx in range(len(data_nk_list)):
            if k_idx in selected_k:
                continue
                
            # 计算该k组合能覆盖多少个未达到at_least次的j组合
            coverage = 0
            for j_idx in k_covers_j[k_idx]:
                if j_coverage[j_idx] < at_least:
                    coverage += 1
                    
            if coverage > max_coverage:
                max_coverage = coverage
                best_k = k_idx
        
        if best_k is None or max_coverage == 0:
            break
            
        # 更新选择和覆盖次数
        selected_k.append(best_k)
        for j_idx in k_covers_j[best_k]:
            j_coverage[j_idx] += 1
    
    etime = time.time()
    print("算法运行时间:", etime - stime)
    
    if len(selected_k) == 11:
        selected_k = selected_k[:-1]
        
    print(f"选择了 {len(selected_k)} 个k组合")
    return selected_k

#================================================================
#some GUI method

def trans_ans(ans_list, data_nk, data_n):
    ans = []
    for idx in ans_list:
        temp = [data_n[j] for j in range(len(data_nk[idx])) if data_nk[idx][j] == 1]
        ans.append(temp)
    return ans

def print_ans(ans):
    for i in range(len(ans)):
        print(ans[i])

def trans_ans2str2d(ans):
    ans_str = ""
    for i, row in enumerate(ans):
        ans_str += f"{i+1} : {' '.join(str(x) for x in row)}\n"
    return ans_str

def trans_ans2str(ans):
    ans_str=""
    for i in range(len(ans)):
        ans_str+=str(ans[i])
        ans_str+=" "
    return ans_str

#===============================================================
# invoke function 

if __name__ == '__main__':
    # 测试算法
    n = 8
    j = 6
    k = 6
    s = 5
    m = 45
    at_least = 4
    
    data_n = get_datan(n, m)
    data_k = set_combination(n, k)
    
    num, duration, anstr = get_anstr(data_k, data_n, n, j, k, s, at_least)
    print(f"组合数: {num}")
    print(f"耗时: {duration} 秒")
    print(anstr)


