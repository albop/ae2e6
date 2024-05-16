// on agent with preference for wealth

var y, c, b;
varexo e_y;

parameters beta, r, q, sigma, rho, eta, phi, zbar, ybar, bbar, cbar, chi, sig_y;


sig_y = 0.01;

r = 1.04;
sigma = 0.5;
q = 1/r;

ybar = 1.0;
bbar = 0.0;
cbar = ybar + bbar*(1-q); //equilibrium consumption

// preference for wealth parameters
eta = 0.6;
phi = 0.05;

beta = 1/r;

// one needs at least a static equation
model;

[name='income process']
y = ybar + 0.1*e_y;                       // income per capita

[name='budget equation']
c = y + (b(-1) - b*q);            // consumption per capita

[name='euler equation']
1/r = beta*(c(1)/c(0))^(-1/sigma);    

end;

steady_state_model;
y = ybar;
b = bbar;         // debt level a the steady-state is targeted to calibrate the model
c = cbar; 
end;

shocks;
var e_y; stderr sig_y;
end;


steady;
check;


stoch_simul(order=1);
