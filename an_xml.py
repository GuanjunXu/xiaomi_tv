# -*- coding: utf-8 -*-

import os
# import codecs

work_path = os.getcwd()
# result_path = work_path + os.sep + 'Result' + os.sep
result_path = work_path + os.sep + 'an_try' + os.sep

resultlist = os.listdir(result_path)

for r in resultlist:
    if '.txt' in r or '.png' in r:
        resultlist.remove(r)

qNo_q_list = []
for q in open('query_list.txt', 'r', encoding = 'utf8'):
    qq = q.strip("\n").split(',')
    qNo_q_list.append(qq[0])
    qNo_q_list.append(qq[1])

f_analysis = open(work_path + os.sep + "ResultAnalysis.txt", 'w', encoding = 'utf8')
f_fail = open(work_path + os.sep + "An_ErrList.txt", 'w', encoding = 'utf8')
for x in resultlist:
    print(x, end = '')
    to_write = {}
    to_write['queryNo'] = x[:-4]
    q_index = qNo_q_list.index(x[:-4])
    to_write['query'] = qNo_q_list[q_index + 1]
    try:
        f_xml = open(result_path + os.sep + x, 'r', encoding = 'utf8')
        xml_lines = f_xml.readlines()
        xml_string = ' '.join(xml_lines)
        # if '" resource-id="com.mitv.tvhome:id/name"' in xml_string:
        if 'resource-id="com.xiaomi.voicecontrol:id/txtTitle"' not in xml_string:
            ind_end = xml_string.index('" resource-id="com.mitv.tvhome:id/name"')
            new_xml_string = xml_string[:ind_end]
            ind_start = new_xml_string.rfind('text=')
            to_write['movie_title'] = xml_string[ind_start + 6:ind_end]
            to_write['tag'] = 'Detail'
        # elif 'resource-id="com.xiaomi.voicecontrol:id/txtTitle"' in xml_string:
        else:
            movie_titles = []
            for node in xml_lines:
                if 'resource-id="com.xiaomi.voicecontrol:id/title"' in node and 'focusable="false"' in node:
                    ind_end = node.index('resource-id="com.xiaomi.voicecontrol:id/title"')
                    new_node = node[:ind_end]
                    ind_start = new_node.rfind('text=')
                    try:
                        if int(node.strip('\n')[-9:-5].split(',')[1]) < 200:
                            to_write['recognition'] = node[ind_start + 6:ind_end-2]
                    except:
                        pass
                elif 'resource-id="com.xiaomi.voicecontrol:id/txtTitle"' in node:
                    ind_end = node.index('resource-id="com.xiaomi.voicecontrol:id/txtTitle"')
                    new_node = node[:ind_end]
                    ind_start = new_node.rfind('text=')
                    to_write['txtTitle'] = node[ind_start + 7:ind_end-2]
                elif 'resource-id="com.xiaomi.voicecontrol:id/title"' in node and 'focusable="true"' in node:
                    ind_end = node.index('resource-id="com.xiaomi.voicecontrol:id/title"')
                    new_node = node[:ind_end]
                    ind_start = new_node.rfind('text=')
                    # to_write['movie_title'] = node[ind_start + 6:ind_end]
                    movie_titles.append(node[ind_start + 6:ind_end-2])
            to_write['tag'] = 'Result'
            to_write['movie_titles'] = movie_titles
        # print to_write
        f_analysis.write(str(to_write) + '\n')
        print('\tDone.')
    except:
        # f_fail.write(x + '\n')
        f_fail.write(str(to_write) + '\n')
        print('\tErr.')
f_analysis.close()
f_fail.close()