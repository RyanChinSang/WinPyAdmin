# WARNING: requires Windows XP SP2 or higher!
# This code is a modified version to the original 'admin.py' by Preston Landers (2010)
# Original: https://github.com/UAlbanyArchives/ants/blob/master/admin.py
# All legal means from above remain the same for WinPyAdmin.
# WinPyAdmin v1.1a

import os
import sys
import types
import ctypes
import traceback
import win32gui
import win32con
import win32event
import win32process
# TODO: Fix unresolved references
from win32com.shell import shellcon
from win32com.shell.shell import ShellExecuteEx


def isUserAdmin():
    """
    Checks whether the current instance of the python console has administrative privileges, or not.
    If not administrator, returns False.
    """
    if os.name == 'nt':
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:  # TODO: Fix this broad clause
            traceback.print_exc()
            print "Administrator check failed. Assuming not an administrator...\n"
            return False
    elif os.name == 'posix':
        # Check for root on Posix
        return os.getuid() == 0
    else:
        raise RuntimeError("Unsupported operating system for this module: " + str(os.name) + "\n")


def runAsAdmin(cmd_line=None, wait=True, console=True):
    # TODO: complete description
    """
    Elevates a new python console window to Administrator.
    1- cmd_line: 
    2- wait    : 
    3- cmd     : Sets whether the python console should show it's window. It shows the window by default.
               : True          = shows the elevated python console window.
               : False or None = does not show the elevated python console window.
    """
    if os.name != 'nt':
        raise RuntimeError("This function is only implemented on Windows.\n")

    python_exe = sys.executable

    if cmd_line is None:
        cmd_line = [python_exe] + sys.argv  # cmd_line = [cmd, params]
    elif type(cmd_line) not in (types.TupleType, types.ListType):
        raise ValueError("cmd_line is not a sequence.\n")

    cmd = '"%s"' % (cmd_line[0],)  # The path of the cmd window

    # TODO: isn't there a function or something we can call to massage command line params?
    params = " ".join(['"%s"' % (x,) for x in cmd_line[1:]])  # The path of the python script that called
    if console is False:
        show_cmd = win32con.SW_HIDE
    else:
        show_cmd = win32con.SW_SHOWNORMAL

    # ShellExecute() doesn't seem to allow us to fetch the PID or handle of the process, so we can't get anything
    # useful from it. Therefore the more complex ShellExecuteEx() must be used.
    # NOTE: lpVerb='runas' causes UAC elevation prompt.
    procInfo = ShellExecuteEx(nShow=show_cmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb='runas',
                              lpFile=cmd,
                              lpParameters=params)

    if wait:
        procHandle = procInfo['hProcess']
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)  # TODO: Necessary?
        rc = win32process.GetExitCodeProcess(procHandle)
    else:
        rc = None

    return rc


def modWin(name, opt=None):
    """
    Modifies a window with 'name'. If 'opt' is incorrectly set, defaults to normal mode - so as to show the user it is 
    wrong. All 'opt' actions are taken from win32con.py.

    01- name: the name of the window to perform the action 'opt' dictates.
    02- opt : a keyword to perform some action to modify the specified window's state.
    """
    window = win32gui.FindWindow(None, name)
    if window != 0:
        if opt == 'hide':
            win32gui.ShowWindow(window, win32con.SW_HIDE)
        elif opt == 'shownorm':
            win32gui.ShowWindow(window, win32con.SW_SHOWNORMAL)
        elif opt == 'showmin':
            win32gui.ShowWindow(window, win32con.SW_SHOWMINIMIZED)
        elif opt == 'max' or opt == 'showmax':
            win32gui.ShowWindow(window, win32con.SW_MAXIMIZE)
        elif opt == 'shownoact':
            win32gui.ShowWindow(window, win32con.SW_SHOWNOACTIVATE)
        elif opt == 'show':
            win32gui.ShowWindow(window, win32con.SW_SHOW)
        elif opt == 'min':
            win32gui.ShowWindow(window, win32con.SW_MINIMIZE)
        elif opt == 'showminnoact':
            win32gui.ShowWindow(window, win32con.SW_SHOWMINNOACTIVE)
        elif opt == 'showna':
            win32gui.ShowWindow(window, win32con.SW_SHOWNA)
        elif opt == 'restore':
            win32gui.ShowWindow(window, win32con.SW_RESTORE)
        elif opt == 'forcemin' or opt == 'maxx':
            win32gui.ShowWindow(window, win32con.SW_FORCEMINIMIZE)
        else:
            print 'WARNING: Parameter opt=\'' + str(opt) + '\' is not valid. Assuming opt=\'norm\'...\n' if opt is not \
                                                                                                            None else ''
            win32gui.ShowWindow(window, win32con.SW_NORMAL)
    else:
        print 'WARNING: No window with name \"' + str(name) + '\" was found. Nothing changed.\n'
