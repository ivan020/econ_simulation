#include "const.c"
#include <stdio.h>
#include <string.h>

#define MAXTYPEA 7
#define H 10

struct Household {
  int name;
  float wealth;
  float m;
  int typeA[MAXTYPEA];
  int typeB[];
};
