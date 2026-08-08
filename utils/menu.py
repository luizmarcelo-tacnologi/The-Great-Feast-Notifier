import wx

class TrayMenu(wx.Frame):

    def __init__(
        self,
        check_now,
        open_config,
        open_logs,
        quit_program
    ):
        super().__init__(
            None,
            style=wx.FRAME_NO_TASKBAR |
                  wx.STAY_ON_TOP |
                  wx.BORDER_NONE
        )

        self.check_now = check_now
        self.open_config = open_config
        self.open_logs = open_logs
        self.quit_program = quit_program

        self.SetSize((180, 250))

        self.create_menu()

        self.Hide()

    def create_menu(self):

        panel = wx.Panel(self)

        panel.SetBackgroundColour(wx.WHITE)

        sizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(
            panel,
            label="The Great Feast Notifier"
        )

        title.SetFont(
            wx.Font(
                12,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )
        )

        sizer.Add(
            title,
            0,
            wx.ALL | wx.ALIGN_CENTER,
            15
        )

        check_button = wx.Button(
            panel,
            label="Check Now"
        )

        check_button.Bind(
            wx.EVT_BUTTON,
            lambda event: self.execute(self.check_now)
        )

        sizer.Add(
            check_button,
            0,
            wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
            10
        )

        config_button = wx.Button(
            panel,
            label="Settings"
        )

        config_button.Bind(
            wx.EVT_BUTTON,
            lambda event: self.execute(self.open_config)
        )

        sizer.Add(
            config_button,
            0,
            wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
            10
        )

        logs_button = wx.Button(
            panel,
            label="Open Logs"
        )

        logs_button.Bind(
            wx.EVT_BUTTON,
            lambda event: self.execute(self.open_logs)
        )

        sizer.Add(
            logs_button,
            0,
            wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
            10
        )

        exit_button = wx.Button(
            panel,
            label="Exit"
        )

        exit_button.Bind(
            wx.EVT_BUTTON,
            lambda event: self.execute(self.quit_program)
        )

        sizer.Add(
            exit_button,
            0,
            wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
            10
        )

        panel.SetSizer(sizer)

        # Make the panel fill the entire frame.
        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        frame_sizer.Add(panel, 1, wx.EXPAND)

        self.SetSizer(frame_sizer)

        # Make sure the sizer calculates the correct sizes.
        self.Layout()

    def execute(self, function):
        self.Hide()
        function()

    def show_menu(self, x, y):

        width, height = self.GetSize()

        self.SetPosition(
            (x - width, y - height)
        )

        self.Show()
        self.Raise()