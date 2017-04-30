# This demonstrates how to use WinPyAdmin
import sys
import WinPyAdmin as wpa


def run():
    if not wpa.isUserAdmin():
        rc = wpa.runAsAdmin()
    else:
        print "You now have Administrator rights. Your code goes here.\n"
        rc = 0
    x = raw_input("Press Enter to continue...")  # This is just used to hold the elevated window. Remove it.
    return rc

if __name__ == '__main__':
    sys.exit(run())
