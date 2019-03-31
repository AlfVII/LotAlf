# -*- coding: utf-8 -*-

import wx
import unicodedata
import lotAlfRegister
# import lotAlfPrinter


statuses = ['Perfecto', 'Defectuoso', 'Falta']

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
        # self.collections_tree = wx.TreeCtrl(self, 1, wx.DefaultPosition, (-1,-1), wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
        self.collections_tree = wx.TreeCtrl(self, 1, wx.DefaultPosition, (-1,-1), wx.TR_HAS_BUTTONS)
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

        self.collections_tree.Expand(root)

    def OnSelChanged(self, event):
        item = event.GetItem()
        item_str = self.collections_tree.GetItemText(item).encode('utf-8')
        if item == self.collections_tree.GetRootItem():
            self.dataPanel.SetPage(4, 0)
        if self.collections_tree.GetItemText(item).encode('utf-8') in self.options:
            parent = self.collections_tree.GetItemParent(item) 
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
            if self.register.get_number_collections() > 0:
                page.UpdateCollection(collection)


        self.sizer.Show(self.pages[enabled_page])
        self.sizer.Layout()


class ViewMenuPanel(wx.Panel):
    def __init__(self, parent, ID, register):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.filters = {}
        self.register = register
        self.parent = parent

        legend_sizer = wx.BoxSizer(wx.VERTICAL)

        self.status_colors = [(0xA2,0xCD,0x5A), (0xF0,0x80,0x80), (0xFF,0xE7,0xBA)]

        perfect = wx.StaticText(self, -1, statuses[0])
        defective = wx.StaticText(self, -1, statuses[1])
        missing = wx.StaticText(self, -1, statuses[2])

        perfect.SetBackgroundColour(self.status_colors[0])
        defective.SetBackgroundColour(self.status_colors[1])
        missing.SetBackgroundColour(self.status_colors[2])

        legend_sizer.Add(perfect, 0, wx.ALIGN_CENTER)
        legend_sizer.Add(defective, 0, wx.ALIGN_CENTER)
        legend_sizer.Add(missing, 0, wx.ALIGN_CENTER)

        filter_button = wx.Button(self, -1, 'Filtrar')
        erase_button = wx.Button(self, wx.ID_ANY, "Borrar filtros")

        print_button = wx.Button(self, -1, 'Imprimir')

        sizer.Add(legend_sizer, 1, wx.ALIGN_CENTER)
        sizer.Add(filter_button, 1, wx.SHAPED)
        sizer.Add(erase_button, 1, wx.SHAPED)
        sizer.Add(print_button, 1, wx.SHAPED)

        self.Bind(wx.EVT_BUTTON, self.OnFilter, filter_button)
        self.Bind(wx.EVT_BUTTON, self.OnErase, erase_button)
        # self.Bind(wx.EVT_BUTTON, self.OnPrint, print_button)

        self.SetSizer(sizer)

    def UpdateCollection(self, collection):
        self.collection = collection

    def OnFilter(self, event):
        filters_dialog = FiltersDialog(self, -1, 'Filtros', self.collection, self.register)
        filters_dialog.ShowModal()
        self.parent.FilterNumbers(self.filtered_data)

    def OnErase(self, event): 
        self.parent.FilterNumbers(None)

    # def OnPrint(self, event):
    #     doc = lotAlfPrinter.DataToPdf('fields', self.filtered_data, sort_by=('size', 'DESC'),
    #                     title='Log Files Over 1MB')
    #     doc.export('LogFiles.pdf')

class ViewPanel(wx.Panel):
    def __init__(self, parent, ID, register):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        self.register = register
        self.parent = parent
        self.filtered_numbers = None

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.collection = None

        total_width, total_height = wx.GetDisplaySize()
        button_width = total_height / 13
        button_height = total_height * 7 / 8 / 10

        self.viewMenuPanel = ViewMenuPanel(self, -1, self.register)

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
        self.filtered_count = wx.StaticText(self, -1, 'Números que cumplen el filtro: 100000')
        self.collection_text = wx.StaticText(self, -1, '')

        sizer.Add(wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL), 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.collection_text, 1, wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL), 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.viewMenuPanel, 1, wx.EXPAND |wx.ALL, 10)
        sizer.Add(wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL), 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.filtered_count, 1, wx.ALL | wx.ALIGN_CENTER)
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
        self.viewMenuPanel.UpdateCollection(collection)
        self.collection_text.SetLabel(self.register.get_collections_names()[collection])

    def FilterNumbers(self, numbers):
        self.filtered_numbers = numbers
        self.filtered_count.SetLabel('Números que cumplen el filtro: {:05d}'.format(len(numbers)))
        print(len(numbers))
        self.UpdateNumbers(0, 0)


    def UpdateNumbers(self, unit, number):

        if unit == 10000:
            self.current_ten_thousands = number
        elif unit == 1000:
            self.current_thousands = number
        elif unit == 100:
            self.current_hundreds = number

        if self.collection is not None:
            for button in self.all_buttons:
                if button.unit == 1:
                    temp_number = self.current_ten_thousands + self.current_thousands + self.current_hundreds + button.number
                    number_data = self.register.get_number_data(self.collection, temp_number)
                    button.SetBackgroundColour(self.viewMenuPanel.status_colors[statuses.index(number_data['status'])])
                    if self.filtered_numbers is not None:
                        if temp_number in self.filtered_numbers:
                            button.Show()
                        else:
                            button.Hide()
                    else:
                        button.Show()


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
        wx.Dialog.__init__(self, parent, id, title, size=(500, 400))
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

            administration_province = administration_province_textctrl.GetValue().encode('utf-8')
            if administration_province == administration_province_textctrl.default_text:
                administration_province = ''
            administration_town = administration_town_textctrl.GetValue().encode('utf-8')
            if administration_town == administration_town_textctrl.default_text:
                administration_town = ''
            administration_number = administration_number_textctrl.GetValue().encode('utf-8')
            if administration_number == administration_number_textctrl.default_text:
                administration_number = ''
            data = {'number': number,
                    'status': str(status_combobox.GetStringSelection()),
                    'year': str(year_textctrl.GetValue()),
                    'coin': str(coin_textctrl.GetValue()),
                    'lot': str(lot_textctrl.GetValue()),
                    'origin': str(origin_textctrl.GetValue()),
                    'copies': 1,
                    'administration_province': administration_province,
                    'administration_town': administration_town,
                    'administration_number': administration_number
                    }

            if self.register.get_number_data(collection, number) is not None:
                self.register.update_collection(collection, number, data) 
            else:
                self.register.add_to_collection(collection, data) 

            self.Destroy() 
        def cancel(evt):
            self.Destroy()
        def load():
            number_data = self.register.get_number_data(collection, number)
            if number_data is not None:
                if number_data['status'] == None:
                    status_combobox.SetSelection('')
                else:
                    status_combobox.SetSelection(status_combobox.FindString(number_data['status']))
                if number_data['year'] == None:
                        year_textctrl.SetValue('')
                else:
                    year_textctrl.SetValue(number_data['year'])
                if number_data['coin'] == None:
                    coin_textctrl.SetValue('')
                else:
                    coin_textctrl.SetValue(number_data['coin'])
                if number_data['lot'] == None:
                    lot_textctrl.SetValue('')
                else:
                    lot_textctrl.SetValue(number_data['lot'])
                if number_data['origin'] == None:
                    origin_textctrl.SetValue('')
                else:
                    origin_textctrl.SetValue(number_data['origin'])
                if number_data['administration_province'] == None:
                    administration_province_textctrl.SetValue('')
                else:
                    administration_province_textctrl.SetValue(number_data['administration_province'])
                if number_data['administration_town'] == None:
                    administration_town_textctrl.SetValue('')
                else:
                    administration_town_textctrl.SetValue(number_data['administration_town'])
                if number_data['administration_number'] == None:
                    administration_number_textctrl.SetValue('')
                else:
                    administration_number_textctrl.SetValue(number_data['administration_number'])


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

        lot_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lot_statictext = wx.StaticText(self, -1, 'Sorteo: ', size=(100, 20))
        lot_textctrl = wx.TextCtrl(self, -1, '', size=(100, 20))
        lot_sizer.Add(lot_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        lot_sizer.Add(lot_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)

        origin_sizer = wx.BoxSizer(wx.HORIZONTAL)
        origin_statictext = wx.StaticText(self, -1, 'Origen: ', size=(100, 20))
        origin_textctrl = wx.TextCtrl(self, -1, '', size=(100, 20))
        origin_sizer.Add(origin_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        origin_sizer.Add(origin_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)

        copies_sizer = wx.BoxSizer(wx.HORIZONTAL)
        copies_statictext = wx.StaticText(self, -1, 'Copias: ', size=(100, 20))
        copies_textctrl = wx.TextCtrl(self, -1, '1', size=(100, 20))
        copies_sizer.Add(copies_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        copies_sizer.Add(copies_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)


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
        sizer.Add(lot_sizer, 1, wx.ALL | wx.ALIGN_LEFT, border=10)
        sizer.Add(origin_sizer, 1, wx.ALL | wx.ALIGN_LEFT, border=10)
        sizer.Add(copies_sizer, 1, wx.ALL | wx.ALIGN_LEFT, border=10)
        sizer.Add(buttons_sizer, 1, wx.ALL | wx.EXPAND, border=10)

        self.SetSizer(sizer)

        load()


class FiltersDialog(wx.Dialog):
    def __init__(self, parent, id, title, collection, register):
        # begin wxGlade: MyDialog.__init__
        self.collection = collection
        self.register = register
        self.parent = parent

        wx.Dialog.__init__(self, parent, id, title)
        self.checkbox_status = wx.CheckBox(self, wx.ID_ANY, "Habilitar", style=wx.ALIGN_RIGHT)
        self.checkbox_not_empty_status = wx.CheckBox(self, wx.ID_ANY, "Rellenado", style=wx.ALIGN_RIGHT)
        self.operation_status_combo_box = wx.ComboBox(self, wx.ID_ANY, choices=["Estado es", "Estado no es"], style=wx.CB_DROPDOWN)
        self.statuses_combo_box = wx.ComboBox(self, wx.ID_ANY, choices=statuses, style=wx.CB_DROPDOWN)
        self.checkbox_year = wx.CheckBox(self, wx.ID_ANY, "Habilitar", style=wx.ALIGN_RIGHT)
        self.checkbox_not_empty_year = wx.CheckBox(self, wx.ID_ANY, "Rellenado", style=wx.ALIGN_RIGHT)
        self.operation_year_combo_box = wx.ComboBox(self, wx.ID_ANY, choices=[u"En el año", u"Antes del año", u"Despues del año", u"Entre los años", u"Fuera de los años"], style=wx.CB_DROPDOWN)
        self.first_year_text_ctrl = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.second_year_text_ctrl = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.checkbox_coin = wx.CheckBox(self, wx.ID_ANY, "Habilitar", style=wx.ALIGN_RIGHT)
        self.checkbox_not_empty_coin = wx.CheckBox(self, wx.ID_ANY, "Rellenado", style=wx.ALIGN_RIGHT)
        self.operation_coin_combo_box = wx.ComboBox(self, wx.ID_ANY, choices=["Moneda es", "Moned no es"], style=wx.CB_DROPDOWN)
        self.coin_combo_box = wx.ComboBox(self, wx.ID_ANY, choices=["Euro", "Peseta"], style=wx.CB_DROPDOWN)
        self.checkbox_lot = wx.CheckBox(self, wx.ID_ANY, "Habilitar", style=wx.ALIGN_RIGHT)
        self.checkbox_not_empty_lot = wx.CheckBox(self, wx.ID_ANY, "Rellenado", style=wx.ALIGN_RIGHT)
        self.lot_text_ctrl = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.checkbox_origin = wx.CheckBox(self, wx.ID_ANY, "Habilitar", style=wx.ALIGN_RIGHT)
        self.checkbox_not_empty_origin = wx.CheckBox(self, wx.ID_ANY, "Rellenado", style=wx.ALIGN_RIGHT)
        self.origin_text_ctrl = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.checkbox_copies = wx.CheckBox(self, wx.ID_ANY, "Habilitar", style=wx.ALIGN_RIGHT)
        self.checkbox_not_empty_copies = wx.CheckBox(self, wx.ID_ANY, "Rellenado", style=wx.ALIGN_RIGHT)
        self.copies_text_ctrl = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.checkbox_administration = wx.CheckBox(self, wx.ID_ANY, "Habilitar", style=wx.ALIGN_RIGHT)
        self.checkbox_not_empty_administration = wx.CheckBox(self, wx.ID_ANY, "Rellenado", style=wx.ALIGN_RIGHT)
        self.province_text_ctrl = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.town_text_ctrl = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.number_text_ctrl = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.ApplyButton = wx.Button(self, wx.ID_ANY, "Aplicar filtro")
        self.CancelButton = wx.Button(self, wx.ID_ANY, "Cancelar")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHECKBOX, self.OnEnable)
        self.Bind(wx.EVT_COMBOBOX, self.OnUpdate)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnUpdate)
        self.Bind(wx.EVT_BUTTON, self.OnApply, self.ApplyButton)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.CancelButton)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        self.SetTitle("Filtrado")

        self.checkbox_status.filter = 'status'
        self.checkbox_not_empty_status.filter = 'status'
        self.checkbox_year.filter = 'year'
        self.checkbox_not_empty_year.filter = 'year'
        self.checkbox_coin.filter = 'coin'
        self.checkbox_not_empty_coin.filter = 'coin'
        self.checkbox_lot.filter = 'lot'
        self.checkbox_not_empty_lot.filter = 'lot'
        self.checkbox_origin.filter = 'origin'
        self.checkbox_not_empty_origin.filter = 'origin'
        self.checkbox_copies.filter = 'copies'
        self.checkbox_not_empty_copies.filter = 'copies'
        self.checkbox_administration.filter = 'administration'
        self.checkbox_not_empty_administration.filter = 'administration'

        self.operation_status_combo_box.Enable(False)
        self.operation_status_combo_box.SetSelection(0)
        self.statuses_combo_box.Enable(False)
        self.statuses_combo_box.SetSelection(0)
        self.operation_year_combo_box.Enable(False)
        self.operation_year_combo_box.SetSelection(0)
        self.first_year_text_ctrl.Enable(False)
        self.second_year_text_ctrl.Enable(False)
        self.operation_coin_combo_box.Enable(False)
        self.operation_coin_combo_box.SetSelection(0)
        self.coin_combo_box.Enable(False)
        self.coin_combo_box.SetSelection(0)
        self.lot_text_ctrl.Enable(False)
        self.origin_text_ctrl.Enable(False)
        self.copies_text_ctrl.Enable(False)
        self.province_text_ctrl.Enable(False)
        self.town_text_ctrl.Enable(False)
        self.number_text_ctrl.Enable(False)
        self.checkbox_not_empty_status.Enable(False)
        self.checkbox_not_empty_year.Enable(False)
        self.checkbox_not_empty_coin.Enable(False)
        self.checkbox_not_empty_lot.Enable(False)
        self.checkbox_not_empty_origin.Enable(False)
        self.checkbox_not_empty_copies.Enable(False)
        self.checkbox_not_empty_administration.Enable(False)
        self.checkbox_not_empty_status.SetValue(1)
        self.checkbox_not_empty_year.SetValue(1)
        self.checkbox_not_empty_coin.SetValue(1)
        self.checkbox_not_empty_lot.SetValue(1)
        self.checkbox_not_empty_origin.SetValue(1)
        self.checkbox_not_empty_copies.SetValue(1)
        self.checkbox_not_empty_administration.SetValue(1)
        # end wxGlade
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: FiltersDialog.__do_layout
        filters_sizer = wx.BoxSizer(wx.VERTICAL)
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        administration_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Filtrar por administración"), wx.HORIZONTAL)
        copies_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Filtrar por numero mínimo de copias"), wx.HORIZONTAL)
        origin_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Filtrar por origen"), wx.HORIZONTAL)
        lot_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Filtrar por sorteo"), wx.HORIZONTAL)
        coin_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Filtrar por moneda"), wx.HORIZONTAL)
        year_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Filtrar por año"), wx.HORIZONTAL)
        status_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Filtrar por estado"), wx.HORIZONTAL)
        instructions_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizers = {'administration' : administration_sizer,
                       'copies' : copies_sizer,
                       'origin' : origin_sizer,
                       'lot' : lot_sizer,
                       'coin' : coin_sizer,
                       'year' : year_sizer,
                       'status' : status_sizer}

        Filtro = wx.StaticText(self, wx.ID_ANY, u"Para usar los filtros, seleccione el boton de habilitar de los filtros deseados, ponga las opciones deseadas y pulse \"Aplicar filtro\".\nPara volver a ver todos los números pulse \"Borrar filtros\".", style=wx.ALIGN_CENTER)
        instructions_sizer.Add(Filtro, 1, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 0)
        filters_sizer.Add(instructions_sizer, 1, wx.EXPAND, 0)
        status_sizer.Add(self.checkbox_status, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        status_sizer.Add(self.checkbox_not_empty_status, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        status_sizer.Add(self.operation_status_combo_box, 6, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        status_sizer.Add(self.statuses_combo_box, 6, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        filters_sizer.Add(status_sizer, 1, wx.EXPAND, 0)
        year_sizer.Add(self.checkbox_year, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        year_sizer.Add(self.checkbox_not_empty_year, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        year_sizer.Add(self.operation_year_combo_box, 4, wx.ALIGN_CENTER | wx.ALL, 10)
        year_sizer.Add(self.first_year_text_ctrl, 4, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        year_sizer.Add(self.second_year_text_ctrl, 4, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        filters_sizer.Add(year_sizer, 1, wx.EXPAND, 0)
        coin_sizer.Add(self.checkbox_coin, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        coin_sizer.Add(self.checkbox_not_empty_coin, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        coin_sizer.Add(self.operation_coin_combo_box, 6, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        coin_sizer.Add(self.coin_combo_box, 6, wx.ALIGN_CENTER | wx.ALL, 10)
        filters_sizer.Add(coin_sizer, 1, wx.EXPAND, 0)
        lot_sizer.Add(self.checkbox_lot, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        lot_sizer.Add(self.checkbox_not_empty_lot, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        lot_sizer.Add(self.lot_text_ctrl, 12, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        filters_sizer.Add(lot_sizer, 1, wx.EXPAND, 0)
        origin_sizer.Add(self.checkbox_origin, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        origin_sizer.Add(self.checkbox_not_empty_origin, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        origin_sizer.Add(self.origin_text_ctrl, 12, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        filters_sizer.Add(origin_sizer, 1, wx.EXPAND, 0)
        copies_sizer.Add(self.checkbox_copies, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        copies_sizer.Add(self.checkbox_not_empty_copies, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        copies_sizer.Add(self.copies_text_ctrl, 12, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        filters_sizer.Add(copies_sizer, 1, wx.EXPAND, 0)
        administration_sizer.Add(self.checkbox_administration, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        administration_sizer.Add(self.checkbox_not_empty_administration, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        administration_sizer.Add(self.province_text_ctrl, 4, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        administration_sizer.Add(self.town_text_ctrl, 4, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        administration_sizer.Add(self.number_text_ctrl, 4, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 10)
        filters_sizer.Add(administration_sizer, 1, wx.EXPAND, 0)
        buttons_sizer.Add(self.ApplyButton, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 10)
        buttons_sizer.Add(self.CancelButton, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 10)
        filters_sizer.Add(buttons_sizer, 1, wx.EXPAND, 0)
        self.SetSizer(filters_sizer)
        filters_sizer.Fit(self)
        self.Layout()
        # end wxGlade

    def CaptureData(self):

        if self.checkbox_status.GetValue():
            if not self.checkbox_not_empty_status.GetValue():
                self.register.set_filter('status', "status is NULL")
            else:
                operation = '=' if self.operation_status_combo_box.GetSelection() == 0 else '!='
                status = self.statuses_combo_box.GetStringSelection()
                self.register.set_filter('status', "status {} \'{}\'".format(operation, status))
        else:
            self.register.set_filter('status', '')

        if self.checkbox_year.GetValue():
            first_year = self.first_year_text_ctrl.GetValue()
            second_year = self.second_year_text_ctrl.GetValue()
            if not self.checkbox_not_empty_year.GetValue():
                self.register.set_filter('year', "year is NULL")
            elif first_year == '':
                self.register.set_filter('year', "year is not NULL")
            else:
                if self.operation_year_combo_box.GetSelection() == 0:
                    self.register.set_filter('year', "year = {}".format(first_year))
                elif self.operation_year_combo_box.GetSelection() == 1:
                    self.register.set_filter('year', "year < {}".format(first_year))
                elif self.operation_year_combo_box.GetSelection() == 2:
                    self.register.set_filter('year', "year > {}".format(first_year))
                elif self.operation_year_combo_box.GetSelection() == 3:
                    self.register.set_filter('year', "year >= {} AND year <= {}".format(first_year, second_year))
                elif self.operation_year_combo_box.GetSelection() == 4:
                    self.register.set_filter('year', "year < {} AND year > {}".format(first_year, second_year))
        else:
            self.register.set_filter('year', '')

        if self.checkbox_coin.GetValue():
            coin = self.coin_combo_box.GetStringSelection()
            if not self.checkbox_not_empty_coin.GetValue():
                self.register.set_filter('coin', "coin is NULL")
            elif coin == '':
                self.register.set_filter('coin', "coin is not NULL")
            else:
                operation = '=' if self.operation_coin_combo_box.GetSelection() == 0 else '!='
                self.register.set_filter('coin', "coin {} \'{}\'".format(operation, coin))
        else:
            self.register.set_filter('coin', '')

        if self.checkbox_lot.GetValue():
            lot = self.lot_text_ctrl.GetValue()
            if not self.checkbox_not_empty_lot.GetValue():
                self.register.set_filter('lot', "lot is NULL")
            elif lot == '':
                self.register.set_filter('lot', "lot is not NULL")
            else:
                self.register.set_filter('lot', "lot LIKE %{}%".format(lot))
        else:
            self.register.set_filter('lot', '')

        if self.checkbox_origin.GetValue():
            origin = self.origin_text_ctrl.GetValue()
            if not self.checkbox_not_empty_origin.GetValue():
                self.register.set_filter('origin', "origin is NULL")
            elif origin == '':
                self.register.set_filter('origin', "origin is not NULL")
            else:
                self.register.set_filter('origin', "origin LIKE %{}%".format(origin))
        else:
            self.register.set_filter('origin', '')

        if self.checkbox_copies.GetValue():
            copies = self.copies_text_ctrl.GetValue()
            if not self.checkbox_not_empty_copies.GetValue():
                self.register.set_filter('copies', "copies is NULL")
            elif copies == '':
                self.register.set_filter('copies', "copies is not NULL")
            else:
                self.register.set_filter('copies', "copies > {}".format(copies))
        else:
            self.register.set_filter('copies', '')

        if self.checkbox_administration.GetValue():
            province = self.province_text_ctrl.GetValue()
            town = self.town_text_ctrl.GetValue()
            number = self.number_text_ctrl.GetValue()
            if not self.checkbox_not_empty_administration.GetValue():
                self.register.set_filter('administration', "(administration_province is NULL OR administration_town is NULL OR administration_number is NULL)")
            elif province == '' and town == '' and number == '':
                self.register.set_filter('administration', "administration is not NULL")
            else:
                query = ''
                if province != '':
                    query += "administration_province LIKE \%{}\% AND ".format(province)
                if town != '':
                    query += " administration_town LIKE \%{}\% AND ".format(town)
                if number != '':
                    query += " administration_number LIKE \%{}\% AND ".format(number)

                if query[-5:] == ' AND ':
                    query = query[:-5]
                query = '(' + query + ')'
                print(query)
                self.register.set_filter('administration', query)
        else:
            self.register.set_filter('administration', '')

    def OnEnable(self, event):  # wxGlade: MyDialog.<event_handler>
        cb = event.GetEventObject()

        sizer = self.sizers[cb.filter]

        children = []
        for child in sizer.GetChildren():
            children.append(child.GetWindow())
        cb_index = children.index(cb)

        for index in range(cb_index + 1, len(sizer.GetChildren())):
            sizer.GetChildren()[index].GetWindow().Enable(cb.GetValue())
        self.CaptureData() 

    def OnUpdate(self, event):  # wxGlade: FiltersDialog.<event_handler>
        # event.Skip()
        self.CaptureData()

    def OnApply(self, event):  # wxGlade: MyDialog.<event_handler>
        self.CaptureData()
        self.parent.filtered_data = self.register.apply_filters(self.collection)
        self.Destroy()


    def OnCancel(self, event):  # wxGlade: MyDialog.<event_handler>
        self.Destroy()


class AddPanel(wx.Panel):
    def __init__(self, parent, ID, register):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        self.register = register

        sizer = wx.BoxSizer(wx.VERTICAL)

        def toggle1(evt):
            if evt.GetEventObject().GetValue().encode('utf-8') == evt.GetEventObject().default_text:
                evt.GetEventObject().SetValue("")
            evt.Skip()
        def toggle2(evt):
            if evt.GetEventObject().GetValue().encode('utf-8') == "".encode('utf-8'):
                evt.GetEventObject().SetValue(evt.GetEventObject().default_text)
            evt.Skip() 
        def add(evt):
            administration_province = administration_province_textctrl.GetValue().encode('utf-8')
            if administration_province == administration_province_textctrl.default_text:
                administration_province = ''
            administration_town = administration_town_textctrl.GetValue().encode('utf-8')
            if administration_town == administration_town_textctrl.default_text:
                administration_town = ''
            administration_number = administration_number_textctrl.GetValue().encode('utf-8')
            if administration_number == administration_number_textctrl.default_text:
                administration_number = ''
            data = {'number': int(number_textctrl.GetValue()),
                    'status': str(status_combobox.GetStringSelection()),
                    'year': str(year_textctrl.GetValue()),
                    'coin': str(coin_textctrl.GetValue()),
                    'lot': str(''),
                    'origin': str(''),
                    'copies': 1,
                    'administration_province': administration_province,
                    'administration_town': administration_town,
                    'administration_number': administration_number
                    }
            self.register.add_to_collection(self.collection, data)

        number_sizer = wx.BoxSizer(wx.HORIZONTAL)
        number_statictext = wx.StaticText(self, -1, 'Número: ', size=(100, 20))
        number_textctrl = wx.TextCtrl(self, -1, '', size=(100, 20))
        number_sizer.Add(number_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        number_sizer.Add(number_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)

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
        

        lot_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lot_statictext = wx.StaticText(self, -1, 'Sorteo: ', size=(100, 20))
        lot_textctrl = wx.TextCtrl(self, -1, '', size=(100, 20))
        lot_sizer.Add(lot_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        lot_sizer.Add(lot_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)

        origin_sizer = wx.BoxSizer(wx.HORIZONTAL)
        origin_statictext = wx.StaticText(self, -1, 'Origen: ', size=(100, 20))
        origin_textctrl = wx.TextCtrl(self, -1, '', size=(100, 20))
        origin_sizer.Add(origin_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        origin_sizer.Add(origin_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)

        copies_sizer = wx.BoxSizer(wx.HORIZONTAL)
        copies_statictext = wx.StaticText(self, -1, 'Copias: ', size=(100, 20))
        copies_textctrl = wx.TextCtrl(self, -1, '1', size=(100, 20))
        copies_sizer.Add(copies_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        copies_sizer.Add(copies_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)



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
        sizer.Add(lot_sizer, 0, wx.ALL | wx.ALIGN_CENTER, border=10)
        sizer.Add(origin_sizer, 0, wx.ALL | wx.ALIGN_CENTER, border=10)
        sizer.Add(copies_sizer, 0, wx.ALL | wx.ALIGN_CENTER, border=10)
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