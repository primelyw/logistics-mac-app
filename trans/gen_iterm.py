import random as rd

i_name = ['phone','computer','books','bike','doll','cup','umbrella','etc']
i_person = ['John','Prime','Bella','Tonny','Ashe','Tim','Allen','Bob','Alice']
i_addr = [i for i in range(8)]
i_aid = [0,1]
i_send_date = [i for i in range(10)]

iterm_count = 20

file = open('iterm.txt','w')
file.write(str(iterm_count)+'\n')

for i in range(iterm_count):
    file.write(i_name[rd.randint(0,len(i_name)-1)]+'\n')

    file.write(i_person[rd.randint(0,len(i_person)-1)]+'\n')
    file.write(i_person[rd.randint(0,len(i_person)-1)]+'\n')

    file.write(str(i_addr[rd.randint(0,len(i_addr)-1)])+'\n')
    file.write(str(i_addr[rd.randint(0,len(i_addr)-1)])+'\n')

    
    file.write(str(i_send_date[rd.randint(0,len(i_send_date)-1)])+'\n')
    file.write(str(i_aid[rd.randint(0,len(i_aid)-1)])+'\n')
    file.write('\n')

file.close()

