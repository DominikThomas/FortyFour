from PyQt4 import QtCore, QtGui # Import the PyQt4 module we'll need
import sys # We need sys so that we can pass argv to QApplication

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

import rozhrani, FortyThree # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer

class FortyFour(QtGui.QMainWindow, rozhrani.Ui_Dialog, FortyThree.Vypocet):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.Forty_Three)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), self.reject)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Prochazet)
        self.slozka = None
        
    def Prochazet(self):
        self.slozka = QtGui.QFileDialog.getExistingDirectory()
        self.textBrowser.setText('Byla vybrána složka %s' %(self.slozka))
    
    def reject(self):
        exit(0)
        
def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = FortyFour()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function