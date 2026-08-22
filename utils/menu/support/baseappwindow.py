import wx

#Just a window that is used in Settings and Logs
class AppWindow(wx.Frame):

    #The initialization
    def __init__(self, title, size):
        #Init the wx.Frame
        super().__init__(None,title=title,style=wx.DEFAULT_FRAME_STYLE)

        #Set the base style & behavior of the window
        self.SetSize(size)
        self.SetBackgroundColour(wx.Colour(32, 32, 32))
        self.Centre()
        self.Bind(wx.EVT_CLOSE, self.on_close)

    #Lil close func
    def on_close(self, event):
        self.Hide()