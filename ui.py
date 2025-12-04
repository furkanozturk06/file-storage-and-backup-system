from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(803, 609)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color:#dee7e3;")
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(10, 10, 780, 580))
        self.stackedWidget.setObjectName("stackedWidget")
        self.first_page = QtWidgets.QWidget()
        self.first_page.setObjectName("first_page")
        self.sign_up_btn = QtWidgets.QPushButton(self.first_page)
        self.sign_up_btn.setGeometry(QtCore.QRect(120, 260, 200, 100))
        self.sign_up_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 22px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"\n"
"            QPushButton:hover {\n"
"                background-color: #45a049;\n"
"                font-size: 26px;\n"
"                font-family: \'Times New Roman\', serif; \n"
"            }")
        self.sign_up_btn.setObjectName("sign_up_btn")
        self.sign_in_btn = QtWidgets.QPushButton(self.first_page)
        self.sign_in_btn.setGeometry(QtCore.QRect(460, 260, 200, 100))
        self.sign_in_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 22px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"\n"
"            QPushButton:hover {\n"
"                background-color: #45a049;\n"
"                font-size: 26px;\n"
"                font-family: \'Times New Roman\', serif; \n"
"            }")
        self.sign_in_btn.setObjectName("sign_in_btn")
        self.tmp = QtWidgets.QLabel(self.first_page)
        self.tmp.setGeometry(QtCore.QRect(90, 50, 601, 100))
        self.tmp.setStyleSheet("QLabel {\n"
"                background-color:#dee7e3;\n"
"                color: #2c3e50;  \n"
"                font-size: 40px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                font-weight: bold;  \n"
"                text-align: center;  \n"
"                padding: 20px;  \n"
"                border-radius: 10px;\n"
"                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); \n"
"            }")
        self.tmp.setObjectName("tmp")
        self.stackedWidget.addWidget(self.first_page)
        self.login_page = QtWidgets.QWidget()
        self.login_page.setObjectName("login_page")
        self.login_btn = QtWidgets.QPushButton(self.login_page)
        self.login_btn.setGeometry(QtCore.QRect(210, 290, 100, 50))
        self.login_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 22px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.login_btn.setObjectName("login_btn")
        self.login_usr = QtWidgets.QLabel(self.login_page)
        self.login_usr.setGeometry(QtCore.QRect(80, 80, 90, 20))
        self.login_usr.setStyleSheet("font-size: 18px;  \n"
"font-family:\'Times New Roman\', serif; ")
        self.login_usr.setObjectName("login_usr")
        self.login_ps = QtWidgets.QLabel(self.login_page)
        self.login_ps.setGeometry(QtCore.QRect(80, 190, 90, 20))
        self.login_ps.setStyleSheet("font-size: 18px;  \n"
"font-family:\'Times New Roman\', serif; ")
        self.login_ps.setObjectName("login_ps")
        self.login_ps_cbx = QtWidgets.QCheckBox(self.login_page)
        self.login_ps_cbx.setGeometry(QtCore.QRect(210, 230, 81, 20))
        self.login_ps_cbx.setCheckable(True)
        self.login_ps_cbx.setChecked(False)
        self.login_ps_cbx.setTristate(False)
        self.login_ps_cbx.setObjectName("login_ps_cbx")
        self.login_usr_text = QtWidgets.QLineEdit(self.login_page)
        self.login_usr_text.setGeometry(QtCore.QRect(210, 70, 220, 40))
        self.login_usr_text.setStyleSheet("background-color:white;\n"
"")
        self.login_usr_text.setObjectName("login_usr_text")
        self.login_ps_text = QtWidgets.QLineEdit(self.login_page)
        self.login_ps_text.setGeometry(QtCore.QRect(210, 180, 220, 40))
        self.login_ps_text.setStyleSheet("background-color:white;\n"
"")
        self.login_ps_text.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_ps_text.setObjectName("login_ps_text")
        self.login_back_btn = QtWidgets.QPushButton(self.login_page)
        self.login_back_btn.setGeometry(QtCore.QRect(30, 540, 93, 30))
        self.login_back_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.login_back_btn.setObjectName("login_back_btn")
        self.login_lbl = QtWidgets.QLabel(self.login_page)
        self.login_lbl.setGeometry(QtCore.QRect(210, 370, 401, 121))
        self.login_lbl.setText("")
        self.login_lbl.setObjectName("login_lbl")
        self.stackedWidget.addWidget(self.login_page)
        self.register_page = QtWidgets.QWidget()
        self.register_page.setObjectName("register_page")
        self.reg_ps_cbx = QtWidgets.QCheckBox(self.register_page)
        self.reg_ps_cbx.setGeometry(QtCore.QRect(210, 230, 81, 20))
        self.reg_ps_cbx.setCheckable(True)
        self.reg_ps_cbx.setChecked(False)
        self.reg_ps_cbx.setTristate(False)
        self.reg_ps_cbx.setObjectName("reg_ps_cbx")
        self.reg_ps = QtWidgets.QLabel(self.register_page)
        self.reg_ps.setGeometry(QtCore.QRect(80, 190, 90, 20))
        self.reg_ps.setStyleSheet("font-size: 18px;  \n"
"font-family:\'Times New Roman\', serif; ")
        self.reg_ps.setObjectName("reg_ps")
        self.reg_btn = QtWidgets.QPushButton(self.register_page)
        self.reg_btn.setGeometry(QtCore.QRect(210, 330, 100, 50))
        self.reg_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 22px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.reg_btn.setObjectName("reg_btn")
        self.reg_usr = QtWidgets.QLabel(self.register_page)
        self.reg_usr.setGeometry(QtCore.QRect(80, 80, 90, 20))
        self.reg_usr.setStyleSheet("font-size: 18px;  \n"
"font-family:\'Times New Roman\', serif; ")
        self.reg_usr.setObjectName("reg_usr")
        self.reg_usr_text = QtWidgets.QLineEdit(self.register_page)
        self.reg_usr_text.setGeometry(QtCore.QRect(210, 70, 220, 40))
        self.reg_usr_text.setStyleSheet("background-color:white;\n"
"")
        self.reg_usr_text.setObjectName("reg_usr_text")
        self.reg_ps_text = QtWidgets.QLineEdit(self.register_page)
        self.reg_ps_text.setGeometry(QtCore.QRect(210, 180, 220, 40))
        self.reg_ps_text.setStyleSheet("background-color:white;\n"
"")
        self.reg_ps_text.setEchoMode(QtWidgets.QLineEdit.Password)
        self.reg_ps_text.setObjectName("reg_ps_text")
        self.rd_admin = QtWidgets.QRadioButton(self.register_page)
        self.rd_admin.setGeometry(QtCore.QRect(210, 280, 95, 20))
        self.rd_admin.setObjectName("rd_admin")
        self.rd_usr = QtWidgets.QRadioButton(self.register_page)
        self.rd_usr.setGeometry(QtCore.QRect(320, 280, 95, 20))
        self.rd_usr.setChecked(True)
        self.rd_usr.setObjectName("rd_usr")
        self.reg_back_btn = QtWidgets.QPushButton(self.register_page)
        self.reg_back_btn.setGeometry(QtCore.QRect(30, 540, 93, 30))
        self.reg_back_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.reg_back_btn.setObjectName("reg_back_btn")
        self.reg_lbl = QtWidgets.QLabel(self.register_page)
        self.reg_lbl.setGeometry(QtCore.QRect(210, 400, 401, 121))
        self.reg_lbl.setText("")
        self.reg_lbl.setObjectName("reg_lbl")
        self.stackedWidget.addWidget(self.register_page)
        self.usr_profile_page = QtWidgets.QWidget()
        self.usr_profile_page.setObjectName("usr_profile_page")
        self.user_label = QtWidgets.QLabel(self.usr_profile_page)
        self.user_label.setGeometry(QtCore.QRect(30, 10, 211, 25))
        self.user_label.setText("")
        self.user_label.setObjectName("user_label")
        self.usr_back_btn = QtWidgets.QPushButton(self.usr_profile_page)
        self.usr_back_btn.setGeometry(QtCore.QRect(30, 540, 93, 30))
        self.usr_back_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.usr_back_btn.setObjectName("usr_back_btn")
        self.change_usrname_btn = QtWidgets.QPushButton(self.usr_profile_page)
        self.change_usrname_btn.setGeometry(QtCore.QRect(30, 60, 140, 40))
        self.change_usrname_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.change_usrname_btn.setObjectName("change_usrname_btn")
        self.change_ps_btn = QtWidgets.QPushButton(self.usr_profile_page)
        self.change_ps_btn.setGeometry(QtCore.QRect(30, 110, 140, 40))
        self.change_ps_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.change_ps_btn.setObjectName("change_ps_btn")
        self.upload_file_btn = QtWidgets.QPushButton(self.usr_profile_page)
        self.upload_file_btn.setGeometry(QtCore.QRect(30, 160, 140, 40))
        self.upload_file_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.upload_file_btn.setObjectName("upload_file_btn")
        self.create_team_btn = QtWidgets.QPushButton(self.usr_profile_page)
        self.create_team_btn.setGeometry(QtCore.QRect(30, 260, 140, 40))
        self.create_team_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.create_team_btn.setObjectName("create_team_btn")
        self.view_file_btn = QtWidgets.QPushButton(self.usr_profile_page)
        self.view_file_btn.setGeometry(QtCore.QRect(30, 210, 140, 40))
        self.view_file_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.view_file_btn.setObjectName("view_file_btn")
        self.add_user_btn = QtWidgets.QPushButton(self.usr_profile_page)
        self.add_user_btn.setGeometry(QtCore.QRect(30, 310, 140, 40))
        self.add_user_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.add_user_btn.setObjectName("add_user_btn")
        self.view_team_btn = QtWidgets.QPushButton(self.usr_profile_page)
        self.view_team_btn.setGeometry(QtCore.QRect(30, 360, 140, 40))
        self.view_team_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.view_team_btn.setObjectName("view_team_btn")
        self.view_team_file_btn = QtWidgets.QPushButton(self.usr_profile_page)
        self.view_team_file_btn.setGeometry(QtCore.QRect(30, 410, 140, 40))
        self.view_team_file_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.view_team_file_btn.setObjectName("view_team_file_btn")
        self.remove_sync_btn = QtWidgets.QPushButton(self.usr_profile_page)
        self.remove_sync_btn.setGeometry(QtCore.QRect(30, 460, 140, 40))
        self.remove_sync_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.remove_sync_btn.setObjectName("remove_sync_btn")
        self.stackedWidget.addWidget(self.usr_profile_page)
        self.admin_page = QtWidgets.QWidget()
        self.admin_page.setObjectName("admin_page")
        self.admin_label = QtWidgets.QLabel(self.admin_page)
        self.admin_label.setGeometry(QtCore.QRect(40, 20, 221, 21))
        self.admin_label.setText("")
        self.admin_label.setObjectName("admin_label")
        self.admin_back_btn = QtWidgets.QPushButton(self.admin_page)
        self.admin_back_btn.setGeometry(QtCore.QRect(30, 540, 93, 30))
        self.admin_back_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.admin_back_btn.setObjectName("admin_back_btn")
        self.notifications_btn = QtWidgets.QPushButton(self.admin_page)
        self.notifications_btn.setGeometry(QtCore.QRect(40, 80, 140, 40))
        self.notifications_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.notifications_btn.setObjectName("notifications_btn")
        self.user_list_btn = QtWidgets.QPushButton(self.admin_page)
        self.user_list_btn.setGeometry(QtCore.QRect(40, 140, 140, 40))
        self.user_list_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.user_list_btn.setObjectName("user_list_btn")
        self.admin_usr_file_btn = QtWidgets.QPushButton(self.admin_page)
        self.admin_usr_file_btn.setGeometry(QtCore.QRect(40, 200, 140, 40))
        self.admin_usr_file_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.admin_usr_file_btn.setObjectName("admin_usr_file_btn")
        self.admin_team_file_btn = QtWidgets.QPushButton(self.admin_page)
        self.admin_team_file_btn.setGeometry(QtCore.QRect(40, 320, 140, 40))
        self.admin_team_file_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.admin_team_file_btn.setObjectName("admin_team_file_btn")
        self.admin_log_file_btn = QtWidgets.QPushButton(self.admin_page)
        self.admin_log_file_btn.setGeometry(QtCore.QRect(40, 380, 140, 40))
        self.admin_log_file_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.admin_log_file_btn.setObjectName("admin_log_file_btn")
        self.admin_user_data_btn = QtWidgets.QPushButton(self.admin_page)
        self.admin_user_data_btn.setGeometry(QtCore.QRect(40, 260, 140, 40))
        self.admin_user_data_btn.setStyleSheet("QPushButton {\n"
"                background-color: #4CAF50;\n"
"                color: white;\n"
"                font-size: 15px;  \n"
"                font-family:\'Times New Roman\', serif; \n"
"                border-radius: 10px;\n"
"                padding: 10px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #45a049; \n"
"            }\n"
"")
        self.admin_user_data_btn.setObjectName("admin_user_data_btn")
        self.stackedWidget.addWidget(self.admin_page)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.sign_up_btn.setText(_translate("MainWindow", "Sign in"))
        self.sign_in_btn.setText(_translate("MainWindow", "Sign up"))
        self.tmp.setText(_translate("MainWindow", "File Storage and Backup System"))
        self.login_btn.setText(_translate("MainWindow", "Sign in"))
        self.login_usr.setText(_translate("MainWindow", "Username:"))
        self.login_ps.setText(_translate("MainWindow", "Password:"))
        self.login_ps_cbx.setText(_translate("MainWindow", "Show"))
        self.login_back_btn.setText(_translate("MainWindow", "Back"))
        self.reg_ps_cbx.setText(_translate("MainWindow", "Show"))
        self.reg_ps.setText(_translate("MainWindow", "Password:"))
        self.reg_btn.setText(_translate("MainWindow", "Sign up"))
        self.reg_usr.setText(_translate("MainWindow", "Username:"))
        self.rd_admin.setText(_translate("MainWindow", "Admin"))
        self.rd_usr.setText(_translate("MainWindow", "User"))
        self.reg_back_btn.setText(_translate("MainWindow", "Back"))
        self.usr_back_btn.setText(_translate("MainWindow", "Back"))
        self.change_usrname_btn.setText(_translate("MainWindow", "Change Username"))
        self.change_ps_btn.setText(_translate("MainWindow", "Change Password"))
        self.upload_file_btn.setText(_translate("MainWindow", "Upload File"))
        self.create_team_btn.setText(_translate("MainWindow", "Create Team"))
        self.view_file_btn.setText(_translate("MainWindow", "View File"))
        self.add_user_btn.setText(_translate("MainWindow", "Add User Team"))
        self.view_team_btn.setText(_translate("MainWindow", "View Team"))
        self.view_team_file_btn.setText(_translate("MainWindow", "View Team File"))
        self.remove_sync_btn.setText(_translate("MainWindow", "Remove Sync"))
        self.admin_back_btn.setText(_translate("MainWindow", "Back"))
        self.notifications_btn.setText(_translate("MainWindow", "Notifications"))
        self.user_list_btn.setText(_translate("MainWindow", "User Quota"))
        self.admin_usr_file_btn.setText(_translate("MainWindow", "View User File"))
        self.admin_team_file_btn.setText(_translate("MainWindow", "View Team File"))
        self.admin_log_file_btn.setText(_translate("MainWindow", "View Log File"))
        self.admin_user_data_btn.setText(_translate("MainWindow", "View User Data"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
