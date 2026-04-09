var y i c n a b k r w lam ret;
varexo epsilon epsilon_r;
parameters bet del alp nss khi eta rho sig rst theta phi kss yss wss css lamss;
parameters tau;

bet=0.98;  alp=0.33; del=0.025; rho=0.95; eta=1; rst=1/bet; nss=0.33; 
theta=2.0; phi=0.5;
tau=0.0;

// some steady-state calculations are needed to define khi
kss = (alp/(1/bet-(1-del)))^(1/(1-alp))*nss; yss=kss^alp*nss^(1-alp);
wss = (1-alp)*yss/nss; css=yss-del*kss; lamss=css^((phi-1)*theta-phi);
khi=lamss*wss*(1-nss)^eta;

model;
ret=rst+tau*(ret(-1)-rst)+epsilon_r;
lam=(c)^(-theta)*c(-1)^(phi*(theta-1));
lam=bet*(r(1)+1-del)*lam(1);
lam=bet*ret*lam(1);
lam=khi/(1-n)^eta/w;
k=(1-del)*k(-1)+i;
y=a*k(-1)^alp*n^(1-alp);
log(a)=rho*log(a(-1))+epsilon;
w=(1-alp)*y/n;
r=alp*y/k(-1);
b=y-c-i+ret*b(-1);
end;

steady_state_model;
a=1;                      r=1/bet-1+del;     n=nss;             
k=kss;  y=k^alp*n^(1-alp); w=(1-alp)*y/n;
i=del*k;                  c=y-i;           b=0;
lam=(c)^(-theta)*c^(phi*(theta-1));
ret=1/bet;
end;

shocks;
var epsilon;stderr 0.009;
var epsilon_r; stderr 0.01;
end;

check;

stoch_simul(irf=20, order=1) y c i b r;