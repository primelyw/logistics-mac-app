#include <iostream>
#include <string>
#include <vector>
using namespace std;
int main()
{
    vector<int> a;
    for(int i = 0; i<10; i++) a.push_back(i);
    for(int i = 0; i<10; i++){
        cout<<a[i]<<" ";
    }cout<<endl;
    vector<int>::iterator  itt;
    for(auto it = a.begin(); it!=a.end();++it){
        if(*it==2){
            itt = it;
        }
    }
    a.erase(a.begin()+2);
    a.pop_back();
    for(int i = 0; i<a.size(); i++){
        cout<<a[i]<<" ";
    }cout<<endl;
    return 0;

}