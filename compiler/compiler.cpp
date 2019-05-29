
/*

keywords = ["create","table","insert","into","display","select","where","update","from","set","values","and","all"]
operator = ["=",">=","<=","<",">","{","}","(",")",";",",","*"]
type= ["int","string"]
literal = [numbers]
identity


*/
#define IDENTITY 0

#define CREATE 1
#define TABLE 2
#define INSERT 3
#define INTO 4
#define DISPLAY 5
#define SELECT 6
#define WHERE 7
#define UPDATE 8
#define FROM 9
#define SET 10
#define VALUES 11
#define AND 12
#define ALL 13

#define EQ 14
#define LP 15
#define RP 16
#define SLP 17
#define SRP 18
#define SEMICOM 19
#define COM 20
#define GE 21
#define LE 22
#define GT 23
#define LT 24



#include <iostream>
#include <iterator>
#include <string>
#include <regex>
using namespace std;


typedef struct _attr{
    int type;
    string val;
}attr;

vector<string> word_analyse(string line){
    vector<string> word;
    string sep = "{},();*";
    return word;

}
 
int main()
{
    string s = "create table CNSS { ID string, DIR string};";
 
    // std::regex self_regex("REGULAR EXPRESSIONS",
    //         std::regex_constants::ECMAScript | std::regex_constants::icase);
    // if (std::regex_search(s, self_regex)) {
    //     std::cout << "Text contains the phrase 'regular expressions'\n";
    // }
 
    std::regex word_regex("[a-zA-Z]*[c][a-zA-Z]*");
    auto words_begin = 
        std::sregex_iterator(s.begin(), s.end(), word_regex);
    auto words_end = std::sregex_iterator();
 
    std::cout << "Found "
              << std::distance(words_begin, words_end)
              << " words\n";
 
    const int N = 0;
    std::cout << "Words longer than " << N << " characters:\n";
    for (std::sregex_iterator i = words_begin; i != words_end; ++i) {
        std::smatch match = *i;
        std::string match_str = match.str();
        if (match_str.size() > N) {
            std::cout << "  " << match_str << '\n';
        }
    }
 
    std::regex long_word_regex("(\\w{7,})");
    std::string new_s = std::regex_replace(s, long_word_regex, "[$&]");
    std::cout << new_s << '\n';
}