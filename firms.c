
#define F 10
#define MAXTYPEA 3
#define MAXTYPEB 3
#define MAXTYPEC_C 3
#define MAXTYPED_C 3
/* firms script */

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
  float theta, Theta; // idk
  float gamma, lambda;
  float loan_rate, deposit_rate;
  float loan, deposit;
  float deposit_with_bank;
  float m_buf;
  float dailyProduction;
  float loan_capacity;
  float borrowed_funds;

  // arrays:
  int typeA[MAXTYPEA];
  int typeB[MAXTYPEB];
  int typeC_C[MAXTYPEC_C];
  int typeD_C[MAXTYPED_C];
};

typedef struct Firm Firm;

// will try dvorak layout
//

void increment_months_with_open_position(Firm firm) {
  firm.months_w_open_position += 1;
}

void make_labour_cheaper(Firm firm) {}

void update_labour_price(Firm firms[]) {
  for (int i = 0; i < F; i++) {
    if (firms[i].to_hire > 0) {
      increment_months_with_open_position(firms[i]);
    }

    if (firms[i].to_hire == 0 && firms[i].months_w_open_position > 0) {
      make_labour_cheaper(firms[i]);
    }
  }
}
