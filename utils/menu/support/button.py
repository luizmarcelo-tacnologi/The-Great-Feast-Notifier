import wx

#A base button class
class MenuButton(wx.Panel):

    #Initialization
    def __init__(self,parent,text,command,icon=None,normal_colour=None,hover_colour=None,pressed_colour=None,text_colour=None):
        #Init the wx.Panel
        super().__init__(parent)

        #Set the passed variables
        self.text = text
        self.command = command
        self.icon = icon
        self.normal_colour = normal_colour or wx.Colour(45, 45, 45)
        self.hover_colour = hover_colour or wx.Colour(56, 56, 56)
        self.pressed_colour = pressed_colour or wx.Colour(65, 65, 65)
        self.text_colour = text_colour or wx.Colour(207, 207, 207)
        #Set the other variables
        self.hovered = False
        self.pressed = False
        self.panel_colour = wx.Colour(32, 32, 32)

        #Base style
        self.SetBackgroundColour(self.panel_colour)
        self.SetMinSize((-1, 25))
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        #Base behavior
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)

    #Function to draw it's contents
    def on_paint(self, event):

        #Buffered drawing
        dc = wx.AutoBufferedPaintDC(self)

        #Paints the background of the button with the color of the parent panel
        dc.SetBackground(wx.Brush(self.panel_colour))
        dc.Clear()

        #Defines the background color of the button based on it's state
        if self.pressed:
            background = self.pressed_colour
        elif self.hovered:
            background = self.hover_colour
        else:
            background = self.normal_colour

        #Defines the size
        width, height = self.GetClientSize()

        #Set the brushes & pens
        dc.SetBrush(wx.Brush(background))
        dc.SetPen(wx.TRANSPARENT_PEN)

        #Draws the button's background color on top of the panel's previous color
        dc.DrawRoundedRectangle(0,0,width,height,6)

        #Sets the text's color, font and size
        dc.SetTextForeground(self.text_colour)
        dc.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))
        text_width, text_height = dc.GetTextExtent(self.text)

        #Test if there is an icon
        if self.icon:
            #Gets the icon's size
            icon_width = self.icon.GetWidth()
            icon_height = self.icon.GetHeight()

            #Sets the space and margin (kinda obvious)
            spacing = 8
            left_margin = 15

            #Defines the icon's starting position
            icon_x = left_margin
            icon_y = (height - icon_height) // 2

            #Defines the text's starting position
            text_x = left_margin + icon_width + spacing
            text_y = (height - text_height) // 2

            #Draws the icon & text
            dc.DrawBitmap(self.icon,icon_x,icon_y,True)
            dc.DrawText(self.text,text_x,text_y)
        else:
            #Defines the text's starting position
            x = (width - text_width) // 2
            y = (height - text_height) // 2
            #Draws it
            dc.DrawText(self.text,x,y)

    #What happens when being hovered
    def on_enter(self, event):
        self.hovered = True
        self.Refresh()
        event.Skip()

    #What happens when stops being hovered
    def on_leave(self, event):
        self.hovered = False
        self.pressed = False
        self.Refresh()
        event.Skip()

    #What happens when being clicked
    def on_left_down(self, event):
        self.pressed = True
        self.Refresh()
        event.Skip()

    #What happens when not being pressed
    def on_left_up(self, event):
        was_pressed = self.pressed
        self.pressed = False
        self.Refresh()
        #If it was pressed runs the assigned command
        if was_pressed and self.hovered:
            self.command()
        event.Skip()