#coding=utf8
import random as rd 

class Gen:
    def __init__(self):
        self.ch_city = ['深圳','北京','上海','杭州','成都','南京','广州','海南']
        self.city_sz = len(self.ch_city)
        self.en_city = ['Shenzhen','Beijing','Shanghai','Hangzhou','Chengdu','Nanjing','Guangzhou','Hainan']
        self.ch_item = ['牙刷','电脑','水杯','笔记本','公仔','红酒','苹果']
        self.item_sz = len(self.ch_item)
        self.en_item = ['Brush','Computer','Cup','Notebook','Doll','Wine','Apple']
        self.person = ['Bella','Ann','Bruce','Prime','Wayne','Tony','Pat','Judy']
        self.peron_sz = len(self.person)

    def get_city_name(self,opt):
        num = rd.randint(0,self.city_sz-1) 
        if opt==0:
            return self.ch_city[num]
        else:
            return self.en_city[num]

    def get_money(self):
        return str(rd.randint(8,40))
    def get_time(self):
        return str(rd.randint(2,10))
    
    def get_phone(self):
        res = '13'
        for i in range(9):
            res += str(rd.randint(0,9))
        return res
    def get_date(self):
        res = '2019-06-'
        s = rd.randint(1,30)
        if s<10:
            s = '0'+str(s)
        else:
            s = str(s)
        return res+s

    def get_item_unit(self,opt):
        ls = []
        if opt ==0:
            ls.append(self.ch_item[rd.randint(0,self.item_sz-1)])
        else:
            ls.append(self.en_item[rd.randint(0,self.item_sz-1)])
        addr0 = self.get_city_name(opt)
        while True:
            addr1 = self.get_city_name(opt)
            if addr1 != addr0:
                ls.append(addr0)
                ls.append(addr1)
                break
        ls.append(self.get_date())
        ls.append(self.get_phone())
        ls.append(str(rd.randint(0,1)))
        return ls

        

    

def test():
    g = Gen()
    print g.get_item_unit(1)
    print g.get_city_name(1)
    print g.get_money()
    print g.get_time()
    pass
if __name__ == '__main__':
    test()