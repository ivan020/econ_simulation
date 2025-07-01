
#define F 10
#define MAXTYPEA 3
#define MAXTYPEB 3
#define MAXTYPEC_C 3
#define MAXTYPED_C 3
#include "randomizer.c"
/* firms script */

const float DELTA = 0.019;
const int GAMMA = 3;
const float phi_max = 0.25;
const float phi_min = 0.0;
const int lambda = 3;
const int nDays = 21;
const float Phi_max = 1.15;
const float Phi_min = 1.025;
const float Theta = 0.75;
const float theta = 0.75;

struct Firm {
  int name;
  int to_hire, to_fire;
  int months_w_open_position;
  int credit_score;

  float w; // wage at the firm
  float m; // liquidity level available;
  float mc;

  // inventory level at firms
  float inv_min;
  float inv_max;
  float inv;
  float d;
  float theta, Theta; // idk
  float gamma, lambda;
  float loan_rate, deposit_rate;
  float loan, deposit;
  float deposit_with_bank;
  float m_buf;
  float dailyProduction;
  float loan_capacity;
  float borrowed_funds;

  // max and min production bounds
  float p, p_max, p_min;

  // arrays:
  int typeA[MAXTYPEA];
  int typeB[MAXTYPEB];
  int typeC_C[MAXTYPEC_C];
  int typeD_C[MAXTYPED_C];
};

typedef struct Firm Firm;

void increment_months_with_open_position(Firm *firm) {
  firm->months_w_open_position += 1;
}

void make_labour_cheaper(Firm *firm) {
  firm->w = firm->w * (1 - rand_float(0.0, DELTA));
  firm->months_w_open_position = 0;
}

void increment_proposed_salary(Firm *firm) {
  firm->w = firm->w * (1 + rand_float(0.0, DELTA));
}

void update_production_inventory(Firm *firm) {
  // update the inventory of the firm
  firm->inv_max = phi_max * firm->d;
  firm->inv_min = phi_min * firm->d;
  firm->d = 0.0;
  firm->mc = firm->w / (float)lambda / (float)nDays;
  firm->p_max = Phi_max * firm->d;
  firm->p_min = Phi_min * firm->d;
}

void increase_production_price(Firm *firm) {
  firm->to_hire = 1;
  firm->to_fire = 0;
  if (firm->p < firm->p_max && rand_float(0.0, 1.0) < Theta) {
    // with random probability increase the price to cool off the demand
    firm->p = firm->p * (1 - rand_float(0.0, theta));
  }
}

void update_labour_price(Firm firms[]) {
  for (int i = 0; i < F; i++) {

    if (firms[i].to_hire > 0) {
      increment_months_with_open_position(&firms[i]);
    }

    if (firms[i].to_hire == 0 && firms[i].months_w_open_position > 0) {
      make_labour_cheaper(&firms[i]);
    }

    if (firms[i].months_w_open_position >= GAMMA) {
      increment_proposed_salary(&firms[i]);
    }

    update_production_inventory(&firms[i]);

    if (firms[i].inv < firms[i].inv_min) {
      increase_production_price(&firms[i]);
    }
  }
}

void populate_firm(Firm *firm, int name, float w, float inv, float inv_min,
                   float inv_max, float p, float p_min, float p_max) {
  firm->name = name;
  firm->credit_score = -1;
  firm->p = p;
  firm->w = w;
  firm->inv = inv;

  firm->inv_min = inv * 0.9;
  firm->inv_max = inv * 1.1;
  firm->p_min = p * 0.9;
  firm->p_max = p * 1.1;

  for (int i = 0; i < MAXTYPEA; i++) {
    firm->typeA[i] = -1;
  }

  for (int i = 0; i < MAXTYPEB; i++) {
    firm->typeB[i] = -1;
  }

  for (int i = 0; i < MAXTYPEC_C; i++) {
    firm->typeC_C[i] = -1;
  }

  for (int i = 0; i < MAXTYPED_C; i++) {
    firm->typeD_C[i] = -1;
  }
}
