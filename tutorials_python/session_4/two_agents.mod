// two agents agent with preference for wealth

var y, z, c_t, c_b, b_t, b_b, B, q, r;
varexo e_y, e_z;

parameters beta_t, beta_b, rbar, sigma, rho_y, rho_z, eta, phi, zbar, ybar, Bbar, c_t_bar, c_b_bar, chi, sig_y, sig_z;


rbar = 1.04;
sigma = 0.5;

chi = 0.05; // fraction of top earners

// steady-state income
zbar = 0.1807; // top 5% income share
lev = 0.91;    // total assets/gdp

ybar = 1;       //  aggregate income
Bbar = lev;     // aggregate leverage ratio

// autocorrelation of gdp shock
rho_y = 0.9;
// autocorrelation of redistributive shock
rho_z = 1.0;

c_t_bar = ybar*zbar/chi         + Bbar/chi    *(1-1/rbar); // per capita consumption for top earners
c_b_bar = ybar*(1-zbar)/(1-chi) - Bbar/(1-chi)*(1-1/rbar); // per capita consumption for bot earners


// preference for wealth parameters
eta = 0.6;
phi = 0.05;

beta_t = 1/rbar - phi*(1+Bbar/chi/rbar)^(-1/eta)/(c_t_bar^(-1/sigma));
beta_b = 1/rbar;

// we need some additional parameters for the steady-state calibration
// debt level a the steady-state is targeted to calibrate the model

sig_y = 0.01;
sig_z = 0.1;


// one needs at least a static equation
model;


y = ybar*(y(-1)/ybar)^(rho_y) + (e_y);
z = zbar + rho_z*(z(-1)-zbar) + (e_z);

b_t = B/chi; // bonds owned per top earners (per capita)
b_b = -B/(1-chi); // bonds owned per bottom earners (per capita)


// top earners
c_t = y*z/chi + (b_t(-1) - b_t*q);
q = beta_t*(c_t(1)/c_t)^(-1/sigma) + phi*(1+b_t*q)^(-1/eta)/(c_t^(-1/sigma));

// bottom earners
c_b = y*(1-z)/(1-chi) + (b_b(-1) - b_b*q);
q = beta_b*(c_b(1)/c_b(0))^(-1/sigma);

r = 1/q;

end;


steady_state_model;

y = ybar;
z = zbar;
B = Bbar;         // debt level a the steady-state is targeted to calibrate the model
b_t = B/chi;
b_b = -B/(1-chi);
c_t = c_t_bar; 
c_b = c_b_bar;
r = rbar;
q = 1/r;
end;

shocks;
var e_y; stderr sig_y;
var e_z; stderr sig_z;
end;


check;

stoch_simul(order=1);

