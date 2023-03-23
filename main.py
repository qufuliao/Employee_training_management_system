# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_me.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
#导入程序运行必须模块
import sys

from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QColor, QBrush
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem, QMessageBox

#导入designer工具生成的login模块
from w1 import Ui_Form
from w2 import Ui_Form as Ui_Form2
from w3 import Ui_Form as Ui_Form3
from w4 import Ui_Form as Ui_Form4
from w5 import  Ui_Form as Ui_Form5
from w6 import  Ui_Form as Ui_Form6
import pymssql

class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.password = None
        self.username = None
        self.setupUi(self)
        self.secondForm = SecondForm()
        self.thirdForm=ThirdForm()
        self.fifthForm=FifthForm()
        #添加登录按钮信号和槽。注意display函数不加小括号()
        self.login_Button.clicked.connect(self.login)
        #添加退出按钮信号和槽。调用close函数
        self.cancel_Button.clicked.connect(self.close)
        #添加注册按钮信号和槽
        self.register_Button.clicked.connect(self.thirdForm.show)
    def login(self):
        # 利用line Edit控件对象text()函数获取界面输入
        self.username = self.user_lineEdit.text()
        self.password = self.pwd_lineEdit.text()
        serverName = '127.0.0.1:1433'
        self.checkBox.isChecked()
        try:
            # 连接数据库
            self.conn = pymssql.connect(serverName, self.username, self.password, "员工培训管理系统",charset="utf8")
            print(f"连接成功{self.conn}")

            if self.conn:
                if self.checkBox.isChecked():
                    self.user_textBrowser.setText("管理员登录成功！\n")
                    self.fifthForm.conn=self.conn
                    self.fifthForm.uid=self.username
                    self.fifthForm.show()
                else:
                    # 利用text Browser控件对象setText()函数设置界面显示
                    self.user_textBrowser.setText("登录成功!\n")
                    self.secondForm.conn=self.conn
                    self.secondForm.username=self.username
                    self.secondForm.show()
                    #self.conn.close()
        except :
            print("\n连接失败")
            # 利用text Browser控件对象setText()函数设置界面显示
            self.user_textBrowser.setText("登录失败!\n")
class SecondForm(QMainWindow, Ui_Form2):
    username=None
    conn=None
    def __init__(self, parent=None):
        super(SecondForm, self).__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.query)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.all_courses_Button.clicked.connect(self.all_courses)
        self.selected_Button.clicked.connect(self.selected_courses)
        self.tableWidget.itemClicked.connect(self.insert_courses)
        self.buttonBox.rejected.connect(lambda : self.tableWidget.setRowCount(0))
        self.information_Button.clicked.connect(self.openInformation)
    def query(self):#查询课程
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        cursor = self.conn.cursor()
        cid=int(self.cid_lineEdit.text() if self.cid_lineEdit.text() != "" else "0")
        name=self.cname_lineEdit.text()
        teacher=self.teacher_lineEdit.text()
        type=self.type_comboBox.currentText()
        sql=f"SELECT * FROM COURSES WHERE cid={cid} AND name='{name}' OR teacher='{teacher}' OR type='{type}'" + (' order by time' if self.time_order.isChecked() else '')
        cursor.execute(sql)
        items=cursor.fetchall()
        self.tableWidget.clear()
        for i in range(len(items)):
            item = items[i]
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            for j in range(len(item)):
                item = QTableWidgetItem(str(items[i][j]))
                self.tableWidget.setItem(row, j, item)
    def all_courses(self):#显示所有课程
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        cursor = self.conn.cursor()
        sql='SELECT * FROM COURSES' + (' order by time' if self.time_order.isChecked() else '')
        cursor.execute(sql)
        items = cursor.fetchall()
        if len(items)==0:
            return
        for i in range(len(items)):
            item = items[i]
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            for j in range(len(item)):
                item = QTableWidgetItem(str(items[i][j]))
                self.tableWidget.setItem(row, j, item)
    def selected_courses(self):#显示已选课程
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        cursor = self.conn.cursor()
        sql=f"SELECT * FROM COURSES, UCR WHERE UCR.uid={self.username} AND COURSES.cid=UCR.cid" + (' order by time' if self.time_order.isChecked() else '')
        cursor.execute(sql)
        items = cursor.fetchall()
        if len(items)==0:
            return
        for i in range(len(items)):
            item = items[i]
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            for j in range(len(item)):
                item = QTableWidgetItem(str(items[i][j]))
                self.tableWidget.setItem(row, j, item)
    def insert_courses(self,Item=None):#选课
        if Item is None:
            return
        else:
            col = Item.column()
            cid= Item.text()
        if col==0:
            #把选中的格子颜色变为蓝色
            Item.setBackground(QBrush(QColor(30,144,255)))
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM UCR WHERE uid=%d AND cid=%d', (int(self.username),int(cid)))
            if cursor.fetchone()==None:
                cursor.execute('INSERT INTO UCR VALUES (%d, %d, NULL)', (int(self.username),int(cid)))
                self.conn.commit()
            else:
                cursor.execute('DELETE FROM UCR WHERE uid=%d AND cid=%d', (int(self.username), int(cid)))
                self.conn.commit()
    def openInformation(self):#打开个人信息界面
        self.forthForm = ForthForm()
        self.forthForm.conn = self.conn
        self.forthForm.uid = self.username
        self.forthForm.show()
        self.forthForm.display()
class ThirdForm(QMainWindow, Ui_Form3):
    def __init__(self, parent=None):
        super(ThirdForm, self).__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.register)
    def register(self):#注册
        conn=pymssql.connect(server = '127.0.0.1:1433', database = "员工培训管理系统")
        cursor=conn.cursor()
        cursor.execute('Select Count(*) From USERS')
        n=cursor.fetchone()[0]
        name=self.lineEdit.text()
        sex=self.lineEdit_2.text()
        age=int(self.lineEdit_3.text())
        dept=self.lineEdit_4.text()
        identity=self.lineEdit_5.text()
        password=self.lineEdit_6.text()
        cursor.execute('insert into USERS values( %d, %s, %s, %d, %s, %s)', ( n+1, name, sex, age, dept, identity))
        cursor.execute(f"create login [{(n+1)}] with password='{password}', default_database=员工培训管理系统")
        cursor.execute(f"create user [{(n+1)}] for login [{(n+1)}] with default_schema=员工培训管理系统")
        conn.commit()
        self.textBrowser.setText("注册成功\n")
        conn.close()
        self.close()
class ForthForm(QMainWindow, Ui_Form4):
    conn=None
    uid=None
    def __init__(self, parent=None):
        super(ForthForm, self).__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.updateInformation)
    def display(self):#显示个人信息
        cursor = self.conn.cursor()
        cursor.execute('Select * From USERS WHERE uid=%d', self.uid)
        inf=list(map(str,cursor.fetchone()))
        self.lineEdit.setText(inf[1])
        self.lineEdit_2.setText(inf[2])
        self.lineEdit_3.setText(inf[3])
        self.lineEdit_4.setText(inf[4])
        self.lineEdit_5.setText(inf[5])
    def updateInformation(self):#更新个人信息
        cursor = self.conn.cursor()
        name=self.lineEdit.text()
        sex=self.lineEdit_2.text()
        age=int(self.lineEdit_3.text())
        dept=self.lineEdit_4.text()
        identity=self.lineEdit_5.text()
        password=self.lineEdit_6.text()
        if password == '':
            a = QMessageBox.warning(self, "警告对话框", "密码为空，你确定要继续？",QMessageBox.Yes | QMessageBox.No)
            if a == QMessageBox.No:
                self.close()
                return
        cursor.execute('UPDATE USERS SET name=%s , sex=%s , age=%d , department=%s , [identity]=%s WHERE uid=%d', ( name,sex,age,dept,identity,int(self.uid) ))
        cursor.execute(f"ALTER LOGIN [{self.uid}] WITH PASSWORD = '{password}'")
        self.conn.commit()
        self.close()
class FifthForm(QMainWindow, Ui_Form5):
    conn=None
    uid=None
    def __init__(self, parent=None):
        super(FifthForm, self).__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.query)
        self.information_Button.clicked.connect(self.openInformation)
        self.buttonBox_2.accepted.connect(self.insert_courses)
        self.delete_Button.clicked.connect(self.openDelete)
    def query(self):#查询
        if self.radioButton.isChecked():
            self.query_courses()
    def query_students(self):#查询学生
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        cursor = self.conn.cursor()
        name = self.lineEdit_2.text()
        cursor.execute(f"SELECT uid,name FROM USERS WHERE name like '{name}%'")
        items = cursor.fetchall()
        self.tableWidget.clear()
        for i in range(len(items)):
            item = items[i]
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            for j in range(len(item)):
                item = QTableWidgetItem(str(items[i][j]))
                self.tableWidget.setItem(row, j, item)
    def query_courses(self):#查询课程
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        cursor = self.conn.cursor()
        cname=self.lineEdit.text()
        cursor.execute(f"SELECT cid,name FROM COURSES WHERE name like '{cname}%'")
        items = cursor.fetchall()
        self.tableWidget.clear()
        for i in range(len(items)):
            item = items[i]
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            for j in range(len(item)):
                item = QTableWidgetItem(str(items[i][j]))
                self.tableWidget.setItem(row, j, item)
    def insert_courses(self):#插入课程
        cursor = self.conn.cursor()
        cursor.execute('Select Count(*) From COURSES')
        n = cursor.fetchone()[0]
        cname=self.lineEdit_3.text()
        context=self.lineEdit_4.text()
        time=self.lineEdit_5.text()
        start=self.lineEdit_6.text()
        end=self.lineEdit_7.text()
        teacher=self.lineEdit_8.text()
        tid=int(self.lineEdit_9.text())
        type=self.comboBox.currentText()
        cursor.execute(f"insert into COURSES values( {n+1}, '{cname}', '{context}', '{time}', '{start}', '{end}', '{teacher}',{tid},'{type}')")
        self.conn.commit()
    def openInformation(self):#打开个人信息
        self.forthForm = ForthForm()
        self.forthForm.conn = self.conn
        self.forthForm.uid = self.uid
        self.forthForm.show()
        self.forthForm.display()
    def openDelete(self):#打开删除课程
        self.sixthForm=SixthForm()
        self.sixthForm.conn=self.conn
        self.sixthForm.uid=self.uid
        self.sixthForm.show()
class SixthForm(QMainWindow, Ui_Form6):
    conn=None
    uid=None
    def __init__(self, parent=None):
        super(SixthForm, self).__init__(parent)
        self.deleteList = list()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.query)
        self.all_courses_Button.clicked.connect(self.all_courses)
        self.tableWidget.itemClicked.connect(self.insert_courses)
        self.selected_Button.clicked.connect(self.selected_courses)
        self.delete_Button.clicked.connect(self.delete_courses)
    def query(self):#查询
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        cursor = self.conn.cursor()
        cid=self.cid_lineEdit.text()
        name=self.cname_lineEdit.text()
        teacher=self.teacher_lineEdit.text()
        type=self.type_comboBox.currentText()
        cursor.execute('SELECT * FROM COURSES WHERE cid=%s OR name=%s OR teacher=%s OR type=%s', (cid, name, teacher, type))
        items=cursor.fetchall()
        self.tableWidget.clear()
        for i in range(len(items)):
            item = items[i]
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            for j in range(len(item)):
                item = QTableWidgetItem(str(items[i][j]))
                self.tableWidget.setItem(row, j, item)
    def all_courses(self):#显示所有课程
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM COURSES')
        items = cursor.fetchall()
        if len(items)==0:
            return
        for i in range(len(items)):
            item = items[i]
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            for j in range(len(item)):
                item = QTableWidgetItem(str(items[i][j]))
                self.tableWidget.setItem(row, j, item)
    def insert_courses(self,Item=None):#选中课程
        if Item is None:
            return
        else:
            col = Item.column()
            cid= Item.text()
        if col==0:
            Item.setBackground(QBrush(QColor(255,0,0)))
            self.deleteList.append(cid)
    def selected_courses(self):#显示选中课程
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        cursor = self.conn.cursor()
        for cid in self.deleteList:
            cursor.execute(f"SELECT * FROM COURSES WHERE cid={cid}")
            items = cursor.fetchall()
            if len(items) == 0:
                continue
            for i in range(len(items)):
                item = items[i]
                row = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row)
                for j in range(len(item)):
                    item = QTableWidgetItem(str(items[i][j]))
                    self.tableWidget.setItem(row, j, item)
    def delete_courses(self):#删除选中课程
        cursor = self.conn.cursor()
        for cid in self.deleteList:
            cursor.execute(f"DELETE FROM COURSES WHERE cid={cid}")#删除课程
            self.conn.commit()
        self.deleteList.clear()

if __name__ == "__main__":
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    #初始化
    myWin = MyMainForm()
    #将窗口控件显示在屏幕上
    myWin.show()
    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())