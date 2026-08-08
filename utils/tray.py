import wx
import wx.adv
import utils.configpath as cfgp

class TrayIcon(wx.adv.TaskBarIcon):

    def __init__(self, check_now, open_config, open_logs, quit_program):
        super().__init__()

        self.check_now = check_now
        self.open_config = open_config
        self.open_logs = open_logs
        self.quit_program = quit_program

        self.SetIcon(
            wx.Icon(
                cfgp.resource_path("hypixel.ico"),
                wx.BITMAP_TYPE_ICO
            ),
            "Grand Feast Notifier"
        )

        self.Bind(
            wx.adv.EVT_TASKBAR_LEFT_UP,
            self.on_left_click
        )

    def on_left_click(self, event):
        x, y = wx.GetMousePosition()

        self.show_menu(x, y)

    def show_menu(self, x, y):
        print(f"Clicked at: {x}, {y}")