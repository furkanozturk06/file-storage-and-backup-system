import os
import sys
import shutil
import hashlib
import datetime
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt5.QtCore import Qt, QTimer, QMetaObject, Q_ARG
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QPushButton,
                             QLabel, QMessageBox, QListWidget, QFormLayout, QWidget,
                             QFileDialog, QVBoxLayout, QDialog, QProgressBar,
                             QAbstractItemView, QListWidgetItem, QInputDialog)
from ui import Ui_MainWindow

class FolderSyncHandler(FileSystemEventHandler):
    def __init__(self, sync_callback):
        self.sync_callback = sync_callback

    def on_modified(self, event):
        self.sync_callback()

    def on_created(self, event):
        self.sync_callback()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.current_user = None 
        self.current_team = None
        self.dynamic_widgets = []
        self.user_inputs = {}

        self.sync_folders = []
        self.sync_observer = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.perform_scheduled_sync)
        self.timer.setInterval(5000)
        self.timer.start()

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(50, 300, 400, 25)
        self.progress_bar.hide()

        self.ui.sign_up_btn.clicked.connect(self.show_register_screen)
        self.ui.sign_in_btn.clicked.connect(self.show_login_screen)

        self.ui.login_back_btn.clicked.connect(self.show_first_screen)
        self.ui.reg_back_btn.clicked.connect(self.show_first_screen)
        self.ui.usr_back_btn.clicked.connect(self.show_first_screen)
        self.ui.admin_back_btn.clicked.connect(self.show_first_screen)

        self.ui.reg_ps_cbx.toggled.connect(self.toggle_password_register)
        self.ui.reg_ps_cbx.stateChanged.connect(self.update_register_checkbox_label)
        self.ui.login_ps_cbx.toggled.connect(self.toggle_password_login)
        self.ui.login_ps_cbx.stateChanged.connect(self.update_login_checkbox_label)

        self.ui.reg_btn.clicked.connect(self.register)
        self.ui.login_btn.clicked.connect(self.login)

        self.ui.change_usrname_btn.clicked.connect(self.add_username_widgets)
        self.ui.change_ps_btn.clicked.connect(self.handle_password_request)
        self.ui.view_file_btn.clicked.connect(lambda: self.view_files(self.current_user))
        self.ui.create_team_btn.clicked.connect(self.show_create_team_screen)
        self.ui.add_user_btn.clicked.connect(self.show_user_list_for_team)
        self.ui.view_team_btn.clicked.connect(self.view_team)
        self.ui.view_team_file_btn.clicked.connect(lambda: self.view_team_files(self.current_user))
        self.ui.upload_file_btn.clicked.connect(self.select_and_sync_folder)
        self.ui.remove_sync_btn.clicked.connect(self.remove_sync_folder)

        self.ui.notifications_btn.clicked.connect(self.toggle_admin_notifications)
        self.ui.user_list_btn.clicked.connect(self.show_user_list)
        self.ui.admin_log_file_btn.clicked.connect(self.show_log_files)
        self.ui.admin_usr_file_btn.clicked.connect(self.show_user_files)
        self.ui.admin_user_data_btn.clicked.connect(self.show_user_data)
        self.ui.admin_team_file_btn.clicked.connect(self.show_team_files)

    def show_first_screen(self):
        for widget in self.dynamic_widgets:
                widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)

    def show_register_screen(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def show_login_screen(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def toggle_password_register(self):
        if self.ui.reg_ps_cbx.isChecked():
            self.ui.reg_ps_text.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.reg_ps_text.setEchoMode(QLineEdit.Password)

    def toggle_password_login(self):
        if self.ui.login_ps_cbx.isChecked():
            self.ui.login_ps_text.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.login_ps_text.setEchoMode(QLineEdit.Password)

    def update_register_checkbox_label(self):
        if self.ui.reg_ps_cbx.isChecked():
            self.ui.reg_ps_cbx.setText("Hide")
        else:
            self.ui.reg_ps_cbx.setText("Show")

    def update_login_checkbox_label(self):
        if self.ui.login_ps_cbx.isChecked():
            self.ui.login_ps_cbx.setText("Hide")
        else:
            self.ui.login_ps_cbx.setText("Show")

    def register(self):
        username = self.ui.reg_usr_text.text()
        password = self.ui.reg_ps_text.text()

        if not username or not password:
            self.ui.reg_lbl.setText("Please enter a username and password!")
            return

        role = "User"
        if self.ui.rd_admin.isChecked():
            role = "Admin"

        try:
            with open('users.txt', 'r') as f:
                users = f.readlines()

            for user in users:
                stored_role, stored_username, _ = user.strip().split(',')[:3]
                if username == stored_username:
                    self.ui.reg_lbl.setText("This username is already taken!")
                    return
        except FileNotFoundError:
            pass

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        quota = 500

        with open('users.txt', 'a') as f:
            f.write(f"{role},{username},{hashed_password},{quota}\n")

        self.ui.reg_lbl.setText(f"{username} successfully registered as {role}!")

        self.ui.reg_usr_text.clear()
        self.ui.reg_ps_text.clear()

    def login(self):
        username = self.ui.login_usr_text.text()
        password = self.ui.login_ps_text.text()

        if not username or not password:
            self.ui.login_lbl.setText("Please enter a username and password!")
            self.log_event(
                category="Login",
                operation_code="MISSING_CREDENTIALS",
                status_code="FAILED",
                user=username,
                message="Username or password not provided"
            )
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            with open('users.txt', 'r') as f:
                users = f.readlines()

            for user in users:
                stored_role, stored_username, stored_password, stored_quota = user.strip().split(',')
                if username == stored_username and hashed_password == stored_password:
                    self.current_user = username
                    self.current_quota = stored_quota
                    self.current_team = self.get_user_team(username)
                    self.load_synced_folders()
                    if stored_role == "Admin":
                        self.ui.admin_label.setText("Welcome! " + username)
                        self.ui.stackedWidget.setCurrentIndex(4)
                        self.log_event(
                            category="Login",
                            operation_code="ADMIN_LOGIN",
                            status_code="SUCCESS",
                            user=username
                        )
                        self.ui.login_usr_text.clear()
                        self.ui.login_ps_text.clear()
                    else:
                        self.ui.user_label.setText("Welcome! " + username)
                        self.log_event(
                            category="Login",
                            operation_code="USER_LOGIN",
                            status_code="SUCCESS",
                            user=username
                        )
                        self.ui.stackedWidget.setCurrentIndex(3)
                        self.show_notifications(self.current_user)
                        self.ui.login_usr_text.clear()
                        self.ui.login_ps_text.clear()
                    return
                if stored_role == "User":
                    if username == stored_username and not hashed_password == stored_password:
                        self.log_event(
                            category="Login",
                            operation_code="USER_LOGIN",
                            status_code="FAILED",
                            user=username,
                            message="Wrong password"
                        )
                        self.track_failed_login(username)

            self.ui.login_lbl.setText("Incorrect username or password!")
        except FileNotFoundError:
            self.ui.login_lbl.setText("No registered users found.")

    def add_username_widgets(self):
        if not self.dynamic_widgets:
            self.username_edit = QLineEdit(self)
            self.username_edit.setGeometry(350, 150, 200, 30)
            self.username_edit.setPlaceholderText("New Username")
            self.username_edit.show()

            self.username_button = QPushButton("Change", self)
            self.username_button.setGeometry(350, 220, 100, 30)
            self.username_button.clicked.connect(self.update_username)
            self.username_button.show()

            self.dynamic_widgets = [self.username_edit, self.username_button]
        else:
            for widget in self.dynamic_widgets:
                widget.hide()
            self.dynamic_widgets = []

    def update_username(self):
        new_username = self.username_edit.text()
        if not new_username:
            return

        try:
            with open('users.txt', 'r') as f:
                users = f.readlines()

            updated_users = []
            for user in users:
                role, stored_username, password ,quota= user.strip().split(',')
                if stored_username == self.current_user:
                    updated_users.append(f"{role},{new_username},{password},{quota}\n")
                    self.current_user = new_username
                else:
                    updated_users.append(user)

            with open('users.txt', 'w') as f:
                f.writelines(updated_users)

            self.username_edit.setText("")
            print("Username successfully updated!")

        except FileNotFoundError:
            print("User file not found!")

    def handle_password_request(self):
        self.track_password_change_request(self.current_user)
        try:
            with open('notifications.txt', 'r') as f:
                notifications = f.readlines()

            for notif in notifications:
                username, status = notif.strip().split(':')
                if username == self.current_user:
                    if status == "Approved":
                        self.show_password_change_ui()
                    elif status == "Rejected":
                        QMessageBox.warning(self, "Rejected", "Your password change request was rejected!")
                    else:
                        QMessageBox.information(self, "Pending", "Your password change request is under review.")
                    return

            with open('notifications.txt', 'a') as f:
                f.write(f"{self.current_user}:Pending\n")

            self.log_event(
                category="PasswordChange",
                operation_code="REQUEST_PASSWORD_CHANGE",
                status_code="PENDING",
                user=self.current_user
            )
            QMessageBox.information(self, "Sent", "Password change request sent.")

        except FileNotFoundError:
            with open('notifications.txt', 'a') as f:
                f.write(f"{self.current_user}:Pending\n")
            QMessageBox.information(self, "Sent", "Password change request sent.")

    def show_password_change_ui(self):
        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(350, 150, 200, 30)
        self.password_input.setPlaceholderText("New Password")
        self.password_input.show()

        self.change_password_btn = QPushButton("Change Password", self)
        self.change_password_btn.setGeometry(350, 220, 200, 30)
        self.change_password_btn.show()
        self.change_password_btn.clicked.connect(self.change_password)

    def change_password(self):
        new_password = self.password_input.text()
        if not new_password:
            QMessageBox.warning(self, "Error", "New password cannot be empty!")
            return

        try:
            with open('users.txt', 'r') as f:
                users = f.readlines()

            updated_users = []
            for user in users:
                role, stored_username, stored_password,quota = user.strip().split(',')
                if stored_username == self.current_user:
                    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                    updated_users.append(f"{role},{stored_username},{hashed_password},{quota}\n")
                else:
                    updated_users.append(user)

            with open('users.txt', 'w') as f:
                f.writelines(updated_users)

            self.remove_password_request()

            QMessageBox.information(self, "Info", "Your password has been successfully changed.")
            self.password_input.hide()
            self.change_password_btn.hide()

            self.log_event(
                category="PasswordChange",
                operation_code="CHANGE_PASSWORD",
                status_code="SUCCESS"
            )

        except FileNotFoundError:
            self.log_event(
                category="PasswordChange",
                operation_code="CHANGE_PASSWORD",
                status_code="FAILED",
                message="File not found!"
            )
            QMessageBox.warning(self, "WARNING", "File not found!")

    def remove_password_request(self):
        try:
            with open('notifications.txt', 'r') as f:
                notifications = f.readlines()

            updated_notifications = [
                notif for notif in notifications
                if not notif.startswith(f"{self.current_user}:")
            ]

            with open('notifications.txt', 'w') as f:
                f.writelines(updated_notifications)

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "Notification file not found!")

    def toggle_admin_notifications(self):
        if hasattr(self, 'requests_list') and self.requests_list.isVisible():
            self.requests_list.hide()
            self.approve_request_btn.hide()
            self.reject_request_btn.hide()
        else:
            if not hasattr(self, 'requests_list'):
                self.requests_list = QListWidget(self)
                self.requests_list.setGeometry(250, 100, 300, 200)

                self.approve_request_btn = QPushButton("Approve", self)
                self.approve_request_btn.setGeometry(250, 320, 100, 30)
                self.approve_request_btn.clicked.connect(self.approve_password_request)

                self.reject_request_btn = QPushButton("Reject", self)
                self.reject_request_btn.setGeometry(370, 320, 100, 30)
                self.reject_request_btn.clicked.connect(self.reject_password_request)

            self.requests_list.clear()
            try:
                with open('notifications.txt', 'r') as f:
                    notifications = f.readlines()

                for notif in notifications:
                    self.requests_list.addItem(notif.strip())
            except FileNotFoundError:
                QMessageBox.information(self, "Notifications", "No requests found.")

            self.requests_list.show()
            self.approve_request_btn.show()
            self.reject_request_btn.show()

    def approve_password_request(self):
        selected_item = self.requests_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Error", "Please select a notification.")
            return

        username = selected_item.text().split(":")[0]
        self.update_notification_status(username, "Approved")
        self.log_event(
            category="PasswordChange",
            operation_code="APPROVE_REQUEST",
            status_code="SUCCESS",
            user=username
        )
        QMessageBox.information(self, "Info", f"{username}'s request has been approved.")
        self.requests_list.takeItem(self.requests_list.currentRow())

    def reject_password_request(self):
        selected_item = self.requests_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Error", "Please select a notification.")
            return

        username = selected_item.text().split(":")[0]
        self.update_notification_status(username, "Rejected")
        self.log_event(
            category="PasswordChange",
            operation_code="REJECT_REQUEST",
            status_code="FAILED",
            user=username
        )
        QMessageBox.information(self, "Info", f"{username}'s request has been rejected.")
        self.requests_list.takeItem(self.requests_list.currentRow())

    def update_notification_status(self, username, status):
        try:
            with open('notifications.txt', 'r') as f:
                notifications = f.readlines()

            updated_notifications = []
            for notif in notifications:
                try:
                    notif_username, notif_status = notif.strip().split(":")
                    if notif_username == username:
                        updated_notifications.append(f"{notif_username}:{status}\n")
                    else:
                        updated_notifications.append(notif)
                except ValueError:
                    continue

            with open('notifications.txt', 'w') as f:
                f.writelines(updated_notifications)

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "Notification file not found!")

    def show_user_list(self):
        user_list_window = QWidget()
        user_list_window.setWindowTitle("User List and Quotas")
        layout = QFormLayout()

        try:
            with open('users.txt', 'r') as f:
                users = f.readlines()

            for user in users:
                role, username, _, quota = user.strip().split(',')

                if role == "User":
                    quota_input = QLineEdit()
                    quota_input.setText(quota)
                    self.user_inputs[username] = quota_input

                    layout.addRow(f"{username}:", quota_input)

            save_button = QPushButton("Save")
            save_button.clicked.connect(self.save_user_quota_changes)
            layout.addRow(save_button)

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "User file not found!")
            return

        user_list_window.setLayout(layout)
        user_list_window.show()
        self.user_list_window = user_list_window

    def save_user_quota_changes(self):
        """Save user quota changes."""
        try:
            with open('users.txt', 'r') as f:
                users = f.readlines()

            updated_users = []

            for user in users:
                role, username, password, quota = user.strip().split(',')

                if role == "User" and username in self.user_inputs:
                    new_quota = self.user_inputs[username].text()

                    if not new_quota.isdigit():
                        QMessageBox.warning(self, "Error", f"Please enter a valid quota for {username}!")
                        return

                    updated_users.append(f"{role},{username},{password},{new_quota}\n")
                else:
                    updated_users.append(user)

            with open('users.txt', 'w') as f:
                f.writelines(updated_users)

            QMessageBox.information(self, "Success", "Quota changes saved successfully!")

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "User file not found!")

    def view_files(self, username):
        """View files uploaded by the user and open them on double-click."""
        user_folder = os.path.join("backups", username)
        if not os.path.exists(user_folder):
            QMessageBox.warning(self, "Error", "No files have been uploaded.")
            return

        files = os.listdir(user_folder)
        if not files:
            QMessageBox.information(self, "Info", "No uploaded files found.")
            return

        self.file_list_dialog = QDialog(self)
        self.file_list_dialog.setWindowTitle("Uploaded Files")
        self.file_list_dialog.setGeometry(800, 400, 600, 400)
        layout = QVBoxLayout(self.file_list_dialog)

        self.file_list_widget = QListWidget(self.file_list_dialog)
        self.file_list_widget.setSelectionMode(QAbstractItemView.MultiSelection)

        for file_name in files:
            file_path = os.path.join(user_folder, file_name)
            file_size = os.path.getsize(file_path)
            file_item = QListWidgetItem(f"{file_name} - {file_size / 1024:.2f} KB")
            file_item.setData(Qt.UserRole, file_path)
            self.file_list_widget.addItem(file_item)

        self.file_list_widget.itemDoubleClicked.connect(self.open_file)

        layout.addWidget(self.file_list_widget)

        close_button = QPushButton("Close", self.file_list_dialog)
        close_button.clicked.connect(self.file_list_dialog.close)
        layout.addWidget(close_button)

        share_button = QPushButton("Share with Team")
        share_button.clicked.connect(lambda: self.share_file_with_team(self.current_user))
        layout.addWidget(share_button)

        self.file_list_dialog.setLayout(layout)
        self.file_list_dialog.exec_()

    def open_file(self, item):
        """Open the selected file in the default application."""
        file_path = item.data(Qt.UserRole)
        if os.path.exists(file_path):
            try:
                os.startfile(file_path)
            except AttributeError:
                import subprocess
                subprocess.call(["xdg-open", file_path])
        else:
            QMessageBox.warning(self, "Error", "File not found.")

    def show_create_team_screen(self):
        """Display the screen for creating a new team."""
        team_name, ok = QInputDialog.getText(self, "Team Name", "Enter a team name:")
        if ok and team_name:
            if self.check_if_user_in_team():
                QMessageBox.warning(self, "Error", "You are already a member of a team. You cannot create another one.")
                return
            self.create_team(team_name)

    def check_if_user_in_team(self):
        """Check if the user is already a member of a team."""
        try:
            with open('teams.txt', 'r') as f:
                teams = f.readlines()
            for team in teams:
                team_name, members = team.strip().split(": ")
                members_list = members.split(", ")
                if self.current_user in members_list:
                    return True
        except FileNotFoundError:
            pass
        return False

    def create_team(self, team_name):
        """Create a new team and add the user to it."""
        try:
            with open('users.txt', 'r') as f:
                users = f.readlines()

            updated_users = []
            for user in users:
                role, username, password, quota = user.strip().split(',')
                if username == self.current_user:
                    updated_users.append(f"{role},{username},{password},{quota}\n")
                else:
                    updated_users.append(user)

            with open('users.txt', 'w') as f:
                f.writelines(updated_users)

            with open('teams.txt', 'a') as f:
                f.write(f"{team_name}: {self.current_user}\n")

            self.current_team = team_name
            QMessageBox.information(self, "Success", f"Team '{team_name}' created successfully and {self.current_user} added to the team!")

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "User file not found!")

    def show_user_list_for_team(self):
        """List users and allow adding them to the team."""
        if self.current_team is None:
            QMessageBox.warning(self, "Error", "You are not a member of any team. Please create a team first.")
            return

        user_list_window = QDialog()
        user_list_window.setWindowTitle("User List")
        user_list_window.setGeometry(800, 400, 200, 300)
        layout = QFormLayout()

        try:
            with open('users.txt', 'r') as f:
                users = f.readlines()

            for user in users:
                role, username, _, _ = user.strip().split(',')

                if role == "User" and not self.is_user_in_team(username):
                    add_button = QPushButton(f"{username} - Add to Team")
                    add_button.clicked.connect(lambda checked, user=username: self.add_user_to_team(user))
                    layout.addRow(add_button)

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "User file not found!")
            return
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Unexpected error occurred: {e}")
            return

        user_list_window.setLayout(layout)
        user_list_window.exec_()

    def is_user_in_team(self, username):
        """Check if the user is a member of a team."""
        try:
            with open('teams.txt', 'r') as f:
                teams = f.readlines()
            for team in teams:
                team_name, members = team.strip().split(": ")
                if username in members.split(", "):
                    return True
        except FileNotFoundError:
            pass
        return False

    def add_user_to_team(self, username):
        """Add the selected user to the team."""
        if self.current_team is None:
            QMessageBox.warning(self, "Error", "You are not a member of any team.")
            return

        try:
            with open('teams.txt', 'r') as f:
                teams = f.readlines()

            updated_teams = []
            team_found = False
            for team in teams:
                team_name, members = team.strip().split(": ")
                if team_name == self.current_team:
                    members_list = members.split(", ")
                    if username not in members_list:
                        members_list.append(username)
                        team_found = True
                    updated_teams.append(f"{team_name}: {', '.join(members_list)}\n")
                else:
                    updated_teams.append(team)
            if not team_found:
                QMessageBox.warning(self, "Error", "Team not found.")
                return
        
            with open('teams.txt', 'w') as f:
                f.writelines(updated_teams)

            self.current_team = self.get_user_team(self.current_user)
            self.add_notification(username, f"You have been added to the team {team_name}!")
            self.log_event(
                category="Team",
                operation_code="ADD_TEAM_MEMBER",
                status_code="SUCCESS",
                user=self.current_user,
                message=f"Added {username} to team {self.current_team}"
            )
            QMessageBox.information(self, "Success", f"{username} successfully added to the team!")

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "Teams file not found!")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Unexpected error occurred: {e}")



    def get_user_team(self, username):
        """Check which team the user belongs to."""
        try:
            with open('teams.txt', 'r') as f:
                teams = f.readlines()

            for team in teams:
                team_name, members = team.strip().split(": ")
                if username in members.split(", "):
                    return team_name
        except FileNotFoundError:
            pass
        return None

    def view_team(self):
        """Show the team and its members that the user belongs to."""
        if self.current_user is None:
            QMessageBox.warning(self, "Error", "Please log in first.")
            return

        team_name = self.get_user_team(self.current_user)

        if not team_name:
            QMessageBox.warning(self, "Error", "You are not a member of any team.")
            return

        team_members = self.get_team_members(team_name)

        team_info_window = QDialog()
        team_info_window.setWindowTitle(f"{team_name} Team")
        team_info_window.setGeometry(800, 400, 200, 300)
        layout = QVBoxLayout()

        team_name_label = QLabel(f"Team Name: {team_name}")
        layout.addWidget(team_name_label)

        members_label = QLabel("Members:")
        layout.addWidget(members_label)

        for member in team_members:
            member_label = QLabel(member)
            layout.addWidget(member_label)

        close_button = QPushButton("Close")
        close_button.clicked.connect(team_info_window.close)
        layout.addWidget(close_button)

        team_info_window.setLayout(layout)
        team_info_window.exec_()

    def get_team_members(self, team_name):
        """Return the members of a team."""
        try:
            with open('teams.txt', 'r') as f:
                teams = f.readlines()

            for team in teams:
                stored_team_name, members = team.strip().split(':')
                if stored_team_name == team_name:
                    return members.split(',')

            return []

        except FileNotFoundError:
            return []

    def add_notification(self, username, message):
        """Add a notification for a specific user."""
        try:
            with open('notifications.txt', 'a') as f:
                f.write(f"{username},{message}\n")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add notification: {e}")

    def show_notifications(self, username):
        """Show notifications for the user and remove displayed ones."""
        try:
            with open('notifications.txt', 'r') as f:
                lines = f.readlines()

            notifications = []
            remaining_notifications = []

            for line in lines:
                if ',' not in line:
                    remaining_notifications.append(line)
                    continue

                stored_username, message = line.strip().split(',', 1)
                if stored_username == username:
                    notifications.append(message)
                else:
                    remaining_notifications.append(line)

            if notifications:
                QMessageBox.information(self, "Notifications", "\n".join(notifications))
            else:
                QMessageBox.information(self, "Notifications", "You have no notifications.")

            with open('notifications.txt', 'w') as f:
                f.writelines(remaining_notifications)

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "Notification file not found.")

    def share_file_with_team(self, username):
        """Share selected files with the user's team."""
        user_team = self.get_user_team(username)

        if not user_team:
            QMessageBox.warning(self, "Error", "You are not a member of any team!")
            return

        selected_items = self.file_list_widget.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, "Error", "No files selected for sharing.")
            return

        for item in selected_items:
            file_name = item.text().split(' - ')[0]
            user_folder = os.path.join("backups", username)
            file_path = os.path.join(user_folder, file_name)

            if not os.path.exists(file_path):
                QMessageBox.warning(self, "Error", f"{file_name} not found!")
                continue

            file_size = os.path.getsize(file_path) / (1024 * 1024)
            remaining_quota = self.get_user_quota(username)

            if file_size > remaining_quota:
                QMessageBox.warning(self, "Error", f"The file {file_size:.2f} MB exceeds the available quota of {remaining_quota:.2f} MB.")
                return

            team_folder = os.path.join("team_uploads", user_team)
            os.makedirs(team_folder, exist_ok=True)

            dest_path = os.path.join(team_folder, file_name)

            try:
                with open(file_path, 'rb') as src_file, open(dest_path, 'wb') as dest_file:
                    dest_file.write(src_file.read())

                with open('team_files.txt', 'a') as f:
                    f.write(f"{user_team},{file_name}\n")

                self.update_user_quota(username, remaining_quota - file_size)

                QMessageBox.information(self, "Success", f"{file_name} successfully shared with the team!")

                self.log_event(
                    category="Team",
                    operation_code="SHARE_FILE",
                    status_code="SUCCESS",
                    source_path=file_path,
                    data_size=file_size
                )        

            except Exception as e:
                self.log_event(
                    category="Team",
                    operation_code="SHARE_FILE",
                    status_code="FAILED",
                    source_path=file_path
                )
                QMessageBox.critical(self, "Error", f"An error occurred while sharing the file: {str(e)}")

    def view_team_files(self, username):
        """View shared files within the user's team."""
        user_team = self.get_user_team(username)

        if not user_team:
            QMessageBox.warning(self, "Error", "You are not a member of any team!")
            return

        team_files = []
        try:
            with open('team_files.txt', 'r') as f:
                for line in f:
                    stored_team, file_name = line.strip().split(',', 1)
                    if stored_team == user_team:
                        team_files.append(file_name)
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "Team files not found.")
            return

        if not team_files:
            QMessageBox.information(self, "Info", f"No files shared in '{user_team}' team.")
            return

        file_list_dialog = QDialog(self)
        file_list_dialog.setWindowTitle(f"{user_team} Team Files")
        file_list_dialog.setGeometry(800, 400, 600, 400)
        layout = QVBoxLayout(file_list_dialog)

        file_list_widget = QListWidget(file_list_dialog)

        for file_name in team_files:
            file_item = QListWidgetItem(file_name)
            file_list_widget.addItem(file_item)

        layout.addWidget(file_list_widget)

        def open_team_file(item):
            file_name = item.text()
            team_folder = os.path.join("team_uploads", user_team)
            file_path = os.path.join(team_folder, file_name)
            if os.path.exists(file_path):
                try:
                    os.startfile(file_path)
                except AttributeError:
                    import subprocess
                    subprocess.call(["xdg-open", file_path])
            else:
                QMessageBox.warning(self, "Error", "File not found.")

        file_list_widget.itemDoubleClicked.connect(open_team_file)

        close_button = QPushButton("Close", file_list_dialog)
        close_button.clicked.connect(file_list_dialog.close)
        layout.addWidget(close_button)

        file_list_dialog.setLayout(layout)
        file_list_dialog.exec_()


    def select_and_sync_folder(self):
        """Select a folder and start synchronization."""
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "")

        if not folder_path:
            QMessageBox.warning(self, "Error", "No folder selected.")
            return

        if folder_path in self.sync_folders:
            QMessageBox.information(self, "Info", "This folder is already being watched.")
            return

        self.sync_folders.append(folder_path)
        self.save_synced_folders()

        backup_folder = os.path.join("backups", self.current_user)
        os.makedirs(backup_folder, exist_ok=True)

        self.sync_folder(folder_path, backup_folder)
        self.start_observing_folder(folder_path, backup_folder)

    def start_observing_folder(self, folder_path, backup_folder):
        """Configure a folder for observation."""
        if not self.sync_observer:
            self.sync_observer = Observer()

        event_handler = FolderSyncHandler(lambda: self.sync_folder(folder_path, backup_folder))
        self.sync_observer.schedule(event_handler, folder_path, recursive=True)

        if not self.sync_observer.is_alive():
            self.sync_observer.start()

    def sync_folder(self, source_folder, backup_folder):
        """Synchronize the source folder with the backup folder and update the quota."""
        def update_progress_bar(value):
            QTimer.singleShot(0, lambda: self.progress_bar.setValue(value))

        def sync():
            total_files = sum(len(files) for _, _, files in os.walk(source_folder))
            self.progress_bar.setMaximum(total_files)
            self.progress_bar.setValue(0)

            processed_files = 0
            remaining_quota = self.get_user_quota(self.current_user)

            for root, dirs, files in os.walk(source_folder):
                relative_path = os.path.relpath(root, source_folder)
                backup_path = os.path.join(backup_folder, relative_path)
                os.makedirs(backup_path, exist_ok=True)

                for backup_file in os.listdir(backup_path):
                    backup_file_path = os.path.join(backup_path, backup_file)
                    source_file_path = os.path.join(root, backup_file)
                    if not os.path.exists(source_file_path):
                        try:
                            if os.path.isdir(backup_file_path):
                                shutil.rmtree(backup_file_path)
                            else:
                                os.remove(backup_file_path)
                            print(f"Deleted: {backup_file_path}")
                        except Exception as e:
                            print(f"Delete error: {e}")
                        processed_files += 1
                        update_progress_bar(processed_files)

                for file in files:
                    source_file = os.path.join(root, file)
                    backup_file = os.path.join(backup_path, file)

                    try:
                        if os.path.exists(backup_file) and os.path.getmtime(source_file) <= os.path.getmtime(backup_file):
                            continue

                        file_size = os.path.getsize(source_file) / (1024 * 1024)
                        if file_size > remaining_quota:
                            print(f"Error: {source_file} exceeds quota ({file_size:.2f} MB, remaining: {remaining_quota:.2f} MB)")
                            continue

                        with open(source_file, 'rb') as src, open(backup_file, 'wb') as dst:
                            shutil.copyfileobj(src, dst)
                        self.update_user_quota(self.current_user, remaining_quota - file_size)
                        remaining_quota -= file_size
                        print(f"Copied: {source_file} -> {backup_file}")

                        self.log_event(
                            category="Backup",
                            operation_code="SYNC_FOLDER",
                            status_code="SUCCESS",
                            source_path=source_folder,
                            data_size=remaining_quota
                        )

                    except PermissionError:
                        print(f"Access error: {source_file}")
                    except Exception as e:
                        self.log_event(
                            category="Backup",
                            operation_code="SYNC_FOLDER",
                            status_code="FAILED",
                            source_path=source_folder
                        )
                        print(f"Copy error: {e}")

                    processed_files += 1
                    update_progress_bar(processed_files)

            QTimer.singleShot(0, lambda: self.progress_bar.hide())

        sync_thread = Thread(target=sync)
        sync_thread.start()

    def show_sync_completed_message(self):
        QMessageBox.information(self, "Synchronization", "Folder synchronized successfully.")

    def perform_scheduled_sync(self):
        """Perform scheduled synchronization."""
        for folder_path in self.sync_folders:
            backup_folder = os.path.join("backups", self.current_user)
            self.sync_folder(folder_path, backup_folder)

    def save_synced_folders(self):
        """Save synchronized folders to a file."""
        try:
            with open(f"{self.current_user}_synced_folders.txt", "w") as f:
                for folder in self.sync_folders:
                    f.write(folder + "\n")
        except Exception as e:
            print(f"Error: {e}")

    def load_synced_folders(self):
        """Load synchronized folders from a file."""
        try:
            with open(f"{self.current_user}_synced_folders.txt", "r") as f:
                self.sync_folders = [line.strip() for line in f.readlines()]

            for folder in self.sync_folders:
                backup_folder = os.path.join("backups", self.current_user)
                os.makedirs(backup_folder, exist_ok=True)

                if not self.sync_observer:
                    self.sync_observer = Observer()

                event_handler = FolderSyncHandler(lambda: self.sync_folder(folder, backup_folder))
                self.sync_observer.schedule(event_handler, folder, recursive=True)

            if self.sync_observer:
                self.sync_observer.start()

        except FileNotFoundError:
            pass

    def remove_sync_folder(self):
        """Remove a folder from synchronization."""
        folder_path, ok = QFileDialog.getExistingDirectory(self, "Remove Sync", ""), True

        if not folder_path or not ok:
            QMessageBox.warning(self, "Error", "No folder selected.")
            return

        if folder_path in self.sync_folders:
            for watch in self.sync_observer._watches:
                if watch.path == folder_path:
                    self.sync_observer.unschedule(watch)
                    break
            self.sync_folders.remove(folder_path)
            self.save_synced_folders()
            QMessageBox.information(self, "Success", f"{folder_path} removed from synchronization.")
        else:
            QMessageBox.warning(self, "Error", "The selected folder is not being watched.")

    def closeEvent(self, event):
        """Stop the observer when the window closes."""
        if self.sync_observer:
            self.sync_observer.stop()
            self.sync_observer.join()
        event.accept()

    def get_user_quota(self, username):
        """Return the current quota of the user."""
        try:
            with open('users.txt', 'r') as f:
                users = f.readlines()

            for user in users:
                role, stored_username, _, quota = user.strip().split(',')
                if stored_username == username:
                    return float(quota)

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "User file not found!")
            return 0

    def update_user_quota(self, username, new_quota):
        """Update the quota of the user."""
        try:
            with open('users.txt', 'r') as f:
                users = f.readlines()

            updated_users = []
            for user in users:
                role, stored_username, password, quota = user.strip().split(',')
                if stored_username == username:
                    updated_users.append(f"{role},{stored_username},{password},{new_quota}\n")
                else:
                    updated_users.append(user)

            with open('users.txt', 'w') as f:
                f.writelines(updated_users)

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "User file not found!")

    def log_event(self, category, operation_code, status_code, source_path=None, data_size=None, user=None, message=None):
        """Log an event."""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{category}.txt")

        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_message = (
            f"Start Time: {start_time}, End Time: {end_time}, "
            f"Operation Code: {operation_code}, Status Code: {status_code}, "
            f"User: {user}, Source Path: {source_path}, Data Size: {data_size}MB, Message: {message}\n"
        )

        with open(log_file, "a") as f:
            f.write(log_message)

    def check_attempts(self, log_file, username, time_limit_minutes=5, max_attempts=3):
        """Check actions within a specified time frame."""
        try:
            with open(log_file, "r") as f:
                lines = f.readlines()

            now = datetime.datetime.now()
            count = 0

            for line in lines:
                logged_username, timestamp = line.strip().split(",")
                if logged_username == username:
                    log_time = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    if (now - log_time).total_seconds() <= time_limit_minutes * 60:
                        count += 1
                        if count >= max_attempts:
                            return True
            return False

        except FileNotFoundError:
            return False

    def track_failed_login(self, username):
        """Track failed login attempts and notify admin if necessary."""
        log_file = "failed_login_attempts.txt"
        with open(log_file, "a") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{username},{timestamp}\n")

        if self.check_attempts(log_file, username):
            with open("notifications.txt", "a") as notif_file:
                notif_file.write(f"Admin: User {username} attempted login 3 times in 5 minutes.\n")

            QMessageBox.warning(None, "Warning", "You have failed to log in 3 times in 5 minutes. Your account may be temporarily locked.")

    def track_password_change_request(self, username):
        """Track password change requests and notify admin if necessary."""
        log_file = "password_change_requests.txt"
        with open(log_file, "a") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{username},{timestamp}\n")

        if self.check_attempts(log_file, username):
            with open("notifications.txt", "a") as notif_file:
                notif_file.write(f"Admin: User {username} made 3 password change requests in 5 minutes.\n")

            QMessageBox.warning(None, "Warning", "You have made 3 password change requests in 5 minutes. Please refrain from further attempts.")

    def show_log_files(self):
        """List log files and open them on double-click."""
        log_folder = "logs"
        if not os.path.exists(log_folder):
            QMessageBox.warning(self, "Error", "Log files not found.")
            return

        files = os.listdir(log_folder)
        if not files:
            QMessageBox.information(self, "Info", "No log files found.")
            return

        self.log_file_list_dialog = QDialog(self)
        self.log_file_list_dialog.setWindowTitle("Log Files")
        self.log_file_list_dialog.setGeometry(800, 400, 600, 400)
        layout = QVBoxLayout(self.log_file_list_dialog)

        log_list_widget = QListWidget(self.log_file_list_dialog)
        for log_file in files:
            file_item = QListWidgetItem(log_file)
            log_list_widget.addItem(file_item)

        def open_log_file(item):
            file_name = item.text()
            file_path = os.path.join(log_folder, file_name)
            if os.path.exists(file_path):
                try:
                    os.startfile(file_path)
                except AttributeError:
                    import subprocess
                    subprocess.call(["xdg-open", file_path])
            else:
                QMessageBox.warning(self, "Error", "Log file not found.")

        log_list_widget.itemDoubleClicked.connect(open_log_file)

        layout.addWidget(log_list_widget)
        close_button = QPushButton("Close", self.log_file_list_dialog)
        close_button.clicked.connect(self.log_file_list_dialog.close)
        layout.addWidget(close_button)

        self.log_file_list_dialog.setLayout(layout)
        self.log_file_list_dialog.exec_()

    def show_user_files(self):
        """List user files and open them on double-click."""
        user_folders = "backups"
        if not os.path.exists(user_folders):
            QMessageBox.warning(self, "Error", "User folders not found.")
            return

        user_dirs = os.listdir(user_folders)
        if not user_dirs:
            QMessageBox.information(self, "Info", "No user folders found.")
            return

        self.user_file_list_dialog = QDialog(self)
        self.user_file_list_dialog.setWindowTitle("User Files")
        self.user_file_list_dialog.setGeometry(800, 400, 600, 400)
        layout = QVBoxLayout(self.user_file_list_dialog)

        user_list_widget = QListWidget(self.user_file_list_dialog)
        for user in user_dirs:
            user_path = os.path.join(user_folders, user)
            if os.path.isdir(user_path):
                user_item = QListWidgetItem(user)
                user_item.setData(Qt.UserRole, user_path)
                user_list_widget.addItem(user_item)

        def open_user_folder(item):
            folder_path = item.data(Qt.UserRole)
            if os.path.exists(folder_path):
                try:
                    os.startfile(folder_path)
                except AttributeError:
                    import subprocess
                    subprocess.call(["xdg-open", folder_path])
            else:
                QMessageBox.warning(self, "Error", "Folder not found.")

        user_list_widget.itemDoubleClicked.connect(open_user_folder)

        layout.addWidget(user_list_widget)
        close_button = QPushButton("Close", self.user_file_list_dialog)
        close_button.clicked.connect(self.user_file_list_dialog.close)
        layout.addWidget(close_button)

        self.user_file_list_dialog.setLayout(layout)
        self.user_file_list_dialog.exec_()

    def show_user_data(self):
        """Display usernames and hashed passwords."""
        try:
            with open('users.txt', 'r') as f:
                users = f.readlines()

            if not users:
                QMessageBox.information(self, "Info", "No user data found.")
                return

            user_data_dialog = QDialog(self)
            user_data_dialog.setWindowTitle("User Data")
            user_data_dialog.setGeometry(800, 400, 400, 400)
            layout = QVBoxLayout(user_data_dialog)

            user_list_widget = QListWidget(user_data_dialog)
            for user in users:
                role, username, hashed_password, _ = user.strip().split(',')
                if role != "Admin":
                    user_list_widget.addItem(f"Username: {username}, Hashed Password: {hashed_password}")

            layout.addWidget(user_list_widget)
            close_button = QPushButton("Close", user_data_dialog)
            close_button.clicked.connect(user_data_dialog.close)
            layout.addWidget(close_button)

            user_data_dialog.setLayout(layout)
            user_data_dialog.exec_()

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "User file not found!")

    def show_team_files(self):
        """List team files and open them on double-click."""
        team_folder = "team_uploads"
        if not os.path.exists(team_folder):
            QMessageBox.warning(self, "Error", "Team files not found.")
            return

        team_dirs = os.listdir(team_folder)
        if not team_dirs:
            QMessageBox.information(self, "Info", "No team folders found.")
            return

        self.team_file_list_dialog = QDialog(self)
        self.team_file_list_dialog.setWindowTitle("Team Files")
        self.team_file_list_dialog.setGeometry(800, 400, 600, 400)
        layout = QVBoxLayout(self.team_file_list_dialog)

        team_list_widget = QListWidget(self.team_file_list_dialog)
        for team in team_dirs:
            team_path = os.path.join(team_folder, team)
            if os.path.isdir(team_path):
                team_item = QListWidgetItem(team)
                team_item.setData(Qt.UserRole, team_path)
                team_list_widget.addItem(team_item)

        def show_team_files_in_folder(item):
            selected_team_path = item.data(Qt.UserRole)
            if os.path.exists(selected_team_path):
                self.display_team_files(selected_team_path)
            else:
                QMessageBox.warning(self, "Error", "Team folder not found.")

        team_list_widget.itemDoubleClicked.connect(show_team_files_in_folder)

        layout.addWidget(team_list_widget)
        close_button = QPushButton("Close", self.team_file_list_dialog)
        close_button.clicked.connect(self.team_file_list_dialog.close)
        layout.addWidget(close_button)

        self.team_file_list_dialog.setLayout(layout)
        self.team_file_list_dialog.exec_()

    def display_team_files(self, team_path):
        """List files in a team folder and open them on double-click."""
        files = os.listdir(team_path)
        if not files:
            QMessageBox.information(self, "Info", "No files uploaded for this team.")
            return

        file_list_dialog = QDialog(self)
        file_list_dialog.setWindowTitle(f"Team Files: {os.path.basename(team_path)}")
        file_list_dialog.setGeometry(800, 400, 600, 400)
        layout = QVBoxLayout(file_list_dialog)

        file_list_widget = QListWidget(file_list_dialog)
        for file_name in files:
            file_item = QListWidgetItem(file_name)
            file_item.setData(Qt.UserRole, os.path.join(team_path, file_name))
            file_list_widget.addItem(file_item)

        def open_team_file(item):
            file_path = item.data(Qt.UserRole)
            if os.path.exists(file_path):
                try:
                    os.startfile(file_path)
                except AttributeError:
                    import subprocess
                    subprocess.call(["xdg-open", file_path])
            else:
                QMessageBox.warning(self, "Error", "File not found.")

        file_list_widget.itemDoubleClicked.connect(open_team_file)

        layout.addWidget(file_list_widget)
        close_button = QPushButton("Close", file_list_dialog)
        close_button.clicked.connect(file_list_dialog.close)
        layout.addWidget(close_button)

        file_list_dialog.setLayout(layout)
        file_list_dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())