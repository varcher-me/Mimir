import win32api
import win32gui
import win32con
import win32process
import time

file = '国寿投资发〔2017〕365号正文.gd'
path_init = 'd:\\temp\\'
path_processed = 'd:\\temp\\'
path_error = 'd:\\temp\\'
path_result = 'd:\\result\\'

win32api.ShellExecute(0, 'open', path_init+file, '','',1)
time.sleep(5)
handle2 = win32gui.FindWindow(None, 'SEP Reader - ['+file+']')
win32gui.SetForegroundWindow(handle2)
print(handle2)
time.sleep(1)
win32api.keybd_event(17,0,0,0) # Ctrl
win32api.keybd_event(80,0,0,0) # P
win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
win32api.keybd_event(80,0,win32con.KEYEVENTF_KEYUP,0)
time.sleep(1)
handle3 = win32gui.FindWindowEx(None, None, None, 'SEP Reader')
print(handle3)
win32gui.SetForegroundWindow(handle3)
win32api.keybd_event(13,0,0,0) # Enter
win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
win32gui.CloseWindow(handle2)
