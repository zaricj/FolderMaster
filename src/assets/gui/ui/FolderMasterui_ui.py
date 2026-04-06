# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FolderMasterui.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTextEdit, QTreeView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1181, 851)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_title = QFrame(self.centralwidget)
        self.frame_title.setObjectName(u"frame_title")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_title.sizePolicy().hasHeightForWidth())
        self.frame_title.setSizePolicy(sizePolicy)
        self.frame_title.setStyleSheet(u"")
        self.frame_title.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_title)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_title = QLabel(self.frame_title)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setPointSize(16)
        self.label_title.setFont(font)
        self.label_title.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label_title.setStyleSheet(u"")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_title)

        self.button_app_settings = QPushButton(self.frame_title)
        self.button_app_settings.setObjectName(u"button_app_settings")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.button_app_settings.sizePolicy().hasHeightForWidth())
        self.button_app_settings.setSizePolicy(sizePolicy1)
        self.button_app_settings.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.button_app_settings)


        self.verticalLayout.addWidget(self.frame_title)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        font1 = QFont()
        font1.setPointSize(9)
        self.line.setFont(font1)
        self.line.setStyleSheet(u"")
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setLineWidth(1)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayout.addWidget(self.line)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_6.addWidget(self.label_4)

        self.line_edit_selected_folder = QLineEdit(self.groupBox_2)
        self.line_edit_selected_folder.setObjectName(u"line_edit_selected_folder")
        self.line_edit_selected_folder.setClearButtonEnabled(True)

        self.horizontalLayout_6.addWidget(self.line_edit_selected_folder)

        self.button_browse_folder = QPushButton(self.groupBox_2)
        self.button_browse_folder.setObjectName(u"button_browse_folder")

        self.horizontalLayout_6.addWidget(self.button_browse_folder)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.widget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.label_2)

        self.combobox_rules = QComboBox(self.groupBox)
        self.combobox_rules.addItem("")
        self.combobox_rules.setObjectName(u"combobox_rules")

        self.horizontalLayout_5.addWidget(self.combobox_rules)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_list_files = QPushButton(self.groupBox)
        self.button_list_files.setObjectName(u"button_list_files")

        self.horizontalLayout.addWidget(self.button_list_files)

        self.button_sort = QPushButton(self.groupBox)
        self.button_sort.setObjectName(u"button_sort")

        self.horizontalLayout.addWidget(self.button_sort)


        self.verticalLayout_6.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.groupBox_4 = QGroupBox(self.widget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.button_add_extension = QPushButton(self.groupBox_4)
        self.button_add_extension.setObjectName(u"button_add_extension")

        self.gridLayout.addWidget(self.button_add_extension, 3, 2, 1, 1)

        self.line_edit_extensions = QLineEdit(self.groupBox_4)
        self.line_edit_extensions.setObjectName(u"line_edit_extensions")
        self.line_edit_extensions.setClearButtonEnabled(True)

        self.gridLayout.addWidget(self.line_edit_extensions, 3, 1, 1, 1)

        self.line_edit_rule_name = QLineEdit(self.groupBox_4)
        self.line_edit_rule_name.setObjectName(u"line_edit_rule_name")
        self.line_edit_rule_name.setClearButtonEnabled(True)

        self.gridLayout.addWidget(self.line_edit_rule_name, 1, 1, 1, 1)

        self.label_6 = QLabel(self.groupBox_4)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)

        self.listWidget = QListWidget(self.groupBox_4)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setAutoFillBackground(False)
        self.listWidget.setAlternatingRowColors(True)

        self.gridLayout.addWidget(self.listWidget, 5, 0, 1, 3)

        self.label_5 = QLabel(self.groupBox_4)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.button_manage_rules = QPushButton(self.groupBox_4)
        self.button_manage_rules.setObjectName(u"button_manage_rules")

        self.gridLayout.addWidget(self.button_manage_rules, 1, 2, 1, 1)


        self.verticalLayout_7.addLayout(self.gridLayout)

        self.button_save_rule = QPushButton(self.groupBox_4)
        self.button_save_rule.setObjectName(u"button_save_rule")

        self.verticalLayout_7.addWidget(self.button_save_rule)


        self.verticalLayout_2.addWidget(self.groupBox_4)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox_5 = QGroupBox(self.widget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy3)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.text_edit_program_output = QTextEdit(self.groupBox_5)
        self.text_edit_program_output.setObjectName(u"text_edit_program_output")

        self.verticalLayout_3.addWidget(self.text_edit_program_output)


        self.verticalLayout_4.addWidget(self.groupBox_5)

        self.groupBox_3 = QGroupBox(self.widget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tree_view_folder = QTreeView(self.groupBox_3)
        self.tree_view_folder.setObjectName(u"tree_view_folder")
        self.tree_view_folder.setAlternatingRowColors(True)

        self.verticalLayout_5.addWidget(self.tree_view_folder)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.button_back = QPushButton(self.groupBox_3)
        self.button_back.setObjectName(u"button_back")
        sizePolicy1.setHeightForWidth(self.button_back.sizePolicy().hasHeightForWidth())
        self.button_back.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.button_back)

        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.label)

        self.combobox_recent_folders = QComboBox(self.groupBox_3)
        self.combobox_recent_folders.setObjectName(u"combobox_recent_folders")

        self.horizontalLayout_3.addWidget(self.combobox_recent_folders)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)


        self.verticalLayout_4.addWidget(self.groupBox_3)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)


        self.verticalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1181, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_title.setText(QCoreApplication.translate("MainWindow", u"Folder Master", None))
        self.button_app_settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Source", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Selected folder:", None))
        self.button_browse_folder.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Organization Settings", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Sort by rule:", None))
        self.combobox_rules.setItemText(0, QCoreApplication.translate("MainWindow", u"Select a rule...", None))

        self.button_list_files.setText(QCoreApplication.translate("MainWindow", u"List Files", None))
        self.button_sort.setText(QCoreApplication.translate("MainWindow", u"Organize", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Custom Rule Settings", None))
        self.button_add_extension.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.line_edit_extensions.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Add file extensions for the new rule (comma-separated)", None))
        self.line_edit_rule_name.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter a name for the new rules...", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Add extensions for rule:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Custom rule name:", None))
        self.button_manage_rules.setText(QCoreApplication.translate("MainWindow", u"Manage Rules", None))
        self.button_save_rule.setText(QCoreApplication.translate("MainWindow", u"Save New Rule", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Output", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Folder Structure", None))
        self.button_back.setText(QCoreApplication.translate("MainWindow", u"Go back", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Recent folders:", None))
    # retranslateUi

