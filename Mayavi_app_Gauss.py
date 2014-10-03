
# to be used, you need to set the QT_API environment variable to 'pyqt'
#os.environ['QT_API'] = 'pyqt'

# To be able to use PySide or PyQt4 and not run in conflicts with traits,
# we need to import QtGui and QtCore from pyface.qt
from PySide import QtGui, QtCore
# Alternatively, you can bypass this line, but you need to make sure that
# the following lines are executed before the import of PyQT:
#   import sip
#   sip.setapi('QString', 2)
import sys
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, \
        SceneEditor

# Create the data.
import numpy as np
from sympy import *

from sympy_calculator import PLOT
from predefined_surfaces import *

def PLOT(S,umax,umin,vmax,vmin):
    global X,Y,Z,Gauss_Curvature

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


a=Symbol('a', real=True)
u=Symbol('u', real=True)
v=Symbol('v', real=True)

[u,v] = np.mgrid[0:2*np.pi +0.01:0.01,0:2*np.pi+0.1:0.1]
a=1
c=2
X =(c+a*np.cos(v))*np.cos(u)
Y =(c+a*np.cos(v))*np.sin(u)
Z =a*np.sin(v)
Gauss_Curvature=np.cos(v)/(a*(c+a*np.cos(v)))

def Helix2():
    S=[u*cos(v),u*sin(v),a*v]
    umax=5
    umin=-5
    vmax=2*pi
    vmin=0
    return PLOT(S,umax,umin,vmax,vmin)
    
def Hyperboloid_one_sheet():
    S=[2*cosh(u/2)*cos(v), 2*cosh(u/2)*sin(v), u]
    umax=3
    umin=-3
    vmax=2*pi
    vmin=0
    return PLOT(S,umax,umin,vmax,vmin)

def Helix():
#dphi, dtheta = pi/250.0, pi/250.0
    global X,Y,Z,Gauss_Curvature
    [u,v] = np.mgrid[-5:5:0.01,0:2*np.pi+0.1:0.1]
    a=2

    X = u*np.cos(v)
    Y = u*np.sin(v)
    Z = a*v
    Gauss_Curvature=-a**2/(u**2 +a**2)**2
    
################################################################################

################################################################################
#The actual visualization
class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())

    @on_trait_change('scene.activated')
    def update_plot(self):
        # This function is called when the view is opened. We don't
        # populate the scene when the view is not yet open, as some
        # VTK features require a GLContext.

        # We can do normal mlab calls on the embedded scene.
        #Helix()
        self.scene.mlab.mesh(X, Y, Z,scalars=Gauss_Curvature)
        self.scene.mlab.colorbar(orientation='horizontal',title='Gaussian Curvature')

    # the layout of the dialog screated
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=250, width=300, show_label=False),
                resizable=True # We need this to resize with the parent widget
                )


################################################################################
# The QWidget containing the visualization, this is pure PyQt4 code.
class MayaviQWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.visualization = Visualization()

        # The edit_traits call will generate the widget to embed.
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)
    


class MainWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle("Embedding Mayavi in a PyQt4 Application")
        
        # define a "complex" layout to test the behaviour
        self.MyLayout = QtGui.QGridLayout()

        # put some stuff around mayavi
        #label_list = []
        for i in range(3):
            for j in range(3):
                if (i==1) and (j==1):continue
                self.label = QtGui.QLabel(self)
                self.label.setText("Your QWidget at (%d, %d)" % (i,j))
                self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                self.MyLayout.addWidget(self.label, i, j)

        
        self.combo = QtGui.QComboBox()
        self.combo.addItem("Helix")
        self.combo.addItem("Ellipsoid")
        self.combo.addItem("Torus")
        self.combo.addItem("Elliptic Paraboloid")
        self.combo.addItem("Hyperboloid of one sheet")
        self.combo.addItem("Hyperboloids of two sheets")
        self.combo.addItem("Hyperboloids of two sheets")
        self.combo.activated.connect(self.onActivated)
        self.MyLayout.addWidget(self.combo, 1,2)
        
        
        
        self.mayavi_widget = MayaviQWidget()

        self.MyLayout.addWidget(self.mayavi_widget, 1, 1)
        
        
        
        self.setLayout(self.MyLayout)
        #container.show()
        #window = QtGui.QMainWindow()
        #window.setCentralWidget(container)
        #window.show()
    
    def onActivated(self):
        global X,Y,Z,Gauss_Curvature
        text= self.combo.currentText()
        print text
        if text=="Helix":
            Helix()
        
        #if text=="Hyperboloid of one sheet":
            #X,Y,Z,Gauss_Curvature=Hyperboloid_one_sheet()
    


if __name__ =='__main__':
# Exception Handling
    try:
        #app = QtGui.QApplication(sys.argv)
        app = QtGui.QApplication.instance()
        myWidget = MainWindow()
        #myWidget.connections()
        myWidget.show()
        app.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print(sys.exc_info()[1])
