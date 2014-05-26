# Create the data.
from numpy import pi, sin, cos, mgrid,cosh

[u,v] = mgrid[0:2*pi +0.01:0.01,0:2*pi+0.1:0.1]
a=1
c=2

x =(c+a*cos(v))*cos(u)
y =(c+a*cos(v))*sin(u)
z =a*sin(v)
K=cos(v)/(a*(c+a*cos(v)))


from mayavi import mlab
s = mlab.mesh(x, y, z,scalars=K)
mlab.colorbar(s, orientation='horizontal',title='Gaussian Curvature')
