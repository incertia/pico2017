#include <stdio.h>

int main(int argc, char **argv)
{
  int x;
  int sp[8];
  int regs[32];

  if (argc != 2) {
    puts("give int");
    return 0;
  }

  regs[0] = 0;
  x = *(int *)argv[1];
  printf("got: %8x\n", x);
  regs[4] = x;
  sp[7] = regs[31];
  sp[6] = regs[16];
  regs[6] = -16777216;
  regs[6] = regs[4] & regs[6];
  regs[16] = 16711680;
  regs[16] = regs[4] & regs[16];
  regs[7] = regs[4] & 0xff00;
  regs[4] = regs[4] & 0xff;
  regs[3] = regs[6] >> 24;
  regs[2] = regs[0];
L3:
  regs[5] = regs[2] < 13 ? 1 : 0;
  regs[2] = regs[2] + 1;
  if (regs[5] == regs[0]) goto L2;
  regs[3] = regs[3] - 13;
  goto L3;
L2:
  regs[3] = regs[3] - 6;
  regs[5] = regs[3] << 24;
  regs[16] = regs[16] >> 16;
  regs[2] = regs[16] - 81;
  regs[8] = regs[2] << 6;
  regs[3] = regs[2] << 8;
  regs[3] = regs[3] - regs[8];
  regs[3] = regs[2] - regs[3];
  regs[7] = regs[7] >> 8;
  regs[2] = regs[4] << 1;
  regs[2] = regs[2] + 3;
  regs[3] = regs[3] << 16;
  if (regs[7] != regs[2]) goto L7;
  regs[2] = 94;
  goto L4;
L7:
  regs[2] = 165;
L4:
  regs[2] = regs[2] - 94;
  regs[2] = regs[2] << 8;
  regs[6] = (signed)((unsigned)regs[6] >> 24);
  regs[16] = regs[6] - regs[16];
  regs[4] = regs[4] - regs[16];
  regs[3] = regs[5] + regs[3];
  regs[3] = regs[2] + regs[3];
  regs[16] = regs[4] + regs[3];
  if (regs[16] != 0) goto L5;
  puts("yay");
  goto L9;
L5:
  puts("nay");
L9:
  return 0;
}
