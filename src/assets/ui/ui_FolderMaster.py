# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FolderMasterqVwDHh.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTableWidget, QTableWidgetItem, QTextEdit,
    QTreeView, QVBoxLayout, QWidget)
import src.assets.ui.qrc_FolderMaster

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1181, 851)
        icon = QIcon()
        icon.addFile(u":/icons/folder.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"QPushButton {\n"
"	background-color: #3E3E42;\n"
"}")
        MainWindow.setIconSize(QSize(24, 24))
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
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

        self.button_manage_rules = QPushButton(self.frame_title)
        self.button_manage_rules.setObjectName(u"button_manage_rules")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.button_manage_rules.sizePolicy().hasHeightForWidth())
        self.button_manage_rules.setSizePolicy(sizePolicy1)
        self.button_manage_rules.setStyleSheet(u"QPushButton:hover {\n"
"	background-color: #A24334;\n"
"}")

        self.horizontalLayout_4.addWidget(self.button_manage_rules)

        self.button_app_settings = QPushButton(self.frame_title)
        self.button_app_settings.setObjectName(u"button_app_settings")
        sizePolicy1.setHeightForWidth(self.button_app_settings.sizePolicy().hasHeightForWidth())
        self.button_app_settings.setSizePolicy(sizePolicy1)
        self.button_app_settings.setStyleSheet(u"QPushButton:hover {\n"
"	background-color: #A24334;\n"
"}")

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

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_4 = QGroupBox(self.widget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.groupBox_2 = QGroupBox(self.groupBox_4)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFlat(True)
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(2, 6, 2, 2)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.label)

        self.combobox_recent_folders = QComboBox(self.groupBox_2)
        self.combobox_recent_folders.setObjectName(u"combobox_recent_folders")

        self.horizontalLayout_3.addWidget(self.combobox_recent_folders)

        self.button_back = QPushButton(self.groupBox_2)
        self.button_back.setObjectName(u"button_back")
        sizePolicy1.setHeightForWidth(self.button_back.sizePolicy().hasHeightForWidth())
        self.button_back.setSizePolicy(sizePolicy1)
        self.button_back.setStyleSheet(u"QPushButton:hover {\n"
"	background-color: #A24334;\n"
"}")

        self.horizontalLayout_3.addWidget(self.button_back)


        self.verticalLayout_10.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
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
        self.button_browse_folder.setStyleSheet(u"QPushButton:hover {\n"
"	background-color: #A24334;\n"
"}")

        self.horizontalLayout_6.addWidget(self.button_browse_folder)


        self.verticalLayout_10.addLayout(self.horizontalLayout_6)

        self.tree_view_folder = QTreeView(self.groupBox_2)
        self.tree_view_folder.setObjectName(u"tree_view_folder")
        self.tree_view_folder.setAlternatingRowColors(True)

        self.verticalLayout_10.addWidget(self.tree_view_folder)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_sort_by_rule = QLabel(self.groupBox_2)
        self.label_sort_by_rule.setObjectName(u"label_sort_by_rule")
        sizePolicy2.setHeightForWidth(self.label_sort_by_rule.sizePolicy().hasHeightForWidth())
        self.label_sort_by_rule.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.label_sort_by_rule)

        self.combobox_rules = QComboBox(self.groupBox_2)
        self.combobox_rules.addItem("")
        self.combobox_rules.setObjectName(u"combobox_rules")

        self.horizontalLayout_5.addWidget(self.combobox_rules)

        self.button_rule_info = QPushButton(self.groupBox_2)
        self.button_rule_info.setObjectName(u"button_rule_info")
        sizePolicy1.setHeightForWidth(self.button_rule_info.sizePolicy().hasHeightForWidth())
        self.button_rule_info.setSizePolicy(sizePolicy1)
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.HelpFaq))
        self.button_rule_info.setIcon(icon1)
        self.button_rule_info.setAutoDefault(False)
        self.button_rule_info.setFlat(True)

        self.horizontalLayout_5.addWidget(self.button_rule_info)


        self.verticalLayout_10.addLayout(self.horizontalLayout_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_add_to_list = QPushButton(self.groupBox_2)
        self.button_add_to_list.setObjectName(u"button_add_to_list")
        self.button_add_to_list.setStyleSheet(u"QPushButton:hover {\n"
"	background-color: #A24334;\n"
"}")

        self.horizontalLayout.addWidget(self.button_add_to_list)

        self.button_list_files = QPushButton(self.groupBox_2)
        self.button_list_files.setObjectName(u"button_list_files")
        self.button_list_files.setStyleSheet(u"QPushButton:hover {\n"
"	background-color: #A24334;\n"
"}")

        self.horizontalLayout.addWidget(self.button_list_files)


        self.verticalLayout_10.addLayout(self.horizontalLayout)


        self.verticalLayout_7.addWidget(self.groupBox_2)

        self.groupBox_6 = QGroupBox(self.groupBox_4)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setFlat(True)
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(2, 6, 2, 2)
        self.table_widget_batch_rules = QTableWidget(self.groupBox_6)
        if (self.table_widget_batch_rules.columnCount() < 4):
            self.table_widget_batch_rules.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_widget_batch_rules.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_widget_batch_rules.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_widget_batch_rules.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_widget_batch_rules.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.table_widget_batch_rules.setObjectName(u"table_widget_batch_rules")
        self.table_widget_batch_rules.horizontalHeader().setCascadingSectionResizes(True)
        self.table_widget_batch_rules.horizontalHeader().setMinimumSectionSize(100)
        self.table_widget_batch_rules.horizontalHeader().setProperty(u"showSortIndicator", True)
        self.table_widget_batch_rules.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_8.addWidget(self.table_widget_batch_rules)


        self.verticalLayout_7.addWidget(self.groupBox_6)

        self.button_sort = QPushButton(self.groupBox_4)
        self.button_sort.setObjectName(u"button_sort")
        self.button_sort.setStyleSheet(u"QPushButton:hover {\n"
"	background-color: #A24334;\n"
"}")

        self.verticalLayout_7.addWidget(self.button_sort)


        self.verticalLayout_2.addWidget(self.groupBox_4)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox_7 = QGroupBox(self.widget)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setFlat(True)
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(2, 6, 2, 2)
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_rule_name = QLabel(self.groupBox_7)
        self.label_rule_name.setObjectName(u"label_rule_name")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_rule_name.sizePolicy().hasHeightForWidth())
        self.label_rule_name.setSizePolicy(sizePolicy3)

        self.horizontalLayout_7.addWidget(self.label_rule_name)

        self.line_edit_rule_name = QLineEdit(self.groupBox_7)
        self.line_edit_rule_name.setObjectName(u"line_edit_rule_name")
        self.line_edit_rule_name.setClearButtonEnabled(True)

        self.horizontalLayout_7.addWidget(self.line_edit_rule_name)


        self.verticalLayout_11.addLayout(self.horizontalLayout_7)


        self.verticalLayout_9.addLayout(self.verticalLayout_11)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_extensions = QLabel(self.groupBox_7)
        self.label_extensions.setObjectName(u"label_extensions")

        self.horizontalLayout_8.addWidget(self.label_extensions)

        self.line_edit_extensions = QLineEdit(self.groupBox_7)
        self.line_edit_extensions.setObjectName(u"line_edit_extensions")
        self.line_edit_extensions.setClearButtonEnabled(True)

        self.horizontalLayout_8.addWidget(self.line_edit_extensions)


        self.verticalLayout_9.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_opt_folder = QLabel(self.groupBox_7)
        self.label_opt_folder.setObjectName(u"label_opt_folder")

        self.horizontalLayout_9.addWidget(self.label_opt_folder)

        self.line_edit_opt_folder = QLineEdit(self.groupBox_7)
        self.line_edit_opt_folder.setObjectName(u"line_edit_opt_folder")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.line_edit_opt_folder.sizePolicy().hasHeightForWidth())
        self.line_edit_opt_folder.setSizePolicy(sizePolicy4)

        self.horizontalLayout_9.addWidget(self.line_edit_opt_folder)


        self.verticalLayout_9.addLayout(self.horizontalLayout_9)

        self.button_save_rule = QPushButton(self.groupBox_7)
        self.button_save_rule.setObjectName(u"button_save_rule")
        self.button_save_rule.setStyleSheet(u"QPushButton:hover {\n"
"	background-color: #388049;\n"
"}")

        self.verticalLayout_9.addWidget(self.button_save_rule)


        self.verticalLayout_4.addWidget(self.groupBox_7)

        self.groupBox_5 = QGroupBox(self.widget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        sizePolicy3.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy3)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.text_edit_program_output = QTextEdit(self.groupBox_5)
        self.text_edit_program_output.setObjectName(u"text_edit_program_output")

        self.verticalLayout_3.addWidget(self.text_edit_program_output)


        self.verticalLayout_4.addWidget(self.groupBox_5)


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
        QWidget.setTabOrder(self.combobox_rules, self.button_rule_info)
        QWidget.setTabOrder(self.button_rule_info, self.button_list_files)
        QWidget.setTabOrder(self.button_list_files, self.text_edit_program_output)
        QWidget.setTabOrder(self.text_edit_program_output, self.combobox_recent_folders)
        QWidget.setTabOrder(self.combobox_recent_folders, self.button_app_settings)

        self.retranslateUi(MainWindow)

        self.button_rule_info.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Folder Master", None))
        self.label_title.setText(QCoreApplication.translate("MainWindow", u"Folder Master", None))
        self.button_manage_rules.setText(QCoreApplication.translate("MainWindow", u"Manage Rules", None))
        self.button_app_settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Main", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Source", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Recent folders:", None))
        self.button_back.setText(QCoreApplication.translate("MainWindow", u"Go back", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Selected folder:", None))
        self.button_browse_folder.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.label_sort_by_rule.setText(QCoreApplication.translate("MainWindow", u"Sort by rule:", None))
        self.combobox_rules.setItemText(0, QCoreApplication.translate("MainWindow", u"Select a rule...", None))

        self.button_rule_info.setText("")
        self.button_add_to_list.setText(QCoreApplication.translate("MainWindow", u"Add to List", None))
        self.button_list_files.setText(QCoreApplication.translate("MainWindow", u"List Files", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Batch Execution List", None))
        ___qtablewidgetitem = self.table_widget_batch_rules.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Rule Name", None));
        ___qtablewidgetitem1 = self.table_widget_batch_rules.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Extensions", None));
        ___qtablewidgetitem2 = self.table_widget_batch_rules.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Opt. Folder Name", None));
        ___qtablewidgetitem3 = self.table_widget_batch_rules.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Target Structure", None));
        self.button_sort.setText(QCoreApplication.translate("MainWindow", u"Organize", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"Create Custom Rules", None))
        self.label_rule_name.setText(QCoreApplication.translate("MainWindow", u"Custom rule name:", None))
        self.line_edit_rule_name.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter a name for the new rules...", None))
        self.label_extensions.setText(QCoreApplication.translate("MainWindow", u"Add extensions for rule:", None))
        self.line_edit_extensions.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Add file extensions for the new rule (comma-separated)", None))
        self.label_opt_folder.setText(QCoreApplication.translate("MainWindow", u"Optional folder for rule:", None))
        self.line_edit_opt_folder.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter a folder name (Optional)", None))
        self.button_save_rule.setText(QCoreApplication.translate("MainWindow", u"Save New Rule", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Output", None))
    # retranslateUi

