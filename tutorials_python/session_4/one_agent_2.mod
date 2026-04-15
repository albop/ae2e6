// on agent with preference for wealth

var y, c, b;
varexo e_y;

parameters beta, r, q, sigma, rho, eta, phi, ybar, bbar, cbar, chi, sig_z;


// shock specification
rho = 1.0;
sig_z = 0.01;

r = 1.04;
sigma = 0.5;
q = 1/r;

ybar = 1.0;
bbar = 0.0;
cbar = ybar + bbar*(1-q); // per capita consumption

// preference for wealth parameters
eta = 1.1;
phi = 0.05;

// adjusted beta
// note that variables are equal to zero so far. Hence we use the 
// parameters bbar and cbar instead
beta = 1/r - phi*(1+bbar*q)^(-1/eta)/(cbar^(-1/sigma));

model;

[name='income process']
y = ybar + rho*(y(-1)-ybar) + e_y;                       // income per capita

[name='budget equation']
c = y + b(-1) - b*q;            // consumption per capita

[name='euler equation']
1/r = beta*(c(1)/c(0))^(-1/sigma) + phi*(1+b*q)^(-1/eta)/(c^(-1/sigma));  

end;

steady_state_model;
y = ybar;
b = bbar;         // debt level a the steady-state is targeted to calibrate the model
c = cbar; 
end;

shocks;
var e_y; stderr sig_z;
end;

check;


stoch_simul(order=1);
