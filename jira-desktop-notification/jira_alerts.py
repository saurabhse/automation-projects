import time
list_a = [1,2,3]
list_b = [2,3]
second = set(list_b)
l = [item for item in list_a if item not in list_b]

l1 = [a for a in list_a+list_b if (a not in list_a) or (a not in list_b)]
from win32api import *
from win32gui import *
import win32con
import sys, os
import struct
import time

class WindowsBalloonTip:
    def __init__(self, title, msg):
        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
        }
        # Register the Window class.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow( classAtom, "Taskbar", style,
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                0, 0, hinst, None)
        UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
           hicon = LoadImage(hinst, iconPathName,
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
          hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY,
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,
                          hicon, "Balloon  tooltip",title,200,msg))
        # self.show_balloon(title, msg)
        time.sleep(10)
        DestroyWindow(self.hwnd)
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.
def balloon_tip(title, msg):
    w=WindowsBalloonTip(msg, title)

ticket_list = []
while True:
    with open('C:\Saurabh\jira\sample.txt') as f:
        issues = f.read().splitlines()

    index = 0
    removed_list = [a for a in ticket_list if a not in issues]
    print(removed_list)
    print(ticket_list)
    print(issues)
    for removed in removed_list:
        ticket_list.remove(removed)
    for issue in issues:
        index = index + 1
        if str(issue) not in ticket_list:
            print(str(index) + ' new ticket arrived', str(issue))
            ticket_list.append(str(issue))
    time.sleep(20)
    balloon_tip('hello', 'world')
    
    from jira import JIRA
import time
from pprint import pprint
options = {'server': ''}
jira = JIRA(options, basic_auth=('', ''))
ticket_list = []
while True:
    issues = jira.search_issues('filter=')
