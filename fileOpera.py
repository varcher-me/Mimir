import win32api
import win32gui
import win32con
# import win32process
import time
import os
import shutil
import logger

path_init = 'd:\\temp\\init\\'
path_processed = 'd:\\temp\\init\\'   # todo:改为正确目录
path_error = 'd:\\temp\\error\\'
path_result = 'd:\\temp\\result\\'
path_printed = 'd:\\temp\\'
file_printed = 'PrintedPDF.pdf'
retry_interval = 0.2
retry_seconds = 20
logger = logger.logger


def get_window(hwnd_father, hwnd_child_after, window_class, window_context):
    retry_time = retry_seconds / retry_interval
    while retry_time > 0:
        time.sleep(0.2)
        hwnd = win32gui.FindWindowEx(hwnd_father, hwnd_child_after, window_class, window_context)
        if hwnd:
            break
        else:
            retry_time -= 1
    if hwnd:
        return hwnd
    else:
        return False    # todo:窗口没有出现，抛异常


def wait_window_disappear(hwnd):
    retry_time = retry_seconds / retry_interval
    while retry_time > 0:
        time.sleep(0.2)
        result = win32gui.IsWindow(hwnd)
        if result:
            retry_time -= 1
        else:
            return True
    return False    # todo:窗口没有消失，抛异常


def wait_for_file(full_file):
    retry_time = retry_seconds / retry_interval
    while retry_time > 0:
        time.sleep(0.2)
        if os.path.isfile(full_file):
            try:
                time.sleep(0.5)
                fp = open(full_file, 'a')
                fp.close()
                return True
            except:
                retry_time -= 1
        else:
            retry_time -= 1
    return False    # todo:文件没有出现，抛异常


def rename_file(printed_file, new_file):
    printed_file = os.path.join(path_printed, file_printed)
    if wait_for_file(printed_file):
        os.rename(printed_file, new_file)
        shutil.move(new_file, path_result)
        print("File"+new_file+" moved.")


def process_file(path, file):
    # 打开文件
    print("Starting processing "+file)
    win32api.ShellExecute(0, 'open', path+file, '', '', 1)
    hwnd_main_sep = get_window(None, None, None, 'SEP Reader - [' + file + ']')
    if 0 == hwnd_main_sep:
        logger.fatal("FATAL ERROR: SEP Reader Window not found! program terminated.")
        exit(100)

    # 发送打印指令
    win32gui.SetForegroundWindow(hwnd_main_sep)
    win32api.keybd_event(17, 0, 0, 0)  # Ctrl
    win32api.keybd_event(80, 0, 0, 0)  # P
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(80, 0, win32con.KEYEVENTF_KEYUP, 0)

    # 等待打印窗体、按回车并判断窗体消失
    hwnd_printer = get_window(None, None, None, 'SEP Reader')
    win32gui.SetForegroundWindow(hwnd_printer)
    win32api.keybd_event(13, 0, 0, 0)  # Enter
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
    if not wait_window_disappear(hwnd_printer):
        logger.error("File [" + file + "] print-window-disappear timed out; WM_CLOSE signal sent.")
        win32api.SendMessage(hwnd_printer, win32con.WM_CLOSE, 0, 0)

    # 窗口清理（SEP为关闭文件，保留程序窗口）
    win32gui.SetForegroundWindow(hwnd_main_sep)
    win32api.keybd_event(17, 0, 0, 0)  # Ctrl
    win32api.keybd_event(87, 0, 0, 0)  # W
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(87, 0, win32con.KEYEVENTF_KEYUP, 0)
    print("File "+file+" printed.")
    # win32api.SendMessage(hwnd_main, win32con.WM_CLOSE, 0, 0)

    # 移动新文件
    count = 0
    printed_file = os.path.join(path_printed, file_printed)
    new_file = os.path.join(path_printed, file+'.pdf')
    while count < 5:
        try:
            rename_file(printed_file, new_file)
            logger.info("File ["+new_file+"] Processed successfully.")
            break;
        except:
            time.sleep(0.5)
            count += 1
    if 5 == count:
        logger.fatal("FATAL ERROR: move file ["+new_file+"] failed. Process Terminated.")


for i in os.walk(path_init):
    for fileName in i[2]:
        process_file(path_init, fileName)
