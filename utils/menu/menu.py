import wx
from utils.base.configpath import resource_path
from utils.menu.support.button import MenuButton

#Sets the traymenu class
class TrayMenu(wx.Frame):

    #Initialization
    def __init__(self,check_now,open_config,open_logs,quit_program):
        #Initializes wx.Frame
        super().__init__(None,style=wx.FRAME_NO_TASKBAR |wx.STAY_ON_TOP |wx.BORDER_NONE |wx.FRAME_SHAPED)

        #Sets the passed variables
        self.check_now = check_now
        self.open_config = open_config
        self.open_logs = open_logs
        self.quit_program = quit_program

        #Sets it's size
        self.SetSize((220, 250))

        #Defines it's behavior
        self.Bind(wx.EVT_ACTIVATE, self.on_activate)
        self.Bind(wx.EVT_SIZE, self.on_size)

        #Creates itself
        self.create_menu()

        #Hides itself, just waiting patiently for the action
        self.Hide()

    #The function to create the menu
    def create_menu(self):

        #Creates the background panel and sets it's color
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(32,32,32))

        #A shared sizer
        sizer = wx.BoxSizer(wx.VERTICAL)

        #Sets the title and it's color & font
        title = wx.StaticText(panel,label="The Great Feast Notifier")
        title.SetForegroundColour(wx.Colour(255, 255, 255))
        title.SetFont(wx.Font(12,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD))

        #Add the title to the menu
        sizer.Add(title,0,wx.ALL | wx.ALIGN_CENTER,15)

        #Defines the "Check Now" button
        check_button = MenuButton(
            panel,
            "Check Now",
            lambda: self.execute(self.check_now),
            wx.Bitmap(resource_path("icons/check.png"),wx.BITMAP_TYPE_PNG)
        )

        #Add the "Check Now" button
        sizer.Add(check_button,0,wx.EXPAND |wx.LEFT |wx.RIGHT |wx.BOTTOM,10)

        #Defines the "Settings" button
        config_button = MenuButton(
            panel,
            "Settings",
            lambda: self.execute(self.open_config),
            wx.Bitmap(resource_path("icons/settings.png"),wx.BITMAP_TYPE_PNG)
        )

        #Add the "Settings" button
        sizer.Add(config_button,0,wx.EXPAND |wx.LEFT |wx.RIGHT |wx.BOTTOM,10)

        #Defines the "Logs" button
        logs_button = MenuButton(
            panel,
            "Logs",
            lambda: self.execute(self.open_logs),
            wx.Bitmap(resource_path("icons/log.png"),wx.BITMAP_TYPE_PNG)
        )

        #Add the "Logs" button
        sizer.Add(logs_button,0,wx.EXPAND |wx.LEFT |wx.RIGHT |wx.BOTTOM,10)

        #Defines the "Close" button
        close_menu_button = MenuButton(
            panel,
            "Close",
            lambda: self.Hide(),
            wx.Bitmap(resource_path("icons/exit.png"),wx.BITMAP_TYPE_PNG)
        )

        #Add the "Close" button
        sizer.Add(close_menu_button,0,wx.EXPAND |wx.LEFT |wx.RIGHT |wx.BOTTOM,10)

        #Defines the separator between the "Close" button and the "Last Checked" label
        separator = wx.Panel(panel)
        separator.SetBackgroundColour(wx.Colour(65,65,65))
        separator.SetMinSize((-1, 1))

        #Add the separator
        sizer.Add(separator,0,wx.EXPAND | wx.LEFT | wx.RIGHT,20)

        #A lil space
        sizer.AddSpacer(10)

        #Defines the "Last Checked" label
        last_checked_title = wx.StaticText(panel, label="Last Checked")
        last_checked_title.SetForegroundColour(wx.Colour(150, 150, 150))
        last_checked_title.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))

        #Add the "Last Checked" label
        sizer.Add(last_checked_title,0,wx.LEFT | wx.RIGHT,20)

        #Defines the status label
        self.status_label = wx.StaticText(panel, label="Never • Not checked")
        self.status_label.SetForegroundColour(wx.Colour(207, 207, 207))
        self.status_label.SetFont(wx.Font(9,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))

        #Add the status label
        sizer.Add(self.status_label,0,wx.LEFT | wx.RIGHT | wx.BOTTOM,20)

        #Defines the "Stop Program" button
        quit_button = MenuButton(
            panel,
            "Stop Program",
            lambda: self.execute(self.quit_program),
            normal_colour=wx.Colour(50,16,16),
            hover_colour=wx.Colour(100,0,0),
            pressed_colour=wx.Colour(195,1,1),
            text_colour=wx.Colour(255,50,50),
            icon=wx.Bitmap(resource_path("icons/quit.png"),wx.BITMAP_TYPE_PNG)
        )

        #Add the "Stop Program" button
        sizer.Add(quit_button,0,wx.EXPAND |wx.LEFT |wx.RIGHT |wx.BOTTOM,10)

        #Set the panel size as the sizer's size
        panel.SetSizer(sizer)

        #Sets a sizer to contain the panel that contains the buttons
        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        frame_sizer.Add(panel, 1, wx.EXPAND)

        #Sets the menu size's as the size of the sizer that contains the panel that contains the buttons
        self.SetSizer(frame_sizer)
        #Arrange the things inside the menu
        self.Layout()

        #Sets the height of the menu to be the minimun required
        best_size = frame_sizer.CalcMin()
        self.SetSize((220, best_size.height))

        #Calls the function to make the menu's edges rounded
        self.set_rounded_shape()

    #The function to make the menu's edges rounded
    def set_rounded_shape(self):

        #Gets the menu's size
        width, height = self.GetClientSize()
        #Prevent's rounding before the menu creation
        if width <= 0 or height <= 0:
            return

        #Sets the radius
        radius = 6

        #Sets a bitmap
        bitmap = wx.Bitmap(width,height,1)
        dc = wx.MemoryDC(bitmap)

        #Sets the bitmap background white
        dc.SetBackground(wx.Brush(wx.WHITE))
        dc.Clear()

        #Draws a rounded rectangle in black (cuz it's a bitmap, so only old tv's colors)
        dc.SetBrush(wx.Brush(wx.BLACK))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRoundedRectangle(0,0,width,height,radius)

        #Creates a new bitmap and saves the progress of the old one on it
        dc.SelectObject(wx.NullBitmap)
        region = wx.Region(bitmap,wx.WHITE)

        #Reshapes the menu to the cooler format
        self.SetShape(region)

    #Function to update the status label
    def update_status(self, time, status):
        self.status_label.SetLabel(f"{time} • {status}")
        #Cool color depending on the connection
        if status == "Connected":
            self.status_label.SetForegroundColour(wx.Colour(100, 200, 100))
        else:
            self.status_label.SetForegroundColour(wx.Colour(255, 100, 100))
        #Refreshes the label
        self.status_label.Refresh()

    #What calls the rounding edges function
    def on_size(self, event):
        event.Skip()
        self.set_rounded_shape()

    #Small helper to hide'n execute the button's functions
    def execute(self, function):
        self.Hide()
        function()

    #Binded to the menu's activation
    def on_activate(self, event):
        if not event.GetActive():
            self.Hide()
        event.Skip()

    #Function to show the menu
    def show_menu(self, x, y):
        width, height = self.GetSize()
        self.SetPosition((x - width,y - height))
        self.Show()
        self.Raise()