#! /usr/bin/env python
#coding=utf8

from compiler import lexer2
from compiler import ast
from fileio import fileio as io
from iterm import  iterm as Itm

class Compiler:
    def __init__(self):
        self.lexer = lexer2.start # lexer2.start(command) -> token_stream
        pass

    def compiling(self,commands,sheet):
        tok_s = self.lexer(commands)
        ast.token_stream = tok_s
        coms_list = ast.start()
        coms_res = ''
        for each in coms_list:
            s = self.option(sheet,each)
            #print type(s)
            coms_res += (s)
        
        return coms_res

    def option(self,sh,req):
        tips = ''#terminal result
        if req[0] == 'ERROR':
            tips = req[1]+'\n'
            return tips
        tb_name = req[1][0]
        #pay = req[1][1]
        opt = req[0]
        #print opt,tb_name#pay
        if opt=='display table':
            #handle no such a table?
            sig,content = sh.print_table(tb_name)
            if not sig[0]:
                tips =  sig[1]
                tips += '\n'
            tips = 'Display table successfully!\n'+content
            
        else:
            payload = req[1][1]
            #print 'payload',payload
            if opt == 'create table':
                sh.create_table([payload],tb_name)
                tips =  'Create table sussfully!\n'
                
            elif opt == 'add log':
                sig = sh.add_logs(tb_name,[payload])
                if not sig[0]:
                    tips =  sig[1]
                    tips += '\n'
                else:
                    tips =  'Add log sussfully!\n'
                
            elif opt == 'search log':
                sig,content = sh.search_logs(tb_name,payload)
                if not sig[0]:
                    tips =  sig[1]
                    tips += '\n'
                else:
                    tips =  'Search log sussfully!\n'+content
                
            elif opt == 'delete log':
                sig = sh.delete_logs(tb_name,payload)
                if not sig[0]:
                    tips =  sig[1]
                    tips += '\n'
                else:
                    tips =  'Delete log sussfully!\n'
        return tips
            

class Data_Pool():
    def __init__(self,sheet_name,user,pwd):
        self.sheet = io.sheet(sheet_name)
        self.iterm_ls = []
        self.city_ls = []
        self.map = []
        self.user_name = user
        self.password = pwd
    
    def add_iterm(self,iu):
        name = iu[0]
        addr0 = iu[1]
        addr1 = iu[2]
        data0 = iu[3]
        phone = iu[4]
        quick = iu[5]
        it_tmp = Itm.iterm(name,addr0,addr1,data0,phone,quick)
        self.iterm_ls.append(it_tmp)
        pass
    
    def add_city(self,name,nei_m,nei_t):
        self.city_ls.append(Itm.city(name,neighbour_m = nei_m,neighbour_t = nei_t))
        pass

    def show_item_list(self):
        content = 'All items:\n'
        for i in self.iterm_ls:
            content += i.print_info()+'\n'
        return content
    
    def show_city_list(self):
        content = 'All cities: \n'
        for i in self.city_ls:
            content+= i.print_all_info()+'\n'
        return content
    
    def form_map(self,map_m,map_t):
        self.map = Itm.city_map(map_m,map_t)
        

    

def main():
    datapool = Data_Pool('prime_sheet')
    sh = datapool.sheet
    c4 = Compiler()
    c4.compiling('create table classmates{name string, age int};display classmates;',sh)
    pass

if __name__ == '__main__':
    main()