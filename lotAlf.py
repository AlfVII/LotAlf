#!/usr/bin/python
# splitterwindow.py
import wx

class MenuPanel(wx.Panel):
    def __init__(self, parent, ID, dataPanel):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        self.parent = parent
        self.dataPanel = dataPanel

        self.collections_tree = wx.TreeCtrl(self, 1, wx.DefaultPosition, (-1,-1), wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)

        sizer = wx.BoxSizer(wx.VERTICAL)

        root = self.collections_tree.AddRoot('Colecciones')

        # self.collections = LoadCollectionsFromDB()
        self.collections = ['Coleccion de Alfonso']
        self.options = ["Anadir", "Ver", "Comparar", "Estadisticas"]
        for collection in self.collections:
            tree = self.collections_tree.AppendItem(root, collection)
            for option in self.options:
                self.collections_tree.AppendItem(tree, option)

        self.collections_tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=1)

        sizer.Add(self.collections_tree, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Centre()

    def OnSelChanged(self, event):
        item = event.GetItem()
        if self.collections_tree.GetItemText(item) in self.options:
            print(self.options.index(self.collections_tree.GetItemText(item)))
            self.dataPanel.SetPage(self.options.index(self.collections_tree.GetItemText(item)))


class UserPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)

class DataPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        viewPanel = ViewPanel(self, -1)
        addPanel = AddPanel(self, -1)
        comparePanel = ComparePanel(self, -1)
        statisticsPanel = StatisticsPanel(self, -1)

        self.sizer.Add(viewPanel, 1, wx.EXPAND)
        self.sizer.Add(addPanel, 1, wx.EXPAND)
        self.sizer.Add(comparePanel, 1, wx.EXPAND)
        self.sizer.Add(statisticsPanel, 1, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.Centre()

        self.pages = [addPanel, viewPanel, comparePanel, statisticsPanel]
        self.SetPage(1)

    def SetPage(self, enabled_page):
        for page in self.pages:
            self.sizer.Hide(page)


        self.sizer.Show(self.pages[enabled_page])
        self.sizer.Layout()

class ViewMenuPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        legend_sizer = wx.BoxSizer(wx.VERTICAL)

        perfect = wx.StaticText(self, -1, 'Perfectos')
        broken = wx.StaticText(self, -1, 'Rotos')
        bent = wx.StaticText(self, -1, 'Doblados')
        missing = wx.StaticText(self, -1, 'Falta')

        perfect.SetBackgroundColour((0xF0,0x80,0x80))
        broken.SetBackgroundColour((0xCA,0xE1,0xFF))
        bent.SetBackgroundColour((0xA2,0xCD,0x5A))
        missing.SetBackgroundColour((0xFF,0xE7,0xBA))

        legend_sizer.Add(perfect, 0, wx.SHAPED)
        legend_sizer.Add(broken, 0, wx.SHAPED)
        legend_sizer.Add(bent, 0, wx.SHAPED)
        legend_sizer.Add(missing, 0, wx.SHAPED)

        filter_button = wx.Button(self, -1, 'Filtrar')

        print_button = wx.Button(self, -1, 'Imprimir')

        sizer.Add(legend_sizer, 1, wx.SHAPED)
        sizer.Add(filter_button, 1, wx.SHAPED)
        sizer.Add(print_button, 1, wx.SHAPED)

        self.SetSizer(sizer)


class ViewPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        sizer = wx.BoxSizer(wx.VERTICAL)

        total_width, total_height = wx.GetDisplaySize()
        button_width = total_height / 13
        button_height = total_height * 7 / 8 / 10

        viewMenuPanel = ViewMenuPanel(self, -1)

        numbers_sizer = wx.BoxSizer(wx.HORIZONTAL)

        ten_thousands_sizer = wx.BoxSizer(wx.VERTICAL)

        for i in range(0, 10):
            ten_thousands_sizer.Add(wx.Button(self, i + 120, str(i), size=(button_width, button_height)), 0, wx.EXPAND)

        thousands_sizer = wx.BoxSizer(wx.VERTICAL)

        for i in range(0, 10):
            thousands_sizer.Add(wx.Button(self, i + 110, str(i), size=(button_width, button_height)), 0, wx.EXPAND)

        hundreds_sizer = wx.BoxSizer(wx.VERTICAL)

        for i in range(0, 10):
            hundreds_sizer.Add(wx.Button(self, i + 100, str(i), size=(button_width, button_height)), 0, wx.EXPAND)

        tens_sizer = wx.GridSizer(10, 10, 0, 0)
        tens_buttons = []
        for j in range(0, 10):
            for i in range(0, 10):
                tens_buttons.append((wx.Button(self, j*10 + i, str(j*10 + i), size=(button_width, button_height)), 0, wx.EXPAND))
        tens_sizer.AddMany(tens_buttons)
        
        numbers_sizer.Add(ten_thousands_sizer, 1, wx.EXPAND)
        numbers_sizer.Add(thousands_sizer, 1, wx.EXPAND)
        numbers_sizer.Add(hundreds_sizer, 1, wx.EXPAND)
        numbers_sizer.Add(tens_sizer, 10, wx.ALL, border=50)

        sizer.Add(viewMenuPanel, 1, wx.EXPAND)
        sizer.Add(numbers_sizer, 7, wx.EXPAND)
        self.SetSizer(sizer)






class AddPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        self.text = wx.StaticText(self, -1, 'AddPanel')

class ComparePanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        self.text = wx.StaticText(self, -1, 'ComparePanel')

class StatisticsPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        self.text = wx.StaticText(self, -1, 'StatisticsPanel')


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(350, 300))

        total_width, total_height = wx.GetDisplaySize()

        global_vertical_splitter = wx.SplitterWindow(self, -1)
        left_horizontal_splitter = wx.SplitterWindow(global_vertical_splitter, -1)
        userPanel = UserPanel(left_horizontal_splitter, -1)
        dataPanel = DataPanel(global_vertical_splitter, -1)
        menuPanel = MenuPanel(left_horizontal_splitter, -1, dataPanel)


        menuPanel.SetBackgroundColour(wx.LIGHT_GREY)
        userPanel.SetBackgroundColour(wx.BLUE)
        menuPanel.SetBackgroundColour(wx.RED)

        left_horizontal_splitter.SplitHorizontally(userPanel, menuPanel)
        left_horizontal_splitter.SetSashPosition(total_height/4, True)
        global_vertical_splitter.SplitVertically(left_horizontal_splitter, dataPanel)
        global_vertical_splitter.SetSashPosition(total_width/6, True)


        self.Centre()
        self.Maximize(True)

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'splitterwindow.py')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()