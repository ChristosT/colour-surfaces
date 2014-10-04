
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

#from sympy_calculator import PLOT
#from predefined_surfaces import *

u=Symbol('u', real=True)
v=Symbol('v', real=True)

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
   
    [U,V] = np.mgrid[umin:umax:0.01,vmin:vmax+0.1:0.1]
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



[U,V] = np.mgrid[0:2*np.pi +0.01:0.01,0:2*np.pi+0.1:0.1]
a=1
c=2
X =(c+a*np.cos(U))*np.cos(U)
Y =(c+a*np.cos(V))*np.sin(V)
Z =a*np.sin(V)
Gauss_Curvature=np.cos(V)/(a*(c+a*np.cos(V)))


    
    
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
        self.scene.mlab.clf()  #clear scene
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
    

################################################################################
# The main Widget containing all the others

class MainWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        #self.setWindowTitle("Embedding Mayavi in a PyQt4 Application")
        
        # define a "complex" layout to test the behaviour
        self.MyLayout = QtGui.QHBoxLayout()

        # put some stuff around mayavi
        #label_list = []
        #for i in range(1,3):
            #for j in range(3):
                #if ((i==1) and (j==1)) or:continue
                #self.label = QtGui.QLabel()
                #self.label.setText("Your QWidget at (%d, %d)" % (i,j))
                #self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                #self.MyLayout.addWidget(self.label, i, j)

        
        self.combo = QtGui.QComboBox()
        self.combo.addItem("Helix")
        self.combo.addItem("Ellipsoid")
        self.combo.addItem("Torus")
        self.combo.addItem("Elliptic Paraboloid")
        self.combo.addItem("Hyperboloid of one sheet")
        self.combo.addItem("Hyperboloids of two sheets")
        self.combo.addItem("Hyperboloids of two sheets")
        self.combo.activated.connect(self.onComboActivated)
        
        
        self.checkbox = QtGui.QCheckBox("Custom Surface")
        self.checkbox.stateChanged.connect(self.onCheckbox)
         #to set the initial state
        
        self.InputLayout=QtGui.QFormLayout()
        self.XLabel=QtGui.QLabel()
        self.XLabel.setText("X(u,v)")
        self.XFormula= QtGui.QLineEdit()
        
        self.YLabel=QtGui.QLabel()
        self.YLabel.setText("Y(u,v)")
        self.YFormula= QtGui.QLineEdit()
        
        self.ZLabel=QtGui.QLabel()
        self.ZLabel.setText("Z(u,v)")
        self.ZFormula= QtGui.QLineEdit()
        
        
        self.ApplyButton=QtGui.QPushButton()
        self.ApplyButton.setText("Apply")
        self.ApplyButton.setDisabled(True)
        self.ApplyButton.clicked.connect(self.onApply)
        
        self.XFormula.setDisabled(True)
        self.YFormula.setDisabled(True)
        self.ZFormula.setDisabled(True)
        
        self.InputLayout.addRow(self.combo)
        self.InputLayout.addRow(self.checkbox)
        self.InputLayout.addRow(self.XLabel, self.XFormula)
        self.InputLayout.addRow(self.YLabel, self.YFormula)
        self.InputLayout.addRow(self.ZLabel, self.ZFormula)
        self.InputLayout.addRow(self.ApplyButton)
        
        # u-v ranges
        self.InputRangeLayout=QtGui.QGridLayout()
        #-5:5:0.01,0:2*np.pi
        
        
        self.uLabel=QtGui.QLabel()
        self.uLabel.setText("u: from ")
        self.InputRangeLayout.addWidget(self.uLabel,0,0)
        self.umin= QtGui.QLineEdit()
        self.InputRangeLayout.addWidget(self.umin,0,1)
        self.u_toLabel=QtGui.QLabel()
        self.u_toLabel.setText("to")
        self.InputRangeLayout.addWidget(self.u_toLabel,0,2)
        self.umax= QtGui.QLineEdit()
        self.InputRangeLayout.addWidget(self.umax,0,3)
        
        self.vLabel=QtGui.QLabel()
        self.vLabel.setText("v: from ")
        self.InputRangeLayout.addWidget(self.vLabel,1,0)
        self.vmin= QtGui.QLineEdit()
        self.InputRangeLayout.addWidget(self.vmin,1,1)
        self.v_toLabel=QtGui.QLabel()
        self.v_toLabel.setText("to")
        self.InputRangeLayout.addWidget(self.v_toLabel,1,2)
        self.vmax= QtGui.QLineEdit()
        self.InputRangeLayout.addWidget(self.vmax,1,3)
        
        self.umax.setDisabled(True)
        self.umin.setDisabled(True)
        self.vmax.setDisabled(True)
        self.vmin.setDisabled(True)

        self.InputLayout.addRow(self.InputRangeLayout)
        

        
        self.MyLayout.addLayout(self.InputLayout)
    
        self.mayavi_widget = MayaviQWidget()

        self.MyLayout.addWidget(self.mayavi_widget,6)
        
        
        
        self.setLayout(self.MyLayout)
        #container.show()
        #window = QtGui.QMainWindow()
        #window.setCentralWidget(container)
        #window.show()
    
    def onComboActivated(self):
        global X,Y,Z,Gauss_Curvature
        text= self.combo.currentText()
        print text
        if text=="Helix":
            Helix()
            self.mayavi_widget.visualization.update_plot()
        
        elif text=="Hyperboloid of one sheet":
            Hyperboloid_one_sheet()
            self.mayavi_widget.visualization.update_plot()
            
    def onCheckbox(self):
        if self.checkbox.isChecked():
            self.combo.setDisabled(True)  
            self.XFormula.setEnabled(True)
            self.YFormula.setEnabled(True)
            self.ZFormula.setEnabled(True)
            self.ApplyButton.setEnabled(True)
            self.umax.setEnabled(True)
            self.umin.setEnabled(True)
            self.vmax.setEnabled(True)
            self.vmin.setEnabled(True)
        else:
            self.combo.setEnabled(True)  
            self.XFormula.setDisabled(True)
            self.YFormula.setDisabled(True)
            self.ZFormula.setDisabled(True)
            self.ApplyButton.setDisabled(True)
            self.umax.setDisabled(True)
            self.umin.setDisabled(True)
            self.vmax.setDisabled(True)
            self.vmin.setDisabled(True)
                
    def onApply(self):
        #try: 
        S=[sympify(self.XFormula.text()),sympify(self.YFormula.text()) ,sympify(self.ZFormula.text()) ]
        umax=sympify(self.umax.text())
        umin=sympify(self.umin.text())
        vmax=sympify(self.vmax.text())
        vmin=sympify(self.vmin.text())
        PLOT(S,umax,umin,vmax,vmin)
        self.mayavi_widget.visualization.update_plot()
        
    
class MainWindow(QtGui.QMainWindow):
    """ Our Main Window class
    """
    def __init__(self):
        """ Constructor Function
        """
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("A Simple Text Editor")
        #self.setWindowIcon(QIcon('appicon.png'))
        
        self.setGeometry(100, 100, 800, 600)
        self.MainWidget = MainWidget()
        self.setCentralWidget(self.MainWidget)


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
