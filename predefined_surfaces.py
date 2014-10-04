from sympy import Symbol,cos,sin,cosh,pi
u=Symbol('u', real=True)
v=Symbol('v', real=True)
from sympy_calculator import PLOT

def Helix():
    S=[u*cos(v),u*sin(v),2*v]
    umax=5
    umin=-5
    vmax=2*pi
    vmin=0
    PLOT(S,umax,umin,vmax,vmin)
    
def Hyperboloid_one_sheet():
    S=[2*cosh(u/2)*cos(v), 2*cosh(u/2)*sin(v), u]
    umax=3
    umin=-3
    vmax=2*pi
    vmin=0
    PLOT(S,umax,umin,vmax,vmin)
