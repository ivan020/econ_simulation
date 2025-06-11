#include "const.c"
#include "randomizer.c"
#include <stdio.h>
#include <string.h>
#define MAXTYPEA 7
#define H 10

struct Household {
  int name;
  float wealth;
  float m;
  int typeA[MAXTYPEA];
};

typedef struct Household Household;

void populate_household(Household *household, int name, float w, float m) {

  household->name = name;
  household->wealth = w;
  household->m = m;

  for (int i = 0; i < MAXTYPEA; i++) {
    household->typeA[i] = -1;
  }
}

int main(void) {

  Household h[H];

  for (int i = 0; i < H; i++) {
    float gen_wealth = rand_float(0.0, 1.0);
    float m = rand_float(0.01, 0.02);
    populate_household(&h[i], i + 1, gen_wealth, m);
  }

  for (int i = 0; i < H; i++) {

    printf("household name->%d\n", h[i].name);
  }
}
