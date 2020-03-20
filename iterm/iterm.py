#! /usr/bin/env python
#coding=utf8
import time

ct2num = {}

class iterm:
    def __init__(self,name='',addr0='',addr1='',date0=None,phone='',quick = False):
        self.name = name; self.addr0 = addr0
        self.date0 = date0
        self.addr1 = addr1;  self.phone = phone
        self.quick = quick
        self.path_m = [];self.path_t = []
        try:
            self.time = int(time.mktime(time.strptime(date0,"%Y-%m-%d")))
        except ValueError:
            print 'Intilized the iterm with no begin date'
    def print_info(self):
        s = ''
        s+= '-----'*10
        s+= '\nName: '+self.name
        s+= '\nFrom: '+self.addr0
        s+= '\nTo: '+self.addr1
        s+= '\nSend date: '+self.date0
        s+= '\nPhone: '+self.phone
        s+= '\nQuick: '+str(self.quick)
        s+= '\nMoney least path: '+str(self.path_m)
        s+= '\nTime least path: '+str(self.path_t)
        s+= "\n"+'-----'*10
        s += '\n'
        return s


class city:
    id = 0
    def __init__(self,name = '',iterm_list = [],neighbour_m = [],neighbour_t = []):
        self.name = name;self.id = city.id; self.iterm_ls = iterm_list
        self.neighbour_m = neighbour_m
        self.neighbour_t = neighbour_t
        self.paths_m = [];self.paths_t = []
        ct2num.update({name:self.id})
        city.id += 1

    def print_all_info(self):
        con = ''
        con+= '--'*10+'\n'+'--'*10+'\n'+'--'*10+'\n'
        con += 'name: '+self.name+'\n'
        con += 'neighbour_m: '+str(self.neighbour_m)+'\n'
        con += 'neigohbour_t: '+str(self.neighbour_t)+'\n'
        con += self.print_iterms()
        con += '--'*10+'\n'+'--'*10+'\n'+'--'*10+'\n'
        return con
    
    def print_city_info(self):
        con = ''
        con+= '--'*10+'\n'+'--'*10+'\n'+'--'*10+'\n'
        con += 'name: '+self.name+'\n'
        con += 'neighbour_m: '+str(self.neighbour_m)+'\n'
        con += 'neigohbour_t: '+str(self.neighbour_t)+'\n'
        con += '--'*10+'\n'+'--'*10+'\n'+'--'*10+'\n'
        return con
    
    def update_iterm_list(self,ls):
        self.iterm_ls = ls
        
    def sort_iterms(self):
        def mycmp(a,b):
            if a.quick == b.quick: return a.time-b.time
            else: return b.quick-a.quick

        self.ls = sorted(self.iterm_ls,cmp = mycmp)

    def print_iterms(self):
        content  = 'Items:\n'
        for i in self.iterm_ls:
            content += i.print_info()+'\n'
        return content
    
    def trans_path(self,ct_mp):
        self.paths_m,self.paths_t = ct_mp.find_my_paths(self.id)
    
    def alloc_iterm_path(self,ct_mp):
        self.trans_path(ct_mp)
        for i in range(len(self.iterm_ls)):
            j = self.iterm_ls[i]
            # self.iterm_ls[i].path_m = self.paths_m[ct2num[self.iterm_ls[i].addr1]]
            # self.iterm_ls[i].path_t = self.paths_t[ct2num[self.iterm_ls[i].addr1]]
            j.path_m = self.paths_m[ct2num[j.addr1]]
            j.path_t = self.paths_t[ct2num[j.addr1]]
        
class city_map:
    def __init__(self,map_m = [],map_t = []):
        self.map_m = map_m
        self.map_t = map_t
        self.size = len(map_m)
    
    def show_map(self):
        print 'Money Map:'
        for i in range(self.size):
            for j in range(self.size):
                print self.map_m[i][j],
            print
        print 'Time Map:'
        for i in range(self.size):
            for j in range(self.size):
                print self.map_t[i][j],
            print
    
    def find_my_paths(self,source):
        return self.dijkstra(source,self.map_m),self.dijkstra(source,self.map_t)

    def dijkstra(self,source,map):
        oo = 10**10
        size = len(map)
        dis = [oo for _ in range(size)]
        vis = [0 for _  in range(size)]
        path = [[] for _ in range(size)]
        pre = [-1 for i in range(size)]

        for i in range(size):
            for j in range(size): 
                if map[i][j]<0 : map[i][j] = oo
        
        dis[source] = 0

        while True:
            cur = -1
            min = oo
            for i in range(size):
                if vis[i]==0 and dis[i]<min:
                    cur = i
                    min = dis[i]
            if cur == -1:
                break
            vis[cur] = 1
            for j in range(size):
                if map[cur][j]+dis[cur] < dis[j]:
                    dis[j] = dis[cur] + map[cur][j]
                    pre[j] = cur
            
        for i in range(size):
            path[i] = [dis[i],[]]
            if path[i][0] == oo:
                continue
            ls = []
            cur = i
            while True:
                if cur == -1:
                    break
                ls.append(cur)
                cur = pre[cur]
            ls.reverse()
            path[i][1] = ls

        return path
        pass


    

def test():

    #test dijkstrea
    oo = 10**10
    map = [[0,3,2,oo],[3,0,3,oo],[2,1,0,oo],[oo,oo,oo,0]]
    city_mp = city_map(map,map)
    dis = city_mp.find_my_paths(0)

    #iterm:
    itm0 = iterm('cup','Shanghai','Shenzhen','2019-6-12',quick = True)
    itm1 = iterm('cup0','Shanghai','Shenzhen','2019-6-11',quick = False)
    it_ls = [itm0,itm1]
    c0 = city('Shanghai',it_ls)
    c1 = city('Shenzhen')
    c0.sort_iterms()
    #c0.print_iterms()

    c0.alloc_iterm_path(city_mp)
    print c0.print_iterms()
    print 'test'
    for i in it_ls:
        print i.print_info()
    #print itm0.path_m



if __name__ == '__main__':
    test()
        





        
