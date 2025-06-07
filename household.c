#include "const.c"
#include <stdio.h>
#include <string.h>

struct Household {
  float wealth;
  float m;
  char typeA[];
  char name[];
};
