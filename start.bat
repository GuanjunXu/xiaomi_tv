@echo off
chcp 936
cls

echo.
echo ����adb���񡭡�
adb kill-server
adb start-server

echo.
echo �����豸����
adb connect 192.168.199.115:5555 
adb connect 192.168.199.216:5555
adb connect 192.168.199.125:5555

echo.
echo ִ�нű�����
python .\xiaomi_v_s.py

echo.
pause