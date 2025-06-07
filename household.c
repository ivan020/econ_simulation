#include "const.c"
#include <stdio.h>
#include <string.h>

#define MAXTYPEA 7

struct Household {
  int name;
  float wealth;
  float m;
  int typeA[MAXTYPEA];
};
