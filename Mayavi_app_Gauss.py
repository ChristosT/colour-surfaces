from PySide import QtGui, QtCore

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
D={'v':v,'u':u} # we use it in order to keep u,v as variable during the 
#use of simpify


    
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
        #self.X=F1(U,V)
        #self.Y=F2(U,V)
        #self.Z=F3(U,V)
        #self.Gauss_Curvature=F4(U,V)
        X=F1(U,V)
        Y=F2(U,V)
        Z=F3(U,V)
        Gauss_Curvature=F4(U,V)


        

Torus = Surface([(2 + cos(v))*cos(u),(2 + cos(v))*sin(u),sin(v)],0,2*pi,0,2*pi)
Helix = Surface([u*cos(v),u*sin(v),2*v],-5,5,0,2*pi)
Hyperboloid_one_sheet=Surface([2*cosh(u/2)*cos(v), 2*cosh(u/2)*sin(v), u],-3,3,0,2*pi)
Ellipsoid=Surface([3*cos(u)*cos(v),4*cos(u)*sin(v),5*sin(u)],0,2*pi,0,pi)
Elliptic_Paraboloid=Surface([2*u*cos(v), 3*u*sin(v),u*u],0,2,0,2*pi)



[U,V] = np.mgrid[0:2*np.pi +0.01:0.01,0:2*np.pi+0.1:0.1]
a=1
c=2
X =(c+a*np.cos(U))*np.cos(V)
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

        assert X.shape==Y.shape and Y.shape==Z.shape and Z.shape==Gauss_Curvature.shape
        self.scene.mlab.clf()  #clear scene
        self.scene.mlab.mesh(X, Y, Z,scalars=Gauss_Curvature)
        #self.scene.isometric_view()
        self.scene.mlab.colorbar(orientation='horizontal',title='Gaussian Curvature')
        #isometric_view(self.scene.mlab)
        self.scene.mlab.view(azimuth=45, elevation=60, distance=30)
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
        
        self.Formulas=[self.XFormula,self.YFormula,self.ZFormula]
        
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

        self.u_v_range=[self.umin,self.umax,self.vmin,self.vmax]
        self.InputLayout.addRow(self.InputRangeLayout)
        

        
        self.MyLayout.addLayout(self.InputLayout)
    
        self.mayavi_widget = MayaviQWidget()

        self.MyLayout.addWidget(self.mayavi_widget,6)
        
        
        
        self.setLayout(self.MyLayout)
        #container.show()
        #window = QtGui.QMainWindow()
        #window.setCentralWidget(container)
        #window.show()
    def writeFormulas(self,Surface1):
        for i in range(0,3):
            self.Formulas[i].setText(str(Surface1.S[i]))
        for i in range(0,4):
            self.u_v_range[i].setText(str(Surface1.u_v_range[i]))
    
    def onComboActivated(self):
        global X,Y,Z,Gauss_Curvature
        text= self.combo.currentText()
        print text
        if text=="Helix":
            Helix.cal()
            self.writeFormulas(Helix)
            
        elif text=="Hyperboloid of one sheet":
            Hyperboloid_one_sheet.cal()
            self.writeFormulas(Hyperboloid_one_sheet)

        elif text=="Torus":
            Torus.cal()
            self.writeFormulas(Torus)
   
        elif text=="Ellipsoid":
            Ellipsoid.cal()
            self.writeFormulas(Ellipsoid)

        elif text=="Elliptic Paraboloid":
            Elliptic_Paraboloid.cal()
            self.writeFormulas(Elliptic_Paraboloid)
        
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
        
        Surface1=Surface([sympify(self.XFormula.text(),D),
                        sympify(self.YFormula.text(),D),
                        sympify(self.ZFormula.text(),D) ],
                        umin=sympify(self.umin.text()),
                        umax=sympify(self.umax.text()),
                        vmin=sympify(self.vmin.text()),        
                        vmax=sympify(self.vmax.text()))
        
        
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
