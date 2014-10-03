# we need to import QtGui and QtCore from pyface.qt
from PySide import QtGui, QtCore
# Alternatively, you can bypass this line, but you need to make sure that
# the following lines are executed before the import of PyQT:
#   import sip
#   sip.setapi('QString', 2)
import sys

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
                #label_list.append(self.label)
        
        #self.label=QtGui.QLabel()
        #self.label.setText("Your QWidget at (%d, %d)" % (1,2))
        ##self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        #self.layout.addWidget(self.label, 1, 2)
        
        #self.label2=QtGui.QLabel()
        #self.label2.setText("Your QWidget at (%d, %d)" % (1,3))
        ##self.label2.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        #self.layout.addWidget(self.label2, 1, 3)
        
        self.combo = QtGui.QComboBox()
        self.combo.addItem("Helix")
        self.combo.addItem("Ellipsoid")
        self.combo.addItem("Torus")
        self.combo.addItem("Elliptic Paraboloid")
        self.combo.addItem("Hyperboloid of one sheet")
        self.combo.addItem("Hyperboloids of two sheets")
        self.combo.addItem("Hyperboloids of two sheets")
        #self.combo.activated.connect(self.onActivated)
        self.MyLayout.addWidget(self.combo, 1,2)
        
        
        self.setLayout(self.MyLayout)
        #self.mayavi_widget = MayaviQWidget()

        #self.layout.addWidget(self.mayavi_widget, 1, 1)
        
        #container.show()
        #window = QtGui.QMainWindow()
        #window.setCentralWidget(container)
        #window.show()
    
    def onActivated(self):
        global X,Y,Z,Gauss_Curvature
        print self.combo.text
        #if text=="Helix":
            #Helix()
        
        #if text=="Hyperboloid of one sheet":
            #X,Y,Z,Gauss_Curvature=Hyperboloid_one_sheet()
    


if __name__ =='__main__':
# Exception Handling
    try:
        app = QtGui.QApplication(sys.argv)
        #app = QtGui.QApplication.instance()
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
