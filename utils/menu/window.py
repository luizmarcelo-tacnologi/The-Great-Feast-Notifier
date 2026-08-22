import wx
import utils.base.configpath as cfgp
from utils.menu.menu import MenuButton
from utils.menu.support.baseappwindow import AppWindow

#Class of the settings window
class SettingsWindow(AppWindow):

    #Initialization
    def __init__(self, config, save_callback):
        #Initializes the AppWindow
        super().__init__("The Great Feast Notifier - Settings",(450, 350))
        #Sets the passed viriables
        self.config = config
        self.save_callback = save_callback
        #Calls for the UI creation
        self.create_ui()

    #UI creation
    def create_ui(self):

        #Creates the main panel and sets it's background color
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(32, 32, 32))

        #The Main Sizer™
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        #Window's title creation
        title = wx.StaticText(panel,label="Settings")
        title.SetForegroundColour(wx.WHITE)
        title.SetFont(wx.Font(16,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD))

        #Add the title
        main_sizer.Add(title,0,wx.LEFT | wx.RIGHT | wx.TOP,25)

        #Defines the interval label
        interval_label = wx.StaticText(panel,label="Check Interval (minutes)")
        interval_label.SetForegroundColour(wx.Colour(207, 207, 207))
        interval_label.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD))

        #Add the interval label
        main_sizer.Add(interval_label,0,wx.LEFT | wx.RIGHT | wx.TOP,25)

        #Defines the interval box
        self.interval = wx.SpinCtrl(panel,min=1,max=1080,initial=self.config.get("check_interval", 300),style=wx.TE_CENTER)
        self.interval.SetBackgroundColour(wx.Colour(45, 45, 45))
        self.interval.SetForegroundColour(wx.Colour(230, 230, 230))

        #Add the interval box
        main_sizer.Add(self.interval,0,wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,25)

        #The Button Sizer™
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        #Defines the "Cancel" button
        cancel_button = MenuButton(panel,"Cancel",self.Hide)

        #Add the "Cancel" button
        button_sizer.Add(cancel_button,1,wx.RIGHT,10)

        #Defines the "Save" button
        save_button = MenuButton(panel,"Save",self.save)

        #Add the "Save" button
        button_sizer.Add(save_button,1)

        #Add The Button Sizer™ to The Main Sizer™
        main_sizer.Add(button_sizer,0,wx.EXPAND | wx.ALL,25)

        #Set the panel's size as The Main Sizer™'s size
        panel.SetSizer(main_sizer)

        #Sets the window to receive keyboard input (maybe it's the documentation)
        self.interval.SetFocus()

    #Defines the "Save" button behavior
    def save(self):
        #Sets the new value
        self.config["check_interval"] = self.interval.GetValue()
        #Saves the new value
        self.save_callback(self.config)
        #Go waiting
        self.Hide()

#Class of the logs window
class LogsWindow(AppWindow):

    #Initialization
    def __init__(self):
        #Initializes the AppWindow
        super().__init__("The Great Feast Notifier - Logs",(700, 500))
        #Calls the UI creation function
        self.create_ui()
        #Calls the refreshing logs function
        self.refresh_logs()

    #The UI creation function
    def create_ui(self):

        #Creates the panel to hold everything, and set it's backgriund color
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(32, 32, 32))

        #The sizer
        sizer = wx.BoxSizer(wx.VERTICAL)

        #Defines the title label
        title = wx.StaticText(panel,label="Logs")
        title.SetForegroundColour(wx.WHITE)
        title.SetFont(wx.Font(16,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD))

        #Add the title label
        sizer.Add(title,0,wx.ALL,20)

        #Defines the logs window
        self.log_text = wx.TextCtrl(panel,style=wx.TE_MULTILINE |wx.TE_READONLY |wx.HSCROLL)
        self.log_text.SetBackgroundColour(wx.Colour(20, 20, 20))
        self.log_text.SetForegroundColour(wx.Colour(210, 210, 210))
        font = wx.Font(9,wx.FONTFAMILY_TELETYPE,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        self.log_text.SetFont(font)

        #Add the logs window
        sizer.Add(self.log_text,1,wx.EXPAND | wx.LEFT | wx.RIGHT,20)

        #The button sizer
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        #Defines the "Refresh" button
        refresh_button = MenuButton(panel,"Refresh",self.refresh_logs)

        #Add the "Refresh" button
        button_sizer.Add(refresh_button,1,wx.RIGHT,10)

        #Defines the "Open File" button
        open_button = MenuButton(panel,"Open File",self.open_log_file)

        #Add the "Open File" button
        button_sizer.Add(open_button,1,wx.RIGHT,10)

        #Defines the "Close" button
        close_button = MenuButton(panel,"Close",self.Hide)

        #Add the "Close" button
        button_sizer.Add(close_button,1)

        #Add the button sizer to the sizer
        sizer.Add(button_sizer,0,wx.EXPAND | wx.ALL,20)

        #Set the panel' size as the sizer's size
        panel.SetSizer(sizer)

    #Function to refresh the logs
    def refresh_logs(self):
        #Tries opening the file
        try:
            #Opens the file
            with open(cfgp.log_path,"r",encoding="utf-8") as file:
                #Gets it's contents
                contents = file.read()
        #In case the file don't
        except FileNotFoundError:
            contents = "No logs available."
        #Sets the log window values to be the log file values
        self.log_text.SetValue(contents)
        self.log_text.ShowPosition(self.log_text.GetLastPosition())

    #Function to open the log file
    def open_log_file(self):
        import os
        os.startfile(cfgp.log_path)