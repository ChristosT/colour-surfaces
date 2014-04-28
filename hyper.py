# Create the data.
from numpy import pi, sin, cos, mgrid,cosh

[u,v] = mgrid[-3:3:0.01,0:2*pi+0.1:0.1]
a=2


x = a*cosh(u/a)*cos(v)
y = a*cosh(u/a)*sin(v)
z = u
K=-1/(a**2*cosh(u/a)**4)

from mayavi import mlab

s = mlab.mesh(x, y, z,scalars=K)
mlab.show()
