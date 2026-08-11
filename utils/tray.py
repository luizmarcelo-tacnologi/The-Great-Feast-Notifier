import wx
import wx.adv
import utils.configpath as cfgp
from utils.menu import TrayMenu

class TrayIcon(wx.adv.TaskBarIcon):

    def __init__(self,check_now,open_config,open_logs,quit_program):

        super().__init__()

        self.menu = TrayMenu(check_now,open_config,open_logs,quit_program)

        self.SetIcon(wx.Icon(cfgp.resource_path("hypixel.ico"),wx.BITMAP_TYPE_ICO),"The Grand Feast Notifier")

        self.Bind(wx.adv.EVT_TASKBAR_LEFT_UP,self.on_left_click)

    def on_left_click(self, event):
        if self.menu.IsShown():
            self.menu.Hide()
            return
        x, y = wx.GetMousePosition()
        self.menu.show_menu(x, y)