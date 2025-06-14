
#define F 10
#define MAXTYPEA 3
#define MAXTYPEB 3
#define MAXTYPEC_C 3
#define MAXTYPED_C 3
/* firms script */

struct Firm {
  int name;
  int mc; // idk
  int to_hire, to_fire;
  int months_w_open_position;

  float w; // wage at the firm
  float m; // liquidity level available;

  // inventory level at firms
  float inv_min;
  float inv_max;
  float theta, Theta; // idk
  float gamma, lambda;
  float loan_rate, deposit_rate;
  float loan, deposit;

  // arrays:
  int typeA[MAXTYPEA];
  int typeB[MAXTYPEB];
  int typeC_C[MAXTYPEC_C];
  int typeD_C[MAXTYPED_C];
};

// will try dvorak layour
