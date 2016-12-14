import wx

# class App(wx.App):
#     def OnInit(self):
#        dlg=wx.MessageDialog(None,"Is this the coolest thing ever!",
#        "MessageDialog",wx.YES_NO|wx.ICON_QUESTION)
#        result=dlg.ShowModal()
#        dlg.Destroy()
# app=App()
# app.MainLoop()

# # -*- coding: utf-8 -*-
# """
# http://blog.csdn.net/chenghit
#
#
# app = wx.App(False) #创建1个APP，禁用stdout/stderr重定向
# frame = wx.Frame(None, wx.ID_ANY, "Hello, World!")  #这是一个顶层的window
# frame.Show(True)    #显示这个frame
# app.MainLoop()

class MainWindow(wx.Frame):
    """We simply derive a new class of Frame."""
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title = title, size = (600, 400))
        self.control = wx.TextCtrl(self, style = wx.TE_MULTILINE)
        self.CreateStatusBar()    # 创建位于窗口的底部的状态栏

        # 设置菜单
        filemenu = wx.Menu()

        # wx.ID_ABOUT和wx.ID_EXIT是wxWidgets提供的标准ID
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", \
            " Information about this program")    # (ID, 项目名称, 状态栏信息)
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", \
            " Terminate the program")    # (ID, 项目名称, 状态栏信息)

        # 创建菜单栏
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")    # 在菜单栏中添加filemenu菜单
        self.SetMenuBar(menuBar)    # 在frame中添加菜单栏

        # 设置events
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        self.Show(True)

    def OnAbout(self, e):
        # 创建一个带"OK"按钮的对话框。wx.OK是wxWidgets提供的标准ID
        dlg = wx.MessageDialog(self, "A small text editor.", \
            "About Sample Editor", wx.OK)    # 语法是(self, 内容, 标题, ID)
        dlg.ShowModal()    # 显示对话框
        dlg.Destroy()    # 当结束之后关闭对话框

    def OnExit(self, e):
        self.Close(True)    # 关闭整个frame


app = wx.App(False)
frame = MainWindow(None, title = "Small editor")
app.MainLoop()