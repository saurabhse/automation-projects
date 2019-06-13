from jira import JIRA
from win32api import *
from win32gui import *
import win32con
import sys, os
import json
import time
import datetime

class WindowsNotification:
    def __init__(self, title, msg):
        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
        }
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map
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
           self.hicon = LoadImage(hinst, iconPathName,
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
          self.hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, self.hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.

    def showNotification(self,title,msg):
        Shell_NotifyIcon(NIM_MODIFY,
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER + 20,
                          self.hicon, "Balloon  tooltip", title, 200, msg))
        time.sleep(10)
        #DestroyWindow(self.hwnd)

def notification_window(title, msg):
    w=WindowsNotification(msg, title)
    return w

def notify(title, msg,obj):
    obj.showNotification(title, msg)

with open('config.json', 'r') as f:
    config = json.load(f)
options = {'server': ''}
jira = JIRA(options, basic_auth=(config['JIRA']['USER_NAME'], config['JIRA']['PASSWORD']))
ticket_list = []
obj = notification_window('hello', 'world')
now = datetime.datetime.now()
today6pm = now.replace(hour=18, minute=0, second=0, microsecond=0)

while now < today6pm if config['PARAMS']['SHUTDOWN'] else True:
    issue_list = jira.search_issues('')
    issues=[]
    new_tickets=[]
    for issue in issue_list:
        issues.append(issue.key)
    removed_list = [a for a in ticket_list if a not in issues]
    #print(removed_list)
    #print(ticket_list)
    #print(issues)
    for removed in removed_list:
        ticket_list.remove(removed)
    for issue in issues:
        if str(issue) not in ticket_list:
            print('New ticket arrived => ', str(issue))
            ticket_list.append(str(issue))
            new_tickets.append(str(issue))

    if len(new_tickets) > 0:
        notify(",".join(new_tickets), 'New Incident Assigned', obj)
    time.sleep(config['PARAMS']['REFRESH_INTERVAL'])


