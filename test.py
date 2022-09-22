import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from menu import Ui_MainWindow
import pymysql
from add_book import Add_book
from del_book import Del_book
from del_user import Del_user
from borrow_book import Borrow_book
from return_book import Return_book
import datetime

conn =pymysql.connect(
    host='localhost',
    port=3306,
    user="root",
    password='123456',
    database='total',
    charset='utf8'
)


class main(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

    def login(self):
        layout = QFormLayout()
        label = QLabel('欢迎使用图书借阅系统')
        label.setGeometry(QtCore.QRect(0, 100, 800, 100))
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("隶书",20,QFont.Bold))
        text1 = QLineEdit()
        text2 = QLineEdit()
        btn = QPushButton('登录')
        btn.setFixedSize(50,30)
        btn.setGeometry(QtCore.QRect(300,0,50,30))
        layout.addRow(label)
        layout.addRow('用户名', text1)
        layout.addRow('密码', text2)

        rb1 = QRadioButton('管理员')
        rb2 = QRadioButton('普通用户')
        rb1.setChecked(True)
        layout.addRow(rb1,rb2)

        layout.addRow(btn)
        btn.clicked.connect(lambda:self.login_btn(rb1,rb2,text1,text2))

        self.stack1.setLayout(layout)

    def login_btn(self,a,b,m,n):
        cursor = conn.cursor()
        sql_1 = "select * from manager where user_name='%s' and user_pwd='%s';"%(m.text(),n.text())
        res_1 = cursor.execute(sql_1)
        sql_2 = "select * from consumer where user_name='%s' and user_pwd='%s';"%(m.text(),n.text())
        res_2 = cursor.execute(sql_2)

        window_4.lineEdit_5.setText(m.text())
        window_5.lineEdit_5.setText(m.text())

        if res_1 and a.isChecked():
            QMessageBox.information(self, '消息', '欢迎登录，管理员！！！', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            self.stack.setCurrentIndex(3)
        elif res_2 and b.isChecked():
            QMessageBox.information(self, '消息', '欢迎登录，普通用户！！！', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            self.stack.setCurrentIndex(2)
        else:
            print('用户名或密码错误')
        cursor.close()

    def show_add(self):
        window_1.show()


    def book_del(self):
        window_2.show()

    def user_del(self):
        window_3.update_user()
        window_3.show()

    def jump(self,m,a,b):
        cursor = conn.cursor()
        sql = 'select * from operate;'
        cnt = cursor.execute(sql)
        res = cursor.fetchall()
        a.removeRows(0, a.rowCount())
        x = int(m.text())
        if cnt > x*10:
            left = (x-1)*10
            right = x*10
        else:
            left = (x-1)*10
            if cnt % 10 == 0:
                right = x*10
            else:
                right = (x - 1) * 10 + cnt % 10

        for i in range(left,right):
            for j in range(0,9):
                item = QStandardItem('%s' % (res[i][j]))

                a.setItem(i%10, j, item)

        b.setModel(a)




    def login_manager(self):
        layout1 = QVBoxLayout()
        btn1 = QPushButton('添加书籍')
        btn2 = QPushButton('淘汰书籍')
        btn3 = QPushButton('用户管理')

        layout1.addWidget(btn1)
        layout1.addWidget(btn2)
        layout1.addWidget(btn3)

        layout2 = QHBoxLayout()
        line1 = QLineEdit()
        btn5 = QPushButton('查询')
        Cbox = QComboBox()
        Cbox.addItems(['按书名查询', '按书号查询', '按作者查询', '按分类查询', '按出版社查询'])
        layout2.addWidget(line1)
        layout2.addWidget(btn5)
        layout2.addWidget(Cbox)

        layout3 = QVBoxLayout()
        model = QStandardItemModel(10, 9)
        model.setHorizontalHeaderLabels(['书名', '书号', '作者', '分类', '出版社', '出版时间', '库存', '剩余可借', '总借阅次数'])


        tv = QTableView()
        tv.setModel(model)
        layout3.addLayout(layout2)
        layout3.addWidget(tv)

        layout4 = QHBoxLayout()
        label1 = QLabel('跳转到第')
        line2 = QLineEdit()
        line2.setText('0')
        self.l1 = QLabel('/0页')
        btn6 = QPushButton('跳转')

        btn6.clicked.connect(lambda:self.jump(line2,model,tv))

        btn7 = QPushButton('前一页')
        btn8 = QPushButton('后一页')

        btn7.clicked.connect(lambda: self.step_1(line2, model, tv))
        btn8.clicked.connect(lambda: self.step_2(line2, model, tv))

        layout4.addWidget(label1)
        layout4.addWidget(line2)
        layout4.addWidget(self.l1)
        layout4.addWidget(btn6)
        layout4.addWidget(btn7)
        layout4.addWidget(btn8)

        layout = QGridLayout()
        layout.addLayout(layout1, 0, 0)
        layout.addLayout(layout3, 0, 1)
        layout.addLayout(layout4, 1, 1)

        btn1.clicked.connect(self.show_add)
        btn2.clicked.connect(self.book_del)
        btn3.clicked.connect(self.user_del)
        btn5.clicked.connect(lambda:self.search_by(line1,Cbox,model,tv,line2))

        cursor = conn.cursor()
        sql = 'select * from operate;'
        a = cursor.execute(sql)
        res = cursor.fetchmany(10)
        if a%10 == 0:
            all = a/10
        else:
            all = a / 10 +1
        self.l1.setText('/%s页' % (int(all)))
        model = QStandardItemModel(10, 9)
        model.setHorizontalHeaderLabels(['书名', '书号', '作者', '分类', '出版社', '出版时间', '库存', '剩余可借', '总借阅次数'])
        if(a>10):
            for i in range(0, 10):
                for j in range(0, 9):
                    item = QStandardItem('%s' % (res[i][j]))
                    model.setItem(i, j, item)
        elif a<=10:
            for i in range(0, a):
                for j in range(0, 9):
                    item = QStandardItem('%s' % (res[i][j]))
                    model.setItem(i, j, item)
        tv.setModel(model)

        if (int(a / 10) >= 1):
            line2.setText('1')

        self.stack4.setLayout(layout)



    def register(self):
        layout = QFormLayout()
        label = QLabel('注册')
        label.setGeometry(QtCore.QRect(0, 100, 800, 100))
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("隶书", 20, QFont.Bold))
        line1 = QLineEdit()
        line2 = QLineEdit()
        line3 = QLineEdit()

        layout.addRow(label)
        layout.addRow('用户名', line1)
        layout.addRow('密码', line2)
        layout.addRow('确认密码', line3)
        btn = QPushButton('注册')
        btn.setFixedSize(50, 30)
        layout.addRow(btn)

        btn.clicked.connect(lambda:self.register_btn(line1,line2,line3))

        self.stack2.setLayout(layout)


    def register_btn(self,a,b,c):
        cursor = conn.cursor()
        if b.text() == c.text():
            sql_1 = "select * from consumer where '%s'=consumer.user_name;"%(a.text())
            sql_2 = "insert into consumer(user_name,user_pwd) values(%s,%s);"
            name = a.text()
            pwd = b.text()
            res_1 = cursor.execute(sql_1)
            if not res_1:
                res_2 = cursor.execute(sql_2,[name,pwd])
                conn.commit()
                if res_2:
                    QMessageBox.information(self, '消息', '注册成功！！！', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            else:
                QMessageBox.warning(self, '警告', '此用户已经注册', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        else:
            QMessageBox.warning(self, '警告', '确认密码要和密码一致!!!', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        cursor.close()

    def quit_sys(self):
        sys.exit(app.exec_())

    def display_0(self):
        self.stack.setCurrentIndex(0)

    def display_1(self):
        self.stack.setCurrentIndex(1)

    def book_borrow(self):
        window_4.show()

    def book_return(self):
        window_5.show()

    def set_1(self,m,x,n,a,b):
        cursor = conn.cursor()
        sql1 = "select * from borrow;"
        cnt_1 = cursor.execute(sql1)
        res_1 = cursor.fetchall()
        n.removeRows(0,n.rowCount())
        for i in range(0, cnt_1):
            for j in range(0, 7):
                item = QStandardItem('%s' % (res_1[i][j]))
                n.setItem(i, j, item)
        x.setModel(n)

        sql2 = "select * from return_bo;"
        cnt_2 = cursor.execute(sql2)
        res_2 = cursor.fetchall()
        for i in range(0, cnt_2):
            for j in range(0, 8):
                item = QStandardItem('%s' % (res_2[i][j]))
                b.setItem(i, j, item)
        a.setModel(b)

        m.setCurrentIndex(1)

    def set_2(self,m,x,y):
        cursor = conn.cursor()
        sql = 'select * from operate;'
        cursor.execute(sql)
        res = cursor.fetchmany(10)
        y.removeRows(0,y.rowCount())
        for i in range(0, 10):
            for j in range(0, 9):
                item = QStandardItem('%s' % (res[i][j]))
                y.setItem(i, j, item)
        x.setModel(y)
        m.setCurrentIndex(0)


    def common_login(self):
        layout1 = QVBoxLayout()
        btn1 = QPushButton('借书')
        btn2 = QPushButton('还书')
        btn3 = QPushButton('借阅状态')
        btn4 = QPushButton('所有书籍')
        layout1.addWidget(btn1)
        layout1.addWidget(btn2)
        layout1.addWidget(btn3)
        layout1.addWidget(btn4)



        btn1.clicked.connect(self.book_borrow)
        btn2.clicked.connect(self.book_return)

        stack1 = QWidget()
        stack2 = QWidget()

        m,n,a,b = self.tab1UI(stack1)
        x,y = self.tab2UI(stack2)

        stack = QStackedWidget()
        stack.addWidget(stack2)
        stack.addWidget(stack1)

        hbox = QHBoxLayout()
        hbox.addLayout(layout1)
        hbox.addWidget(stack)

        btn3.clicked.connect(lambda: self.set_1(stack,m,n,a,b))
        btn4.clicked.connect(lambda: self.set_2(stack,x,y))

        self.stack3.setLayout(hbox)

    def tab1UI(self,m):
        layout2 = QVBoxLayout()
        label1 = QLabel('未归还:')
        tv1 = QTableView()
        model1 = QStandardItemModel()
        model1.setHorizontalHeaderLabels(['书名', '书号', '作者', '分类', '出版社', '出版时间', '借出时间'])
        cursor = conn.cursor()
        sql1 = "select * from borrow;"
        cnt_1 = cursor.execute(sql1)
        res_1 = cursor.fetchall()
        for i in range(0, cnt_1):
            for j in range(0, 7):
                item = QStandardItem('%s' % (res_1[i][j]))
                model1.setItem(i, j, item)
        tv1.setModel(model1)


        label2 = QLabel("已归还:")
        tv2 = QTableView()
        model2 = QStandardItemModel()
        model2.setHorizontalHeaderLabels(['书名', '书号', '作者', '分类', '出版社', '出版时间', '借出时间','归还时间'])
        sql2 = "select * from return_bo;"
        cnt_2 = cursor.execute(sql2)
        res_2 = cursor.fetchall()
        for i in range(0, cnt_2):
            for j in range(0, 8):
                item = QStandardItem('%s' % (res_2[i][j]))
                model2.setItem(i, j, item)
        tv2.setModel(model2)
        layout2.addWidget(label1)
        layout2.addWidget(tv1)
        layout2.addWidget(label2)
        layout2.addWidget(tv2)

        layout = QVBoxLayout()
        layout.addLayout(layout2)

        m.setLayout(layout)
        return tv1,model1,tv2,model2

    def tab2UI(self,m):
        layout2 = QHBoxLayout()
        line1 = QLineEdit()
        btn5 = QPushButton('查询')
        Cbox = QComboBox()
        Cbox.addItems(['按书名查询','按书号查询','按作者查询','按分类查询','按出版社查询'])
        layout2.addWidget(line1)
        layout2.addWidget(btn5)
        layout2.addWidget(Cbox)

        layout3 = QVBoxLayout()
        model = QStandardItemModel(10,9)
        model.setHorizontalHeaderLabels(['书名', '书号', '作者','分类','出版社','出版时间','库存','剩余可借','总借阅次数'])
        tv = QTableView()
        tv.setModel(model)
        layout3.addLayout(layout2)
        layout3.addWidget(tv)


        layout4 = QHBoxLayout()
        label1 = QLabel('跳转到第')
        line2 = QLineEdit()
        line2.setText('0')
        self.l2 = QLabel()
        btn6 = QPushButton('跳转')

        btn6.clicked.connect(lambda :self.jump(line2,model,tv))

        btn7 = QPushButton('前一页')
        btn8 = QPushButton('后一页')

        btn7.clicked.connect(lambda :self.step_1(line2,model,tv))
        btn8.clicked.connect(lambda :self.step_2(line2,model,tv))

        layout4.addWidget(label1)
        layout4.addWidget(line2)
        layout4.addWidget(self.l2)
        layout4.addWidget(btn6)
        layout4.addWidget(btn7)
        layout4.addWidget(btn8)

        layout = QVBoxLayout()
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(layout4)

        cursor = conn.cursor()
        sql = 'select * from operate;'
        a = cursor.execute(sql)
        res = cursor.fetchmany(10)
        if a%10 == 0:
            all = a/10
        else:
            all = a / 10 + 1
        self.l2.setText('/%s页' % (int(all)))
        for i in range(0, 10):
            for j in range(0, 9):
                item = QStandardItem('%s' % (res[i][j]))
                model.setItem(i, j, item)
        tv.setModel(model)

        if (int(a / 10) >= 1):
            line2.setText('1')

        cursor.close()

        btn5.clicked.connect(lambda:self.search_by(line1,Cbox,model,tv,line2))


        m.setLayout(layout)
        return tv,model

    def step_2(self,m,a,b):
        cursor = conn.cursor()

        sql_2 = 'select * from operate;'
        cnt_2 = cursor.execute(sql_2)
        res = cursor.fetchall()

        x = int(m.text())

        all = int(cnt_2/10)
        if cnt_2%10 != 0:
            all += 1

        if x+1 > all:
            pass
        else:
            a.removeRows(0, a.rowCount())
            m.setText(str(x+1))
            x += 1
            if cnt_2 > x * 10:
                left = (x - 1) * 10
                right = x * 10
            else:
                left = (x - 1) * 10
                right = (x - 1) * 10 + cnt_2 % 10

            for i in range(left, right):
                for j in range(0, 9):
                    item = QStandardItem('%s' % (res[i][j]))

                    a.setItem(i % 10, j, item)

            b.setModel(a)

    def step_1(self,m,a,b):

        cursor = conn.cursor()
        sql_2 = 'select * from operate;'
        cnt_2 = cursor.execute(sql_2)
        res = cursor.fetchall()



        x = int(m.text())
        all = cnt_2/10
        if cnt_2%10 != 0:
            all += 1
        if x-1 <= 0:
            pass
        else:
            a.removeRows(0, a.rowCount())
            m.setText(str(x-1))
            x -= 1
            if cnt_2 > x * 10:
                left = (x - 1) * 10
                right = x * 10
            else:
                left = (x - 1) * 10
                right = (x - 1) * 10 + cnt_2 % 10

            for i in range(left, right):
                for j in range(0, 9):
                    item = QStandardItem('%s' % (res[i][j]))

                    a.setItem(i % 10, j, item)

            b.setModel(a)


    def search_by(self,m,n,o,p,x):

        if m.text() == '':
            pass
        if n.currentText() == "按书名查询":
            cursor = conn.cursor()
            sql = "select * from operate where '%s'=operate.书名;"%(m.text())
            cnt = cursor.execute(sql)
            res = cursor.fetchmany(cnt)
            if cnt==0:
                o.clear()
                model = QStandardItemModel(10, 9)
                model.setHorizontalHeaderLabels(['书名', '书号', '作者', '分类', '出版社', '出版时间', '库存', '剩余可借', '总借阅次数'])
                p.setModel(model)
                QMessageBox.information(self, '消息', '无查询信息', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if cnt >0 and cnt<=10:
                o.clear()
                model = QStandardItemModel(10, 9)
                model.setHorizontalHeaderLabels(['书名', '书号', '作者', '分类', '出版社', '出版时间', '库存', '剩余可借', '总借阅次数'])
                for i in range(0, cnt):
                    for j in range(0, 9):
                        item = QStandardItem('%s' % (res[i][j]))
                        model.setItem(i, j, item)
                p.setModel(model)
                x.setText('1')


        if n.currentText() == "按书号查询":
            cursor = conn.cursor()
            sql = "select * from operate where '%s'=operate.书号;" % (m.text())
            cnt = cursor.execute(sql)
            res = cursor.fetchmany(cnt)
            if cnt == 0:
                o.clear()
                model = QStandardItemModel(10, 9)
                model.setHorizontalHeaderLabels(['书名', '书号', '作者', '分类', '出版社', '出版时间', '库存', '剩余可借', '总借阅次数'])
                p.setModel(model)
                QMessageBox.information(self, '消息', '无查询信息', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if cnt > 0 and cnt <= 10:
                o.clear()
                model = QStandardItemModel(10, 9)
                model.setHorizontalHeaderLabels(['书名', '书号', '作者', '分类', '出版社', '出版时间', '库存', '剩余可借', '总借阅次数'])
                for i in range(0, cnt):
                    for j in range(0, 9):
                        item = QStandardItem('%s' % (res[i][j]))
                        model.setItem(i, j, item)
                p.setModel(model)
                x.setText('1')

        if n.currentText() == "按作者查询":
            cursor = conn.cursor()
            sql = "select * from operate where '%s'=operate.作者;" % (m.text())
            cnt = cursor.execute(sql)
            res = cursor.fetchmany(cnt)
            if cnt == 0:
                o.clear()
                model = QStandardItemModel(10, 9)
                model.setHorizontalHeaderLabels(['书名', '书号', '作者', '分类', '出版社', '出版时间', '库存', '剩余可借', '总借阅次数'])
                p.setModel(model)
                QMessageBox.information(self, '消息', '无查询信息', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if cnt > 0 and cnt <= 10:
                o.clear()
                model = QStandardItemModel(10, 9)
                model.setHorizontalHeaderLabels(['书名', '书号', '作者', '分类', '出版社', '出版时间', '库存', '剩余可借', '总借阅次数'])
                for i in range(0, cnt):
                    for j in range(0, 9):
                        item = QStandardItem('%s' % (res[i][j]))
                        model.setItem(i, j, item)
                p.setModel(model)
                x.setText('1')

        if n.currentText() == "按分类查询":
            cursor = conn.cursor()
            sql = "select * from operate where '%s'=operate.分类;" % (m.text())
            cnt = cursor.execute(sql)
            res = cursor.fetchmany(cnt)
            if cnt == 0:
                o.clear()
                model = QStandardItemModel(10, 9)
                model.setHorizontalHeaderLabels(['书名', '书号', '作者', '分类', '出版社', '出版时间', '库存', '剩余可借', '总借阅次数'])
                p.setModel(model)
                QMessageBox.information(self, '消息', '无查询信息', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if cnt > 0 and cnt <= 10:
                o.clear()
                model = QStandardItemModel(10, 9)
                model.setHorizontalHeaderLabels(['书名', '书号', '作者', '分类', '出版社', '出版时间', '库存', '剩余可借', '总借阅次数'])
                for i in range(0, cnt):
                    for j in range(0, 9):
                        item = QStandardItem('%s' % (res[i][j]))
                        model.setItem(i, j, item)
                p.setModel(model)
                x.setText('1')

        if n.currentText() == "按出版社查询":
            cursor = conn.cursor()
            sql = "select * from operate where '%s'=operate.出版社;" % (m.text())
            cnt = cursor.execute(sql)
            res = cursor.fetchmany(cnt)
            if cnt == 0:
                o.clear()
                model = QStandardItemModel(10, 9)
                model.setHorizontalHeaderLabels(['书名', '书号', '作者', '分类', '出版社', '出版时间', '库存', '剩余可借', '总借阅次数'])
                p.setModel(model)
                QMessageBox.information(self, '消息', '无查询信息', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if cnt > 0 and cnt <= 10:
                o.clear()
                model = QStandardItemModel(10, 9)
                model.setHorizontalHeaderLabels(['书名', '书号', '作者', '分类', '出版社', '出版时间', '库存', '剩余可借', '总借阅次数'])
                for i in range(0, cnt):
                    for j in range(0, 9):
                        item = QStandardItem('%s' % (res[i][j]))
                        model.setItem(i, j, item)
                p.setModel(model)
                x.setText('1')

class Method_1(QDialog,Add_book):
    def __init__(self):
        super(Method_1,self).__init__()
        self.setupUi(self)

    def book_add(self):
        t1 = self.lineEdit.text()
        t2 = self.lineEdit_2.text()
        t3 = self.lineEdit_3.text()
        t4 = self.lineEdit_4.text()
        t5 = self.lineEdit_5.text()
        t6 = self.comboBox.currentText()
        t7 = self.dateEdit.text()
        cursor = conn.cursor()
        sql = "insert into operate values('%s','%s','%s','%s','%s','%s','%s','%s','%s');"%(t1,t2,t3,t6,t4,t7,t5,t5,0)
        cursor.execute(sql)
        conn.commit()
        sql_1 = "select * from operate;"
        cnt = cursor.execute(sql_1)
        if (cnt-1) % 10 == 0:
            w.l1.setText('/%s页' % (int(cnt / 10+1)))
            w.l2.setText('/%s页' % (int(cnt / 10+1)))
        QMessageBox.information(self, '消息', '添加成功！！！', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        window_1.close()
        window_3.update_user()


class Method_2(QDialog,Del_book):
    def __init__(self):
        super(Method_2,self).__init__()
        self.setupUi(self)

    def book_del(self):
        t1 = self.lineEdit.text()
        cursor = conn.cursor()
        sql = "delete from operate where 书名='%s';"%(t1)
        cursor.execute(sql)
        conn.commit()
        sql_1 = "select * from operate;"
        cnt = cursor.execute(sql_1)
        if cnt % 10 == 0:
            w.l1.setText('/%s页' % (int(cnt / 10)))
            w.l2.setText('/%s页' % (int(cnt / 10)))
        QMessageBox.information(self, '消息', '书籍已被淘汰！！！', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        window_2.close()
        window_3.update_user()

class Method_3(QDialog,Del_user):
    def __init__(self):
        super(Method_3,self).__init__()
        self.setupUi(self)

    def update_user(self):
        self.model.removeRows(0, self.model.rowCount())
        cursor = conn.cursor()
        sql = "select * from consumer"
        cnt = cursor.execute(sql)
        res = cursor.fetchall()
        for i in range(0, cnt):
            for j in range(0, 2):
                item = QStandardItem('%s' % (res[i][j]))
                self.model.setItem(i, j, item)
        self.tableView.setModel(self.model)

    def del_btn(self):
        cursor = conn.cursor()
        index = self.tableView.currentIndex()  # 取得当前选中行的index
        text1 = self.model.data(self.model.index(index.row(),0))
        text2 = self.model.data(self.model.index(index.row(),1))
        sql = "delete from consumer where user_name='%s' and user_pwd='%s';"%(text1,text2)
        cursor.execute(sql)
        conn.commit()

        self.model.removeRow(index.row())  # 通过index的row()操作得到行数进行删除



class Method_4(QDialog,Borrow_book):
    def __init__(self):
        super(Method_4,self).__init__()
        self.setupUi(self)

    def book_borrow(self):
        t1 = self.lineEdit.text()
        t2 = self.lineEdit_2.text()
        t3 = self.lineEdit_3.text()
        t4 = self.comboBox.currentText()
        t5 = self.lineEdit_4.text()
        t6 = self.dateEdit.text()

        cursor = conn.cursor()
        sql = "select * from operate where 书名='%s' and 书号= '%s' and 作者='%s' and 分类='%s' and 出版社='%s' and 出版时间='%s';"%(t1,t2,t3,t4,t5,t6)

        cnt = cursor.execute(sql)
        if cnt:
            QMessageBox.information(self, '消息', '借阅成功！！！', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            sql_1 = "insert into borrow values('%s','%s','%s','%s','%s','%s','%s');"%(t1,t2,t3,t4,t5,t6,datetime.date.today())
            flag = cursor.execute(sql_1)
            conn.commit()

            if flag:
                cursor = conn.cursor()
                sql_2 = "select 剩余可借,总借阅次数 from operate where 书名='%s';"%(t1)
                cursor.execute(sql_2)
                res = cursor.fetchall()
                sql_3 = "update operate set 剩余可借=%s where 书名='%s';"%(int(res[0][0])-1,t1)
                sql_4 = "update operate set 总借阅次数 = %s where 书名='%s';"%(int(res[0][1])+1,t1)
                cursor.execute(sql_3)
                cursor.execute(sql_4)
                conn.commit()

            window_4.close()


class Method_5(QDialog,Return_book):
    def __init__(self):
        super(Method_5,self).__init__()
        self.setupUi(self)

    def book_return(self):
        t1 = self.lineEdit_2.text()
        t2 = self.lineEdit_3.text()
        t3 = self.lineEdit.text()
        t4 = self.comboBox.currentText()
        t5 = self.lineEdit_4.text()
        t6 = self.dateEdit.text()
        cursor = conn.cursor()
        sql = "select 最新借阅时间 from borrow where 书名='%s' and 书号= '%s' and 作者='%s' and 分类='%s' and 出版社='%s' and 出版时间='%s';" % (
        t1, t2, t3, t4, t5, t6)

        cnt = cursor.execute(sql)
        res = cursor.fetchall()
        if cnt:
            QMessageBox.information(self, '消息', '归还成功！！！', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            sql_1 = "insert into return_bo values('%s','%s','%s','%s','%s','%s','%s','%s');" % (
            t1, t2, t3, t4, t5, t6, res[0][0],datetime.date.today())
            sql_2 = "delete from borrow where 书名='%s';"%(t1)
            cursor.execute(sql_1)
            flag = cursor.execute(sql_2)
            conn.commit()

            if flag:
                cursor = conn.cursor()
                sql_2 = "select 剩余可借,总借阅次数 from operate where 书名='%s';"%(t1)
                cursor.execute(sql_2)
                res = cursor.fetchall()
                sql_3 = "update operate set 剩余可借=%s where 书名='%s';"%(int(res[0][0])+1,t1)
                cursor.execute(sql_3)
                conn.commit()

            window_5.close()


if __name__=='__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('images/1.jpg'))
    w = main()
    window_1 = Method_1()
    window_2 = Method_2()
    window_3 = Method_3()
    window_4 = Method_4()
    window_5 = Method_5()
    w.move(400,200)
    w.show()
    sys.exit(app.exec_())
