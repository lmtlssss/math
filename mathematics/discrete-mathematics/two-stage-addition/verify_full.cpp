// Complete operand-domain comparison. Author lmtlssss🜐. License MIT.
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <unordered_set>
#include <vector>
static const unsigned mid[5]={0,85,165,170,255};
static const unsigned pen[3]={64,229,234},last[3]={84,164,254};
static unsigned code(unsigned B,unsigned C,unsigned S,unsigned H){
 unsigned x=C+S,r=x%B,v=(r+H)%B;
 if(v<B-2){unsigned t=r==B-1?2:((x/B)?3+(r+H)/B:(r+H)/B);return 5*v+t;}
 unsigned t=r==B-1?1:2*(x/B);return 5*(B-2)+3*(v-(B-2))+t;
}
static std::pair<unsigned,unsigned> decode(unsigned B,unsigned id){
 unsigned cut=5*(B-2);
 if(id<cut)return {id/5,mid[id%5]};
 unsigned t=id-cut;return {B-2+t/3,t<3?pen[t]:last[t-3]};
}
int main(){
 try{
  std::cout<<"{\"status\":\"PASS\",\"domains\":[";
  for(unsigned w=1;w<=8;w++){
   unsigned B=1u<<w,N=5*B-4;std::vector<uint64_t> keys(N,~uint64_t(0));
   std::vector<uint64_t> count(N,0);std::array<uint64_t,5> rank{};
   for(unsigned C=0;C<B;C++)for(unsigned S=0;S<B;S++)for(unsigned H=0;H<B;H++){
    unsigned id=code(B,C,S,H);auto [v,map]=decode(B,id);uint64_t key=0;unsigned seen=0;
    for(unsigned a=0;a<2;a++)for(unsigned b=0;b<2;b++){
     unsigned u=C+S+a,ca=u/B,z=(u%B)+H+b,cb=z/B,res=z%B,index=2*a+b;
     unsigned pred=(map>>(2*index))&3;
     if((v+a+b)%B!=res || pred!=2*ca+cb)throw std::runtime_error("whole-function mismatch");
     key|=uint64_t(4*res+2*ca+cb)<<((w+2)*index);seen|=1u<<(2*ca+cb);
    }
    if(keys[id]!=~uint64_t(0) && keys[id]!=key)throw std::runtime_error("merged distinct functions");
    keys[id]=key;count[id]++;rank[__builtin_popcount(seen)]++;
   }
   std::unordered_set<uint64_t> unique(keys.begin(),keys.end());
   if(unique.size()!=N || unique.count(~uint64_t(0)))throw std::runtime_error("class census failed");
   if(rank[1]!=uint64_t(B)*(B-1)*(B-2)||rank[2]!=3ull*B*B-4ull*B||rank[3]!=2ull*B||rank[4])throw std::runtime_error("carry distribution failed");
   if(w>1)std::cout<<",";
   std::cout<<"{\"width\":"<<w<<",\"triples\":"<<(uint64_t(B)*B*B)<<",\"classes\":"<<N<<",\"carry_image_histogram\":["<<rank[1]<<","<<rank[2]<<","<<rank[3]<<","<<rank[4]<<"]}";
  }
  std::cout<<"]}\n";
 }catch(const std::exception& e){std::cerr<<e.what()<<"\n";return 1;}
}
