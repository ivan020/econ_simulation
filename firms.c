
#define F 10
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
};

// will try dvorak layour
