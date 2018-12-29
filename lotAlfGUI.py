# -*- coding: utf-8 -*-

import wx
import unicodedata
import lotAlfRegister

class MenuPanel(wx.Panel):
    def __init__(self, parent, ID, dataPanel, register):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        self.parent = parent
        self.dataPanel = dataPanel
        self.register = register


        sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetSizer(sizer)
        self.Centre()

        self.CreateCollectionTrees()

    def CreateCollectionTrees(self):

        if self.GetSizer().GetItemCount() > 0:
            self.GetSizer().Clear(0)
            self.collections_tree.Destroy()
        self.collections_tree = wx.TreeCtrl(self, 1, wx.DefaultPosition, (-1,-1), wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
        root = self.collections_tree.AddRoot('Colecciones')

        self.collections = self.register.get_collections_names()
        self.options = ["Añadir", "Ver", "Comparar", "Estadísticas"]
        for collection in self.collections:
            tree = self.collections_tree.AppendItem(root, collection)
            for option in self.options:
                self.collections_tree.AppendItem(tree, option)

        self.collections_tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=1)

        self.GetSizer().Add(self.collections_tree, 1, wx.EXPAND)
        self.GetSizer().Layout()


    def OnSelChanged(self, event):
        item = event.GetItem()
        item_str = self.collections_tree.GetItemText(item).encode('utf-8')
        if self.collections_tree.GetItemText(item).encode('utf-8') in self.options:
            parent = self.collections_tree.GetItemParent(item) 
            print(self.collections_tree.GetItemText(parent).encode('utf-8'))
            print(self.collections)
            self.dataPanel.SetPage(self.options.index(self.collections_tree.GetItemText(item).encode('utf-8')), self.collections.index(self.collections_tree.GetItemText(parent).encode('utf-8')))


class UserPanel(wx.Panel):
    def __init__(self, parent, ID, register):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)


class DataPanel(wx.Panel):
    def __init__(self, parent, ID, register):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        self.register = register

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        startPanel = StartPanel(self, -1, register)
        viewPanel = ViewPanel(self, -1, register)
        addPanel = AddPanel(self, -1, register)
        comparePanel = ComparePanel(self, -1, register)
        statisticsPanel = StatisticsPanel(self, -1, register)

        self.sizer.Add(startPanel, 1, wx.EXPAND)
        self.sizer.Add(viewPanel, 1, wx.EXPAND)
        self.sizer.Add(addPanel, 1, wx.EXPAND)
        self.sizer.Add(comparePanel, 1, wx.EXPAND)
        self.sizer.Add(statisticsPanel, 1, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.Centre()

        self.pages = [addPanel, viewPanel, comparePanel, statisticsPanel, startPanel]
        self.SetPage(4, 0)

    def SetPage(self, enabled_page, collection):
        for page in self.pages:
            self.sizer.Hide(page)
            if len(self.register.get_collections()) > 0:
                page.UpdateCollection(collection)


        self.sizer.Show(self.pages[enabled_page])
        self.sizer.Layout()


class ViewMenuPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        legend_sizer = wx.BoxSizer(wx.VERTICAL)

        self.statuses = ['Perfecto', 'Roto', 'Doblado', 'Falta']
        self.status_colors = [(0xF0,0x80,0x80), (0xCA,0xE1,0xFF), (0xA2,0xCD,0x5A), (0xFF,0xE7,0xBA)]

        perfect = wx.StaticText(self, -1, self.statuses[0])
        broken = wx.StaticText(self, -1, self.statuses[1])
        bent = wx.StaticText(self, -1, self.statuses[2])
        missing = wx.StaticText(self, -1, self.statuses[3])

        perfect.SetBackgroundColour(self.status_colors[0])
        broken.SetBackgroundColour(self.status_colors[1])
        bent.SetBackgroundColour(self.status_colors[2])
        missing.SetBackgroundColour(self.status_colors[3])

        legend_sizer.Add(perfect, 0, wx.ALIGN_CENTER)
        legend_sizer.Add(broken, 0, wx.ALIGN_CENTER)
        legend_sizer.Add(bent, 0, wx.ALIGN_CENTER)
        legend_sizer.Add(missing, 0, wx.ALIGN_CENTER)

        filter_button = wx.Button(self, -1, 'Filtrar')

        print_button = wx.Button(self, -1, 'Imprimir')

        sizer.Add(legend_sizer, 1, wx.ALIGN_CENTER)
        sizer.Add(filter_button, 1, wx.SHAPED)
        sizer.Add(print_button, 1, wx.SHAPED)

        self.SetSizer(sizer)


class ViewPanel(wx.Panel):
    def __init__(self, parent, ID, register):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        self.register = register

        sizer = wx.BoxSizer(wx.VERTICAL)

        total_width, total_height = wx.GetDisplaySize()
        button_width = total_height / 13
        button_height = total_height * 7 / 8 / 10

        self.viewMenuPanel = ViewMenuPanel(self, -1)

        numbers_sizer = wx.BoxSizer(wx.HORIZONTAL)


        self.all_buttons = []

        ten_thousands_sizer = wx.GridSizer(10, 1, 0, 0)

        for i in range(0, 10):
            button = wx.Button(self, wx.ID_ANY, str(i), size=(button_width, button_height))
            button.number = i * 10000
            button.unit = 10000
            self.all_buttons.append(button)
            ten_thousands_sizer.Add(button, 0, wx.EXPAND)

        thousands_sizer =  wx.GridSizer(10, 1, 0, 0)

        for i in range(0, 10):
            button = wx.Button(self, wx.ID_ANY, str(i), size=(button_width, button_height))
            button.number = i * 1000
            button.unit = 1000
            self.all_buttons.append(button)
            thousands_sizer.Add(button, 0, wx.EXPAND)

        hundreds_sizer =  wx.GridSizer(10, 1, 0, 0)

        for i in range(0, 10):
            button = wx.Button(self, wx.ID_ANY, str(i), size=(button_width, button_height))
            button.number = i * 100
            button.unit = 100
            self.all_buttons.append(button)
            hundreds_sizer.Add(button, 0, wx.EXPAND)

        tens_sizer = wx.GridSizer(10, 10, 0, 0)
        tens_buttons = []
        for j in range(0, 10):
            for i in range(0, 10):
                button = wx.Button(self, wx.ID_ANY, str(j*10 + i), size=(button_width, button_height))
                button.number = j*10 + i
                button.unit = 1
                self.all_buttons.append(button)
                tens_buttons.append((button, 0, wx.EXPAND))
        tens_sizer.AddMany(tens_buttons)
        
        numbers_sizer.Add(ten_thousands_sizer, 1, wx.EXPAND)
        numbers_sizer.Add(thousands_sizer, 1, wx.EXPAND)
        numbers_sizer.Add(hundreds_sizer, 1, wx.EXPAND)
        numbers_sizer.Add(tens_sizer, 10, wx.ALL, border=30)


        self.number = wx.StaticText(self, -1, 'Centena: 00000')
        self.collection_text = wx.StaticText(self, -1, '')

        sizer.Add(wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL), 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.collection_text, 1, wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL), 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.viewMenuPanel, 1, wx.EXPAND |wx.ALL, 10)
        sizer.Add(wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL), 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.number, 1, wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL), 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(numbers_sizer, 7, wx.EXPAND)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.OnClick)
        self.Bind(wx.EVT_SHOW, self.OnShow)

        self.current_ten_thousands = 0
        self.current_thousands = 0
        self.current_hundreds = 0

    def UpdateCollection(self, collection):
        self.collection = collection
        self.collection_text.SetLabel(self.register.get_collections_names()[collection])

    def UpdateNumbers(self, unit, number):

        if unit == 10000:
            self.current_ten_thousands = number
        elif unit == 1000:
            self.current_thousands = number
        elif unit == 100:
            self.current_hundreds = number

        for button in self.all_buttons:
            if button.unit == 1:
                temp_number = self.current_ten_thousands + self.current_thousands + self.current_hundreds + button.number
                number_data = self.register.get_number_data(self.collection, temp_number)
                if number_data is not None:
                    button.SetBackgroundColour(self.viewMenuPanel.status_colors[self.viewMenuPanel.statuses.index(number_data['status'])])
                else:
                    button.SetBackgroundColour(self.viewMenuPanel.status_colors[self.viewMenuPanel.statuses.index('Falta')])


        self.number.SetLabel('Centena: {:05d}'.format(self.current_ten_thousands + self.current_thousands + self.current_hundreds))

    def OnShow(self, event):
        self.UpdateNumbers(0, 0)

    def OnClick(self, event):

        for button in self.all_buttons:
            if button.unit > 1:
                if event.GetEventObject().unit == button.unit:
                    button.SetBackgroundColour(wx.NullColour)

        if event.GetEventObject().unit > 1:
            event.GetEventObject().SetBackgroundColour(wx.LIGHT_GREY)
        else:
            number = self.current_ten_thousands + self.current_thousands + self.current_hundreds + event.GetEventObject().number
            numberdialog = NumberDialog(self, -1, 'Número {}'.format(number), self.register, self.collection, number)
            numberdialog.ShowModal()

        self.UpdateNumbers(event.GetEventObject().unit, event.GetEventObject().number)


class StartPanel(wx.Panel):
    def __init__(self, parent, ID, register):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        self.register = register
        self.parent = parent
        sizer = wx.BoxSizer(wx.VERTICAL)

        welcome_font = wx.Font(38, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        name_font = wx.Font(69, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)

        welcome_statictext = wx.StaticText(self, -1, 'Bienvenido a')
        welcome_statictext.SetFont(welcome_font)
        name_statictext = wx.StaticText(self, -1, 'LotAlf')
        name_statictext.SetFont(name_font)

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)

        new_collection_button = wx.Button(self, -1, 'Nueva Colección')
        import_button = wx.Button(self, -1, 'Importar Colección')

        new_collection_button.Bind(wx.EVT_BUTTON, self.NewCollection)

        buttons_sizer.Add(new_collection_button, 1, wx.ALL | wx.ALIGN_CENTER, border=50)
        buttons_sizer.Add(import_button, 1, wx.ALL | wx.ALIGN_CENTER, border=50)

        sizer.Add(welcome_statictext, 1, wx.ALL | wx.ALIGN_CENTER, border=10)
        sizer.Add(name_statictext, 1, wx.ALL | wx.ALIGN_CENTER, border=10)
        sizer.Add(buttons_sizer, 1, wx.ALL | wx.EXPAND, border=10)

        self.SetSizer(sizer)

    def UpdateCollection(self, collection):
        self.collection = collection

    def NewCollection(self, event):
        newCollectionDialog = NewCollectionDialog(self, -1, 'Nueva Colección', self.register)
        newCollectionDialog.ShowModal()

class NewCollectionDialog(wx.Dialog):
    def __init__(self, parent, id, title, register):
        total_width, total_height = wx.GetDisplaySize()
        wx.Dialog.__init__(self, parent, id, title, size=(500, 300))
        self.register = register
        self.parent = parent
        sizer = wx.BoxSizer(wx.VERTICAL)
  
        def new(evt):
            self.register.new_collection(name_textctrl.GetValue(), fill_checkbox.GetValue()) 
            self.parent.parent.menuPanel.CreateCollectionTrees()
            self.Destroy() 
        def cancel(evt):
            self.Destroy()

        name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        name_statictext = wx.StaticText(self, -1, 'Nombre: ', size=(100, 20))
        name_textctrl = wx.TextCtrl(self, -1, '', size=(100, 20))
        name_sizer.Add(name_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        name_sizer.Add(name_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)

        fill_sizer = wx.BoxSizer(wx.HORIZONTAL)
        fill_checkbox = wx.CheckBox(self, -1, 'Marcar todos como completados', (10, 10))
        fill_sizer.Add(fill_checkbox, 1, wx.ALL | wx.ALIGN_CENTER)

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        new_button = wx.Button(self, -1, 'Guardar')
        cancel_button = wx.Button(self, -1, 'Cancelar')
        new_button.Bind(wx.EVT_BUTTON, new)
        cancel_button.Bind(wx.EVT_BUTTON, cancel)

        buttons_sizer.Add(new_button, 1, wx.ALL | wx.ALIGN_CENTER)
        buttons_sizer.Add(cancel_button, 1, wx.ALL | wx.ALIGN_CENTER)

        sizer.Add(name_sizer, 1, wx.ALL | wx.ALIGN_LEFT, border=10)
        sizer.Add(fill_sizer, 1, wx.ALL | wx.ALIGN_LEFT, border=10)
        sizer.Add(buttons_sizer, 1, wx.ALL | wx.EXPAND, border=10)

        self.SetSizer(sizer)


class NumberDialog(wx.Dialog):
    def __init__(self, parent, id, title, register, collection, number):
        total_width, total_height = wx.GetDisplaySize()
        wx.Dialog.__init__(self, parent, id, title, size=(500, 300))
        self.register = register
        sizer = wx.BoxSizer(wx.VERTICAL)

        def toggle1(evt):
            if evt.GetEventObject().GetValue() == evt.GetEventObject().default_text:
                evt.GetEventObject().SetValue("")
            evt.Skip()
        def toggle2(evt):
            if evt.GetEventObject().GetValue() == "":
                evt.GetEventObject().SetValue(evt.GetEventObject().default_text)
            evt.Skip()   
        def save(evt):
            data = {'status': status_combobox.GetStringSelection(),
                    'year': year_textctrl.GetLabel(),
                    'coin': coin_textctrl.GetLabel(),
                    'administration': {'province': administration_province_textctrl.GetLabel(),
                                       'town': administration_town_textctrl.GetLabel(),
                                       'number': administration_number_textctrl.GetLabel()
                                      }
                    }
            self.register.save_to_collection(collection, number, data) 
            self.Destroy() 
        def cancel(evt):
            self.Destroy()
        def load():
            number_data = self.register.get_number_data(collection, number)
            if number_data is not None:
                status_combobox.SetSelection(status_combobox.FindString(number_data['status']))
                year_textctrl.SetLabel(number_data['year'])
                coin_textctrl.SetLabel(number_data['coin'])
                administration_province_textctrl.SetLabel(number_data['administration']['province'])
                administration_town_textctrl.SetLabel(number_data['administration']['town'])
                administration_number_textctrl.SetLabel(number_data['administration']['number'])


        statuses = ['Perfecto', 'Roto', 'Doblado', 'Falta']
        status_sizer = wx.BoxSizer(wx.HORIZONTAL)
        status_statictext = wx.StaticText(self, -1, 'Estado: ', size=(100, 20))
        status_combobox = wx.ComboBox(self, -1, choices=statuses, style=wx.CB_READONLY,  size=(100, 20))
        status_sizer.Add(status_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        status_sizer.Add(status_combobox, 1, wx.ALL | wx.ALIGN_CENTER)

        year_sizer = wx.BoxSizer(wx.HORIZONTAL)
        year_statictext = wx.StaticText(self, -1, 'Año: ', size=(100, 20))
        year_textctrl = wx.TextCtrl(self, -1, '', size=(100, 20))
        year_sizer.Add(year_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        year_sizer.Add(year_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)

        coin_sizer = wx.BoxSizer(wx.HORIZONTAL)
        coin_statictext = wx.StaticText(self, -1, 'Moneda: ', size=(100, 20))
        coin_textctrl = wx.TextCtrl(self, -1, '', size=(100, 20))
        coin_sizer.Add(coin_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        coin_sizer.Add(coin_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)

        administration_sizer = wx.BoxSizer(wx.HORIZONTAL)
        administration_statictext = wx.StaticText(self, -1, 'Administración', size=(100, 20))
        administration_province_textctrl = wx.TextCtrl(self, -1, 'Provincia', size=(100, 20))
        administration_province_textctrl.default_text = 'Provincia'
        administration_province_textctrl.Bind(wx.EVT_SET_FOCUS, toggle1)
        administration_province_textctrl.Bind(wx.EVT_KILL_FOCUS, toggle2)
        administration_town_textctrl = wx.TextCtrl(self, -1, 'Municipio', size=(200, 20))
        administration_town_textctrl.default_text = 'Municipio'
        administration_town_textctrl.Bind(wx.EVT_SET_FOCUS, toggle1)
        administration_town_textctrl.Bind(wx.EVT_KILL_FOCUS, toggle2)
        administration_number_textctrl = wx.TextCtrl(self, -1, 'Número', size=(50, 20))
        administration_number_textctrl.default_text = 'Número'
        administration_number_textctrl.Bind(wx.EVT_SET_FOCUS, toggle1)
        administration_number_textctrl.Bind(wx.EVT_KILL_FOCUS, toggle2)
        administration_sizer.Add(administration_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        administration_sizer.Add(administration_province_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)
        administration_sizer.Add(administration_town_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)
        administration_sizer.Add(administration_number_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)


        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        save_button = wx.Button(self, -1, 'Guardar')
        cancel_button = wx.Button(self, -1, 'Cancelar')
        save_button.Bind(wx.EVT_BUTTON, save)
        cancel_button.Bind(wx.EVT_BUTTON, cancel)

        buttons_sizer.Add(save_button, 1, wx.ALL | wx.ALIGN_CENTER)
        buttons_sizer.Add(cancel_button, 1, wx.ALL | wx.ALIGN_CENTER)

        sizer.Add(status_sizer, 1, wx.ALL | wx.ALIGN_LEFT, border=10)
        sizer.Add(year_sizer, 1, wx.ALL | wx.ALIGN_LEFT, border=10)
        sizer.Add(coin_sizer, 1, wx.ALL | wx.ALIGN_LEFT, border=10)
        sizer.Add(administration_sizer, 1, wx.ALL | wx.ALIGN_LEFT, border=10)
        sizer.Add(buttons_sizer, 1, wx.ALL | wx.EXPAND, border=10)

        self.SetSizer(sizer)

        load()


class AddPanel(wx.Panel):
    def __init__(self, parent, ID, register):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        self.register = register

        sizer = wx.BoxSizer(wx.VERTICAL)

        def toggle1(evt):
            if evt.GetEventObject().GetValue() == evt.GetEventObject().default_text:
                evt.GetEventObject().SetValue("")
            evt.Skip()
        def toggle2(evt):
            if evt.GetEventObject().GetValue() == "":
                evt.GetEventObject().SetValue(evt.GetEventObject().default_text)
            evt.Skip() 
        def add(evt):
            data = {'status': status_combobox.GetStringSelection(),
                    'year': year_textctrl.GetLabel(),
                    'coin': coin_textctrl.GetLabel(),
                    'administration': {'province': administration_province_textctrl.GetLabel(),
                                       'town': administration_town_textctrl.GetLabel(),
                                       'number': administration_number_textctrl.GetLabel()
                                      }
                    }
            self.register.add_to_collection(self.collection, number_textctrl.GetValue(), data)

        number_sizer = wx.BoxSizer(wx.HORIZONTAL)
        number_statictext = wx.StaticText(self, -1, 'Número: ', size=(100, 20))
        number_textctrl = wx.TextCtrl(self, -1, '', size=(100, 20))
        number_sizer.Add(number_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        number_sizer.Add(number_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)

        statuses = ['Perfecto', 'Roto', 'Doblado', 'Falta']
        status_sizer = wx.BoxSizer(wx.HORIZONTAL)
        status_statictext = wx.StaticText(self, -1, 'Estado: ', size=(100, 20))
        status_combobox = wx.ComboBox(self, -1, choices=statuses, style=wx.CB_READONLY,  size=(100, 20))
        status_sizer.Add(status_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        status_sizer.Add(status_combobox, 1, wx.ALL | wx.ALIGN_CENTER)

        year_sizer = wx.BoxSizer(wx.HORIZONTAL)
        year_statictext = wx.StaticText(self, -1, 'Año: ', size=(100, 20))
        year_textctrl = wx.TextCtrl(self, -1, '', size=(100, 20))
        year_sizer.Add(year_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        year_sizer.Add(year_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)

        coin_sizer = wx.BoxSizer(wx.HORIZONTAL)
        coin_statictext = wx.StaticText(self, -1, 'Moneda: ', size=(100, 20))
        coin_textctrl = wx.TextCtrl(self, -1, '', size=(100, 20))
        coin_sizer.Add(coin_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        coin_sizer.Add(coin_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)

        administration_sizer = wx.BoxSizer(wx.HORIZONTAL)
        administration_statictext = wx.StaticText(self, -1, 'Administración', size=(100, 20))
        administration_province_textctrl = wx.TextCtrl(self, -1, 'Provincia', size=(100, 20))
        administration_province_textctrl.default_text = 'Provincia'
        administration_province_textctrl.Bind(wx.EVT_SET_FOCUS,toggle1)
        administration_province_textctrl.Bind(wx.EVT_KILL_FOCUS,toggle2)
        administration_town_textctrl = wx.TextCtrl(self, -1, 'Municipio', size=(100, 20))
        administration_town_textctrl.default_text = 'Municipio'
        administration_town_textctrl.Bind(wx.EVT_SET_FOCUS,toggle1)
        administration_town_textctrl.Bind(wx.EVT_KILL_FOCUS,toggle2)
        administration_number_textctrl = wx.TextCtrl(self, -1, 'Número', size=(100, 20))
        administration_number_textctrl.default_text = 'Número'
        administration_number_textctrl.Bind(wx.EVT_SET_FOCUS,toggle1)
        administration_number_textctrl.Bind(wx.EVT_KILL_FOCUS,toggle2)
        administration_sizer.Add(administration_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        administration_sizer.Add(administration_province_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)
        administration_sizer.Add(administration_town_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)
        administration_sizer.Add(administration_number_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)


        log_statictext = wx.StaticText(self, -1, 'Listo', style=wx.ALIGN_CENTRE_HORIZONTAL, size=(100, 20))


        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        save_button = wx.Button(self, -1, 'Añadir')

        buttons_sizer.Add(save_button, 1, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, border=100)
        save_button.Bind(wx.EVT_BUTTON, add)

        sizer.Add(wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL), 1, wx.EXPAND | wx.ALL, 20)
        sizer.Add(number_sizer, 0, wx.ALL | wx.ALIGN_CENTER, border=10)
        sizer.Add(status_sizer, 0, wx.ALL | wx.ALIGN_CENTER, border=10)
        sizer.Add(year_sizer, 0, wx.ALL | wx.ALIGN_CENTER, border=10)
        sizer.Add(coin_sizer, 0, wx.ALL | wx.ALIGN_CENTER, border=10)
        sizer.Add(administration_sizer, 0, wx.ALL | wx.ALIGN_CENTER, border=10)
        sizer.Add(log_statictext, 0, wx.ALL | wx.ALIGN_CENTER, border=10)
        sizer.Add(buttons_sizer, 0, wx.ALL | wx.ALIGN_CENTER, border=10)
        sizer.Add(wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL), 1, wx.EXPAND | wx.ALL, 20)

        self.SetSizer(sizer)

    def UpdateCollection(self, collection):
        self.collection = collection

class ComparePanel(wx.Panel):
    def __init__(self, parent, ID, register):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        self.text = wx.StaticText(self, -1, 'ComparePanel')

    def UpdateCollection(self, collection):
        self.collection = collection

class StatisticsPanel(wx.Panel):
    def __init__(self, parent, ID, register):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        self.text = wx.StaticText(self, -1, 'StatisticsPanel')

    def UpdateCollection(self, collection):
        self.collection = collection


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title, register):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(350, 300))

        total_width, total_height = wx.GetDisplaySize()

        global_vertical_splitter = wx.SplitterWindow(self, -1)
        left_horizontal_splitter = wx.SplitterWindow(global_vertical_splitter, -1)
        userPanel = UserPanel(left_horizontal_splitter, -1, register)
        dataPanel = DataPanel(global_vertical_splitter, -1, register)
        menuPanel = MenuPanel(left_horizontal_splitter, -1, dataPanel, register)
        dataPanel.menuPanel = menuPanel


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
        register = lotAlfRegister.Register()
        frame = MyFrame(None, -1, 'LotAlf', register)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()