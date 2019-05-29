#include <iostream>
#include <cstdlib>
#include <algorithm>
#include <vector>
#include <cstdio>
#include <fstream>
using namespace std;
void dijkstra(int dis[30],int path[30][30],int source,int time[30][30],int money[30][30],int opt,int air);
void city_best_alloc(int idx);

typedef struct iterm_input{
    int id;
    string name, sender,recver;
    int from_addr,to_addr;
    int send_date;
    bool first_aid;
} iterm_input;


typedef struct cost_pair{
    int time,money;
    void update_both(int x,int y){
        time = x;
        money = y;
    }
    void update_money(int m){
        money = m;
    }
    void update_time(int t){
        time = t;
    }
}cost_pair;

typedef struct city_input{
    int city_size;
    cost_pair normal_map[10][10];
    cost_pair air_map[10][10];
}city_input;    



class iterm{
public:
    int id;
    string name;
    string sender;
    string recver;
    int from_addr;
    int to_addr;
    bool first_aid;
    int send_date;
    int current_addr;
    int arrived_date;
    bool done;
    int air_time,air_money;
    int time_least_time,time_least_money;
    int money_least_money,money_least_time;
    vector<int> normal_path_time;
    vector<int> normal_path_money;
    vector<int> air_path;
public:
    iterm(iterm_input ii){
        id = ii.id;
        name = ii.name;
        sender = ii.sender;
        recver = ii.recver;
        from_addr = ii.from_addr;
        to_addr = ii.to_addr;
        send_date = ii.send_date;
        first_aid = ii.first_aid;
        current_addr = -1;
        arrived_date = -1;
        done = false;
        time_least_time = time_least_money = money_least_money = money_least_time = 0;
    }
    void update_current_addr(int place){
        this->current_addr = place;
    }
    void set_arrived_addr(int place){
        this->arrived_date = place;
    }
    void print_info(){
        for(int i = 0; i<3; i++) cout<<"-----";
        cout<<"Iterm Info";
        for(int i = 0; i<3; i++) cout<<"-----";cout<<endl;
        cout<<"Iterm: "<<name<<endl;
        cout<<"ID:"<<id<<endl;
        cout<<"Sender: "<<sender<<endl;
        cout<<"Recver: "<<recver<<endl;
        cout<<"From: "<<from_addr<<endl;
        cout<<"To: "<<to_addr<<endl;
        cout<<"Air: ";
        if (first_aid){
            cout<<"Yes"<<endl;
        }else cout<<"No"<<endl;

        for(int i = 0; i<3; i++) cout<<"-----";
        cout<<"Transport Line";
        for(int i = 0; i<3; i++) cout<<"-----";cout<<endl;

        cout<<"Air Line:";
        for(int i = 0; i<air_path.size(); i++){
            printf("---> City(%d) ",air_path[i]);
        }cout<<endl;
        cout<<"Least_time:"<<air_time<<endl;
        cout<<"Money_cost:"<<air_money<<endl;
        cout<<endl;

        cout<<"NORMAL Line: time_least";
        for(int i = 0; i<normal_path_time.size(); i++){
            printf("---> City(%d) ",normal_path_time[i]);
        }cout<<endl;
        cout<<"Least_time:"<<time_least_time<<endl;
        cout<<"Money_cost:"<<time_least_money<<endl;
        cout<<endl;

        cout<<"NORMAL Line: money_least";
        for(int i = 0; i<normal_path_money.size(); i++){
            printf("---> City(%d) ",normal_path_money[i]);
        }cout<<endl;
        cout<<"Least_time:"<<money_least_time<<endl;
        cout<<"Money_cost:"<<money_least_money<<endl;
        cout<<endl;
        
    }
};

class city{
public:
    int size;
    cost_pair normal_map[10][10];
    cost_pair air_map[10][10];


    void update(city_input ci){
        size = ci.city_size;
        for(int i= 0; i<size; i++){
            for(int j = 0; j<size; j++){
                normal_map[i][j] = ci.normal_map[i][j];
            }
        }
        for(int i= 0; i<size; i++){
            for(int j = 0; j<size; j++){
                air_map[i][j] = ci.air_map[i][j];
            }
        }
    }

    city(city_input ci){
        update(ci);
    }
    city(){}
};

vector<iterm> iterm_list;
city city_map;
vector<vector<iterm> > city_iterm_list;


void initial_iterm_info(){
    ifstream iterm_info ("iterm.txt");
    ifstream city_info("city.txt");
    int city_size;
    city_info>>city_size;
    city_info.close();

    
    if (iterm_info.is_open()){
        int num;
        iterm_info>>num;
        //cout<<"num: "<<num<<endl;
        iterm_input ii;

        for(int i = 0; i<city_size; i++){
            vector<iterm> vi;
            city_iterm_list.push_back(vi);
        }
        for(int i = 0; i<num; i++){
            ii.id = i;
            iterm_info>>ii.name;
            
            iterm_info>>ii.sender;
            
            iterm_info>>ii.recver;
            iterm_info>>ii.from_addr;
            iterm_info>>ii.to_addr;
            iterm_info>>ii.send_date;
            iterm_info>>ii.first_aid;
            
            iterm i_tmp = iterm(ii);
            
            city_iterm_list[i_tmp.from_addr].push_back(i_tmp);
        }
    }
    else cout<<"Unable to open 'iterm_txt' file";
}


city_input initial_city(){
    ifstream city_info("city.txt");
    city_input ci;
    if(city_info.is_open()){
        int size;
        city_info>>size;
        ci.city_size = size;
        for(int i = 0; i<size; i++){
            for(int j = 0; j<size; j++){
                int tmp;
                city_info>>tmp;if(i==j) tmp = 0;
                ci.normal_map[i][j].update_time(tmp);
            }
        }

        for(int i = 0; i<size; i++){
            for(int j = 0; j<size; j++){
                int tmp;
                city_info>>tmp;
                if(i==j) tmp = 0;
                ci.normal_map[i][j].update_money(tmp);
            }
        }

        for(int i = 0; i<size; i++){
            for(int j = 0; j<size; j++){
                int tmp;
                city_info>>tmp;if(i==j) tmp = 0;
                ci.air_map[i][j].update_time(tmp);
            }
        }

        for(int i = 0; i<size; i++){
            for(int j = 0; j<size; j++){
                int tmp;
                city_info>>tmp;if(i==j) tmp = 0;
                ci.air_map[i][j].update_money(tmp);
            }
        }
    }else cout<<"Unable to open the 'city.txt' file"<<endl;
    city_info.close(); 
    city_map.update(ci);
    return ci;
}

bool iterm_cmp(iterm i1,iterm i2){
    return i1.send_date<i2.send_date;
}

void sort_iterm_in_city(){
    int city_size = city_iterm_list.size();
    for(int i = 0; i<city_size; i++){
        vector<iterm> &ref = city_iterm_list[i];
        sort(ref.begin(),ref.end(),iterm_cmp);
    }
}


void test(){
    // initial_city();
    // int size = city_map.size;
    // for(int i= 0; i<size; i++){
    //     for(int j = 0; j<size; j++){
    //         cost_pair tmp  = city_map.normal_map[i][j];
    //         printf("(%d,%d) ",tmp.time,tmp.money);
    //     }
    //     cout<<endl;
    // }
    // cout<<endl;

    // for(int i= 0; i<size; i++){
    //     for(int j = 0; j<size; j++){
    //         cost_pair tmp  = city_map.air_map[i][j];
    //         printf("(%d,%d) ",tmp.time,tmp.money);
    //     }
    //     cout<<endl;
    // }

    // for(int i =0; i<iterm_list.size(); i++){
    //     iterm_list[i].print_info();
    // }

    // for(int i = 0; i< city_iterm_list.size(); i++){
    //     printf("City(%d):",i);
    //     for(int j = 0; j<city_iterm_list[i].size(); j++){
    //         printf("--->");
    //         cout<<city_iterm_list[i][j].name;
    //         iterm &ref = city_iterm_list[i][j];
    //         printf("(%d,%d)",ref.id,ref.send_date);
    //     }
    //     cout<<endl;
    // }

    // sort_iterm_in_city();
    // cout<<endl<<endl<<endl;

    // for(int i = 0; i< city_iterm_list.size(); i++){
    //     printf("City(%d):",i);
    //     for(int j = 0; j<city_iterm_list[i].size(); j++){
    //         printf("--->");
    //         cout<<city_iterm_list[i][j].name;iterm &ref = city_iterm_list[i][j];
    //         printf("(%d,%d)",ref.id,ref.send_date);
    //     }
    //     cout<<endl;
    // }

    city_best_alloc(0);
    cout<<city_iterm_list[0].size()<<endl;
    for(int i= 0; i<city_iterm_list[0].size(); i++){
        iterm &ref = city_iterm_list[0][i];
        ref.print_info();
    }


    
}

void city_best_alloc(int idx){
    //initial();
    int normal_dis_time[30],normal_dis_money[30],air_dis[30];
    int NUM = city_iterm_list.size();
    for(int i = 0; i<NUM; i++){
        normal_dis_money[i] = normal_dis_time[i] = air_dis[i] = 1<<30;
    }
    int normal_time[30][30],normal_money[30][30];
    int air_time[30][30],air_money[30][30];
    for(int i =0; i<NUM; i++){
        for(int j= 0; j<NUM; j++){
            air_time[i][j] = city_map.air_map[i][j].time;
            air_money[i][j] = city_map.air_map[i][j].money;
        }
    }
    for(int i =0; i<NUM; i++){
        for(int j= 0; j<NUM; j++){
            normal_time[i][j] = city_map.normal_map[i][j].time;
            normal_money[i][j] = city_map.normal_map[i][j].money;
        }
    }
    //
    
    int air_path[30][30];
    int normal_time_path[30][30];
    int normal_money_path[30][30];
    for(int i = 0; i<30; i++){
        for(int j = 0; j<30; j++){
            air_path[i][j] = normal_time_path[i][j] = normal_money_path[i][j] = -1;
        }
    }

    // for(int i= 0; i<NUM;i++){
    //     for(int j = 0; j<NUM; j++){
    //         cout<<air_money[i][j]<<" ";
    //     }
    //     cout<<endl;
    // }

    dijkstra(air_dis,air_path,idx,air_time,air_money,0,1);
   


    // for(int i = 0; i<NUM; i++){
    //     for(int j = 0; j<NUM; j++){
    //         cout<<air_time[i][j]<<" ";
    //     }cout<<endl;
    // }

    dijkstra(normal_dis_time,normal_time_path,idx,normal_time,normal_money,0,0);
    
    dijkstra(normal_dis_money,normal_money_path,idx,normal_time,normal_money,1,0);

    //iterm analyze;
    for(int i = 0; i<city_iterm_list[idx].size(); i++){
        iterm &ref = city_iterm_list[idx][i];
        int to_addr = ref.to_addr;
        int cnt;
        //air_line;
        ref.air_time = air_dis[to_addr];
        cnt = air_path[to_addr][0];

        ref.air_money = 0;
        for(int j = 1; j<= cnt; j++){
            int next_addr,now_addr;
            now_addr = air_path[to_addr][j];
            if(j+1<=cnt){
                next_addr = air_path[to_addr][j+1];
                ref.air_money += air_money[now_addr][next_addr];
            }
            
            ref.air_path.push_back(air_path[to_addr][j]);
        }
        //done;

        //normal
        //time;
        ref.time_least_time = normal_dis_time[to_addr];
        cnt = normal_time_path[to_addr][0];
        for(int j = 1; j<= cnt; j++){
            int next_addr,now_addr;
            now_addr = normal_time_path[to_addr][j];
            if(j+1<=cnt){
                next_addr = normal_time_path[to_addr][j+1];
            }
            ref.time_least_money += normal_money[now_addr][next_addr];
            ref.normal_path_time.push_back(normal_time_path[to_addr][j]);
        }
        //done;
        //moeny:
        ref.money_least_money = normal_dis_money[to_addr];
        cnt = normal_money_path[to_addr][0];
        for(int j = 1; j<= cnt; j++){
            int next_addr,now_addr;
            now_addr = normal_money_path[to_addr][j];
            if(j+1<=cnt){
                next_addr = normal_money_path[to_addr][j+1];
            }
            ref.money_least_time += normal_time[now_addr][next_addr];
            ref.normal_path_money.push_back(normal_money_path[to_addr][j]);
        }

        
    }
    
}

void dijkstra(int dis[30],int path[30][30],int source,int time[30][30],int money[30][30],int opt,int air){
    
     //dijkstra;
     //opt = 0: time_least; opt = 1: money_least;
    //int dis[10];
    int NUM = city_iterm_list.size();


    bool visit[10];
    int  pre[10];
    for(int i = 0; i<NUM; i++){
        //dis[i] = (1<<30);
        pre[i] = -1;
        visit[i] = false;
    };
    //int source = 0;
    dis[source] = 0;

    while(true){
        
        int id = -1,cur_dis = 1<<30;
        for(int i = 0; i<NUM; i++){
            if(!visit[i]){
                if(cur_dis>dis[i]){
                    id = i;
                    cur_dis = dis[i];
                }
            }
        }
        if(id==-1){ break;}
        visit[id] = true;
        for(int i = 0; i<NUM; i++){
            if(!visit[i]){
                int tmp;
                //*
                if (air ==0){
                    if(opt==0)
                        tmp = cur_dis + time[id][i];
                    else
                        tmp = cur_dis + money[id][i];
                }
                else tmp = cur_dis+time[id][i];

                if(tmp<dis[i]){
                        pre[i] = id;
                        dis[i] = tmp;
                }
            }
        }
    }
    
    //print path:
    // for(int i = 0; i<NUM; i++){
    //     cout<<i<<":"<<dis[i]<<endl;
    // }

    //path[30][30] = matrix{-1} 
    bool first = 1;
    
    for(int cur = 0; cur<NUM; cur++){
        int path2[30],pos = 1;
        //cout<<"Path:";
        //cout<<"hello1"<<cur<<endl;
        int cur_city = cur;
        while(cur_city!=-1){
            path2[pos++] = cur_city;
            cur_city = pre[cur_city];
            
        }
        //cout<<"hello2"<<cur<<endl;
        pos-=1;
        path[cur][0] = pos;
        for(int i = 1;i<=pos; i++){
            path[cur][i] = path2[pos+1-i];
        }
        // if(first){
        //     cout<<"Path:";
        //     for(int i = 1;i<=pos; i++){
        //         cout<<path[cur][i]<<"----->";
        //     }cout<<endl;
        // }
    }
    //cout<<"DONE"<<endl;
    // for(int i = 0; i<pos; i++){
    //     cout<<path[i]<<" ";
    // }cout<<endl;

}





int main(){
    initial_iterm_info();
    initial_city();
    //transport policy:
    int city_size = city_iterm_list.size();
    for(int i = 0; i<city_size; i++){
        city_best_alloc(i);
        cout<<"City("<<i<<"):"<<endl;
        vector<iterm> &it = city_iterm_list[i];
        for(int j = 0; j<it.size(); j++){
            it[j].print_info();
        }
    }

    return 0;
}
