import wx

class MenuButton(wx.Panel):

    def __init__(self, parent, text, command):
        super().__init__(parent)

        self.text = text
        self.command = command
        self.hovered = False
        self.pressed = False

        self.panel_colour = wx.Colour(32, 32, 32)
        self.normal_colour = wx.Colour(45, 45, 45)
        self.hover_colour = wx.Colour(56, 56, 56)
        self.pressed_colour = wx.Colour(65, 65, 65)
        self.text_colour = wx.Colour(207, 207, 207)

        self.SetBackgroundColour(self.panel_colour)
        self.SetMinSize((-1, 40))
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)

    def on_paint(self, event):

        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBackground(wx.Brush(self.panel_colour))
        dc.Clear()

        if self.pressed:
            background = self.pressed_colour
        elif self.hovered:
            background = self.hover_colour
        else:
            background = self.normal_colour

        width, height = self.GetClientSize()
        dc.SetBrush(wx.Brush(background))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRoundedRectangle(0, 0,width, height,6)

        dc.SetTextForeground(self.text_colour)
        font = wx.Font(10,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        dc.SetFont(font)
        text_width, text_height = dc.GetTextExtent(self.text)
        x = 15
        y = (height - text_height) // 2
        dc.DrawText(self.text,x,y)

    def on_enter(self, event):
        self.hovered = True
        self.Refresh()
        event.Skip()

    def on_leave(self, event):
        self.hovered = False
        self.pressed = False
        self.Refresh()
        event.Skip()

    def on_left_down(self, event):
        self.pressed = True
        self.Refresh()
        event.Skip()

    def on_left_up(self, event):
        was_pressed = self.pressed
        self.pressed = False
        self.Refresh()
        if was_pressed and self.hovered:
            self.command()
        event.Skip()

class TrayMenu(wx.Frame):

    def __init__(self,check_now,open_config,open_logs,quit_program):

        super().__init__(None,style=wx.FRAME_NO_TASKBAR |wx.STAY_ON_TOP |wx.BORDER_NONE |wx.FRAME_SHAPED)

        self.check_now = check_now
        self.open_config = open_config
        self.open_logs = open_logs
        self.quit_program = quit_program

        self.SetSize((220, 250))
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.create_menu()
        self.Hide()

    def create_menu(self):

        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(32,32,32))

        sizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel,label="The Great Feast Notifier")
        title.SetForegroundColour(wx.Colour(255, 255, 255))
        title.SetFont(wx.Font(12,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD))

        sizer.Add(title,0,wx.ALL | wx.ALIGN_CENTER,15)

        check_button = MenuButton(panel,"Check Now",lambda: self.execute(self.check_now))

        sizer.Add(check_button,0,wx.EXPAND |wx.LEFT |wx.RIGHT |wx.BOTTOM,10)

        config_button = MenuButton(panel,"Settings",lambda: self.execute(self.open_config))

        sizer.Add(config_button,0,wx.EXPAND |wx.LEFT |wx.RIGHT |wx.BOTTOM,10)

        logs_button = MenuButton(panel,"Logs",lambda: self.execute(self.open_logs))

        sizer.Add(logs_button,0,wx.EXPAND |wx.LEFT |wx.RIGHT |wx.BOTTOM,10)

        exit_button = MenuButton(panel,"Close Program",lambda: self.execute(self.quit_program))

        sizer.Add(exit_button,0,wx.EXPAND |wx.LEFT |wx.RIGHT |wx.BOTTOM,10)

        panel.SetSizer(sizer)

        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        frame_sizer.Add(panel, 1, wx.EXPAND)

        self.SetSizer(frame_sizer)
        self.Layout()
        self.set_rounded_shape()

    def set_rounded_shape(self):

        width, height = self.GetClientSize()
        if width <= 0 or height <= 0:
            return
        
        radius = 6
        bitmap = wx.Bitmap(width,height,1)
        dc = wx.MemoryDC(bitmap)

        dc.SetBackground(wx.Brush(wx.WHITE))
        dc.Clear()
        dc.SetBrush(wx.Brush(wx.BLACK))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRoundedRectangle(0,0,width,height,radius)
        dc.SelectObject(wx.NullBitmap)

        region = wx.Region(bitmap,wx.WHITE)

        self.SetShape(region)

    def on_size(self, event):
        event.Skip()
        self.set_rounded_shape()

    def execute(self, function):
        self.Hide()
        function()

    def show_menu(self, x, y):
        width, height = self.GetSize()
        self.SetPosition((x - width,y - height))
        self.Show()
        self.Raise()