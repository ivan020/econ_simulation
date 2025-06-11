#include <stdlib.h>
#include <time.h>

void seed_rng() { srand((unsigned int)time(NULL)); }

float rand_float(float min, float max) {
  return min + ((float)rand() / RAND_MAX) * (max - min);
}
