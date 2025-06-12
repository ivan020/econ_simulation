/*
 * Household is the largest population in our simulation;
 *  -> defines the structure;
 *  -> initial seeding function;
 *  -> households have at max HHRELATIONS relations with firms and banks;
 */
#include "const.c"
#include "randomizer.c"
#include "utils.c"
#include <math.h>
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
  float m;        // money --- liquidity available to the household
  float c;        // consumption
  float dividend; // dividend
  float alpha;    // idk again
  float P;        // product --- some homogenous product a household owns
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

void populate_household(Household *household, int name, float w, float m,
                        float c) {
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
  household->c = c;

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

float temporal_consumption(float current_wealth, float productsP) {
  // temporal consumption function;
  return current_wealth / productsP;
}

void hh_consumption_update(Household households[]) {
  /* update each households' consumption preferences */
  for (int i = 0; i < H; i++) {
    float current_wealth = households[i].m;
    float productsP = households[i].P;
    float hhAlpha = households[i].alpha;
    float temp_c = temporal_consumption(current_wealth, productsP);
    float raised = pow(temp_c, hhAlpha);
    float new_consumption = (raised > temp_c) ? temp_c : raised;
    households[i].c = new_consumption;
  }
}

int main(void) {
  // for illustration of how the seeding function works;

  Household h[H];

  for (int i = 0; i < H; i++) {
    float gen_wealth = rand_float(0.0, 1.0);
    float m = rand_float(0.01, 1.0);
    float c = rand_float(0.01, 1.0);
    populate_household(&h[i], i + 1, gen_wealth, m, c);
  }

  for (int i = 0; i < H; i++) {
    print_household(&h[i]);
  }
}

void print_household(Household *household) {
  // a debug-ish function to show the household data struct

  printf("Household\n");

  printf("\t name: %d\n", household->name);
  printf("\t address: %p\n", &household);
  printf("\t risk_profile: %d\n", household->risk_profile);
  printf("\t employment status: %d\n", household->employed);

  printf("\t wealth: %f\n", household->wealth);
  printf("\t money: %f\n", household->m);
  printf("\t alpha: %f\n", household->alpha);
  printf("\t P: %f\n", household->P);
  printf("\t deposit: %f\n", household->deposit);
  printf("\t rate_on_deposit: %f\n", household->rate_on_deposit);
  printf("\t loan: %f\n", household->loan);
  printf("\t loan_rate: %f\n", household->loan_rate);
  printf("\t loan_capacity: %f\n", household->loan_capacity);
  printf("\t serviceable_loan: %f\n", household->serviceable_loan);

  printf("\tType a relations A with:");
  print_list(household->typeA, MAXTYPEA);

  printf("\tType a relations B with:");
  print_list(household->typeB, MAXTYPEB);

  printf("\tType a relations C with:");
  print_list(household->typeC_R, MAXTYPEC_R);

  printf("\tType a relations D with:");
  print_list(household->typeD_R, MAXTYPED_R);
}
