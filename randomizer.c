#include <stdlib.h>
#include <time.h>

#define HIGHEST 2147483647

void seed_rng() { srand((unsigned int)time(NULL)); }

float rand_float(float min, float max) {
  return min + ((float)rand() / HIGHEST) * (max - min);
}

int rand_int(int min, int max) {
  return min + ((int)rand() / HIGHEST) * (max - min);
}
