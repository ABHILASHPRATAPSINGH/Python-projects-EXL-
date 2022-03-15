import time
from threading import Thread
import pandas
import rapidfuzz
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from userform.duplicatePayment import duplicatePayment

class UpdateLabelThread(Thread,QObject):
    numberSignal=pyqtSignal(int)
    setmaxSignal=pyqtSignal(int)
    completeSuccessfulSignal=pyqtSignal()
    errorSignal=pyqtSignal(str)

    def __init__(self,listwidget_finalFile1,listwidget_finalFile2,listwidget_quantify1,listwidget_quantify2,listwidget_uniqueFile1,listwidget_uniqueFile2,line_file1Path,line_file2Path,line_numberOfSearch,line_percentage,line_saveToPath):
        Thread.__init__(self)
        QObject.__init__()
        self.listwidget_finalFile1=listwidget_finalFile1
        self.listwidget_finalFile2=listwidget_finalFile2
        self.listwidget_quantify1=listwidget_quantify1
        self.listwidget_quantify2=listwidget_quantify2
        self.listwidget_uniqueFile1=listwidget_uniqueFile1
        self.listwidget_uniqueFile2=listwidget_uniqueFile2
        self.line_file1Path=line_file1Path
        self.line_file2Path=line_file2Path
        self.line_numberOfSearch=line_numberOfSearch
        self.line_percentage=line_percentage
        self.line_saveToPath=line_saveToPath

    def run(self) -> None:
        try:
            itemsFinalFile1List=[]
            for i in range(self.listwidget_finalFile1.count()):
                itemsFinalFile1List.append(self.listwidget_finalFile1.item(i).text())

            itemsFinalFile2List=[]
            for i in range(self.listwidget_finalFile2.count()):
                itemsFinalFile2List.append(self.listwidget_finalFile2.item(i).text())

            itemsQuantify1=[]
            for i in range(self.listwidget_quantify1.count()):
                itemsQuantify1.append(self.listwidget_quantify1.item(i).text())

            itemsQuantify2=[]
            for i in range(self.listwidget_quantify2.count()):
                itemsQuantify2.append(self.listwidget_quantify2.item(i).text())

            itemsUnique1List=[]
            for i in range(self.listwidget_uniqueFile1.count()):
                itemsUnique1List.append(self.listwidget_uniqueFile1.item(i).text())


            itemsUnique2List = []
            for i in range(self.listwidget_uniqueFile2.count()):
                itemsUnique2List.append(self.listwidget_uniqueFile2.item(i).text())


            if self.line_file1Path.text()=="" or self.line_file2Path.text()=="":
                errorString="Field : '{} can't blank. Please Check".format("Select File")
                self.errorSignal.emit(errorString)
                return

            if len(itemsFinalFile1List)==0 or len(itemsFinalFile2List)==0:
                errorString="Field : '{}' can't be empty. Please select atleaset one item".format("Final Items")
                self.errorSignal.emit(errorString)
                return

            if len(itemsQuantify1)!=len(itemsQuantify2):
                errorString="Number of items in Field 'Qantify items' must be equal. Please Check"
                self.errorSignal.emit(errorString)
                return

            if len(itemsUnique1List)!=len(itemsUnique2List):
                errorString="Number of items in Field 'Unique items' must be equal. Please Check"
                self.errorSignal.emit(errorString)
                return

            numberOfSearch=self.line_numberOfSearch.text()
            try:
                numberOfSearch=int(numberOfSearch)
            except ValueError:
                errorString="Field : 'No of Search' must be integer, provided '{}' ".format(numberOfSearch)
                self.errorSignal.emit(errorString)
                return

            thresholdPercentage=self.line_percentage.text()
            try:
                thresholdPercentage=float(thresholdPercentage)
            except ValueError:
                errorString="Field : '% threshold' must be numeric, provided '{}' ".format(thresholdPercentage)
                self.errorSignal.emit(errorString)
                return

            saveToPath=self.line_saveToPath.text()
            if saveToPath=="":
                errorString="Field : 'Save to' can't blank. Please select folder"
                self.errorSignal.emit(errorString)
                return

            file1=self.line_file1Path.text()
            df1=pandas.read_csv(file1,thousands=",",encoding="ISO-8859-1")
            df1=self.getConcatenatedColumn(df1,itemsFinalFile1List,"concateColumns1")

            try:
                for item in itemsQuantify1:
                    pandas.to_numeric(df1[item])
            except ValueError:
                errorString="Field : '{}' contains string data, File : '{}' please check".format("Quantify items",file1)
                self.errorSignal.emit(errorString)
                return

            file2 = self.line_file2Path.text()
            df2 = pandas.read_csv(file2, thousands=",", encoding="ISO-8859-1")

            try:
                for item in itemsQuantify2:
                    pandas.to_numeric(df2[item])
            except ValueError:
                errorString = "Field : '{}' contains string data, File : '{}' please check".format("Quantify items", file2)
                self.errorSignal.emit(errorString)
                return

            df2 = self.getConcatenatedColumn(df2, itemsFinalFile2List, "concateColumns2")
            df2['rowIndex']=df2.index+1

            finalDf=pandas.DataFrame({})
            self.setMaxSignal.emit(df1.shape[0]-1)

            for i in range(df1.shape[0]):
                rowDF1=df1.iloc[i,:].to_frame().transpose()

                if len(itemsUnique1List)!=0:
                    filterDF2=df2.merge(rowDF1,left_on=itemsUnique2List, right_on=itemsUnique1List,suffixed=('','y'))
                    filterDF2=filterDF2[df2.columns]

                else:
                    filterDF2=df2
                l1=rowDF1["concateColumns1"]
                l2=filterDF2['concateColumns2']

                score=rapidfuzz.process.extract(l1.to_list(),l2.to_list(),limit=numberOfSearch)
                score=pandas.DataFrame(score,columns=['concat','Score','rowNumber'])
                score=score.set_index(["rowNumber"])
                score=score[score["Score"]]>=thresholdPercentage

                k=score.join(filterDF2,how='left')
                k=k.reset_index(drop=True)
                rowDF1=rowDF1.reset_index(drop=True)
                dd=pandas.concat([rowDF1,k],axis=1)

                if len(itemsQuantify1)>0 and len(itemsQuantify2)>0:
                    rowCount=1
                    for leftItem, rightItem in zip(itemsQuantify1,itemsQuantify2):
                        qun=k[rightItem].cumsum()
                        lQun=rowDF1[leftItem].to_list()[0]
                        quant=qun-lQun
                        columnName='Absolute_'+ leftItem+str(rowCount)
                        dd[columnName]=quant
                        rowCount=rowCount+1

                dd['Batch Number']=i+1
                dd=dd.append(pandas.Series(),ignore_index=True)
                finalDf=finalDf.append(dd)
                self.numberSignal.emit(i)

            filePath=saveToPath+"/Consolidated_Result.csv"
            try:
                finalDf.to_csv(filePath,index=False)

            except PermissionError:
                errorString="Error", "'{}' file already opened".format("Consolidated_Result.csv")
                self.errorSignal.emit(errorString)
                return

            self.completedSuccessfulSignal.emit()
        except BaseException as e:
            errorString=str(e)
            self.errorSignal.emit(errorString)

    def getConcatenatedColumn(self,df,columnListToConcatenate:list,resultColumnName:str="concateCols"):
        df[resultColumnName]=df[columnListToConcatenate].apply(lambda raw: "".join(raw.values.astype(str)),axis=1)
        return df



