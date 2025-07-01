
#include "firms.c"
#include "household.c"
#include "randomizer.c"

#define nDays 21
#define H 10
#define F 3
#define B 1

Household households[H];
Firm firms[F];

void generate_households(void) {
  // generate H households to be stored as arrays
  for (int i = 0; i < H; i++) {
    float gen_wealth = rand_float(0.0, 1.0);
    float m = rand_float(0.01, 1.0);
    float c = rand_float(0.01, 1.0);
    populate_household(&households[i], i + 1, gen_wealth, m, c);
  }
}

void generate_firms(void) {
  // generate F firms to be stored as arrays
  for (int i = 0; i < F; i++) {
    float gen_wealth = rand_float(0.0, 1.0);
    float initial_production = rand_float(0.015, 0.002);
    float intial_inv = (float)rand_int(1, 10);
    populate_firm();
  }
}
