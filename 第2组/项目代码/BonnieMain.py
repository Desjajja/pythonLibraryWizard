from PyQt5.QtWidgets import *      
from PyQt5.QtGui import *           
from PyQt5.QtCore import *          
import module.items                 
import os
from view.Login import Ui_ChatLoginWindow
from view.Chat import Ui_ChatForm   ## 聊天室
import sys
import time
import json
from search import *
# from day01.b06_xiaohuang_bot import bot_response  # 引用day01 xiaohuang_bot

## 登录窗口
class LoginWindow(QMainWindow, Ui_ChatLoginWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 加载样式
        qss_file = open('view/qss/Login_style.qss').read()
        self.setStyleSheet(qss_file)
        self.txt_pwd.setEchoMode(QLineEdit.Password)
        self.my_info = {}
        self.friends_list = []

        # 信号槽  设置操作信号
        self.btn_login.clicked.connect(self.login_click)

    def login_click(self):
        
        self.rootname = self.txt_user.text()
        self.pwd = self.txt_pwd.text()
        # # 登录认证
        data = []
        if self.rootname == "team2":
            if self.pwd == "1234":
                data.append(self.rootname)
                print("login_click> data", data)   
                # 添加登录用户信息
                self.my_info = {'yang':"yang", 'avatar':'images/adou.jpg'}
                print("login_click>my_info", self.my_info)
                self.bot_list = []
                self.hide()
                self.dia = Mychat(self.my_info, self.bot_list)
                self.dia.show()
            # 报错回复
            else:
                QMessageBox.information(self, "提示", "用户名或密码错误！",
                                                QMessageBox.Yes)
                self.txt_user.clear()
                self.txt_pwd.clear()


## 聊天室
class Mychat(QMainWindow, Ui_ChatForm):
    def __init__(self, my_info, bot_list):
        super().__init__()
        self.setupUi(self)

        self.strXBHistory = ""
        self.strADHistroy = ""

        ## 加载聊天室的样式
        qss_file = open('view/qss/Chat_style.qss').read()
        self.setStyleSheet(qss_file)
        
        ## 初始化信息
        self.my_info = my_info
        print("Chat-Bot> botlist>", bot_list)
        
        ''' 
        模拟添加不同的机器人
        ''' 
        self.bot_list = {}
        # bot 1
        bot_list.insert(0, ['Bonnie', '图书管理员', 'images/bot2.jpg'])
        
        # show bot
        self.bot_list = bot_list
        self.listWidget1_1._set_items(self.bot_list)
        # self.chat3()
        # self.chat4()
        
        ''' 
        绑定事件
        ''' 
        # 1 发送消息
        self.send_Button.clicked.connect(self.Send)
        # 2 退出
        self.quit_Button.clicked.connect(self.Quit)
        # 3 DO_A
        self.pushButton_4.clicked.connect(self.do_A)
        # 4 DO_B
        self.pushButton_2.clicked.connect(self.do_B)
        # 5 DO_C
        self.pushButton.clicked.connect(self.do_C)
        
        # 6 DO_D
        self.pushButton_7.clicked.connect(self.do_D)  
        # 7 DO_E
        self.pushButton_3.clicked.connect(self.do_E)
        
        # 8 点击头像开始聊天
        self.listWidget1_1.set_doubleclick_slot(self.chat)

        # ## 展示机器人的信息
        print("show my bot")

    
    def do_A(self):
        os.system("python ./untils/main01.py")
        # import chat
        print("DO_A")
        pass
    
    def do_B(self):
        # os.system("python ./untils/main02.py")
        print("DO_B")
        pass
    
    def do_C(self):
        import chat
        print("DO_C")
        pass
    
    def do_D(self):
        print("DO_D")
        pass 
    
    def do_E(self):
        print("DO_E")
        pass

    
    ## 关闭事件
    def closeEvent(self, QCloseEvent):
        print("进入closeEvent")
        
    ## 退出聊天室
    def Quit(self):
        sys.exit()
    
    def chat3(self):
        """ 
        展示bot1的介绍信息
        """ 
        self.chat_info = dict(zip(
            ["type", "rootname", "nickname", "gender", "tel", "address", "email", "birthday", "avatar", "style",
            "onlinestatus"],
            ["I", "1000", "Bonnie", "女", '10000', '图书问答机器人', '10000.com', '1月1日', 'images/bot2.jpg',
            '今天看点什么？', '在线']))
        self.showinit(self.chat_info)
        print("init执行完毕")
        # self.textBrowser.clear()
    

    # 点击头像切换聊天
    def chat(self, name, flag):
        if flag =="图书管理员":
            self.strADHistroy = self.textBrowser.document().toPlainText()
            self.textBrowser.clear()
            self.textBrowser.append(self.strXBHistory)
            self.chat3()
            print("chat>falg")#, '不要迷恋哥，哥只是个传说')
        else:
            pass

    ''' 
    展示机器信息
    
    ''' 
    def showinit(self, chat_info):
        print("进入了showinit")
        self.chatname_label.setText(chat_info["nickname"])
        print("1")
        # 登录者的信息
        self.my_avatar_label.setStyleSheet("background-color: gainsboro;border-image: url('%s');" % self.my_info["avatar"])
        # 机器人的信息
        self.f_avatar_label.setStyleSheet("background-color: gainsboro;border-image: url('%s');" % chat_info["avatar"])
        print("2")
        self.f_nickname_label.setText(chat_info["nickname"])
        print("3")
        self.style_label.setText(chat_info["style"])
        print("4")
        self.address_label.setText(chat_info["address"])
        print("5")
        self.email_label.setText(chat_info["email"])
        print("6")
        self.tel_label.setText(chat_info["tel"])
        print("7")
        self.birthday_label.setText(chat_info["birthday"])
        print("8")
        self.onlinestatus_label.setText(chat_info["onlinestatus"])
        print("showinit执行完毕")
    

    ''' 
    发送消息：

        将用户的聊天追加到文本显示框
        将机器人的回复追加到文本显示框

    ''' 
    def Send(self):  # 发送消息
        
        data = self.textEdit.toPlainText()
        print("Send:", data)
        RES1=book_name_search(book_search_element(),data)
        
        text = "用户" + '  ' + "%02d:%02d:%02d" % time.localtime()[3:6] + '\n' + data +'\n'
        self.textBrowser.append(text)
        
        if data in ['马克思主义理论学科文献借阅中心','农业食品轻工环境化工学科文献借阅中心','自动化与计算机技术学科文献借阅中心','材料机械能源学科文献借阅中心','文学学科文献借阅中心']:
            RES2=site_storage(data)
            print('该馆藏点藏有以下书籍：')
            for i in RES2:
                OUTPUT=(i['Name']+' '+i['author']+' '+i['series_num']+' '+i['site']+'\n')
                self.botReplyMessage(OUTPUT)
            print("Send>end")
        else:
            if len(RES1) == 0:
                    OUTPUT=('很抱歉，找不到你要看的书呢~')
                    self.botReplyMessage(OUTPUT)
                    print("Send>end")
            else:
                for i in RES1:
                    OUTPUT=(i['Name']+' '+i['author']+' '+i['series_num']+' '+i['site']+'\n')
                    # 将消息追加到文本框
                    self.botReplyMessage(OUTPUT)
                print("Send>end")
        
        
        # ## 将消息追加到文本框
        # self.textBrowser.append(text)
        # self.botReplyMessage(OUTPUT)

        # 每次发送完消息，清空发送框
        self.textEdit.setText("")
    

    def botReplyMessage(self,strMessage):
        ''' 
        机器人回复消息追加
        ''' 
        text = "Bot" + '  ' + "%02d:%02d:%02d" % time.localtime()[3:6] + '\n' + strMessage + '\n'
        self.textBrowser.append(text)
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat = LoginWindow()
    chat.show()
    sys.exit(app.exec_())
