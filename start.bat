@echo off
chcp 936
cls

echo.
echo 重启adb服务……
adb kill-server
adb start-server

echo.
echo 连接设备……
adb connect 192.168.199.115:5555 
adb connect 192.168.199.216:5555
adb connect 192.168.199.125:5555

echo.
echo 执行脚本……
python .\xiaomi_v_s.py

echo.
pause