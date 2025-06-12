/*
 * Household is the largest population in our simulation;
 *  -> defines the structure;
 *  -> initial seeding function;
 *  -> households have at max HHRELATIONS relations with firms and banks;
 */
#include "const.c"
#include "randomizer.c"
#include <stdio.h>
#define TRUE 1
#define FALSE 0
#define HHRELATIONS 4
#define MAXTYPEA 7
#define MAXTYPEB 7
#define MAXTYPEC_R 7
#define MAXTYPED_R 7
#define H 10

struct Household {
  int name;
  int risk_profile;
  int employed; // employment flag;

  float wealth;
  float m;        // idk
  float c;        // consumption
  float dividend; // dividend
  float alpha;    // idk again
  float P;        // idk again
  float loan;
  float deposit;
  float rate_on_deposit;
  float deposited_funds;
  float loan_rate;
  float loan_capacity;
  float serviceable_loan;

  int typeA[MAXTYPEA];
  int typeB[MAXTYPEB];
  int typeC_R[MAXTYPEC_R];
  int typeD_R[MAXTYPED_R];
};

typedef struct Household Household;

// some  debugging functions
void print_household(Household *household);
void print_household_parameters(Household *household);

void populate_household(Household *household, int name, float w, float m) {
  // function to generate the household data point
  int i;

  household->name = name;
  household->risk_profile = -1;
  household->employed = FALSE;

  household->alpha = 0.0;
  household->P = 0.0;
  household->loan = 0.0;
  household->deposit = 0.0;
  household->rate_on_deposit = 0.0;
  household->deposited_funds = 0.0;
  household->loan_rate = 0.0;
  household->deposit = 0.0;
  household->rate_on_deposit = 0.0;
  household->loan_capacity = 0.0;
  household->serviceable_loan = 0.0;

  household->wealth = w;
  household->m = m;

  // not very nice but need to populate arrays somehow;

  for (i = 0; i < MAXTYPEA; i++) {
    household->typeA[i] = -1;
  }

  for (i = 0; i < MAXTYPEB; i++) {
    household->typeB[i] = -1;
  }

  for (i = 0; i < MAXTYPEC_R; i++) {
    household->typeC_R[i] = -1;
  }

  for (i = 0; i < MAXTYPED_R; i++) {
    household->typeD_R[i] = -1;
  }
}

int main(void) {
  // for illustration of how the seeding function works;

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
