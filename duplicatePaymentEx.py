
import os
import traceback
import numpy
import pandas
import rapidfuzz as rapidfuz
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox, QLineEdit

# from otherPy.UpdateLabelThread import UpdateLabelThread
from userform.duplicatePayment import  duplicatePayment

class duplicatePaymentEx(duplicatePayment):
    def __init__(self):
        super(duplicatePaymentEx, self).__init__()
        self.button_browseFile1.clicked.connect(self.browseFile1)
        self.button_browseFile2.clicked.connect(self.browseFile2)
        self.button_addTo1.clicked.connect(self.add1)
        self.button_addTo2.clicked.connect(self.add2)
        self.button_removeTo1.clicked.connect(self.remove1)
        self.button_removeTo2.clicked.connect(self.remove2)
        self.listWidget_finalFile1.itemDoubleClicked.connect(self.addToUnique1)
        self.listWidget_finalFile2.itemDoubleClicked.connect(self.addToUnique2)
        self.listWidget_uniqueFile1.itemDoubleClicked.connect(self.removeToUnique1)
        self.listWidget_uniqueFile2.itemDoubleClicked.connect(self.removeToUnique2)
        self.button_addToQuantify1.clicked.connect(self.addToQuantify1)
        self.button_addToQuantify2.clicked.connect(self.addToQuantify2)
        self.button_removeQuantify1.clicked.connect(self.removeToQuantify1)

        # self.button_remove.clicked.connect(self.removeToQuantify2)

        # self.button_browseSaveTo.clicked.connect(self.button_browseSaveTo)
            self.button_submit.clicked.connect(self.testingThread)
        # self.button_submit.clicked.connect(self.submit)
        self.button_clear.clicked.connect(self.clear)
        self.line_file1Path.textChanged.connect(self.clearFieldOnChangeSelectFile1)
        self.line_file2Path.textChanged.connect(self.clearFieldOnChangeSelectFile2)
        self.progressBar.setHidden(True)

    def removeToQuantify1(self):
        try:
            item=self.listwidget_quantify1.selectedItems()[0]
            rowNumber=self.listwidget_quantify1.row(item)
            self.listwidget_qunatify1.takeitem(rowNumber)
        except IndexError:
            QMessageBox.critical(self,"Error","Please choose item from list")
        except BaseException as e:
            QMessageBox.critical(self,"Error",str(e))


    def removeToQuantify2(self):
        try:
            item=self.listwidget_quantify1.selectedItems()[0]
            rowNumber=self.listwidget_quantify2.row(item)
            self.listwidget_qunatify2.takeitem(rowNumber)
        except IndexError:
            QMessageBox.critical(self,"Error","Please choose item from list")
        except BaseException as e:
            QMessageBox.critical(self,"Error",str(e))

    def addToQuantify1(self):
        try:
            item=self.listWidget_chooseFile1.selectedItems()[0]
            self.listWidget_quantify1.addItem(item.text())
        except IndexError:
            QMessageBox.critical(self,"Error","Please choose item from list")
        except BaseException as e:
            QMessageBox.critical(self,"Error",str(e))

    def addToQuantify2(self):
        try:
            item = self.listWidget_chooseFile2.selectedItems()[0]
            self.listWidget_quantify2.addItem(item.text())
        except IndexError:
            QMessageBox.critical(self, "Error", "Please choose item from list")
        except BaseException as e:
            QMessageBox.critical(self, "Error", str(e))

    def browseSaveTo(self):
        try:
            desktopPath=os.path.expanduser("~/Documents")
            filePath=QFileDialog.getExistingDirectory(self,"Select file",desktopPath)
            self.line_saveToPath.setText(filePath)
        except BaseException as e:
            QMessageBox.critical(self,"Error",str(e))

    def addToAmount1(self):
        try:
            item=self.listWidget_chooseFile1.selectedItems()[0]
            self.line_addToAmount.setText(item.text())
        except IndexError:
            QMessageBox.critical(self,"Error","Please choose item from list")
        except BaseException as e:
            QMessageBox.critical(self,"Error",str(e))


    def addToAmount2(self):
        try:
            item=self.listWidget_chooseFile2.selectedItems()[0]
            self.line_addToAmount.setText(item.text())
        except IndexError:
            QMessageBox.critical(self,"Error","Please choose item from list")
        except BaseException as e:
            QMessageBox.critical(self,"Error",str(e))


    def addToUnique1(self,item):
        try:
            self.listWidget_uniqueFile1.additem(item.text())
        except BaseException as e:
            QMessageBox.critical(self,"Error",str(e))

    def addToUnique2(self, item):
        try:
            self.listWidget_uniqueFile2.additem(item.text())
        except BaseException as e:
            QMessageBox.critical(self, "Error", str(e))

    def removeToUnique1(self,item):
        try:
            rowNumber=self.listWidget_uniqueFile1.row(item)
            self.listWidget_uniqueFile1.takeItem(rowNumber)
        except BaseException as e:
            QMessageBox.critical(self,"Error",str(e))

    def removeToUnique2(self, item):
        try:
            rowNumber = self.listWidget_uniqueFile2.row(item)
            self.listWidget_uniqueFile2.takeItem(rowNumber)
        except BaseException as e:
            QMessageBox.critical(self, "Error", str(e))

    def add1(self):
        try:
            item=self.listWidget_chooseFile1.selectedItems()[0]
            self.listWidget_finalFile1.addItem(item.text())
            rowNumber=self.listWidget_chooseFile1.row(item)
            self.listWidget_chooseFile1.takeItem(rowNumber)
        except IndexError:
            QMessageBox.critical(self,"Error","Please choose item from list")
        except BaseException as e:
            QMessageBox.critical(self,"Error",str(e))

    def add2(self):
        try:
            item = self.listWidget_chooseFile2.selectedItems()[0]
            self.listWidget_finalFile2.addItem(item.text())
            rowNumber = self.listWidget_chooseFile2.row(item)
            self.listWidget_chooseFile2.takeItem(rowNumber)
        except IndexError:
            QMessageBox.critical(self, "Error", "Please choose item from list")
        except BaseException as e:
            QMessageBox.critical(self, "Error", str(e))

    def remove1(self):
        try:
            item=self.listWidget_finalFile1.selectedItems()[0]
            self.listWidget_chooseFile1.addItem(item.text())
            rowNumber=self.listWidget_finalFile1.row(item)
            self.listWidget_finalFile1.takeItem(rowNumber)
        except IndexError:
            QMessageBox.critical(self,"Error","Please choose item from list")
        except BaseException as e:
            QMessageBox.critical(self,"Error",str(e))

    def remove2(self):
        try:
            item = self.listWidget_finalFile2.selectedItems()[0]
            self.listWidget_chooseFile2.addItem(item.text())
            rowNumber = self.listWidget_finalFile2.row(item)
            self.listWidget_finalFile2.takeItem(rowNumber)
        except IndexError:
            QMessageBox.critical(self, "Error", "Please choose item from list")
        except BaseException as e:
            QMessageBox.critical(self, "Error", str(e))

    def browseFile1(self):
        try:
            try:
                desktopPath=os.path.expanduser("~/Documents/")
                filePath=QFileDialog.getOpenFileName(self,"Select file",desktopPath,"CSV files (*.csv)")
                self.line_file1path.setText(filePath[0])
                df=self.readCsvFile(self.line_file1path.text())
            except FileNotFoundError:
                return
            except BaseException as e:
                traceback.print_exc()
                QMessageBox.critical(self,"Error",str(e))
                return
            rowHeader=df[0]
            rowheader=[ str(x) for x in rowHeader]
            for i in rowHeader:
                if i=='nan':
                    continue
                self.listWidget_chooseFile1.addItem(i)
            rowCount=len(df)
            columnCount=df.shape[1]
            self.tableWidget_file1.setRowCount(rowCount)
            self.tableWidget_file1.setColumnCount(columnCount)
            r=0
            for eachtuple in df:
                c=0
                for eachItem in eachtuple:
                    self.tableWidget_file1.setItem(r,c,QTableWidgetItem(str(eachItem)))
                    c=c+1
                r=r+1

        except BaseException as e:
            traceback.print_exc()
            QMessageBox.critical(self,"Error",str(e))
            return

    def clearFieldOnChangeSelectFile1(self):
        self.tableWidget_file1.clear()
        self.listWidget_chooseFile1.clear()
        self.listWidget_finalFile1.clear()
        self.listWidget_uniqueFile1.clear()
        self.listWidget_quantify1.clear()

    def readCsvFile(self,filePath):
        df=pandas.read_csv(filePath,header=None,encoding="ISO-8859-1")
        df=df.head(10)
        df=df.values
        return df

    def browseFile2(self):
        try:
            try:
                desktopPath = os.path.expanduser("~/Documents/")
                filePath = QFileDialog.getOpenFileName(self, "Select file", desktopPath, "CSV files (*.csv)")
                self.line_file2path.setText(filePath[0])
                df = self.readCsvFile(self.line_file2path.text())
            except FileNotFoundError:
                return
            except BaseException as e:
                traceback.print_exc()
                QMessageBox.critical(self, "Error", str(e))
                return
            rowHeader = df[0]
            rowheader = [str(x) for x in rowHeader]
            for i in rowHeader:
                if i == 'nan':
                    continue
                self.listWidget_chooseFile2.addItem(i)
            rowCount = len(df)
            columnCount = df.shape[1]
            self.tableWidget_file1_2.setRowCount(rowCount)
            self.tableWidget_file1_2.setColumnCount(columnCount)
            r = 0
            for eachtuple in df:
                c = 0
                for eachItem in eachtuple:
                    self.tableWidget_file1_2.setItem(r, c, QTableWidgetItem(str(eachItem)))
                    c = c + 1
                r = r + 1

        except BaseException as e:
            traceback.print_exc()
            QMessageBox.critical(self, "Error", str(e))
            return
    def clearFieldOnChangeSelectFile2(self):
        self.tableWidget_file1_2.clear()
        self.listWidget_chooseFile2.clear()
        self.listWidget_finalFile2.clear()
        self.listWidget_uniqueFile2.clear()
        self.listWidget_quantify2.clear()

    def getConcatenatedColumn(self,df,columnListToConcatenate:list,resultColumnName:str="concateCols"):
        df[resultColumnName]=df[columnListToConcatenate].apply(lambda raw:"".join(raw.valuesastype(str)),axis=1)
        return df

    def updateLabel(self,x):
        self.progressBar.setvalue(x)

    def setMaxLimit(self,x):
        self.progressBar.setMaximum(x)

    def errorRaise(self,errorString):
        self.updateLabel(0)
        self.progressBar.setHidden(True)
        QMessageBox.critical(self,"Error",errorString)

    def completeSuccess(self):
        self.progressBar.setHidden(True)
        QMessageBox.information(self,"Status","Completed")

    def testingThread(self):
        self.progressBar.setHidden(False)
        labelThread=UpdateLabelThread(self.listWidget_finalFile1,self.listWidget_finalFile2,self.listWidget_quantify1,self.listWidget_quantify2,self.listWidget_uniqueFile1,self.listWidget_uniqueFile2,self.line_file1Path,self.line_file2Path,self.line_numberOfSearch,self.line_percentage,self.line_saveToPath)
        labelThread.numberSignal.connect(self.updateLabel)
        labelThread.errorSignal.connect(self.errorRaise)
        labelThread.completedSuccessfulSignal.connect(self.completeSuccess)
        labelThread.setMaxSignal.connect(self.setMaxLimit)
        labelThread.start()
        
    def clear(self):
        self.line_file1Path.clear()
        self.line_file2Path.clear()
        self.tableWidget_file1.clear()
        self.tableWidget_file1_2.clear()
        self.listWidget_chooseFile1.clear()
        self.listWidget_chooseFile2.clear()
        self.listWidget_chooseFile2.clear()
        self.listWidget_chooseFile1.clear()
        self.listWidget_finalFile1.clear()
        self.listWidget_finalFile2.clear()
        self.listWidget_uniqueFile1.clear()
        self.listWidget_uniqueFile2.clear()
        self.line_numberOfSearch.clear()
        self.line_percentage.clear()
        self.line_saveToPath.clear()
        self.listWidget_quantify1.clear()
        self.listWidget_quantify2.clear()
        self.updateLabel(0)
        self.setMaxLimit(100)


# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QFrame
# # from userform import icons
#
# class duplicatePayment(QFrame):
#     def __init__(self):
#         super(duplicatePayment, self).__init__()
#         self.setupUi()
#
#     def setupUi(self):
#         Fram e =self