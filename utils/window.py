import wx
import utils.configpath as cfgp
from utils.menu import MenuButton

class AppWindow(wx.Frame):

    def __init__(self, title, size):
        super().__init__(None,title=title,style=wx.DEFAULT_FRAME_STYLE)
        self.SetSize(size)
        self.SetBackgroundColour(wx.Colour(32, 32, 32))
        self.Centre()
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        self.Hide()

class SettingsWindow(AppWindow):

    def __init__(self, config, save_callback):
        super().__init__("The Great Feast Notifier - Settings",(450, 350))
        self.config = config
        self.save_callback = save_callback
        self.create_ui()

    def create_ui(self):

        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(32, 32, 32))

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel,label="Settings")
        title.SetForegroundColour(wx.WHITE)
        title.SetFont(wx.Font(16,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD))

        main_sizer.Add(title,0,wx.LEFT | wx.RIGHT | wx.TOP,25)

        api_label = wx.StaticText(panel,label="Hypixel API Key")
        api_label.SetForegroundColour(wx.Colour(207, 207, 207))

        main_sizer.Add(api_label,0,wx.LEFT | wx.RIGHT | wx.TOP,25)

        self.api_key = wx.TextCtrl(panel,value=self.config.get("api_key", ""),style=wx.TE_CENTER)
        self.api_key.SetBackgroundColour(wx.Colour(45, 45, 45))
        self.api_key.SetForegroundColour(wx.Colour(230, 230, 230))

        main_sizer.Add(self.api_key,0,wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,25)

        interval_label = wx.StaticText(panel,label="Check Interval (minutes)")
        interval_label.SetForegroundColour(wx.Colour(207, 207, 207))

        main_sizer.Add(interval_label,0,wx.LEFT | wx.RIGHT | wx.TOP,25)

        self.interval = wx.SpinCtrl(panel,min=1,max=1080,initial=self.config.get("check_interval", 300),style=wx.TE_CENTER)
        self.interval.SetBackgroundColour(wx.Colour(45, 45, 45))
        self.interval.SetForegroundColour(wx.Colour(230, 230, 230))

        main_sizer.Add(self.interval,0,wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,25)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        cancel_button = MenuButton(panel,"Cancel",self.Hide)

        save_button = MenuButton(panel,"Save",self.save)

        button_sizer.Add(cancel_button,1,wx.RIGHT,10)

        button_sizer.Add(save_button,1)

        main_sizer.Add(button_sizer,0,wx.EXPAND | wx.ALL,25)

        panel.SetSizer(main_sizer)

        self.api_key.SetSelection(0, 0)
        self.interval.SetFocus()

    def save(self):
        self.config["api_key"] = self.api_key.GetValue()
        self.config["check_interval"] = self.interval.GetValue()
        self.save_callback(self.config)
        self.Hide()

class LogsWindow(AppWindow):

    def __init__(self):
        super().__init__("The Great Feast Notifier - Logs",(700, 500))
        self.create_ui()
        self.refresh_logs()

    def create_ui(self):

        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(32, 32, 32))

        sizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel,label="Logs")
        title.SetForegroundColour(wx.WHITE)
        title.SetFont(wx.Font(16,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD))

        sizer.Add(title,0,wx.ALL,20)

        self.log_text = wx.TextCtrl(panel,style=wx.TE_MULTILINE |wx.TE_READONLY |wx.HSCROLL)
        self.log_text.SetBackgroundColour(wx.Colour(20, 20, 20))
        self.log_text.SetForegroundColour(wx.Colour(210, 210, 210))
        font = wx.Font(9,wx.FONTFAMILY_TELETYPE,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        self.log_text.SetFont(font)

        sizer.Add(self.log_text,1,wx.EXPAND | wx.LEFT | wx.RIGHT,20)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        refresh_button = MenuButton(panel,"Refresh",self.refresh_logs)

        open_button = MenuButton(panel,"Open File",self.open_log_file)

        close_button = MenuButton(panel,"Close",self.Hide)

        button_sizer.Add(refresh_button,1,wx.RIGHT,10)
        button_sizer.Add(open_button,1,wx.RIGHT,10)
        button_sizer.Add(close_button,1)

        sizer.Add(button_sizer,0,wx.EXPAND | wx.ALL,20)

        panel.SetSizer(sizer)

    def refresh_logs(self):

        try:
            with open(cfgp.log_path,"r",encoding="utf-8") as file:
                contents = file.read()
        except FileNotFoundError:
            contents = "No logs available."
        self.log_text.SetValue(contents)
        self.log_text.ShowPosition(self.log_text.GetLastPosition())

    def open_log_file(self):
        import os
        os.startfile(cfgp.log_path)