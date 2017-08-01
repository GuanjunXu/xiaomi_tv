import os
import codecs

work_path = os.getcwd()
# result_path = work_path + os.sep + 'Result' + os.sep
result_path = work_path + os.sep + 'an_try' + os.sep

resultlist = os.listdir(result_path)

for r in resultlist:
    if '.txt' in r or '.png' in r:
        resultlist.remove(r)

f_analysis = codecs.open(work_path + os.sep + "result_analysis.txt", 'w', 'utf-8')
for x in resultlist:
    to_write = {}
    to_write['queryNo'] = x[:-4]
    f_xml = open(result_path + os.sep + x, 'r')
    xml_lines = f_xml.readlines()
    xml_string = ' '.join(xml_lines)
    if '" resource-id="com.mitv.tvhome:id/name"' in xml_string:
        ind_end = xml_string.index('" resource-id="com.mitv.tvhome:id/name"')
        new_xml_string = xml_string[:ind_end]
        ind_start = new_xml_string.rfind('text="')
        to_write['movie_title'] = xml_string[ind_start + 6:ind_end]
    else:
        movie_titles = []
        for node in xml_lines:
            if 'resource-id="com.xiaomi.voicecontrol:id/title"' in node and 'focusable="false"' in node:
                ind_end = node.index('resource-id="com.xiaomi.voicecontrol:id/title"')
                new_node = node[:ind_end]
                ind_start = new_node.rfind('text="')
                to_write['recognition'] = node[ind_start + 6:ind_end]
            elif 'resource-id="com.xiaomi.voicecontrol:id/txtTitle"' in node:
                ind_end = node.index('resource-id="com.xiaomi.voicecontrol:id/txtTitle"')
                new_node = node[:ind_end]
                ind_start = new_node.rfind('text="')
                to_write['txtTitle'] = node[ind_start + 6:ind_end]
            elif 'resource-id="com.xiaomi.voicecontrol:id/title"' in node and 'focusable="true"' in node:
                ind_end = node.index('resource-id="com.xiaomi.voicecontrol:id/title"')
                new_node = node[:ind_end]
                ind_start = new_node.rfind('text="')
                # to_write['movie_title'] = node[ind_start + 6:ind_end]
                movie_titles.append(node[ind_start + 6:ind_end])
        to_write['movie_titles'] = movie_titles
    f_analysis.write(str(to_write) + '\n')

f_analysis.close()