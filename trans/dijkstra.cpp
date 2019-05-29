#include <iostream>
#include <algorithm>
#include <fstream>
using namespace std;
#define NUM 7

int main(){
    ifstream file("t.txt");
    int map[10][10];
    if(file.is_open()){
        for(int i = 0; i<NUM; i++){
            for(int j = 0; j<NUM; j++){
                int tmp;
                file>>tmp;
                if(i!=j&&tmp==0) tmp = 1<<30;
                map[i][j] = tmp;
            }
        }
    }
    

    for(int i = 0; i<NUM; i++){
        for(int j = 0;j<NUM; j++){
            cout<<map[i][j]<<" ";
        }cout<<endl;
    }

    

    //dijkstra;
    int dis[10];
    bool visit[10];
    int  pre[10];
    for(int i = 0; i<NUM; i++){
        dis[i] = (1<<30);
        pre[i] = -1;
        visit[i] = false;
    };
    int source = 0;
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
                int tmp = cur_dis + map[id][i];
                if(tmp<dis[i]){
                    pre[i] = id;
                    dis[i] = tmp;
                }
            }
        }
    }

    //print path:
    for(int i = 0; i<NUM; i++){
        cout<<i<<":"<<dis[i]<<endl;
    }

    int cur = 4;
    int path2[10],path[10],pos = 0;
    cout<<"Path:";
    path2[pos++] = cur;
    while(pre[cur]!=-1){
        path2[pos++] = pre[cur];
        cur = pre[cur];
    }
    for(int i = 0;i<pos; i++){
        path[i] = path2[pos-1-i];
    }
    for(int i = 0; i<pos; i++){
        cout<<path[i]<<" ";
    }cout<<endl;




    return 0;
}