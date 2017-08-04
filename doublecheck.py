# -*- coding: utf-8 -*-

import re
# import Levenshtein

f_a = open('ResultAnalysis.txt', 'r')
# f_q = open('query_list.txt', 'r')

query_in_result = f_a.readline()

qNo_q_list = []
for q in open('query_list.txt', 'r', encoding = 'utf-8'):
    qq = q.strip("\n").split(',')
    qNo_q_list.append(qq[0])
    qNo_q_list.append(qq[1])

f_diff = open('diff.txt', 'w', encoding = 'utf-8')
f_diff.write('No.\tQuery\tRecognize\n')

f_err = open('check_ErrList.txt', 'w', encoding = 'utf-8')

while query_in_result:
    try:
        q_dct = eval(query_in_result)
        q_No = q_dct['queryNo']
        print(q_No)
        if q_dct['tag'] == 'Detail':
            q_rec = q_dct['movie_title']
        elif q_dct['tag'] == 'Result':
            q_rec = q_dct['recognition']
        q_index = qNo_q_list.index(q_No)
        q_tar = qNo_q_list[q_index + 1]
        q_tar = re.sub("[\s+\.\!\/_,$-%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）《》]+", "", q_tar)
        #if Levenshtein.ratio(q_tar, q_rec) < 0.85:
        if q_tar != q_rec:
            f_diff.write(q_No + '\t' + q_tar + '\t' + q_rec + '\n')
        query_in_result = f_a.readline()
        print("\tDone.")
    except:
        f_err.write(q_No + '\t' + q_tar + '\t' + q_rec + '\n')
        print("\tErr.")
    query_in_result = f_a.readline()
f_diff.close()
f_err.close()