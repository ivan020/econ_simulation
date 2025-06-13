
/* firms script */

struct Firm {
  int name;
  float w; // wage at the firm
  float m; // liquidity level available;

  // inventory level at firms
  float inv_min;
  float inv_max;
};

// will try dvorak layour
