/*
 Constant values to be used in the simulation execution;
 * */
int nMonths = 1000;
int nDays = 21;
int burn = 1000;
int H = 1000;
int F = 100;
int B = 10;

int num_typeA = 7;
float delta = 0.019;
int phi_max = 1;
double phi_min = 0.25;
double theta = 0.75;
double Phi_max = 1.15;
double Phi_min = 1.025;
int alpha = 3;
double Psi_price = 0.25;
double Psi_quant = 0.25;
double xi = 0.10;
double pi = 0.10;
int lambda = 3;
double Theta = 0.75;
int gamma = 3;
int beta = 5;
int n = 7;
double ki = 0.01; // figure out what that is
double r = 0.03;

int bav = 2; // firm or a household is visiting at most bav banks;
int ber = 1; // required banks liquidity;

double pla_hh = 0.5;  // prob loan approval for high-risk hh;
double pla_fi = 0.35; // prob loan approval for high-risk firm;
double plb_hh = 0.20; // prob risk-free hh will take the loan;
double plb_fi = 0.30; // prob risk-free firm will take on the loan;
