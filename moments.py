import numpy as np

A = np.array([[0.001, 0], [0.6, 1.9]])
B = np.eye(2)
Σ = np.array([[0.001, 0], [0, 0.02]])


def compute_moments(A,B,Σ, T=1000, τ_η=1e-8):

    Ω0 = np.eye(2)

    for t in range(T):
        
        Ω1 = A*Ω0*A.T + B*Σ*B.T

        Ω1[Ω1>=1e8] = np.inf

        d = abs(Ω0-Ω1)
        η = d[np.isfinite(d)].max()

        if η<τ_η:
            return Ω1
        
        Ω0 = Ω1
    
    raise Exception("No convergence")


compute_moments(A,B,Σ)