import wx

class AppWindow(wx.Frame):

    def __init__(self, title, size):
        super().__init__(None,title=title,style=wx.DEFAULT_FRAME_STYLE)
        self.SetSize(size)
        self.SetBackgroundColour(wx.Colour(32, 32, 32))
        self.Centre()
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        self.Hide()