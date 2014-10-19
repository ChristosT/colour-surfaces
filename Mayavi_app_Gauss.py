from PySide import QtGui, QtCore

import sys
import time

from traits.api import HasTraits, Instance, on_trait_change, Range
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, \
        SceneEditor

# Create the data.

from sympy import sympify
from predefined_surfaces import *

D={'v':v,'u':u} # we use it in order to keep u,v as variable during the 
                #use of simpify
    
onScreen=Torus

################################################################################

################################################################################
#The actual visualization
class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())
    change=Range(0.0, 100.0, value=1.0)

    @on_trait_change('change')
    def update_plot(self):
        # This function is called when the view is opened. We don't
        # populate the scene when the view is not yet open, as some
        # VTK features require a GLContext.

        # We can do normal mlab calls on the embedded scene.

        # todo use set from mlab
        self.scene.mlab.clf()  #clear scene
        #do the drawing 
        onScreen.cal()
        try:
            self.scene.mlab.mesh(onScreen.X, onScreen.Y, onScreen.Z,scalars=onScreen.Gauss_Curvature)
            #add the colorbar
            self.scene.mlab.colorbar(orientation='horizontal',title='Gaussian Curvature')

        except AssertionError: # in same cases it fails so we just plot 
                                #the surface with one color
                                # TODO: minimize these cases
            print 'error'
            self.scene.mlab.mesh(onScreen.X, onScreen.Y, onScreen.Z,color=(0,1,0))
        # adjust camera
        self.scene.mlab.view(azimuth=45, elevation=60, distance=30)
        #print 'scene updated'
        

    # the layout of the dialog screated
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=250, width=400, show_label=False),
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
       
        
class MainWindow(QtGui.QMainWindow):
    """ Our Main Window class
    """
    def __init__(self):
        """ Constructor Function
        """
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("Exploring the Gaussian Curvature")
        #self.setWindowIcon(QIcon('appicon.png'))
        
        self.resize(800, 600)
        self.center()
        self.StatusBar = QtGui.QStatusBar()
        self.setStatusBar(self.StatusBar)
        self.StatusBar.showMessage('Ready')
        
        self.MainWidget = QtGui.QWidget()
        self.create_MainWidget()
        self.setCentralWidget(self.MainWidget)
        self.connections()
    
    def create_MainWidget(self):
        self.MainWidget.MyLayout = QtGui.QHBoxLayout()
        #example combobox
        self.MainWidget.combo = QtGui.QComboBox()
        self.MainWidget.combo.addItem("Torus")
        self.MainWidget.combo.addItem("Helix")
        self.MainWidget.combo.addItem("Ellipsoid")
        self.MainWidget.combo.addItem("Elliptic Paraboloid")
        self.MainWidget.combo.addItem("Hyperboloid of one sheet")
        self.MainWidget.combo.addItem("Hyperboloids of two sheets")
        self.MainWidget.combo.addItem("Hyperboloids of two sheets")
        #self.MainWidget.ApplyButton.clicked.connect(self.MainWidget.onApply)
        
        
        self.MainWidget.checkbox = QtGui.QCheckBox("Custom Surface")
        
        self.MainWidget.custom_controls=[] # list holding all the controls 
                                #that need to be disabled when 
                                #custom checkbox is not enabled
        
        #Input Layout
        self.MainWidget.InputLayout=QtGui.QFormLayout()
        
        self.MainWidget.XLabel=QtGui.QLabel()
        self.MainWidget.XLabel.setText("X(u,v)")
        self.MainWidget.custom_controls.append(self.MainWidget.XLabel)
        
        self.MainWidget.XFormula= QtGui.QLineEdit()
        self.MainWidget.custom_controls.append(self.MainWidget.XFormula)
        
        self.MainWidget.YLabel=QtGui.QLabel()
        self.MainWidget.YLabel.setText("Y(u,v)")
        self.MainWidget.custom_controls.append(self.MainWidget.YLabel)
        self.MainWidget.YFormula= QtGui.QLineEdit()
        self.MainWidget.custom_controls.append(self.MainWidget.YFormula)
        
        self.MainWidget.ZLabel=QtGui.QLabel()
        self.MainWidget.ZLabel.setText("Z(u,v)")
        self.MainWidget.custom_controls.append(self.MainWidget.ZLabel)
        self.MainWidget.ZFormula= QtGui.QLineEdit()
        self.MainWidget.custom_controls.append(self.MainWidget.ZFormula)
        
        self.MainWidget.Formulas=[self.MainWidget.XFormula,self.MainWidget.YFormula,self.MainWidget.ZFormula]
        
        self.MainWidget.ApplyButton=QtGui.QPushButton()
        self.MainWidget.ApplyButton.setText("Apply")
        
        self.MainWidget.custom_controls.append(self.MainWidget.ApplyButton)
        
        self.MainWidget.InputLayout.addRow(self.MainWidget.combo)
        self.MainWidget.InputLayout.addRow(self.MainWidget.checkbox)
        self.MainWidget.InputLayout.addRow(self.MainWidget.XLabel, self.MainWidget.XFormula)
        self.MainWidget.InputLayout.addRow(self.MainWidget.YLabel, self.MainWidget.YFormula)
        self.MainWidget.InputLayout.addRow(self.MainWidget.ZLabel, self.MainWidget.ZFormula)
        self.MainWidget.InputLayout.addRow(self.MainWidget.ApplyButton)
        
        # u-v ranges
        self.MainWidget.InputRangeLayout=QtGui.QGridLayout()
        
        self.MainWidget.uLabel=QtGui.QLabel()
        self.MainWidget.uLabel.setText("u: from ")     
        self.MainWidget.InputRangeLayout.addWidget(self.MainWidget.uLabel,0,0)
        self.MainWidget.custom_controls.append(self.MainWidget.uLabel)  

        self.MainWidget.umin= QtGui.QLineEdit()
        self.MainWidget.InputRangeLayout.addWidget(self.MainWidget.umin,0,1)
        self.MainWidget.custom_controls.append(self.MainWidget.umin)
        
        self.MainWidget.u_toLabel=QtGui.QLabel()
        self.MainWidget.u_toLabel.setText("to")
        self.MainWidget.InputRangeLayout.addWidget(self.MainWidget.u_toLabel,0,2)
        self.MainWidget.custom_controls.append(self.MainWidget.u_toLabel)
       
        self.MainWidget.umax= QtGui.QLineEdit()
        self.MainWidget.InputRangeLayout.addWidget(self.MainWidget.umax,0,3)
        self.MainWidget.custom_controls.append(self.MainWidget.umax)
        
        self.MainWidget.vLabel=QtGui.QLabel()
        self.MainWidget.vLabel.setText("v: from ")
        self.MainWidget.InputRangeLayout.addWidget(self.MainWidget.vLabel,1,0)
        self.MainWidget.custom_controls.append(self.MainWidget.vLabel)
         
        self.MainWidget.vmin= QtGui.QLineEdit()
        self.MainWidget.InputRangeLayout.addWidget(self.MainWidget.vmin,1,1)
        self.MainWidget.custom_controls.append(self.MainWidget.vmin)
         
        self.MainWidget.v_toLabel=QtGui.QLabel()
        self.MainWidget.v_toLabel.setText("to")
        self.MainWidget.InputRangeLayout.addWidget(self.MainWidget.v_toLabel,1,2)
        self.MainWidget.custom_controls.append(self.MainWidget.v_toLabel) 
        
        self.MainWidget.vmax= QtGui.QLineEdit()
        self.MainWidget.InputRangeLayout.addWidget(self.MainWidget.vmax,1,3)
        self.MainWidget.custom_controls.append(self.MainWidget.vmax) 
        
        self.MainWidget.u_v_range=[self.MainWidget.umin,self.MainWidget.umax,self.MainWidget.vmin,self.MainWidget.vmax]
       
        #self.MainWidget.onCheckbox() #set the initial state of the custom controls
            
        self.MainWidget.InputLayout.addRow(self.MainWidget.InputRangeLayout)
        self.MainWidget.MyLayout.addLayout(self.MainWidget.InputLayout)
        #insert mayaviwidget to the main window
        self.MainWidget.mayavi_widget = MayaviQWidget()
        self.MainWidget.MyLayout.addWidget(self.MainWidget.mayavi_widget,4)
          
        self.MainWidget.setLayout(self.MainWidget.MyLayout)
        
    def connections(self):
        
        self.MainWidget.combo.activated.connect(self.onComboActivated)
        self.MainWidget.checkbox.stateChanged.connect(self.onCheckbox)
        self.MainWidget.ApplyButton.clicked.connect(self.onApply)
        self.onCheckbox()
    def center(self):
        #http://zetcode.com/gui/pysidetutorial/firstprograms/
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def writeFormulas(self,Surface1):
        """when an example is chosen write the formulas in the input Forms
        """
        for i in range(0,3):
            self.MainWidget.Formulas[i].setText(str(Surface1.S[i]))
        for i in range(0,4):
            self.MainWidget.u_v_range[i].setText(str(Surface1.u_v_range[i]))
   
        
    def onComboActivated(self):
        global onScreen
        text=self.MainWidget.combo.currentText()
        
        if text=="Helix":
            onScreen=Helix
            
        elif text=="Hyperboloid of one sheet":
            onScreen=Hyperboloid_one_sheet
 
        elif text=="Torus":
            onScreen=Torus
    
        elif text=="Ellipsoid":
            onScreen=Ellipsoid

        elif text=="Elliptic Paraboloid":
            onScreen=Elliptic_Paraboloid
        
                
        self.StatusBar.showMessage("Processing...")
        self.StatusBar.showMessage("Processing...")
        time.sleep(4)
        self.writeFormulas(onScreen)
        self.MainWidget.mayavi_widget.visualization.update_plot()
        self.StatusBar.showMessage("Ready!")
        
        
    def onCheckbox(self):
        if self.MainWidget.checkbox.isChecked():
            self.MainWidget.combo.setDisabled(True)  
            
            for i in self.MainWidget.custom_controls:
                i.setEnabled(True)
        else:
            self.MainWidget.combo.setEnabled(True)  
            for i in self.MainWidget.custom_controls:
                i.setDisabled(True)
            
    def onApply(self):
        global onScreen
        
        self.StatusBar.showMessage("Processing...")
        self.StatusBar.showMessage("Processing...")
        onScreen=Surface([sympify(self.MainWidget.XFormula.text(),D),
                          sympify(self.MainWidget.YFormula.text(),D),
                          sympify(self.MainWidget.ZFormula.text(),D) ],
                          umin=sympify(self.MainWidget.umin.text()),
                          umax=sympify(self.MainWidget.umax.text()),
                          vmin=sympify(self.MainWidget.vmin.text()),        
                          vmax=sympify(self.MainWidget.vmax.text()))
        
        
        self.MainWidget.mayavi_widget.visualization.update_plot()
        self.StatusBar.showMessage("Ready!")


if __name__ =='__main__':
# Exception Handling
    try:
        #app = QtGui.QApplication(sys.argv)
        app = QtGui.QApplication.instance()
        myWidget = MainWindow()
        myWidget.show()
        app.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window...")
    except Exception:
        print(sys.exc_info()[1])
    except Error:
        print("Error")
    
