// Direct complete-fiber oracle for the declared widths and tap sets.
#define main archived_frontier_cli
#include "frontier.cpp"
#undef main
int main() {
 uint64_t queries=0, evaluations=0;
 for(int w=4;w<=7;w++) {
  int r1=w==4?2:3, r2=w==4?3:4, sh=1;
  uint64_t mask=(uint64_t(1)<<w)-1;
  auto rot=[&](uint64_t x,int r){return ((x>>r)|(x<<(w-r)))&mask;};
  auto linear=[&](uint64_t x){return rot(x,r1)^rot(x,r2)^(x>>sh);};
  for(uint64_t D=0;D<=mask;D++) {
   std::vector<uint64_t> counts(mask+1,0);
   for(uint64_t a=0;a<=mask;a++) {
    counts[(linear((a+D)&mask)+linear(a))&mask]++; evaluations++;
   }
   for(uint64_t S=0;S<=mask;S++) {
    Solver solver(w,r1,r2,sh,Big(D),Big(S),true,20000000,5);
    Ans got=solver.solve(); queries++;
    if(solver.capped || got.count!=counts[S]) return 1;
   }
  }
 }
 std::cout << "{\"complete_fibers\":" << queries << ",\"direct_evaluations\":"
           << evaluations << ",\"all_equal\":true}\n";
}
