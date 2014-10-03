from sympy import lambdify,diff,Matrix

def PLOT(S,umax,umin,vmax,vmin):
    #global X,Y,Z,Gauss_Curvature

    #from sympy.abc import a, u,v

    xu=Matrix([diff(f,u) for f in S])
    xv=Matrix([diff(f,v) for f in S])
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
   
    [U,V] = mgrid[umin:umax:0.01,vmin:vmax+0.1:0.1]
    # convert Sympy formula to numpy lambda functions
    F1=lambdify((u,v), S[0], "numpy")
    F2=lambdify((u,v), S[1], "numpy")
    F3=lambdify((u,v), S[2], "numpy")
    F4=lambdify((u,v), K, "numpy")
    #Calculate numpy arrays 
    X=F1(U,V);
    Y=F2(U,V);
    Z=F3(U,V);
    Gauss_Curvature=F4(U,V);
    return X,Y,Z,Gauss_Curvature
