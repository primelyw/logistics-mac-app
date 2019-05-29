#include <unistd.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <string>

using namespace std;

typedef struct UNIT{
    int type;
    string val;
    UNIT(int x = -1,string y = ""){
        type = x,val = y;
    }
}UNIT;

typedef struct REQ_UNIT{
    string val;
    string key;
    REQ_UNIT(string k,string v){
        val = v;
        key = k;
    }
}REQ_UNIT;

typedef struct LOG{
    vector<UNIT> v;
}LOG;
typedef struct COL{
    vector<UNIT> v;
}COL;



typedef struct COLUMN{
    int type;
    string name;
    int log_sz;
    vector<int> int_log;
    vector<string> str_log;
    COLUMN(int x=0,string y="NO_NAME"){
        type=x;
        name = y;
        log_sz = 0;
    }

    void set_name(string s){
        name = s;
    }
    
    void add_log(string s){
        str_log.push_back(s);
        log_sz ++;
    }
    void add_log(int x){
        int_log.push_back(x);
        log_sz++;
    }

}COLUMN;



class TABLE{
public:
    vector<COLUMN>col;
    string name;
    int col_sz,log_sz;

    TABLE(string nam = "NO_NAME"){
        col = vector<COLUMN>(0);
        name = nam;
        col_sz = log_sz = 0;
    }

    void clear(){
        col_sz = log_sz = 0;
        name = "NO_NAME";
        col = vector<COLUMN>(0);
    }

    int delete_log(int idx){
        if(idx>=log_sz) return 0;
        for(int i = 0; i<col_sz; i++){
            if(col[i].type==0){
                col[i].int_log.erase(col[i].int_log.begin()+idx);
            }
            else{
                col[i].str_log.erase(col[i].str_log.begin()+idx);
            }
        }
        log_sz --;
        return 1;
    }

    void print_info(){
        cout<<"------"<<name<<"------"<<endl;
        cout<<"NUM"<<"\t";
        for(int i = 0; i<col.size(); i++){
            cout<<col[i].name<<"\t";
        }cout<<endl;
        for(int i = 0; i<log_sz; i++){
            cout<<i<<"\t";
            for(int j = 0; j<col.size(); j++){
                if(col[j].type ==0){
                    cout<<col[j].int_log[i]<<"\t";
                }
                else if(col[j].type ==1){
                    cout<<col[j].str_log[i]<<"\t";
                }
            }cout<<endl;
        }
    }

    void set_column(vector<UNIT> column){
        for(int i = 0; i<column.size(); i++){
            UNIT &ref = column[i];
            col.push_back(COLUMN(ref.type,ref.val));
        }
        col_sz = col.size();
    }

    int add_log(vector<UNIT> log){
        //0: success
        //-1: fail
        bool ok = true;
        if (log.size()!=col.size()) ok  = false;
        for(int i = 0; i<log.size();i++){
            if(log[i].type!=col[i].type){
                ok = false;
                break;
            }
        }
        if(!ok) return -1;
        for(int i = 0; i<log.size(); i++){
            UNIT &ref = log[i];
            if(ref.type==0){
                int tmp = stoi(ref.val);

                col[i].add_log(tmp);
            }
            else if(ref.type==1){
                col[i].add_log(ref.val);
            }
        }
        log_sz ++;

        return 0;
    }
    
    
};

string get_suffix(string s,string pre){
    int pre_len = pre.length();
    int pos = s.find(pre);
    int all_len = s.length();
    int len = all_len - pre_len;
    pos += pre_len;
    string left = s.substr(pos,len);
    return left;
}


class SHEET{
public:
    string sheet_name;
    vector<TABLE> table_list;
    SHEET(string fname){
        sheet_name = fname;
    }    

    int create_table(string tbname){
        TABLE tb;
        tb.name = tbname;
        table_list.push_back(tb);
        return 1;
    }

    

    int have_table(string tb_name){
        int tb_idx = -1;
        for(int i = 0; i<table_list.size(); i++){
            if(table_list[i].name == tb_name){
                tb_idx = i;
            }
        }
        return tb_idx;
    }

    int delete_table(string tb_name){
        int idx = have_table(tb_name);
        if(idx==-1){
            cout<<"NO such a table"<<endl;
            return 0;
        }
        TABLE &tb = table_list[idx];
        tb.clear();
        return 1;
    }

    int print_table(string tb_name){
        int tb_idx = have_table(tb_name);
        if(tb_idx==-1){
            cout<<"NO such a table <"<<tb_name<<">"<<endl;

            return 0;
        }
        else{
            table_list[tb_idx].print_info();
            return 1;
        }
    }

    int set_column(string tb_name,vector<UNIT> col){
        int tb_idx = have_table(tb_name);
        if(tb_idx!=-1){
            TABLE &tb = table_list[tb_idx];
            tb.set_column(col);
            return 1;
        }
        else return 0;
        
    }

    int add_log(string tb_name,vector<UNIT>log){
        int tb_idx = have_table(tb_name);
        if(tb_idx!=-1){
            TABLE &tb = table_list[tb_idx];
            int res = tb.add_log(log);
            return res;
        }
        else return 0;
    }

    vector<vector<UNIT> > search_log(string tb_name,vector<REQ_UNIT> request,int opt){
        // opt:
        //0:for search to print;
        //1: search to delete;
        vector<vector<UNIT> > log_list;

        int tb_idx = have_table(tb_name);
        if(tb_idx==-1){
            cout<<"No such a table!"<<endl;
            return log_list;
        }
        bool get = true;
        TABLE &tb = table_list[tb_idx];
        vector<int> pos;
        for(int i = 0; i<request.size(); i++){
            bool sub_get = false;
            for(int j = 0; j<tb.col_sz;j++){
                if(tb.col[j].name == request[i].key){
                    sub_get  = true;
                    pos.push_back(j);
                    break;
                }
            }
            if(!sub_get){
                get = false;
            }
        }
        if(!get){
            cout<<"Some COL_NAME is not right in the table<"<<table_list[tb_idx].name<<">"<<endl;
            return log_list;
        }

        
        for(int i = 0; i<tb.log_sz; i++){
            vector<UNIT> tmp_log;
            
            for(int j = 0; j<tb.col_sz;j++){
                UNIT tmp_unit;
                tmp_unit.type = tb.col[j].type;
                if(tb.col[j].type == 0){
                    tmp_unit.val = tb.col[j].int_log[i];
                }
                else{
                    tmp_unit.val = tb.col[j].str_log[i];
                }
                tmp_log.push_back(tmp_unit);
                //check request;
                //tmp_log.push_back(UNIT(tb.col[j].type,tb.col[j].))
            }
            bool ok = true;
            for(int j = 0; j<pos.size(); j++){
                int idx = pos[j];
                string cmp; 
                if(tb.col[idx].type==1){
                    cmp = tb.col[idx].str_log[i]; 
                }
                else{
                    cmp = to_string(tb.col[idx].int_log[i]);
                }
                if(cmp!=request[j].val){
                    ok = false;
                }
            }
            if(ok){
                log_list.push_back(tmp_log);
            }
        }
        
        //print all searched logs
        if(opt == 0){
            cout<<"Search successfully!"<<endl;
            cout<<"------------------------"<<endl;
            for(int i = 0; i<log_list.size(); i++){
                for(int j = 0; j<log_list[i].size(); j++){
                    cout<<log_list[i][j].val<<"\t";
                }cout<<endl;
            }
            cout<<"------------------------"<<endl;
            cout<<"Done!"<<endl;
        }
        return log_list;
    }

    int delete_log(string tb_name,vector<REQ_UNIT> request){
        
        vector<vector<UNIT> > log_list = search_log(tb_name,request,1);
        cout<<"Delete debug:"<<endl;
        cout<<log_list.size()<<endl;
        for(int i = 0; i<log_list.size(); i++){
            for(int j = 0; j<log_list[i].size(); j++){
                cout<<log_list[i][j].val<<"\t";
            }cout<<endl;
        }

        if(log_list.size()==0){
            cout<<"Bad thing happened!\n";
            cout<<"1).No such a record in the table\n";
            cout<<"2).No such a table in the sheet\n";
            cout<<"3).Some thing wrong in the delete request\n";
            return 0;
        }
        int tb_idx = have_table(tb_name);
        TABLE &tb = table_list[tb_idx];
        //cout<<"debug"<<log_list.size()<<endl;   

        for(int k = 0; k<log_list.size(); k++){
            vector<UNIT> log = log_list[k];
            int idx = 0;
            
            while(idx<tb.log_sz){
                
                bool ok = true;
                for(int i = 0; i<tb.col_sz; i++){
                    string cmp;
                    if(tb.col[i].type==0){
                        cmp = to_string(tb.col[i].int_log[idx]);
                    }
                    else{
                        cmp = tb.col[i].str_log[idx];
                    }
                    if(cmp!=log[i].val) ok = false;
                    //
                }
                
                if(ok){
                    //cout<<"GOt"<<endl;
                    break;
                }
                idx++;
            }
            tb.delete_log(idx);
        }


        return 1;
        
    }


    int import_table(string fname){
        ifstream fin(fname);
        string line;
        TABLE tb;
        if(fin.is_open()){
            while(getline(fin,line)){
                if(line=="TABLE_BEGIN"){
                    tb.clear();
                }
                else if(line=="TABLE_END"){
                    table_list.push_back(tb);
                    //cout<<"debug"<<endl;
                }
                else if(line.find("NAME:\t")==0){
                    int pos = line.find("NAME:\t");
                    int all_len = line.length();
                    int len = all_len - 6;
                    pos += 6;
                    string name = line.substr(pos,len);
                    tb.name = name;
                    //cout<<"NAME:"<<name<<endl;
                }

                else if(line.find("SIZE:\t")==0){
                    int pos;
                    string ran = get_suffix(line,"SIZE:\t");
                    //cout<<ran<<endl;
                    string cnt_n;
                    string cnt_m;
                    int n_cnt = -1;
                    int m_cnt = -1;
                    pos = 0;
                    bool first = true;
                    while(true){
                        char cur = ran[pos++];
                        if(cur == '\x00'){
                            m_cnt = stoi(cnt_m);
                            break;
                        }
                        else if(cur == ','){
                            first = false;
                            n_cnt = stoi(cnt_n);
                        }
                        else{
                            if(first){
                                cnt_n += cur;
                            }
                            else{
                                cnt_m += cur;
                            }
                        }
                    }
                    tb.log_sz = n_cnt;
                    tb.col_sz  = m_cnt;
                    //cout<<"SIZE:"<<n_cnt<<","<<m_cnt<<endl;
                }
                else if(line.find("TYPE:\t")==0){
                    int pos;
                    string left = get_suffix(line,"TYPE:\t");
                    for(int i = 0; i<left.length(); i+=2){
                        int ty = (int)left[i]-'0';
                        tb.col.push_back(COLUMN(ty));
                    }
                    //cout<<"debug"<<endl;
                }
                else if(line.find("COL:\t")==0){
                    //store col_name;
                    int pos;
                    //cout<<"LINE:"<<line<<endl;
                    string left = get_suffix(line,"COL:\t");
                    //cout<<"COL_NAME:  "<<left<<endl;
                    string tmp;
                    pos = 0;
                    int col_cnt = 0;
                    while(true){
                        char cur = left[pos++];
                        if(cur=='\t'){
                            tb.col[col_cnt++].set_name(tmp);
                            //cout<<tmp<<"\t";
                            tmp.clear();
                        }
                        else if(cur=='\x00'){
                            break;
                        }
                        else{
                            tmp += cur;
                        }
                    }
                    //cout<<"debug"<<endl;

                }
                else{
                    //store log;
                    int pos = 0;
                    int col_cnt = 0;
                    string tmp;
                    while(true){
                        char cur = line[pos++];
                        if(cur == '\t'){
                            if(tb.col[col_cnt].type==0){
                                tb.col[col_cnt].int_log.push_back(stoi(tmp));
                            }
                            else{
                                tb.col[col_cnt].str_log.push_back(tmp);
                            }
                            col_cnt ++;
                            //cout<<"debug"<<tmp<<"\t";
                            tmp.clear();
                        }
                        else if(cur == '\x00') break;
                        else{
                            tmp += cur;
                        }
                    }
                    //cout<<endl;
                }
            }
            // cout<<table_list.size()<<endl;
            // for(int i = 0; i<table_list.size(); i++){
            //     table_list[i].print_info();
            // }
            
            return 1;
        }
        else{
            cout<<"Can't open file "<<sheet_name<<endl;
            return 0;
        }

    }    

    int export_table(string fname){
        ofstream fout(fname);
        if(fout.is_open()){
            for(int ti = 0; ti<table_list.size(); ti++){
                TABLE &tb = table_list[ti];
                //cout<<"debug"<<endl;
                //tb.print_info();

                fout<<"TABLE_BEGIN\nNAME:\t"<<tb.name<<"\n";
                fout<<"SIZE:\t"<<tb.log_sz<<","<<tb.col_sz<<endl;

                fout<<"TYPE:\t";
                for(int i =0; i< tb.col_sz; i++){
                    fout<<tb.col[i].type<<"\t";
                }fout<<endl;

                fout<<"COL:\t";
                for(int i =0; i< tb.col_sz; i++){
                    fout<<tb.col[i].name<<"\t";
                }fout<<endl;

                for(int log= 0; log<tb.log_sz;log++){
                    for(int i = 0; i<tb.col_sz; i++){
                        if(tb.col[i].type ==0){
                            fout<<tb.col[i].int_log[log]<<"\t";
                        }
                        else{
                            fout<<tb.col[i].str_log[log]<<"\t";
                        }
                    }
                    fout<<endl;
                }
                fout<<"TABLE_END"<<endl;
            }
            fout.close();
            return 1;
        }
        else{
            cout<<"Fail to open "<<sheet_name<<endl;
            return 0;
        }

    }
};

void create_a_table(SHEET sh){
    string tb_name;
    cout<<"table name:";
    cin>>tb_name;
    sh.create_table(tb_name);
    cout<<"Successfully!";
    cout<<endl<<endl;

    vector<UNIT> col;
    cout<<"set column"<<endl;
    cout<<"number of column:"<<endl;
    int num;cin>>num;
    for(int i = 0; i<num; i++){
        int ty;string nam;
        cout<<"type:";cin>>ty;
        cout<<"column name:";cin>>nam;
        col.push_back(UNIT(ty,nam));
    }
    sh.set_column(tb_name,col);
}

void add_a_log(SHEET sh){
    return;
}
void search_a_log(SHEET sh){
    return;
}
void delete_a_log(SHEET sh){
    return;
}
void import_tables(SHEET sh){
    return;
}

void export_tables(SHEET sh){
    return;

}



void login(){
    cout<<"User name:";
    string name;
    string passwd;
    cin>>name;
    cout<<"pwd:";
    cin>>passwd;
    if(!(name=="root"&&passwd=="root")){
        cout<<"Login Fail!";
        return ;
    }

    SHEET sheet(name);
    
    while(true){
        int opt;
        //menu;
        cout<<"1.create a table"<<endl;
        cout<<"2.add a log"<<endl;
        cout<<"3.search a log"<<endl;
        cout<<"4.delete a log"<<endl;
        cout<<"5.import tables from a file"<<endl;
        cout<<"6.export tables to a file"<<endl;
        cout<<"7.exit"<<endl;
        cin>>opt;
        
        switch(opt){
            case 1:
                create_a_table(sheet);
                break;
            default:
                break;
                
        }
    }

}

void test(){

    SHEET sheet = SHEET("prime");
    sheet.import_table("new_db2.txt");
    //sheet.print_table("PERSON");

    sheet.create_table("CNSS");
    vector<UNIT>col;
    col.push_back(UNIT(1,"ID"));
    col.push_back(UNIT(1,"DIR"));
    sheet.set_column("CNSS",col);

    vector<UNIT>log;
    log.push_back(UNIT(1,"yype"));
    log.push_back(UNIT(1,"Bin"));
    sheet.add_log("CNSS",log);
    
    log.clear();
    log.push_back(UNIT(1,"primelee"));
    log.push_back(UNIT(1,"Web"));
    sheet.add_log("CNSS",log);

    log.clear();
    log.push_back(UNIT(1,"N0rth3y"));
    log.push_back(UNIT(1,"Web"));
    sheet.add_log("CNSS",log);
    sheet.print_table("CNSS");


    sheet.export_table("new_db.txt");





    // //sheet.print_table("PERSON");

    // REQ_UNIT req = REQ_UNIT("DIR","Web");
    // vector<REQ_UNIT> req_list;// = {REQ_UNIT("DIR","Web"),REQ_UNIT("ID","primelee")};
    // req_list.push_back(req);
    // //req_list.push_back(REQ_UNIT("DIR","Web"));
    // sheet.search_log("CNSS",req_list,0);
    // sheet.print_table("CNSS");
    
    // sheet.export_table("new_db.txt");

}


int main(){
    login();
    return 0;
}