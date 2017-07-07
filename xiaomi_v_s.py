# -*- coding: utf-8 -*-

from uiautomator import Device
import os
import time
import xlrd
import xlwt

tv_d, controller_d, reader_d = "", "", ""

tv = Device(tv_d)
controller = Device(controller_d)
reader = Device(reader_d)

reader_activity = ""
controller_activity = ""

f_query = open("query_list.txt", "r")
query = f_query.readline()

wb = xlwt.Workbook()
ws = wb.add_sheet('Xiaomi search result')

col_names = ["Query", "Recognition", "ResultCount", "Results", "ImgPath"]

work_path = os.getcwd()

def longpressDown(hold):
    os.popen("adb -s %s shell sendevent /dev/input/event2 3 57 143"%controller_d)
    os.popen("adb -s %s shell sendevent /dev/input/event2 3 53 1165"%controller_d)
    os.popen("adb -s %s shell sendevent /dev/input/event2 3 54 2375"%controller_d)
    os.popen("adb -s %s shell sendevent /dev/input/event2 1 330 1"%controller_d)
    os.popen("adb -s %s shell sendevent /dev/input/event2 3 0 1165"%controller_d)
    os.popen("adb -s %s shell sendevent /dev/input/event2 3 1 2375"%controller_d)
    os.popen("adb -s %s shell sendevent /dev/input/event2 0 0 0"%controller_d)

def longpressUp(hold):
    time.sleep(hold)
    os.popen("adb -s %s shell sendevent /dev/input/event2 3 57 4294967295"%controller_d)
    os.popen("adb -s %s shell sendevent /dev/input/event2 1 330 0"%controller_d)
    os.popen("adb -s %s shell sendevent /dev/input/event2 0 0 0"%controller_d)
    time.sleep(hold)

def launchReader():
    if d(packageName = '').wait.gone():
        os.popen("adb -s %s shell am start -n %s"%(reader_d, reader_activity))

def launchController():
    if d(packageName = '').wait.gone():
        os.popen("adb -s %s shell am start -n %s"%(controller_d, controller_activity))

def findText(txt):
    before = s.index(u"找到")
    after = s.index(u"部\"")
    res_count = s[before+2:after]
    rec = s[after+2:-1]
    return res_count, rec

def screencapAndPullOut(imgname, pullpath):
    imgname = str(imgname)
    os.popen("adb shell screencap -p /sdcard/%s.png"%imgname)
    os.popen("adb pull /sdcard/%s.png %s"%(imgname, pullpath))
    os.popen("adb shell rm /sdcard/%s.png"%imgname)

for m in range(len(col_names)):
    ws.write(0, m, col_names[m])

i = 1
while query:
    line_w = []
    query = query.strip("\n")
    line_w.append(query)
    launchReader()
    reader(resourceId = '').set_text(query) # 朗读机输入文字
    launchController()
    longpressDown() # 遥控器按住语音键
    reader(resourceId = '').click() # 朗读机按下朗读键
    longpressUp(len(query)/2) # 遥控器释放语音键
    result_txtTitle = tv(resourceId = 'com.xiaomi.voicecontrol:id/txtTitle').info['text']
    find_list = findText(result_txtTitle)
    res_count, rec = find_list[0], find_list[1]
    line_w.append(res_count)
    line_w.append(rec)
    result_count = tv(resourceId = 'com.xiaomi.voicecontrol:id/poster').count
    res_tit_list = []
    for t in range(result_count):
        res_tit = tv(resourceId = 'com.xiaomi.voicecontrol:id/poster', instance = t).down(resourceId = 'com.xiaomi.voicecontrol:id/title').info['text']
        res_tit_list.append(res_tit)
    line_w.append(res_tit_list)
    line_w.append(work_path + str(i) + ".png")
    for n in range(len(line_w)):
        ws.write(i, n, line_w(n))
    screencapAndPullOut(i, work_path)
    query = f_query.readline()

wb.save('xiaomi_voicesearch_%s.xls'%time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime(time.time())))




