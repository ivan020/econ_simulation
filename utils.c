/*
 * a set of utilities funcitons
 */

#include <stdio.h>

void print_list(int *array, int array_len) {
  // in case we work with arrays
  for (int i = 0; i < array_len; i++) {
    printf(" %d", array[i]);
  }
  printf("\n");
}
