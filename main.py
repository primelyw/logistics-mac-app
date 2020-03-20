#coding=utf8
import wx,time
import wx.adv
from SQL import sql_class as sql
import os
from Data_Gen import data_gen as DG

datapool = sql.Data_Pool('prime','admin','admin')
sh = datapool.sheet
class Login(wx.Frame):
    def __init__(self,parent,*args,**kwargs):
        super(Login,self).__init__(*args,**kwargs)

        # self.SetSize(420,280)
        self.parent = parent
        self.init_UI()
        self.Centre()
    def init_UI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        handler = wx.TextCtrl(panel,style =wx.TE_PROCESS_ENTER); self.handler = handler
        #self.Bind(wx.EVT_TEXT_ENTER,self.OnEnter,id = handler.GetId())
        passwd = wx.TextCtrl(panel, style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER) ;self.passwd = passwd
        self.Bind(wx.EVT_TEXT_ENTER,self.OnLogin,id = passwd.GetId())

        st1 = wx.StaticText(panel, label='handler    ', style=wx.ALIGN_LEFT)
        st2 = wx.StaticText(panel, label='password', style=wx.ALIGN_LEFT)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        Btn1 = wx.Button(panel, wx.ID_ANY, 'Exit', size=(90, 30))
        Btn2 = wx.Button(panel, wx.ID_ANY, 'Login', size=(90, 30))
        self.Bind(wx.EVT_BUTTON,self.OnLogin,id = Btn2.GetId())
        self.Bind(wx.EVT_BUTTON,self.OnExit,id = Btn1.GetId())
        
        hbox.Add(Btn1,flag = wx.RIGHT,border = 10)
        hbox.Add(Btn2,flag = wx.RIGHT,border = 20)

        hbox1.Add(st1,flag = wx.RIGHT,border =10)
        hbox1.Add(handler,proportion = 1)

        hbox2.Add(st2,flag = wx.RIGHT,border = 10)
        hbox2.Add(passwd,proportion = 1)

        vbox.Add((-1,30))

        vbox.Add(hbox1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border = 10)
        vbox.Add(hbox2,flag = wx.ALIGN_CENTRE|wx.EXPAND|wx.ALL,border = 10)
        vbox.Add(hbox,flag = wx.ALIGN_RIGHT,border = 30)
        panel.SetSizer(vbox)


    def OnExit(self,e):
        self.Close()

    def OnLogin(self,e):
        hd = self.handler.GetLineText(self.handler.GetNumberOfLines()-1)
        pwd = self.passwd.GetLineText(self.passwd.GetNumberOfLines()-1)
        if hd == datapool.user_name and pwd == datapool.password:
            print 'Login'
            for i in range(len(self.parent.tool_ls)):
                self.parent.tb.EnableTool(self.parent.tool_ls[i].GetId(),True)
            self.Close()
            
        else:
            wx.MessageBox('Ops,wrong password or username', 'Info',
            wx.OK | wx.ICON_INFORMATION)

class PrintList(wx.Frame):
    def __init__(self,cont,head,*args,**kwargs):
        super(PrintList,self).__init__(*args,**kwargs)
        self.cont = cont
        self.head = head
        self.Centre()
        self.SetSize(420,800)
        self.init_UI()
    def OnExit(self):
        self.Close()
    def init_UI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        icon = ''
        if self.head == 'Cities':
            icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('image/print_city.png'))
        else:
            icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('image/print_item.png'))
        vbox.Add(icon,flag = wx.ALIGN_CENTRE|wx.ALL,border = 10)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        tc2.WriteText(self.cont)
        hbox3.Add(tc2, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND|wx.BOTTOM,border=10)

        panel.SetSizer(vbox)


class Work(wx.Frame):
    def __init__(self,*args,**kwargs):
        super(Work,self).__init__(*args,**kwargs)
        self.Centre()
        #self.SetSize(600,1000)
        self.init_UI()

    def init_UI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        svbox0 = wx.BoxSizer(wx.VERTICAL)
        svbox1 = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        printer_icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('image/setup.png'))
        vbox.Add(printer_icon,flag = wx.ALIGN_CENTRE|wx.ALL,border = 10)
        
        st1 = wx.StaticText(panel,label = 'Sorting')
        pib = wx.BitmapButton(panel,wx.ID_ANY,wx.Bitmap('image/sort.png'))
        self.Bind(wx.EVT_BUTTON,self.OnSort,id = pib.GetId())
        svbox0.Add(st1,flag = wx.LEFT,border = 14)
        svbox0.Add(pib,flag = wx.LEFT,border = 10)

        st2 = wx.StaticText(panel,label = 'Transporting')
        pcb = wx.BitmapButton(panel,wx.ID_ANY,wx.Bitmap('image/transport.png'))
        self.Bind(wx.EVT_BUTTON,self.OnTransport,id = pcb.GetId())
        svbox1.Add(st2,flag = wx.LEFT,border = 10)
        svbox1.Add(pcb,flag = wx.LEFT,border = 20)
        
        hbox.Add(svbox0,flag = wx.LEFT|wx.EXPAND,border = 0)
        hbox.Add(svbox1,flag = wx.LEFT|wx.EXPAND,border = 25)

        vbox.Add(hbox,proportion = 1,flag = wx.ALIGN_CENTRE|wx.ALL,border = 10)
        panel.SetSizer(vbox)
    def bind_city_item(self):
        print 'Binding city and item...'
        for i in range(len(datapool.city_ls)):
            ct = datapool.city_ls[i]
            ct_ls = []
            for j in range(len(datapool.iterm_ls)):
                it = datapool.iterm_ls[j]
                if it.addr0 == ct.name:
                    ct_ls.append(it)
            ct.update_iterm_list(ct_ls)

    def OnSort(self,e):
        self.bind_city_item()
        print 'Sorting...'
        for i in range(len(datapool.city_ls)):
            datapool.city_ls[i].sort_iterms()
        wx.MessageBox('Sorting Completed', 'Info',
            wx.OK | wx.ICON_INFORMATION)
        pass
    def OnTransport(self,e):
        self.bind_city_item()
        print 'Transporting...'
        #form map
        map_m = [];map_t = []
        for i in datapool.city_ls:
            map_m.append([int(j) for j in i.neighbour_m])
            map_t.append([int (j) for j in i.neighbour_t])
        datapool.form_map(map_m,map_t)
        map = datapool.map
        map.show_map()

        for i in datapool.city_ls:
            i.alloc_iterm_path(map)
        print 'Allocating successfully!'
        wx.MessageBox('Transporting Completed', 'Info',
            wx.OK | wx.ICON_INFORMATION)
        pass

class Print(wx.Frame):
    def __init__(self,*args,**kwargs):
        super(Print,self).__init__(*args,**kwargs)
        self.Centre()
        #self.SetSize(600,1000)
        self.init_UI()

    def init_UI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        svbox0 = wx.BoxSizer(wx.VERTICAL)
        svbox1 = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        printer_icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('image/printer.png'))
        vbox.Add(printer_icon,flag = wx.ALIGN_CENTRE|wx.ALL,border = 10)
        
        pib = wx.BitmapButton(panel,wx.ID_ANY,wx.Bitmap('image/print_item.png'))
        self.Bind(wx.EVT_BUTTON,self.OnPrintItem,id = pib.GetId())
        svbox0.Add(pib,flag = wx.ALL,border = 10)

        pcb = wx.BitmapButton(panel,wx.ID_ANY,wx.Bitmap('image/print_city.png'))
        self.Bind(wx.EVT_BUTTON,self.OnPrintCity,id = pcb.GetId())
        svbox1.Add(pcb,flag = wx.ALL,border = 10)
        
        hbox.Add(svbox0,flag = wx.LEFT,border = 100)
        hbox.Add(svbox1,flag = wx.LEFT,border = 25)

        vbox.Add(hbox,proportion = 1,flag = wx.LEFT|wx.RIGHT|wx.EXPAND)
        panel.SetSizer(vbox)
    
    def OnPrintItem(self,e):
        print 'item printed'
        txt = datapool.show_item_list()
        plf = PrintList(txt,'Item',None,title = 'Cities')
        plf.Show()

    def OnPrintCity(self,e):
        print 'city printed'
        txt = datapool.show_city_list()
        plf = PrintList(txt,'Cities',None,title = 'Cities')
        plf.Show()
       

class EditIterm(wx.Frame):
    def __init__(self,*args,**kwargs):
        super(EditIterm,self).__init__(*args,**kwargs)
        self.Centre()
        self.SetSize(700,400)
        self.list_cnt = len(datapool.iterm_ls)
        self.init_UI()
        self.data_init()
    
    def init_UI(self):
        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # self.listbox = wx.ListBox(panel)
        # hbox.Add(self.listbox, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)

        self.list = wx.ListCtrl(panel, wx.ID_ANY, style=wx.LC_REPORT)
        self.list.InsertColumn(0, 'Name',width=140)
        self.list.InsertColumn(1, 'From address',width=140)
        self.list.InsertColumn(2, 'To address',width=140)
        self.list.InsertColumn(3, 'Send Date',width=140)
        self.list.InsertColumn(4, 'Phone number',width=140)
        self.list.InsertColumn(5, 'Quick?',width=140)

        hbox.Add(self.list, wx.ID_ANY, wx.EXPAND | wx.ALL, 10)

        btnPanel = wx.Panel(panel)
        vbox = wx.BoxSizer(wx.VERTICAL)
        newBtn = wx.Button(btnPanel, wx.ID_ANY, 'New', size=(90, 30))
        delBtn = wx.Button(btnPanel, wx.ID_ANY, 'Delete', size=(90, 30))
        clrBtn = wx.Button(btnPanel, wx.ID_ANY, 'Clear', size=(90, 30))

        self.Bind(wx.EVT_BUTTON, self.NewItem, id=newBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDelete, id=delBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnClear, id=clrBtn.GetId())
        
        vbox.Add((-1, 20))
        vbox.Add(newBtn)
        vbox.Add(delBtn, 0, wx.TOP, 5)
        vbox.Add(clrBtn, 0, wx.TOP, 5)

        btnPanel.SetSizer(vbox)
        hbox.Add(btnPanel, 0.6, wx.EXPAND | wx.RIGHT, 20)
        panel.SetSizer(hbox)
        self.Centre()
        pass
    def NewItem(self, event):

        g = DG.Gen()
        iu = g.get_item_unit(1)

        name = wx.GetTextFromUser("New item's name", 'Insert dialog',iu[0]) ;
        if name == '': return 
        from_addr = wx.GetTextFromUser("New item's from address", 'Insert dialog',iu[1]);
        if from_addr == '': return 
        to_addr = wx.GetTextFromUser("New item's to address", 'Insert dialog',iu[2]);
        if to_addr == '': return 
        date0 = wx.GetTextFromUser("New item's send date", 'Insert dialog',iu[3]);
        if date0 == '': return 
        phone = wx.GetTextFromUser("New item's phone number", 'Insert dialog',iu[4]);
        if phone == '': return 
        quick = wx.GetTextFromUser("Does ew item need quick delivery? (0 / 1)", 'Insert dialog',iu[5]);
        if quick == '': return 
        datapool.add_iterm([name,from_addr,to_addr,date0,phone,int(quick)])
        
        index = self.list.InsertItem(self.list_cnt, name)
        self.list.SetItem(index, 1, from_addr)
        self.list.SetItem(index, 2, to_addr)
        self.list.SetItem(index, 3, date0)
        self.list.SetItem(index, 4, phone)
        self.list.SetItem(index, 5, quick)
        self.list_cnt += 1

    def OnDelete(self, event):
        sel = self.list.GetFocusedItem()
        #print sel
        if sel != -1:
            self.list.DeleteItem(sel)
            datapool.iterm_ls.pop(sel)

    def OnClear(self, event):
        self.list.ClearAll()
        datapool.iterm_ls = []
    def data_init(self):
        if self.list_cnt==0:return
        #self.list.InsertColumn(0,'self',width = 80);self.ls2.InsertColumn(0,'self',width = 80)
            
        for i in range(len(datapool.iterm_ls)):
            it = datapool.iterm_ls[i]
            index1 = self.list.InsertItem(i, it.name)
            
            self.list.SetItem(index1, 1,it.addr0)
            self.list.SetItem(index1, 2,it.addr1)
            self.list.SetItem(index1, 3,it.date0)
            self.list.SetItem(index1, 4,it.phone)
            self.list.SetItem(index1, 5,str(it.quick))

           
            
        pass

class Terminal(wx.Frame):
    def __init__(self,*args,**kwargs):
        super(Terminal,self).__init__(*args,**kwargs)
        self.Centre()
        self.init_UI()
        self.compiler = sql.Compiler()
    
    def init_UI(self):
        panel = wx.Panel(self)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        cmd_space = wx.TextCtrl(panel, style=wx.TE_MULTILINE) ; self.cmd_space = cmd_space
        self.line_cnt = 1
        cmd_space.WriteText("""MINI-SQLite3 designed by Prime Lee\n>> """)
        self.Bind(wx.EVT_TEXT,self.OnTextEnter,id = cmd_space.GetId())
        hbox3.Add(cmd_space, proportion=1, flag=wx.EXPAND)
        panel.SetSizer(hbox3)

    def OnTextEnter(self,e):
        line_cnt = self.cmd_space.GetNumberOfLines()-1
        line_len = self.cmd_space.GetLineLength(line_cnt)

        if line_len == 0:
            cur_cmd = self.cmd_space.GetLineText(line_cnt-1)[3:]
            #print 'Current command:',cur_cmd
            if cur_cmd ==  'quit();':
                self.Close()
            else:
                coms_res = self.compiler.compiling(cur_cmd,sh)
                #print 'compiling result:',repr(coms_res)
                info = wx.adv.AboutDialogInfo()
                info.SetIcon(wx.Icon('image/compile_res.png', wx.BITMAP_TYPE_PNG))
                info.SetName('Compiling result')
                info.SetDescription(coms_res)
                info_box = wx.adv.AboutBox(info)
                pass 
            
            self.cmd_space.WriteText('>> ')
        elif line_len<=2:
            self.cmd_space.WriteText(' ')

class Map(wx.Frame):
    def __init__(self,*args,**kwargs):
        super(Map,self).__init__(*args,**kwargs)
        self.Centre()
        self.SetSize(700,600)
        self.list_cnt = len(datapool.city_ls)
        self.init_UI()
        self.data_init()
    
    def init_UI(self):
        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox0 = wx.BoxSizer(wx.VERTICAL)

        font = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.DEFAULT)

        txt1 = "Money cost between cities"
        st1 = wx.StaticText(panel, label=txt1, style=wx.ALIGN_LEFT)

        txt2 = "Time cost between cities"
        st2 = wx.StaticText(panel, label=txt2, style=wx.ALIGN_LEFT)

        st1.SetFont(font)
        st2.SetFont(font)

        self.list = wx.ListCtrl(panel, wx.ID_ANY, style=wx.LC_REPORT)
        self.list.InsertColumn(0, 'Self',width=80)
        self.ls2 = wx.ListCtrl(panel, wx.ID_ANY, style=wx.LC_REPORT)
        self.ls2.InsertColumn(0, 'Self',width=80)
        


        vbox0.Add(st1, flag=wx.ALL, border=2)
        vbox0.Add(self.list,wx.ID_ANY,wx.EXPAND | wx.ALL, 10)
        vbox0.Add(st2, flag=wx.ALL, border=2)
        vbox0.Add(self.ls2,wx.ID_ANY,wx.EXPAND | wx.ALL, 10)
        hbox.Add(vbox0, wx.ID_ANY, wx.EXPAND | wx.ALL, 10)

        btnPanel = wx.Panel(panel)
        vbox = wx.BoxSizer(wx.VERTICAL)
        newBtn = wx.Button(btnPanel, wx.ID_ANY, 'New', size=(90, 30))
        delBtn = wx.Button(btnPanel, wx.ID_ANY, 'Delete', size=(90, 30))
        clrBtn = wx.Button(btnPanel, wx.ID_ANY, 'Clear', size=(90, 30))

        self.Bind(wx.EVT_BUTTON, self.NewItem, id=newBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDelete, id=delBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnClear, id=clrBtn.GetId())
        
        vbox.Add((-1, 20))
        vbox.Add(newBtn)
        vbox.Add(delBtn, 0, wx.TOP, 5)
        vbox.Add(clrBtn, 0, wx.TOP, 5)

        btnPanel.SetSizer(vbox)
        hbox.Add(btnPanel, 0.6, wx.EXPAND | wx.RIGHT, 20)
         
        panel.SetSizer(hbox)
        self.Centre()
        pass
    def NewItem(self, event):
        gen = DG.Gen()
        while True:
            if self.list_cnt >7:
                aName = 'NOCITY'
                break
            aName = gen.get_city_name(1)
            ok = True
            if self.list_cnt == 0:
                break
            for i in datapool.city_ls:
                if i.name == aName:
                    ok = False
                    break
            if ok:
                break
        

    
        name = wx.GetTextFromUser("New city's name", 'Insert dialog',aName)
        if name == '': return
        ct_name = name
        ct_nei_m = [];ct_nei_t = []

        index = self.list.InsertItem(self.list_cnt, name)
        index2 = self.ls2.InsertItem(self.list_cnt, name)

        
        self.list.InsertColumn(self.list_cnt +1 ,name,width = 80)
        self.ls2.InsertColumn(self.list_cnt +1 ,name,width = 80)
        self.ls2.SetItem(index,self.list_cnt+1,'0')
        self.list.SetItem(index,self.list_cnt+1,'0')

        for i in range(self.list_cnt):
            aMoney = gen.get_money()
            dis = wx.GetTextFromUser("Money cost between %s and %s"%(name,datapool.city_ls[i].name), 'Insert dialog',aMoney)
            self.list.SetItem(index, i+1, dis)
            self.list.SetItem(i,index+1,dis)
            ct_nei_m.append(int(dis))
            datapool.city_ls[i].neighbour_m.append(int(dis))


        for i in range(self.list_cnt):
            aTime = gen.get_time()
            dis = wx.GetTextFromUser("Time cost between %s and %s"%(name,datapool.city_ls[i].name), 'Insert dialog',aTime)
            self.ls2.SetItem(index2, i+1, dis)
            self.ls2.SetItem(i,index2+1,dis)
            ct_nei_t.append(int(dis))
            datapool.city_ls[i].neighbour_t.append(int(dis))

        ct_nei_m.append(0);ct_nei_t.append(0)

        datapool.add_city(ct_name,ct_nei_m,ct_nei_t)
        self.list_cnt += 1

        #print all city:
        # print 'All city'
        # for i in range(len(datapool.city_ls)):
        #     ct = datapool.city_ls[i]
        #     print '--'*10
        #     print 'name: ',ct.name
        #     print 'neighbour_m:',ct.neighbour_m
        #     print 'neigohbour_t:',ct.neighbour_t
        #     print '--'*10

        

        #datapool.add_iterm([name,from_addr,to_addr,date0,phone,int(quick)])
        
        # index = self.list.InsertItem(self.list_cnt, name)
        # self.list.SetItem(index, 1, from_addr)
        # self.list_cnt += 1

    def OnDelete(self, event):
        sel = self.list.GetFocusedItem()
        print sel
        #print sel
        if sel != -1:
            self.list.DeleteItem(sel);self.ls2.DeleteItem(sel)
            self.list.DeleteColumn(sel+1);self.ls2.DeleteColumn(sel+1)
            datapool.city_ls.pop(sel)
            for i in range(len(datapool.city_ls)):
                datapool.city_ls[i].neighbour_m.pop(sel)
                datapool.city_ls[i].neighbour_t.pop(sel)
            
            self.list_cnt -= 1
            #datapool.iterm_ls.pop(sel)

        # print 'All city'
        # for i in range(len(datapool.city_ls)):
        #     ct = datapool.city_ls[i]
        #     print '--'*10
        #     print 'name: ',ct.name
        #     print 'neighbour_m:',ct.neighbour_m
        #     print 'neigohbour_t:',ct.neighbour_t
        #     print '--'*10

    def OnClear(self, event):
        self.list.ClearAll()
        self.ls2.ClearAll()
        self.list.InsertColumn(0, 'Self',width=80)
        self.ls2.InsertColumn(0, 'Self',width=80)
        self.list_cnt = 0
        datapool.city_ls = []
        #datapool.iterm_ls = []

    def data_init(self):
        if self.list_cnt==0:return
        #self.list.InsertColumn(0,'self',width = 80);self.ls2.InsertColumn(0,'self',width = 80)
    
        for i in range(len(datapool.city_ls)):
            self.list.InsertColumn(i+1,'%s'%datapool.city_ls[i].name,width = 80)
            self.ls2.InsertColumn(i+1,'%s'%datapool.city_ls[i].name,width = 80)
            
        for i in range(len(datapool.city_ls)):
            ct = datapool.city_ls[i]
            index1 = self.list.InsertItem(i, ct.name)
            index2 = self.ls2.InsertItem(i, ct.name)

            for j in range(len(ct.neighbour_m)):
                self.list.SetItem(index1, j+1, str(ct.neighbour_m[j]))
                self.ls2.SetItem(index2, j+1, str(ct.neighbour_t[j]))
        
        #index = self.list.InsertItem(self.list_cnt, name)
        #self.list.SetItem(index, i+1, dis)

        
        pass

class my_frame(wx.Frame):
    def __init__(self,*args,**kwargs):
        super(my_frame,self).__init__(*args,**kwargs)

        self.SetSize(470,280)
        self.init_UI()
        self.Centre()
        self.expand = False
    
    def init_UI(self):
        
        #menu
        filemenu= wx.Menu()
        filemenu.Append(wx.ID_EXIT, "E&xit"," Terminate the program")
        editmenu = wx.Menu()
        netmenu = wx.Menu()
        showmenu = wx.Menu()
        configmenu = wx.Menu()
        helpmenu = wx.Menu()

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(editmenu, "&Edit")
        menuBar.Append(netmenu, "&Net")
        menuBar.Append(showmenu, "&Show")
        menuBar.Append(configmenu, "&Config")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)

        #toolbar
        tb = self.CreateToolBar( wx.TB_HORIZONTAL | wx.NO_BORDER |
		      wx.TB_FLAT)
        self.tb = tb

        
        login1 = tb.AddTool(0, 'login', wx.Bitmap('image/login.png'), shortHelp='Login')
        ter = tb.AddTool(10, 'Terminal', wx.Bitmap('image/terminal.png'), shortHelp='Terminal')
        edt = tb.AddTool(20, 'EditList', wx.Bitmap('image/edit2.png'), shortHelp='List')
        mmp = tb.AddTool(30, 'Map', wx.Bitmap('image/map.png'), shortHelp='Map')
        pt = tb.AddTool(40, 'Print', wx.Bitmap('image/show.png'), shortHelp='Print')
        
        tb.AddSeparator()
        #tips = tb.AddTool(60, 'tips', wx.Bitmap('image/tips.png'), shortHelp='Help tips')
        wk = tb.AddTool(50, 'Setup', wx.Bitmap('image/setup.png'), shortHelp='Work')
        tips = tb.AddTool(60, 'tips', wx.Bitmap('image/tips.png'), shortHelp='Tutorial')
        info = tb.AddTool(70, 'info', wx.Bitmap('image/help.png'), shortHelp='Info')
        folder = tb.AddTool(80, 'expand', wx.Bitmap('image/folder.png'), shortHelp='Folder')
        clse = tb.AddTool(90, 'expand', wx.Bitmap('image/expand0.png'), shortHelp='Expand')

        self.tool_ls = [login1,ter,edt,mmp,pt,wk,tips,info,folder,clse]
        

        self.Bind(wx.EVT_TOOL,self.OnTerminal,id = ter.GetId())
        self.Bind(wx.EVT_TOOL,self.OnMap,id = mmp.GetId())
        self.Bind(wx.EVT_TOOL,self.OnAbout,id = info.GetId())
        self.Bind(wx.EVT_TOOL,self.OnExpand,id = clse.GetId())
        self.Bind(wx.EVT_TOOL,self.OnTips,id = tips.GetId())
        self.Bind(wx.EVT_TOOL,self.OnEditIterm,id = edt.GetId())
        self.Bind(wx.EVT_TOOL,self.OnPrint,id = pt.GetId())
        self.Bind(wx.EVT_TOOL,self.OnFolder,id = folder.GetId())
        self.Bind(wx.EVT_TOOL,self.OnWork,id = wk.GetId())
        self.Bind(wx.EVT_TOOL,self.OnLogin,id = login1.GetId())
 

        # Lock tools
        tb.EnableTool(ter.GetId(),False)
        tb.EnableTool(edt.GetId(),False)
        tb.EnableTool(mmp.GetId(),False)
        tb.EnableTool(pt.GetId(),False)
        tb.EnableTool(wk.GetId(),False)
        tb.EnableTool(tips.GetId(),False)
        tb.EnableTool(folder.GetId(),False)
        tb.EnableTool(clse.GetId(),False)
        tb.EnableTool(info.GetId(),False)
        
        
        tb.Realize()


        #select Tool
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        st = wx.StaticText(panel, label="Select a tool")
        icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('image/tool.png'))
        vbox.Add((-1,40))
        vbox.Add(icon, flag=wx.ALIGN_CENTER_HORIZONTAL|wx.RIGHT|wx.LEFT|wx.BOTTOM, border=8)
        vbox.Add(st, flag=wx.ALIGN_CENTER_HORIZONTAL|wx.RIGHT|wx.LEFT, border=8)
        vbox.Add((-1,20))
        panel.SetSizer(vbox)
        pass
    def OnLogin(self,e):
        self.login = Login(self,None,title = 'Login')
        self.login.Show()
        pass
    def OnWork(self,e):
        wk = Work(None,title = 'Work')
        wk.Show()
        pass
    def OnEditIterm(self,e):
        ET = EditIterm(None,title = 'Edit Iterms')
        ET.Show()
        pass

    def OnTips(self,e):
        info_tips = """
        Mini-SQLite Usage:
            Create table:
                create table table_name {col_name col_type, ...};
            Display table:
                display table_name;
            Add a log:
                insert into table_name values(value1,valu2,...);
            Search a log:
                select from table_name where(col_name = value1,col_nae2 = value2,...);
            Delete a log:
                Delete from table_name where(col_name1 = value1,...);
        """
        #wx.MessageBox(info,'Tutorial',wx.OK | wx.ICON_INFORMATION)
        description = info_tips
        info = wx.adv.AboutDialogInfo()
        info.SetIcon(wx.Icon('image/tips.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Tutorial')
        info.SetDescription(description)
        wx.adv.AboutBox(info)
        pass

    def OnTerminal(self,e):
        tf = Terminal(None,title = 'Terminal')
        tf.Show()
        pass
    def OnMap(self,e):
        mf = Map(None,title = 'Map Data')
        mf.Show()
        pass

    def OnAbout(self,e):
        description = """A transportation and Mini-SQL software developped by primelee"""
        
        licence = """MIT Licence"""
        info = wx.adv.AboutDialogInfo()
        #info.SetIcon(wx.Icon('welcome.JPG', wx.BITMAP_TYPE_PNG))
        info.SetName('Transportation')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2019 primelee')
        info.SetWebSite('http://primelyw.github.io')
        info.SetLicence(licence)
        info.AddDeveloper('Prime Lee')
        info.AddDocWriter('Prime Lee')
        info.AddArtist('The Tango crew')
        info.AddTranslator('Bella')
        wx.adv.AboutBox(info)
        
    def OnExit(self,e):
        self.Close()
    def OnExpand(self,e):
        #self.Close()
        if self.expand:
            self.SetSize(470,280)
            self.expand = False
        else:
            self.SetSize(470,65)
            self.expand = True
    
    def OnPrint(self,e):
        pf = Print(None,title = 'Printer')
        pf.Show()
        pass
    def OnFolder(self,e):
        ff = Folder(None,title = 'Folder')
        ff.Show()
        pass

class MyListCtrl(wx.ListCtrl):


    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT)

        images = ['image/folder_img/empty.png', 'image/folder_img/folder.png', 'image/folder_img/source-py.png',
		      'image/folder_img/image.png', 'image/folder_img/pdf.png', 'image/folder_img/up16.png']

        self.InsertColumn(0, 'Name')
        self.InsertColumn(1, 'Ext')
        self.InsertColumn(2, 'Size', wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(3, 'Modified')

        self.SetColumnWidth(0, 220)
        self.SetColumnWidth(1, 70)
        self.SetColumnWidth(2, 100)
        self.SetColumnWidth(3, 420)



        self.il = wx.ImageList(16, 16)

        for i in images:
            self.il.Add(wx.Bitmap(i))

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
   


        j = 1

        self.InsertItem(0, '..')
        self.SetItemImage(0, 5)

        files = os.listdir('.')

        for i in files:

            (name, ext) = os.path.splitext(i)
            ex = ext[1:]
            size = os.path.getsize(i)
            sec = os.path.getmtime(i)

            self.InsertItem(j, name)
            self.SetItem(j, 1, ex)
            self.SetItem(j, 2, str(size) + ' B')
            self.SetItem(j, 3, time.strftime('%Y-%m-%d %H:%M', time.localtime(sec)))

            if os.path.isdir(i):
                self.SetItemImage(j, 1)
            elif ex == 'py':
                self.SetItemImage(j, 2)
            elif ex == 'jpg':
                self.SetItemImage(j, 3)
            elif ex == 'pdf':
                self.SetItemImage(j, 4)
            else:
                self.SetItemImage(j, 0)

            if (j % 2) == 0:

                self.SetItemBackgroundColour(j, '#e6f1f5')

            j = j + 1

class Folder(wx.Frame):

    def __init__(self, *args, **kw):
        super(Folder, self).__init__(*args, **kw)

        self.InitUI()

    def InitUI(self):



        p1 = MyListCtrl(self)


        filemenu= wx.Menu()
        filemenu.Append(200, "E&xit"," Terminate the program")
        editmenu = wx.Menu()
        netmenu = wx.Menu()
        showmenu = wx.Menu()
        configmenu = wx.Menu()
        helpmenu = wx.Menu()

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(editmenu, "&Edit")
        menuBar.Append(netmenu, "&Net")
        menuBar.Append(showmenu, "&Show")
        menuBar.Append(configmenu, "&Config")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnExit, id=200)

        tb = self.CreateToolBar( wx.TB_HORIZONTAL | wx.NO_BORDER |
		      wx.TB_FLAT)

        tb.AddTool(10, 'Previous', wx.Bitmap('image/folder_img/previous.png'), shortHelp='Previous')
        tb.AddTool(20, 'Up', wx.Bitmap('image/folder_img/up.png'), shortHelp='Up one directory')
        tb.AddTool(30, 'Home', wx.Bitmap('image/folder_img/home.png'), shortHelp='Home')
        tb.AddTool(40, 'Refresh', wx.Bitmap('image/folder_img/refresh.png'), shortHelp='Refresh')

        tb.Realize()

        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        button1 = wx.Button(self,100 + 1, "F3 View")
        button2 = wx.Button(self,100 + 2, "F4 Edit")
        button3 = wx.Button(self,100 + 3, "F5 Copy")
        button4 = wx.Button(self,100 + 4, "F6 Move")
        button5 = wx.Button(self,100 + 5, "F7 Mkdir")
        button6 = wx.Button(self,100 + 6, "F8 Delete")
        button7 = wx.Button(self,100 + 7, "F9 Rename")
        button8 = wx.Button(self, 200, "F10 Quit")

        self.sizer2.Add(button1, 1, wx.EXPAND)
        self.sizer2.Add(button2, 1, wx.EXPAND)
        self.sizer2.Add(button3, 1, wx.EXPAND)
        self.sizer2.Add(button4, 1, wx.EXPAND)
        self.sizer2.Add(button5, 1, wx.EXPAND)
        self.sizer2.Add(button6, 1, wx.EXPAND)
        self.sizer2.Add(button7, 1, wx.EXPAND)
        self.sizer2.Add(button8, 1, wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self.OnExit, id=200)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(p1,1,wx.EXPAND)
        self.sizer.Add(self.sizer2,0,wx.EXPAND)
        self.SetSizer(self.sizer)


        sb = self.CreateStatusBar()
        sb.SetStatusText(os.getcwd())

        self.SetTitle("File Hunter")
        self.Center()


    def OnExit(self, e):

        self.Close(True)


def main():
    app = wx.App()
    frm = my_frame(None,title = 'Logistics Management Systems')
    frm.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()

