from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys,os
import xml.etree.ElementTree as ET

__all__ = ['easyComGui']

class easyComTree(QTreeWidget):
    signalid = 0
    def __init__(self,parent):  
        super(QTreeWidget,self).__init__(parent) 
        self.root =  parent
        list = ['Signal Name','Start Bit','Bit Size','Msg CAN Id','Bus','Format','Init Value','Comment']
        self.setHeaderLabels(QStringList(list))
        self.setColumnWidth(0,150)
        self.setColumnWidth(4,120)
        self.connect(self, SIGNAL('itemSelectionChanged()'),self.itemSelectionChanged)
    def itemSelectionChanged(self):
        try:
            pTree = self.currentItem()
            name = self.itemWidget(pTree,0).text()
            # update Action 
            self.root.qAction1.setText('Delete Signal <%s>'%(name))
            self.root.qAction1.setStatusTip('Delete This Signal <%s> Object, BeCareful as this action is dangerous.'%(name))
            self.root.qAction1.setDisabled(False)
            self.root.qAction2.setDisabled(True)
        except:
            self.root.qAction1.setDisabled(True)
            self.root.qAction2.setDisabled(True)
    def loadXML(self,ROOT):
        # delete all as reload
        for i in range(0,self.topLevelItemCount()):
            self.takeTopLevelItem(0)
        # reload
        SignalList = ROOT.find('SignalList')
        if(SignalList == None):
            return
        for Signal in SignalList:
            self.addSignal(Signal)

    def toXML(self):
        List = ET.Element('SignalList')
        for i in range(0,self.topLevelItemCount()):
            Node = ET.Element('Signal')
            tree = self.topLevelItem(i)
            Node.attrib['name'] = str(self.itemWidget(tree,0).text())
            Node.attrib['start'] = str(self.itemWidget(tree,1).value())
            Node.attrib['size'] = str(self.itemWidget(tree,2).value())
            Node.attrib['canid'] = str(self.itemWidget(tree,3).text())
            Node.attrib['bus'] = str(self.itemWidget(tree,4).currentText())
            Node.attrib['format'] = str(self.itemWidget(tree,5).currentText())
            Node.attrib['init'] = str(self.itemWidget(tree,6).text())
            Node.attrib['comment'] = str(self.itemWidget(tree,7).text())
            List.append(Node)
        return List
    
    def deleteSignal(self):
        self.takeTopLevelItem(self.indexOfTopLevelItem(self.currentItem()))
    def addSignal(self,Node=None):
        treeItem = QTreeWidgetItem()
        self.addTopLevelItem(treeItem) 
        if(Node != None):
            sname = Node.attrib['name']
            sstart = int(Node.attrib['start'])
            ssize = int(Node.attrib['size'])
            scanid = Node.attrib['canid']
            sbus = Node.attrib['bus']
            sformat = Node.attrib['format']
            sinit = Node.attrib['init']
            scomment = Node.attrib['comment']
        else:  
            sname =  'Signal%s'%(self.signalid)
            sstart = 0
            ssize  = 8  
            scanid = '0x???' 
            sbus = 'CAN_CTRL_0'
            sformat = 'Motorola'
            sinit = '0x00'
            scomment = ''
        name = QLineEdit(sname)
        start = QSpinBox()
        start.setToolTip("""It is the same with the Vector CANoe Motorola Format
| Map    | BIT7 | BIT6 | BIT5 | BIT4 | BIT3 | BIT2 | BIT1 | BIT0 |
| Byte 0 |   63 |   62 |   61 |   60 |   59 |   58 |   57 |   56 |
| Byte 1 |   55 |   54 |   53 |   52 |   51 |   50 |   49 |   48 |
| Byte 2 |   47 |   46 |   45 |   44 |   43 |   42 |   41 |   40 |
| Byte 3 |   39 |   38 |   37 |   36 |   35 |   34 |   33 |   32 |
| Byte 4 |   31 |   30 |   29 |   28 |   27 |   26 |   25 |   24 |
| Byte 5 |   23 |   22 |   21 |   20 |   19 |   18 |   17 |   16 |
| Byte 6 |   15 |   14 |   13 |   12 |   11 |   10 |    9 |    8 |
| Byte 7 |    7 |    6 |    5 |    4 |    3 |    2 |    1 |    0 |""")
        start.setRange(0,63)
        start.setValue(sstart)
        size = QSpinBox()
        size.setRange(0,32)  
        size.setValue(ssize)
        canid = QLineEdit(scanid)
        bus = QComboBox()
        bus.addItems(QStringList(['CAN_CTRL_0','CAN_CTRL_1','CAN_CTRL_2','CAN_CTRL_3','CAN_CTRL_4']))
        bus.setCurrentIndex(bus.findText(sbus))
        format = QComboBox()
        format.addItems(QStringList(['Motorola']))
        format.setCurrentIndex(format.findText(sformat))
        init = QLineEdit(sinit)
        comment = QLineEdit(scomment)
        self.setItemWidget(treeItem,0,name)    
        self.setItemWidget(treeItem,1,start) 
        self.setItemWidget(treeItem,2,size) 
        self.setItemWidget(treeItem,3,canid) 
        self.setItemWidget(treeItem,4,bus)
        self.setItemWidget(treeItem,5,format) 
        self.setItemWidget(treeItem,6,init) 
        self.setItemWidget(treeItem,7,comment) 
        self.signalid += 1
        
    
class easyDcmTree(QTreeWidget):
    def __init__(self,parent):  
        super(QTreeWidget,self).__init__(parent) 
        self.root =  parent
        list = ['Service Name','Stack Size','Priority','Activation','Autostart','Schedule']
        self.setHeaderLabels(QStringList(list))
        self.setColumnWidth(0,150)
        self.connect(self, SIGNAL('itemSelectionChanged()'),self.itemSelectionChanged)
    def itemSelectionChanged(self):
        pass
    def loadXML(self,ROOT):
        # delete all as reload
        for i in range(0,self.topLevelItemCount()):
            self.takeTopLevelItem(0)
        # reload

    def toXML(self):
        List = ET.Element('TODOList')
        for i in range(0,self.topLevelItemCount()):
            Node = ET.Element('TODO')
            tree = self.topLevelItem(i)
            Node.attrib['name'] = str(self.itemWidget(tree,0).text())
            List.append(Node)
        return List

class easyComCfgTree(QTreeWidget):
    def __init__(self,parent=None):  
        super(QTreeWidget,self).__init__(parent)
        self.setHeaderLabel('easyCom')
        self.addTopLevelItem(QTreeWidgetItem(QStringList('Com')))
        self.addTopLevelItem(QTreeWidgetItem(QStringList('Dcm')))
        self.setMaximumWidth(200); 

class easyComGui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        self.easyTree = easyComCfgTree(self)
        self.easyComTree = easyComTree(self)
        self.easyDcmTree = easyDcmTree(self)
        self.qSplitter = QSplitter(Qt.Horizontal,self)
        self.creMenu()
        self.creGui()
        
    def creMenu(self):
        #  create Three three Action
        self.qAction1=QAction(self.tr('Action1'),self) 
        self.connect(self.qAction1,SIGNAL('triggered()'),self.mqAction1) 
        self.menuBar().addAction(self.qAction1)
        self.qAction1.setDisabled(True)
        
        self.qAction2=QAction(self.tr('Action2'),self) 
        self.connect(self.qAction2,SIGNAL('triggered()'),self.mqAction2) 
        self.menuBar().addAction(self.qAction2)
        self.qAction2.setDisabled(True)
    def mqAction1(self):
        if(self.qAction1.text() == 'Add Signal'):
            self.easyComTree.addSignal()
        elif(str(self.qAction1.text()).find('Delete Signal') != -1):
            self.easyComTree.deleteSignal()
    def mqAction2(self):
        pass

    def creGui(self):
        self.qSplitter.insertWidget(0,self.easyTree)
        self.qSplitter.insertWidget(1,self.easyComTree)
        self.qSplitter.insertWidget(1,self.easyDcmTree)
        self.showTableWidget(self.easyComTree)
        self.setCentralWidget(self.qSplitter)
        self.connect(self.easyTree,SIGNAL('itemClicked(QTreeWidgetItem*, int)'),self.easyTreeClicked)  
    def showTableWidget(self,widget):
        if(self.easyDcmTree == widget):
            self.qAction1.setDisabled(True)
            self.qAction2.setDisabled(True)            
            self.easyDcmTree.setVisible(True);
        else:
            self.easyDcmTree.setVisible(False);
            
        if(self.easyComTree == widget):
            self.qAction1.setText('Add Signal')
            self.qAction1.setStatusTip('Add Signal for COM')
            self.qAction1.setDisabled(False)
            self.qAction2.setDisabled(True)
            self.easyComTree.setVisible(True);
        else:
            self.easyComTree.setVisible(False);
    def easyTreeClicked(self,item,column):
        if(item.text(0) == 'Com'):
            self.showTableWidget(self.easyComTree)
        elif(item.text(0) == 'Dcm'):
            self.showTableWidget(self.easyDcmTree)
    def mOpen(self,pdir):
        wfxml = '%s/com.wfxml'%(pdir)
        root = ET.parse(wfxml).getroot();
        self.easyComTree.loadXML(root)
        self.easyDcmTree.loadXML(root)
        self.qAction1.setDisabled(True)
        self.qAction2.setDisabled(True)
    def mSave(self,pdir):
        wfxml = '%s/com.wfxml'%(pdir)
        ROOT = ET.Element('COMROOT')
        ROOT.append(self.easyComTree.toXML())
        ROOT.append(self.easyDcmTree.toXML())
        tree = ET.ElementTree(ROOT)
        tree.write(wfxml, encoding="utf-8", xml_declaration=True);
    def mGen(self,pdir):
        return
        from gen.GenCom import GenCom
        wfxml = '%s/com.wfxml'%(pdir)
        GenCom(str(wfxml))