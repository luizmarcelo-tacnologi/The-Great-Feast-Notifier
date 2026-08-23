import ctypes
import ctypes.wintypes as wintypes
import wx

WM_WTSSESSION_CHANGE = 0x02B1
WTS_SESSION_UNLOCK = 0x8
NOTIFY_FOR_THIS_SESSION = 0
DESKTOP_SWITCHDESKTOP = 0x0100

user32 = ctypes.windll.user32
wtsapi32 = ctypes.windll.wtsapi32

wtsapi32.WTSRegisterSessionNotification.argtypes = [wintypes.HWND, wintypes.DWORD]
wtsapi32.WTSRegisterSessionNotification.restype = wintypes.BOOL
wtsapi32.WTSUnRegisterSessionNotification.argtypes = [wintypes.HWND]
wtsapi32.WTSUnRegisterSessionNotification.restype = wintypes.BOOL
user32.OpenInputDesktop.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
user32.OpenInputDesktop.restype = wintypes.HANDLE
user32.CloseDesktop.argtypes = [wintypes.HANDLE]
user32.CloseDesktop.restype = wintypes.BOOL

#Windows has no direct "is it locked" query, so this is the standard workaround:
#a normal process can't open the interactive input desktop while locked
def is_session_locked():
    hdesk = user32.OpenInputDesktop(0, False, DESKTOP_SWITCHDESKTOP)
    if hdesk:
        user32.CloseDesktop(hdesk)
        return False
    return True

#An invisible window whose only job is to catch WM_WTSSESSION_CHANGE, so we know
#the moment the session unlocks - including after ARSO, where Startup apps run
#while the session is still locked following an update-triggered restart
class SessionMonitor(wx.Frame):

    def __init__(self, on_unlock):
        super().__init__(None)
        self._on_unlock = on_unlock
        wtsapi32.WTSRegisterSessionNotification(self.GetHandle(), NOTIFY_FOR_THIS_SESSION)

    def MSWWindowProc(self, msg, wParam, lParam):
        if msg == WM_WTSSESSION_CHANGE and wParam == WTS_SESSION_UNLOCK:
            self._on_unlock()
        return super().MSWWindowProc(msg, wParam, lParam)

    def close(self):
        wtsapi32.WTSUnRegisterSessionNotification(self.GetHandle())
        self.Destroy()