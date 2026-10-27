// Exact bounded-frontier inversion of L(a+D)+L(a)=S modulo 2^w.
// L=ROR(r1) XOR ROR(r2) XOR SHR(s), 0<s<r1<r2<w.
// Exact integer count and witness. Author: lmtlssss🜐. License: MIT.
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
#include <array>
#include <unordered_map>
#include <chrono>
#include <string>
#include <algorithm>
#include <stdexcept>
#include <boost/multiprecision/cpp_int.hpp>
using U=uint64_t; using Big=boost::multiprecision::cpp_int; using Wide=Big;
struct Ans {Wide count=0; Big witness=0; U sum=0,xors=0;};
std::string dec(const Wide& x){return x.str();}
struct Solver {
 int w,r1,r2,sh,h; Big D,S,mask; U hmask,tailA,tailB; int tailCarry;
 bool memoOn,capped=false; uint64_t nodes=0,hits=0,transitions=0,seeds=0,maxNodes;
 std::vector<uint64_t> layers; std::vector<Ans> table; std::vector<uint32_t> stamp; uint32_t generation=0; U stride;
 std::chrono::steady_clock::time_point started; double seconds;
 Solver(int w_,int r1_,int r2_,int s_,Big d,Big s,bool mem,U lim,double sec):w(w_),r1(r1_),r2(r2_),sh(s_),D(d),S(s),memoOn(mem),maxNodes(lim),seconds(sec){
  if(w<3||w>512||!(0<sh&&sh<r1&&r1<r2&&r2<w))throw std::runtime_error("invalid taps/width");
  h=r2-sh;if(h>12)throw std::runtime_error("frontier setup limit: span>12");
  mask=1; mask<<=w; mask-=1;D&=mask;S&=mask;hmask=(U(1)<<h)-1; stride=U(1)<<(h+1); started=std::chrono::steady_clock::now(); if(memoOn){table.resize(w*stride); stamp.resize(w*stride);} layers.resize(w);
 }
 int bit(const Big& v,int j) const {return static_cast<int>((v>>j)&1);}
 int bit(U v,int j) const {return (v>>j)&1;}
 Big rr(const Big& v,int r) const {return ((v>>r)|(v<<(w-r)))&mask;}
 Big L(const Big& v)const{return rr(v,r1)^rr(v,r2)^(v>>sh);}
 int prev(U hist,int distance)const{return (hist>>(distance-1))&1;}
 int linearBit(int i,int cur,U hist)const{
  int out=cur^prev(hist,r2-r1);
  if(i+sh<w)out^=prev(hist,h);
  return out;
 }
 Ans visit(int j,U ah,U bh,int tin){
  if(capped)return {};
  if(j==w)return {1,0};
  // For j<h, the initial tail is fixed and ah names every assigned prefix.
  // For j>=h, a history plus the carry ENTERING that history determines
  // the whole b history and current carry. The oldest difference recovers it.
  int leftCarry=j<h?0:(prev(ah^bh,h)^bit(D,j-h));
  U key=U(j)*stride+ah+(U(leftCarry)<<h);
  if(memoOn && stamp[key]==generation){hits++;return table[key];}
  nodes++;layers[j]++;
  if(nodes>maxNodes || ((nodes&4095)==0 && std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count()>seconds)){capped=true;return {};}
  int i=(j-r2+w)%w;
  int delta=bit(D,j)^tin;
  int carry=bit(S,i)^linearBit(i,delta,ah^bh);
  if(i==0 && carry!=0){if(memoOn){stamp[key]=generation;table[key]={};}return {};}
  Ans result;
  bool tail=(j>=w-h);
  int first=tail?bit(tailA,j-(w-h)):0,last=tail?first:1;
  for(int av=first;av<=last;av++){
   transitions++;
   int total=av+bit(D,j)+tin,bv=total&1,tout=total>>1;
   if(j+1==w-h && tout!=tailCarry)continue;
   if(tail && bv!=bit(tailB,j-(w-h)))continue;
   int x=linearBit(i,av,ah),y=linearBit(i,bv,bh);
   int outCarry=(x+y+carry)>>1;
   U an=((ah<<1)|U(av))&hmask,bn=((bh<<1)|U(bv))&hmask;
   if(i!=w-1){
    int jn=(j+1)%w,tn=(j==w-1?0:tout);
    int dn=bit(D,jn)^tn;
    int cn=bit(S,i+1)^linearBit(i+1,dn,an^bn);
    if(outCarry!=cn)continue;
   }
   Ans child=visit(j+1,an,bn,tout);
   if(child.count){if(!result.count)result.witness=child.witness|(Big(av)<<j);result.count+=child.count; U bitv=j<64?(U(av)<<j):0; result.sum+=child.sum+static_cast<U>(child.count & ((Big(1)<<64)-1))*bitv; result.xors^=child.xors^((child.count&1)?bitv:0);}
   if(capped)break;
  }
  if(memoOn&&!capped){stamp[key]=generation;table[key]=result;}
  return result;
 }
 Ans solve(){
  Ans sum;
  for(U tail=0;tail<(U(1)<<h)&&!capped;tail++)for(int tc=0;tc<2&&!capped;tc++){
   tailA=tail;tailCarry=tc;tailB=0;int t=tc;
   for(int k=0;k<h;k++){int q=bit(tail,k)+bit(D,w-h+k)+t;tailB|=U(q&1)<<k;t=q>>1;}
   U ah=0,bh=0;
   for(int k=0;k<h;k++){ah=((ah<<1)|U(bit(tailA,k)))&hmask;bh=((bh<<1)|U(bit(tailB,k)))&hmask;}
   generation++;
   seeds++;
   Ans cur=visit(0,ah,bh,0);
   if(cur.count){if(!sum.count)sum.witness=cur.witness;sum.count+=cur.count; sum.sum+=cur.sum;sum.xors^=cur.xors;}
  }
  return sum;
 }
};
int main(int argc,char**argv){try{
 if(argc<7)throw std::runtime_error("width r1 r2 shift D S [memo=1] [maxnodes=20000000] [seconds=5]");
 int w=atoi(argv[1]),r1=atoi(argv[2]),r2=atoi(argv[3]),sh=atoi(argv[4]);Big D(argv[5]),S(argv[6]);bool mem=argc>7?atoi(argv[7]):1;U lim=argc>8?std::stoull(argv[8]):20000000;double sec=argc>9?std::stod(argv[9]):5;
 Solver f(w,r1,r2,sh,D,S,mem,lim,sec);Ans a=f.solve();double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-f.started).count();
 bool check=!a.count || (((f.L((a.witness+D) & f.mask)+f.L(a.witness))&f.mask)==f.S);
 std::cout<<"{\"width\":"<<w<<",\"D\":"<<f.D<<",\"S\":"<<f.S<<",\"complete\":"<<(f.capped?"false":"true")<<",\"count\":\""<<dec(a.count)<<"\",\"witness\":"<<a.witness<<",\"sum_mod64\":"<<a.sum<<",\"xor\":"<<a.xors<<",\"witness_checked\":"<<(check?"true":"false")<<",\"nodes\":"<<f.nodes<<",\"cache_hits\":"<<f.hits<<",\"transitions\":"<<f.transitions<<",\"seeds\":"<<f.seeds<<",\"seconds\":"<<elapsed<<",\"layer_nodes\":[";
 for(int i=0;i<w;i++){if(i)std::cout<<',';std::cout<<f.layers[i];}std::cout<<"]}\n";
 return check?0:2;
 }catch(std::exception&e){std::cerr<<e.what()<<"\n";return 1;}}
