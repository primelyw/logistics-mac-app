from random import randint as rdi;
f = open('city.txt','w')
city_cnt = 8
f.write(str(city_cnt)+'\n')
ran = [(2,7),(10,20),(1,2),(30,40)]

for k in ran:

    for i in range(8):
        line = ''
        for j in range(8):
            if j==7:
                line += str(rdi(k[0],k[1]))
            else:
                line += str(rdi(k[0],k[1]))+' '
        line += '\n'
        f.write(line)
    f.write('\n')
f.close()



