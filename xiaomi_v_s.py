# -*- coding: utf-8 -*-

from uiautomator import Device
import os
import time
import xlrd
import xlwt

# os.popen('CHCP 65001')

tv_d, controller_d, reader_d = "192.168.199.115:5555", "192.168.199.216:5555", "192.168.199.125:5555"

tv = Device(tv_d)
controller = Device(controller_d)
reader = Device(reader_d)

reader_activity = "com.kingfore.TextToVoice/com.iflytek.common.LaunchService"
controller_activity = "com.duokan.phone.remotecontroller/com.xiaomi.mitv.phone.remotecontroller.home.MainActivity"

f_query = open("query_list_2.txt", "r")
query = f_query.readline()

wb = xlwt.Workbook()
ws = wb.add_sheet('Xiaomi search result', cell_overwrite_ok = True)

col_names = ["Query", "Recognition", "ResultCount", "Results", "ImgPath", "ResultMsg"]

work_path = os.getcwd()
result_path = "Results"
try:
    os.mkdir(result_path)
except:
    pass

def longpressDown():
    os.popen("adb -s %s shell sendevent /dev/input/event2 3 57 50"%controller_d)
    os.popen("adb -s %s shell sendevent /dev/input/event2 3 53 1135"%controller_d)
    os.popen("adb -s %s shell sendevent /dev/input/event2 3 54 2436"%controller_d)
    os.popen("adb -s %s shell sendevent /dev/input/event2 1 330 1"%controller_d)
    os.popen("adb -s %s shell sendevent /dev/input/event2 3 0 1135"%controller_d)
    os.popen("adb -s %s shell sendevent /dev/input/event2 3 1 2436"%controller_d)
    os.popen("adb -s %s shell sendevent /dev/input/event2 0 0 0"%controller_d)

def longpressUp(hold):
    time.sleep(hold)
    os.popen("adb -s %s shell sendevent /dev/input/event2 3 57 4294967295"%controller_d)
    os.popen("adb -s %s shell sendevent /dev/input/event2 1 330 0"%controller_d)
    os.popen("adb -s %s shell sendevent /dev/input/event2 0 0 0"%controller_d)
    time.sleep(hold)

def launchReader():
    if reader(packageName = 'com.kingfore.TextToVoice').wait.gone():
        # os.popen("adb -s %s shell am start -n %s"%(reader_d, reader_activity))
        reader.press('home')
        time.sleep(2)
        reader.press('home')
        reader(text = u'文字转语音合成器').click()
        time.sleep(5)

controller.watcher("gototv").when(text=u"客厅的小米电视").click(text=u"客厅的小米电视")

def launchController():
    if controller(packageName = 'com.duokan.phone.remotecontroller', text = u'开关').wait.gone():
        # os.popen("adb -s %s shell am start -n %s"%(controller_d, controller_activity))
        controller.press('home')
        time.sleep(2)
        controller.press('home')
        controller(text = u'万能遥控').click()
        time.sleep(2)
        if controller(text = u'开关').wait.gone():
            controller(text = u'客厅的小米电视').click()
            time.sleep(2)

def findText(txt):
    before = s.index(u"找到")
    after = s.index(u"部\"")
    res_count = s[before+2:after]
    rec = s[after+2:-1]
    return res_count, rec

def screencapAndPullOut(imgname, pullpath):
    imgname = str(imgname)
    os.popen("adb -s %s shell screencap -p /sdcard/%s.png"%(tv_d,imgname))
    os.popen("adb -s %s pull /sdcard/%s.png %s"%(tv_d,imgname, pullpath))
    os.popen("adb -s %s shell rm /sdcard/%s.png"%(tv_d,imgname))

while query:
    q = query.strip("\n").split(',')
    no = q[0]
    print no + ":"
    word = q[1]
    try:
        launchReader()
        reader(resourceId = 'com.kingfore.TextToVoice:id/mainEditText1').set_text(word) # 朗读机输入文字
        launchController()
        print "\tPress down... ",
        longpressDown() # 遥控器按住语音键
        print "\tReading... ",
        reader(text = u'朗读').click() # 朗读机按下朗读键
        print "\tRelease... ",
        longpressUp(len(word)/2) # 遥控器释放语音键
        # if tv(resourceId = 'com.mitv.tvhome:id/collect_btn').wait.exists():
        #     res_tit = tv(resourceId = 'com.mitv.tvhome:id/name').text
        #     dict_w['title'] = res_tit
        #     dict_w['tag'] = 'description'
        # else:
        #     lstResult = tv(resourceId = 'com.xiaomi.voicecontrol:id/lstResult')
        #     result_count = lstResult.childCount
        #     res_tit_list = []
        #     for t in range(result_count):
        #         print t,
        #         res_tit = lstResult.child(resourceId = 'com.xiaomi.voicecontrol:id/titleBar',instance = t).child(resourceId = 'com.xiaomi.voicecontrol:id/title').text
        #         print res_tit,
        #         res_tit_list.append(res_tit)
        #     dict_w['title'] = res_tit_list
        #     dict_w['tag'] = 'result_list'
        #     dict_w['recognition'] = tv(resourceId = 'com.xiaomi.voicecontrol:id/title').text
        #     dict_w['result_msg'] = tv(resourceId = 'com.xiaomi.voicecontrol:id/txtTitle').text
        tv.dump("%s.xml"%(work_path + os.sep + result_path + os.sep + no))
        screencapAndPullOut(no, work_path + os.sep + result_path)
        tv.press('back')
        print "Done."
        print "*-*-*-*-*-*-*-*-*-*-*-*-*-*-"
    except:
        # dict_w['tag'] = 'occur_err'
        print "occur_err"
        pass
    # f_result.write(str(dict_w).encode('utf-8'))
    query = f_query.readline()
    
print "*** All clear ***"
# f_result.close()