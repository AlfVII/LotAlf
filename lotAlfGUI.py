# -*- coding: utf-8 -*-

import wx
import copy
import numpy
import unicodedata
import lotAlfRegister
# import lotAlfPrinter
from numpy import arange, sin, pi
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import datetime

statuses = ['Perfecto', 'Defectuoso', 'Falta']
coins = ['PESETA', 'EURO']
initial_year = 1967
maximum_lot = 105
origins = ['ORDINARIO', 'NAVIDAD', 'EXTRAORDINARIO', 'ESPECIAL', 'NIÑO', 'ANTIGUO', 'JUEVES', 'ESCRITO']
administration_province = ['ALBACETE', 'ALICANTE', 'ALMERÍA', 'ARABA', 'ASTURIAS', 'ÁVILA', 'BADAJOZ', 'BARCELONA', 'BIZKAIA', 'BURGOS', 'CÁCERES', 'CÁDIZ', 'CANTABRIA', 'CASTELLÓN', 'CEUTA', 'CIUDAD REAL', 'CÓRDOBA', 'CORUÑA (A)', 'CUENCA', 'GIPÚZKOA', 'GIRONA', 'GRAN CANARIA', 'GRANADA', 'GUADALAJARA', 'HUELVA', 'HUESCA', 'ISLAS BALEARES', 'JAÉN', 'LEÓN', 'LLEIDA', 'LUGO', 'MADRID', 'MÁLAGA', 'MELILLA', 'MURCIA', 'NAVARRA', 'OURENSE', 'PALENCIA', 'PALMAS (LAS)', 'PONTEVEDRA', 'RIOJA (LA)', 'SALAMANCA', 'SEGOVIA', 'SEVILLA', 'SORIA', 'TARRAGONA', 'TENERIFE', 'TERUEL', 'TOLEDO', 'VALENCIA', 'VALLADOLID', 'ZAMORA', 'ZARAGOZA']

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
        self.options = ["Añadir", "Ver", "Estadísticas"]
        self.suboptions = {"Añadir": [], "Ver": [], "Estadísticas": ["Provincia", "Municipio", "Año", "Estado", "Origen"]}

        self.pages = ["Añadir", "Ver", "Estadísticas", "Provincia", "Municipio", "Año", "Estado", "Origen"]
        for collection in self.collections:
            tree = self.collections_tree.AppendItem(root, collection)
            for option in self.options:
                option_branch = self.collections_tree.AppendItem(tree, option)
                for suboption in self.suboptions[option]:
                    self.collections_tree.AppendItem(option_branch, suboption)

        self.collections_tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=1)

        self.GetSizer().Add(self.collections_tree, 1, wx.EXPAND)
        self.GetSizer().Layout()

        self.collections_tree.Expand(root)

    def OnSelChanged(self, event):
        item = event.GetItem()
        item_str = self.collections_tree.GetItemText(item).encode('utf-8')
        if item == self.collections_tree.GetRootItem():
            self.dataPanel.SetPage(-1, 0)
        parent = self.collections_tree.GetItemParent(item) 
        parent_str = self.collections_tree.GetItemText(parent).encode('utf-8')
        if item_str in self.options:
            self.dataPanel.SetPage(self.pages.index(item_str), self.collections.index(self.collections_tree.GetItemText(parent).encode('utf-8')))

        elif item_str in self.suboptions[parent_str]:
            uberparent = self.collections_tree.GetItemParent(parent) 
            self.dataPanel.SetPage(self.pages.index(item_str), self.collections.index(self.collections_tree.GetItemText(uberparent).encode('utf-8')))


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
        statisticsPanel = StatisticsPanel(self, -1, register)
        statisticsProvincePanel = StatisticsProvincePanel(self, -1, register)
        statisticsTownPanel = StatisticsTownPanel(self, -1, register)
        statisticsYearPanel = StatisticsYearPanel(self, -1, register)
        statisticsStatusPanel = StatisticsStatusPanel(self, -1, register)
        statisticsOriginPanel = StatisticsOriginPanel(self, -1, register)

        self.sizer.Add(startPanel, 1, wx.EXPAND)
        self.sizer.Add(viewPanel, 1, wx.EXPAND)
        self.sizer.Add(addPanel, 1, wx.EXPAND)
        self.sizer.Add(statisticsPanel, 1, wx.EXPAND)
        self.sizer.Add(statisticsProvincePanel, 1, wx.EXPAND)
        self.sizer.Add(statisticsTownPanel, 1, wx.EXPAND)
        self.sizer.Add(statisticsYearPanel, 1, wx.EXPAND)
        self.sizer.Add(statisticsStatusPanel, 1, wx.EXPAND)
        self.sizer.Add(statisticsOriginPanel, 1, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.Centre()

        self.pages = [addPanel, viewPanel, statisticsPanel, statisticsProvincePanel, statisticsTownPanel, statisticsYearPanel, statisticsStatusPanel, statisticsOriginPanel, startPanel]
        # self.pages = [addPanel, viewPanel, statisticsPanel, startPanel]
        self.SetPage(-1, 0)

        statisticsPanel.draw()
        statisticsProvincePanel.draw()
        statisticsTownPanel.draw()
        statisticsYearPanel.draw()
        statisticsStatusPanel.draw()
        statisticsOriginPanel.draw()

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

class ViewPanelFilteredList(wx.Panel):
    def __init__(self,  parent, ID):
        # begin wxGlade: MyDialog.__init__
        # kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self,  parent, ID)
        self.parent = parent
        self.filter_list = wx.ListCtrl(self, wx.ID_ANY, size = (10,10), style=wx.BORDER_DEFAULT | wx.FULL_REPAINT_ON_RESIZE | wx.LC_AUTOARRANGE | wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES | wx.LC_NO_HEADER)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDoubleClick, self.filter_list)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        self.filter_list.AppendColumn("Number", format=wx.LIST_FORMAT_LEFT)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        filtered_numbers_label = wx.StaticText(self, wx.ID_ANY, u"Números")
        sizer_1.Add(filtered_numbers_label, 0, wx.ALIGN_CENTER)
        sizer_1.Add(self.filter_list, 10, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

    def OnDoubleClick(self, event): 
        number = event.GetText()
        self.parent.SetNumber(int(number))
        numberdialog = NumberDialog(self, -1, 'Número {}'.format(number), self.parent.register, self.parent.collection, number)
        numberdialog.ShowModal()

        self.parent.UpdateNumbers(1, number)

    def SetFilteredNumbers(self, numbers):
        for number in numbers:
            self.filter_list.Append([number])

    def ClearList(self):
        self.filter_list.DeleteAllItems()


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

        self.viewPanelFilteredList = ViewPanelFilteredList(self, -1)

        self.viewPanelFilteredList.Hide()
        
        numbers_sizer.Add(ten_thousands_sizer, 1, wx.EXPAND)
        numbers_sizer.Add(thousands_sizer, 1, wx.EXPAND)
        numbers_sizer.Add(hundreds_sizer, 1, wx.EXPAND)
        numbers_sizer.Add(tens_sizer, 10, wx.ALL, border=30)
        numbers_sizer.Add(self.viewPanelFilteredList, 1, wx.ALL | wx.EXPAND, border=5)


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
        self.Layout()

    def UpdateCollection(self, collection):
        self.collection = collection
        self.viewMenuPanel.UpdateCollection(collection)
        self.collection_text.SetLabel(self.register.get_collections_names()[collection])

    def FilterNumbers(self, numbers):
        self.filtered_numbers = numbers
        if numbers is not None:
            self.filtered_count.SetLabel('Números que cumplen el filtro: {:05d}'.format(len(numbers)))
            self.viewPanelFilteredList.SetFilteredNumbers(numbers)
            self.viewPanelFilteredList.Show()
            self.Layout()
        
        else:
            self.filtered_count.SetLabel('Números que cumplen el filtro: {:05d}'.format(100000))
            self.viewPanelFilteredList.ClearList()
            self.viewPanelFilteredList.Hide()
            self.Layout()
        self.UpdateNumbers(0, 0)


    def SetNumber(self, number):
        # Unsued for now
        self.UpdateNumbers(10000, int(number / 10000) * 10000)
        self.UpdateNumbers(1000, int(number % 10000 / 1000)  * 1000)
        self.UpdateNumbers(100, int(number % 1000 / 100)  * 100)
        self.UpdateNumbers(1, number)

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
                    if number_data is None:
                        button.SetBackgroundColour(self.viewMenuPanel.status_colors[statuses.index(statuses[-1])])
                    else:
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
            administration_town = administration_town_textctrl.GetValue().encode('utf-8')
            if administration_town == administration_town_textctrl.default_text:
                administration_town = ''
            administration_number = administration_number_textctrl.GetValue().encode('utf-8')
            if administration_number == administration_number_textctrl.default_text:
                administration_number = ''
            data = {'number': number,
                    'status': str(status_combobox.GetStringSelection().encode('utf-8')),
                    'year': str(year_combobox.GetValue()),
                    'coin': str(coin_combobox.GetValue()),
                    'lot': str(lot_combobox.GetStringSelection().encode('utf-8')) + '/' + str(year_combobox.GetValue())[-2:],
                    'origin': str(origin_combobox.GetValue().encode('utf-8')),
                    'copies': 1,
                    'administration_province': str(administration_province_combobox.GetStringSelection().encode('utf-8')),
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
                    pass
                else:
                    year_combobox.SetSelection(year_combobox.FindString(number_data['year']))
                    year_combobox.SetValue(number_data['year'])
                if number_data['coin'] == None:
                    pass
                else:
                    coin_combobox.SetSelection(coin_combobox.FindString(number_data['coin']))
                    coin_combobox.SetValue(number_data['coin'])
                if number_data['lot'] == None:
                    pass
                else:
                    lot_combobox.SetSelection(lot_combobox.FindString(number_data['lot'].split('/')[0]))
                if number_data['origin'] == None:
                    origin_combobox.SetValue('')
                else:
                    origin_combobox.SetSelection(origin_combobox.FindString(number_data['origin']))
                    origin_combobox.SetValue(number_data['origin'])
                if number_data['administration_province'] == None:
                    pass
                else:
                    administration_province_combobox.SetSelection(administration_province_combobox.FindString(number_data['administration_province']))
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

        years = [str(x) for x in range(initial_year, datetime.datetime.now().year + 1)]
        year_sizer = wx.BoxSizer(wx.HORIZONTAL)
        year_statictext = wx.StaticText(self, -1, 'Año: ', size=(100, 20))
        year_combobox = wx.ComboBox(self, -1, choices=years, style=wx.CB_READONLY,  size=(100, 20))
        year_sizer.Add(year_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        year_sizer.Add(year_combobox, 1, wx.ALL | wx.ALIGN_CENTER)

        coin_sizer = wx.BoxSizer(wx.HORIZONTAL)
        coin_statictext = wx.StaticText(self, -1, 'Moneda: ', size=(100, 20))
        coin_combobox = wx.ComboBox(self, -1, choices=coins, style=wx.CB_READONLY,  size=(100, 20))
        coin_sizer.Add(coin_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        coin_sizer.Add(coin_combobox, 1, wx.ALL | wx.ALIGN_CENTER)

        administration_sizer = wx.BoxSizer(wx.HORIZONTAL)
        administration_statictext = wx.StaticText(self, -1, 'Administración', size=(100, 20))
        administration_province_combobox = wx.ComboBox(self, -1, choices=administration_province, style=wx.CB_READONLY,  size=(100, 20))

        administration_town_textctrl = wx.TextCtrl(self, -1, 'Municipio', size=(200, 20))
        administration_town_textctrl.default_text = 'Municipio'
        administration_town_textctrl.Bind(wx.EVT_SET_FOCUS, toggle1)
        administration_town_textctrl.Bind(wx.EVT_KILL_FOCUS, toggle2)
        administration_number_textctrl = wx.TextCtrl(self, -1, 'Número', size=(50, 20))
        administration_number_textctrl.default_text = 'Número'
        administration_number_textctrl.Bind(wx.EVT_SET_FOCUS, toggle1)
        administration_number_textctrl.Bind(wx.EVT_KILL_FOCUS, toggle2)
        administration_sizer.Add(administration_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        administration_sizer.Add(administration_province_combobox, 1, wx.ALL | wx.ALIGN_CENTER)
        administration_sizer.Add(administration_town_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)
        administration_sizer.Add(administration_number_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)

        lots = [str(x) for x in range(1, maximum_lot + 1)]
        lot_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lot_statictext = wx.StaticText(self, -1, 'Sorteo: ', size=(100, 20))
        lot_combobox = wx.ComboBox(self, -1, choices=lots, style=wx.CB_READONLY,  size=(100, 20))
        lot_sizer.Add(lot_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        lot_sizer.Add(lot_combobox, 1, wx.ALL | wx.ALIGN_CENTER)

        origin_sizer = wx.BoxSizer(wx.HORIZONTAL)
        origin_statictext = wx.StaticText(self, -1, 'Origen: ', size=(100, 20))
        origin_combobox = wx.ComboBox(self, -1, choices=origins, style=wx.CB_READONLY,  size=(100, 20))
        origin_sizer.Add(origin_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        origin_sizer.Add(origin_combobox, 1, wx.ALL | wx.ALIGN_CENTER)

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
        self.operation_coin_combo_box = wx.ComboBox(self, wx.ID_ANY, choices=["Moneda es", "Moneda no es"], style=wx.CB_DROPDOWN)
        self.coin_combo_box = wx.ComboBox(self, wx.ID_ANY, choices=["EURO", "PESETA"], style=wx.CB_DROPDOWN)
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
            lot = self.lot_text_ctrl.GetValue().encode('utf-8')
            if not self.checkbox_not_empty_lot.GetValue():
                self.register.set_filter('lot', "lot is NULL")
            elif lot == '':
                self.register.set_filter('lot', "lot is not NULL")
            else:
                self.register.set_filter('lot', "lot LIKE \'%{}%\'".format(lot))
        else:
            self.register.set_filter('lot', '')

        if self.checkbox_origin.GetValue():
            origin = self.origin_text_ctrl.GetValue().encode('utf-8')
            if not self.checkbox_not_empty_origin.GetValue():
                self.register.set_filter('origin', "origin is NULL")
            elif origin == '':
                self.register.set_filter('origin', "origin is not NULL")
            else:
                self.register.set_filter('origin', "origin LIKE \'%{}%\'".format(origin))
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
            province = self.province_text_ctrl.GetValue().encode('utf-8')
            town = self.town_text_ctrl.GetValue().encode('utf-8')
            number = self.number_text_ctrl.GetValue()
            if not self.checkbox_not_empty_administration.GetValue():
                self.register.set_filter('administration', "(administration_province is NULL OR administration_town is NULL OR administration_number is NULL)")
            elif province == '' and town == '' and number == '':
                self.register.set_filter('administration', "administration is not NULL")
            else:
                query = ''
                if province != '':
                    query += "administration_province LIKE \'%{}%\' AND ".format(province)
                if town != '':
                    query += " administration_town LIKE \'%{}%\' AND ".format(town)
                if number != '':
                    query += " administration_number LIKE \'%{}%\' AND ".format(number)

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
            administration_town = administration_town_textctrl.GetValue().encode('utf-8')
            if administration_town == administration_town_textctrl.default_text:
                administration_town = ''
            administration_number = administration_number_textctrl.GetValue().encode('utf-8')
            if administration_number == administration_number_textctrl.default_text:
                administration_number = ''
            data = {'number': int(number_textctrl.GetValue()),
                    'status': str(status_combobox.GetStringSelection().encode('utf-8')),
                    'year': str(year_combobox.GetValue()),
                    'coin': str(coin_combobox.GetValue()),
                    'lot': str(lot_combobox.GetStringSelection()) + '/' + str(year_combobox.GetValue())[-2:],
                    'origin': str(origin_combobox.GetValue().encode('utf-8')),
                    'copies': 1,
                    'administration_province': str(administration_province_combobox.GetStringSelection().encode('utf-8')),
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

        years = [str(x) for x in range(initial_year, datetime.datetime.now().year + 1)]
        year_sizer = wx.BoxSizer(wx.HORIZONTAL)
        year_statictext = wx.StaticText(self, -1, 'Año: ', size=(100, 20))
        year_combobox = wx.ComboBox(self, -1, choices=years, style=wx.CB_READONLY,  size=(100, 20))
        year_sizer.Add(year_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        year_sizer.Add(year_combobox, 1, wx.ALL | wx.ALIGN_CENTER)

        coin_sizer = wx.BoxSizer(wx.HORIZONTAL)
        coin_statictext = wx.StaticText(self, -1, 'Moneda: ', size=(100, 20))
        coin_combobox = wx.ComboBox(self, -1, choices=coins, style=wx.CB_READONLY,  size=(100, 20))
        coin_sizer.Add(coin_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        coin_sizer.Add(coin_combobox, 1, wx.ALL | wx.ALIGN_CENTER)

        administration_sizer = wx.BoxSizer(wx.HORIZONTAL)
        administration_statictext = wx.StaticText(self, -1, 'Administración', size=(100, 20))

        administration_province_combobox = wx.ComboBox(self, -1, choices=administration_province, style=wx.CB_READONLY,  size=(100, 20))

        administration_town_textctrl = wx.TextCtrl(self, -1, 'Municipio', size=(100, 20))
        administration_town_textctrl.default_text = 'Municipio'
        administration_town_textctrl.Bind(wx.EVT_SET_FOCUS,toggle1)
        administration_town_textctrl.Bind(wx.EVT_KILL_FOCUS,toggle2)
        administration_number_textctrl = wx.TextCtrl(self, -1, 'Número', size=(100, 20))
        administration_number_textctrl.default_text = 'Número'
        administration_number_textctrl.Bind(wx.EVT_SET_FOCUS,toggle1)
        administration_number_textctrl.Bind(wx.EVT_KILL_FOCUS,toggle2)
        administration_sizer.Add(administration_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        administration_sizer.Add(administration_province_combobox, 1, wx.ALL | wx.ALIGN_CENTER)
        administration_sizer.Add(administration_town_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)
        administration_sizer.Add(administration_number_textctrl, 1, wx.ALL | wx.ALIGN_CENTER)
        
        lots = [str(x) for x in range(1, maximum_lot + 1)]
        lot_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lot_statictext = wx.StaticText(self, -1, 'Sorteo: ', size=(100, 20))
        lot_combobox = wx.ComboBox(self, -1, choices=lots, style=wx.CB_READONLY,  size=(100, 20))
        lot_sizer.Add(lot_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        lot_sizer.Add(lot_combobox, 1, wx.ALL | wx.ALIGN_CENTER)

        origin_sizer = wx.BoxSizer(wx.HORIZONTAL)
        origin_statictext = wx.StaticText(self, -1, 'Origen: ', size=(100, 20))
        origin_combobox = wx.ComboBox(self, -1, choices=origins, style=wx.CB_READONLY,  size=(100, 20))
        origin_sizer.Add(origin_statictext, 1, wx.ALL | wx.ALIGN_CENTER)
        origin_sizer.Add(origin_combobox, 1, wx.ALL | wx.ALIGN_CENTER)

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

# StatisticsTownPanel
# StatisticsOriginPanel
class StatisticsPanel(wx.Panel):
    def __init__(self, parent, ID, register):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        self.text = wx.StaticText(self, -1, 'StatisticsPanel')
        self.register = register
        self.SetBackgroundColour('white')

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        subsizer = wx.BoxSizer(wx.VERTICAL)

        self.Layout()

        self.figure_provinces = Figure()
        self.axes_provinces = self.figure_provinces.add_subplot(111)
        canvas_provinces = FigureCanvas(self, -1, self.figure_provinces)
        sizer.Add(canvas_provinces, 1, wx.RIGHT | wx.TOP | wx.EXPAND)

        figure_status = Figure()
        self.axes_status = figure_status.add_subplot(111)
        canvas_status = FigureCanvas(self, -1, figure_status)
        subsizer.Add(canvas_status, 1, wx.CENTER | wx.TOP)

        figure_year = Figure()
        self.axes_year = figure_year.add_subplot(111)
        canvas_year = FigureCanvas(self, -1, figure_year)
        subsizer.Add(canvas_year, 1, wx.LEFT | wx.TOP | wx.EXPAND)
        sizer.Add(subsizer, 3, wx.LEFT | wx.TOP | wx.EXPAND)

        # figure_lot = Figure()
        # self.axes_lot = figure_lot.add_subplot(111)
        # canvas_lot = FigureCanvas(self, -1, figure_lot)
        # sizer.Add(canvas_lot, 1, wx.LEFT | wx.TOP | wx.EXPAND)

        self.SetSizer(sizer)
        self.Fit()

    def draw(self):
        def remove_tildes(label):
            label = label.replace('\xc3\x81', 'A')
            label = label.replace('\xc3\x89', 'E')
            label = label.replace('\xc3\x8d', 'I')
            label = label.replace('\xc3\x93', 'O')
            label = label.replace('\xc3\x9A', 'U')
            return label

        province_data = self.register.get_count_filtered_data(self.collection, 'administration_province')
        counts = []
        labels = []
        for province_datum in province_data:
            if province_datum[1] is not None:
                counts.append(province_datum[0])
                labels.append(province_datum[1])
        labels_for_order = []
        labels_with_tildes_ordered = []
        counts_ordered = []

        for label in labels:
            labels_for_order.append(remove_tildes(label))

        labels_for_order.sort()
        for label in labels_for_order:
            for label_with_tilde in labels:
                if label == remove_tildes(label_with_tilde):
                    labels_with_tildes_ordered.append(label_with_tilde)
                    counts_ordered.append(counts[labels.index(label_with_tilde)])

        labels_with_tildes_ordered.reverse()
        counts_ordered.reverse()

        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        self.axes_provinces.barh(labels_with_tildes_ordered, counts_ordered, 0.8, label='Provincias')
        self.figure_provinces.tight_layout()


        status_data = self.register.get_count_filtered_data(self.collection, 'status')
        filled_data = self.register.get_count_filtered_data(self.collection, 'status', 'WHERE administration_province is not NULL AND year is not NULL AND coin is not NULL AND lot is not NULL AND origin is not NULL AND status = \'Perfecto\'', False)
        unfilled_data = self.register.get_count_filtered_data(self.collection, 'status', 'WHERE (administration_province is NULL OR year is NULL OR coin is NULL OR lot is NULL OR origin is NULL) AND status = \'Perfecto\'', False)

        counts_outer = []
        labels_outer = []
        for status_datum in status_data:
            counts_outer.append(status_datum[0])
            labels_outer.append(status_datum[1])
        counts_inner = copy.deepcopy(counts_outer)[:-1]
        labels_inner = []
        labels_inner.append("")
        labels_inner.append("")
        labels_inner.append("Rellenados")
        counts_inner.append(filled_data[0][0])
        labels_inner.append("Por rellenar")
        counts_inner.append(unfilled_data[0][0])

        cmap = plt.get_cmap("tab20")
        outer_colors = cmap([0, 4, 16])
        inner_colors = cmap(numpy.array([0, 4, 17, 18]))
        size = 0.3
        self.axes_status.pie(counts_outer, labels=labels_outer, colors=outer_colors, radius=1, autopct='%1.1f%%', shadow=True, startangle=90, labeldistance=.9, wedgeprops=dict(width=size, edgecolor='w'))
        self.axes_status.pie(counts_inner, labels=labels_inner, colors=inner_colors, radius=1-size, autopct='%1.1f%%', shadow=True, startangle=90, labeldistance=.8)

        year_data = self.register.get_count_filtered_data(self.collection, 'year')
        counts = []
        labels = []
        for year_datum in year_data:
            if year_datum[1] is not None:
                counts.append(year_datum[0])
                labels.append(year_datum[1])

        self.axes_year.bar(labels, counts, 0.35)
        labels = self.axes_year.get_xticklabels()
        plt.setp(labels, rotation=90, horizontalalignment='right')
        plt.subplots_adjust(left=0.3, right=1, bottom=0.3, top=0.9)

        self.Fit()
        self.GetSizer().Layout()

        origin_data = self.register.get_count_filtered_data(self.collection, 'origin')
        coin_data = self.register.get_count_filtered_data(self.collection, 'coin')

        # lot_data = self.register.get_count_filtered_data(self.collection, 'lot')
        # # print(lot_data)
        # counts = []
        # labels = []
        # for lot_datum in lot_data:
        #     if lot_datum[1] is not None:
        #         counts.append(lot_datum[0])
        #         labels.append(lot_datum[1])

        # self.axes_lot.barh(labels, counts, 0.35, label='Sorteos')


        # t = arange(0.0, 3.0, 0.01)
        # s = sin(2 * pi * t)
        # self.axes_year.plot(t, s)
        # self.axes_lot.plot(t, s)

    def UpdateCollection(self, collection):
        self.collection = collection


class StatisticsProvincePanel(wx.Panel):
    def __init__(self, parent, ID, register):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        self.text = wx.StaticText(self, -1, 'StatisticsProvincePanel')
        self.register = register
        self.SetBackgroundColour('white')

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        subsizer = wx.BoxSizer(wx.VERTICAL)

        self.Layout()

        self.figure_provinces = Figure()
        self.axes_provinces = self.figure_provinces.add_subplot(111)
        canvas_provinces = FigureCanvas(self, -1, self.figure_provinces)
        sizer.Add(canvas_provinces, 1, wx.RIGHT | wx.TOP | wx.EXPAND)

        self.SetSizer(sizer)
        self.Fit()

    def draw(self):
        def remove_tildes(label):
            label = label.replace('\xc3\x81', 'A')
            label = label.replace('\xc3\x89', 'E')
            label = label.replace('\xc3\x8d', 'I')
            label = label.replace('\xc3\x93', 'O')
            label = label.replace('\xc3\x9A', 'U')
            return label

        province_data = self.register.get_count_filtered_data(self.collection, 'administration_province')
        counts = []
        labels = []
        for province_datum in province_data:
            if province_datum[1] is not None:
                counts.append(province_datum[0])
                labels.append(province_datum[1])
        labels_for_order = []
        labels_with_tildes_ordered = []
        counts_ordered = []

        for label in labels:
            labels_for_order.append(remove_tildes(label))

        labels_for_order.sort()
        for label in labels_for_order:
            for label_with_tilde in labels:
                if label == remove_tildes(label_with_tilde):
                    labels_with_tildes_ordered.append(label_with_tilde)
                    counts_ordered.append(counts[labels.index(label_with_tilde)])

        labels_with_tildes_ordered.reverse()
        counts_ordered.reverse()

        self.axes_provinces.barh(labels_with_tildes_ordered, counts_ordered, 0.8, label='Provincias')
        self.figure_provinces.tight_layout()


    def UpdateCollection(self, collection):
        self.collection = collection

class StatisticsTownPanel(wx.Panel):
    def __init__(self, parent, ID, register):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition) 
        self.text = wx.StaticText(self, -1, 'StatisticsTownPanel')
        self.register = register
        self.SetBackgroundColour('white')

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.Layout()

        self.province = 'MADRID'
        administration_statictext = wx.StaticText(self, -1, 'Elige una provincia:', size=(300, 20))
        self.administration_province_combobox = wx.ComboBox(self, -1, choices=administration_province, style=wx.CB_READONLY,  size=(300, 20))
        self.administration_province_combobox.SetSelection(self.administration_province_combobox.FindString(self.province))

        self.figure_towns = Figure()
        self.axes_towns = self.figure_towns.add_subplot(111)
        self.canvas_towns = FigureCanvas(self, -1, self.figure_towns)
        self.canvas_towns.draw()
        sizer.Add(administration_statictext, 0, wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.administration_province_combobox, 0, wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.canvas_towns, 1, wx.TOP | wx.EXPAND)


        self.SetSizer(sizer)
        self.Fit()

        self.Bind(wx.EVT_COMBOBOX, self.OnSelChanged, self.administration_province_combobox)

    def OnSelChanged(self, event):
        new_province = str(self.administration_province_combobox.GetStringSelection().encode('utf-8'))
        self.province = new_province
        self.figure_towns.clf()
        self.axes_towns = self.figure_towns.add_subplot(111)
        self.draw()
        self.canvas_towns.draw()

    def draw(self):
        def remove_tildes(label):
            label = label.replace('\xc3\x81', 'A')
            label = label.replace('\xc3\x89', 'E')
            label = label.replace('\xc3\x8d', 'I')
            label = label.replace('\xc3\x93', 'O')
            label = label.replace('\xc3\x9A', 'U')
            return label

        town_data = self.register.get_count_filtered_data(self.collection, 'administration_town', where_clause='WHERE administration_province == \'{}\''.format(self.province))
        counts = []
        labels = []
        for province_datum in town_data:
            if province_datum[1] is not None:
                counts.append(province_datum[0])
                labels.append(province_datum[1])
        labels_for_order = []
        labels_with_tildes_ordered = []
        counts_ordered = []

        for label in labels:
            labels_for_order.append(remove_tildes(label))

        labels_for_order.sort()
        for label in labels_for_order:
            for label_with_tilde in labels:
                if label == remove_tildes(label_with_tilde):
                    labels_with_tildes_ordered.append(label_with_tilde)
                    counts_ordered.append(counts[labels.index(label_with_tilde)])

        labels_with_tildes_ordered.reverse()
        counts_ordered.reverse()

        self.axes_towns.barh(labels_with_tildes_ordered, counts_ordered, 0.8, label='Provincias')
        self.figure_towns.tight_layout()


    def UpdateCollection(self, collection):
        self.collection = collection

class StatisticsYearPanel(wx.Panel):
    def __init__(self, parent, ID, register):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        self.text = wx.StaticText(self, -1, 'StatisticsYearPanel')
        self.register = register
        self.SetBackgroundColour('white')

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        subsizer = wx.BoxSizer(wx.VERTICAL)

        self.Layout()

        figure_year = Figure()
        self.axes_year = figure_year.add_subplot(111)
        canvas_year = FigureCanvas(self, -1, figure_year)
        subsizer.Add(canvas_year, 1, wx.LEFT | wx.TOP | wx.EXPAND)
        sizer.Add(subsizer, 3, wx.LEFT | wx.TOP | wx.EXPAND)

        self.SetSizer(sizer)
        self.Fit()

    def draw(self):

        year_data = self.register.get_count_filtered_data(self.collection, 'year')
        counts = []
        labels = []
        for year_datum in year_data:
            if year_datum[1] is not None:
                counts.append(year_datum[0])
                labels.append(year_datum[1])

        self.axes_year.bar(labels, counts, 0.35)
        labels = self.axes_year.get_xticklabels()
        plt.setp(labels, rotation=90, horizontalalignment='right')
        plt.subplots_adjust(left=0.3, right=1, bottom=0.3, top=0.9)

        self.Fit()
        self.GetSizer().Layout()

    def UpdateCollection(self, collection):
        self.collection = collection

class StatisticsStatusPanel(wx.Panel):
    def __init__(self, parent, ID, register):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        self.text = wx.StaticText(self, -1, 'StatisticsStatusPanel')
        self.register = register
        self.SetBackgroundColour('white')

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        subsizer = wx.BoxSizer(wx.VERTICAL)

        self.Layout()

        figure_status = Figure()
        self.axes_status = figure_status.add_subplot(111)
        canvas_status = FigureCanvas(self, -1, figure_status)
        subsizer.Add(canvas_status, 1, wx.CENTER | wx.TOP | wx.EXPAND)

        self.SetSizer(sizer)
        self.Fit()

    def draw(self):

        status_data = self.register.get_count_filtered_data(self.collection, 'status')
        filled_data = self.register.get_count_filtered_data(self.collection, 'status', 'WHERE administration_province is not NULL AND year is not NULL AND coin is not NULL AND lot is not NULL AND origin is not NULL AND status = \'Perfecto\'', False)
        unfilled_data = self.register.get_count_filtered_data(self.collection, 'status', 'WHERE (administration_province is NULL OR year is NULL OR coin is NULL OR lot is NULL OR origin is NULL) AND status = \'Perfecto\'', False)

        counts_outer = []
        labels_outer = []
        for status_datum in status_data:
            counts_outer.append(status_datum[0])
            labels_outer.append(status_datum[1])
        counts_inner = copy.deepcopy(counts_outer)[:-1]
        labels_inner = []
        labels_inner.append("")
        labels_inner.append("")
        labels_inner.append("Rellenados")
        counts_inner.append(filled_data[0][0])
        labels_inner.append("Por rellenar")
        counts_inner.append(unfilled_data[0][0])

        cmap = plt.get_cmap("tab20")
        outer_colors = cmap([0, 4, 16])
        inner_colors = cmap(numpy.array([0, 4, 17, 18]))
        size = 0.3
        self.axes_status.pie(counts_outer, labels=labels_outer, colors=outer_colors, radius=1, autopct='%1.1f%%', shadow=True, startangle=90, labeldistance=.9, wedgeprops=dict(width=size, edgecolor='w'))
        self.axes_status.pie(counts_inner, labels=labels_inner, colors=inner_colors, radius=1-size, autopct='%1.1f%%', shadow=True, startangle=90, labeldistance=.8)

    def UpdateCollection(self, collection):
        self.collection = collection

class StatisticsOriginPanel(wx.Panel):
    def __init__(self, parent, ID, register):
        wx.Panel.__init__(self, parent, ID, wx.DefaultPosition)
        self.text = wx.StaticText(self, -1, 'StatisticsOriginPanel')
        self.register = register
        self.SetBackgroundColour('white')

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        subsizer = wx.BoxSizer(wx.VERTICAL)

        self.Layout()

        figure_status = Figure()
        self.axes_status = figure_status.add_subplot(111)
        canvas_status = FigureCanvas(self, -1, figure_status)
        subsizer.Add(canvas_status, 1, wx.CENTER | wx.TOP | wx.EXPAND)

        self.SetSizer(sizer)
        self.Fit()

    def draw(self):

        origin_data = self.register.get_count_filtered_data(self.collection, 'origin')

        counts_outer = []
        labels_outer = []
        for origin_datum in origin_data:
            if origin_datum[1] is not None:
                counts_outer.append(origin_datum[0])
                labels_outer.append(origin_datum[1])
        counts_inner = copy.deepcopy(counts_outer)[:-1]

        cmap = plt.get_cmap("tab20")
        outer_colors = cmap([0, 4, 16])
        size = 0.3
        self.axes_status.pie(counts_outer, labels=[unicode(x, 'utf-8') for x in labels_outer], colors=outer_colors, radius=1, autopct='%1.1f%%', shadow=True, startangle=90, labeldistance=.9)

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


    # app = wx.PySimpleApp()
    # fr = wx.Frame(None, title='test')
    # panel = CanvasPanel(fr)
    # panel.draw()
    # fr.Show()
    # app.MainLoop()

app = MyApp(0)
app.MainLoop()