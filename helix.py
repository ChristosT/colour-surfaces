# Create the data.
from numpy import pi, sin, cos, mgrid
[u,v] = mgrid[-5:5:0.01,0:2*pi+0.1:0.1]
a=2

x = u*cos(v)
y = u*sin(v)
z = a*v
K=-a**2/(u**2 +a**2)**2

from mayavi import mlab
s = mlab.mesh(x, y, z,scalars=K)
mlab.colorbar(orientation='horizontal',title='Gaussian Curvature')
mlab.show()
