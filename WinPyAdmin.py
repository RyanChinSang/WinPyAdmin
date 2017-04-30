# WARNING: requires Windows XP SP2 or higher!
# This code is a slightly modified version to the original 'admin.py' by Preston Landers 2010
# Original: https://github.com/UAlbanyArchives/ants/blob/master/admin.py
# All legal means from above remain the same for WinPyAdmin.
# WinPyAdmin v1.0

import os
import sys
import types
import traceback
import win32api, win32con, win32event, win32process
from win32com.shell import shellcon
from win32com.shell.shell import ShellExecuteEx


def isUserAdmin():
    """
    Checks whether the current instance of the python console has administrative privileges, or not.
    If not administrator, returns False.
    """
    if os.name == 'nt':
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            traceback.print_exc()
            print "Admin check failed, assuming not an admin."
            return False
    elif os.name == 'posix':
        # Check for root on Posix
        return os.getuid() == 0
    else:
        raise RuntimeError, "Unsupported operating system for this module: %s" % (os.name,)


def runAsAdmin(cmdLine=None, wait=True, cmd=True):
    """
    Elevates a new python console window to Administrator.
    1- cmdLine: 
    2- wait   : 
    3- cmd    : Sets whether the python console should show it's window. It shows the window by default.
              : True          = shows the elevated python console window.
              : False or None = does not show the elevated python console window.

    """
    if os.name != 'nt':
        raise RuntimeError, "This function is only implemented on Windows."

    python_exe = sys.executable

    if cmdLine is None:
        cmdLine = [python_exe] + sys.argv
    elif type(cmdLine) not in (types.TupleType,types.ListType):
        raise ValueError, "cmdLine is not a sequence."
    cmd = '"%s"' % (cmdLine[0],)

    # XXX TODO: isn't there a function or something we can call to massage command line params?
    params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
    cmdDir = ''

    if cmd is False:
        showCmd = win32con.SW_HIDE
    elif cmd is None:
        showCmd = win32con.SW_HIDE
    else:
        showCmd = win32con.SW_SHOWNORMAL
    lpVerb = 'runas'  # causes UAC elevation prompt.

    # ShellExecute() doesn't seem to allow us to fetch the PID or handle
    # of the process, so we can't get anything useful from it. Therefore
    # the more complex ShellExecuteEx() must be used.
    procInfo = ShellExecuteEx(nShow=showCmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb=lpVerb,
                              lpFile=cmd,
                              lpParameters=params)

    if wait:
        procHandle = procInfo['hProcess']
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
    else:
        rc = None
    return rc
