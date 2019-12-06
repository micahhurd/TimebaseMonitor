@echo off
cd C:\Users\Micah\PycharmProjects\TimebaseMonitor
pscp -pw raspberry TimebaseMonitor.py pi@10.10.0.217:
exit
