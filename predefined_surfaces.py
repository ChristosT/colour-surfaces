import numpy as np
from sympy import Matrix,diff,simplify,lambdify,Symbol, cos, sin,cosh,sinh,pi
u=Symbol('u', real=True)
v=Symbol('v', real=True)

class Surface():
    
    def __init__(self,S,umin,umax,vmin,vmax):
        self.S=S
        self.umax=umax
        self.umin=umin
        self.vmax=vmax
        self.vmin=vmin
        self.u_v_range=[umin,umax,vmin,vmax]
   
    def cal(self):
        global X,Y,Z,Gauss_Curvature

        xu=Matrix([diff(f,u) for f in self.S])
        xv=Matrix([diff(f,v) for f in self.S])
        xuu=Matrix([diff(f,u) for f in xu])
        xvv=Matrix([diff(f,v) for f in xv])
        xuv=Matrix([diff(f,v) for f in xu])
        E=simplify(xu.dot(xu))
        G=simplify(xv.dot(xv))
        F=simplify(xu.dot(xv))


        H1=Matrix([xuu,xu,xv]).reshape(3,3)
        H2=Matrix([xvv,xu,xv]).reshape(3,3)
        H3=Matrix([xuv,xu,xv]).reshape(3,3)
        K=simplify(((H1.det()*H2.det() -(H3.det()**2)))/ (xu.norm()**2*xv.norm()**2 -F*F)**2)

        #Pass to numpy
        du=float(self.umax-self.umin)/100
        dv=float(self.vmax-self.vmin)/100
        [U,V] = np.mgrid[self.umin:self.umax+du:du,self.vmin:self.vmax+dv:dv]
        # convert Sympy formula to numpy lambda functions
        F1=lambdify((u,v), self.S[0], "numpy")
        F2=lambdify((u,v), self.S[1], "numpy")
        F3=lambdify((u,v), self.S[2], "numpy")
        F4=lambdify((u,v), K, "numpy")
        #Calculate numpy arrays 
        self.X=F1(U,V)
        self.Y=F2(U,V)
        self.Z=F3(U,V)
        self.Gauss_Curvature=F4(U,V)
        #X=F1(U,V)
        #Y=F2(U,V)
        #Z=F3(U,V)
        #Gauss_Curvature=F4(U,V)


        

Torus = Surface([(2 + cos(v))*cos(u),(2 + cos(v))*sin(u),sin(v)],0,2*pi,0,2*pi)
Helix = Surface([u*cos(v),u*sin(v),2*v],-5,5,0,2*pi)
Hyperboloid_one_sheet=Surface([2*cosh(u/2)*cos(v), 2*cosh(u/2)*sin(v), u],-3,3,0,2*pi)
Ellipsoid=Surface([3*cos(u)*cos(v),4*cos(u)*sin(v),5*sin(u)],0,2*pi,0,pi)
Elliptic_Paraboloid=Surface([2*u*cos(v), 3*u*sin(v),u*u],0,2,0,2*pi)
