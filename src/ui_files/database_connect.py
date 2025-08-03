# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'database_connect.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QLineEdit, QSizePolicy, QWidget)

class Ui_db_dialog(object):
    def setupUi(self, db_dialog):
        if not db_dialog.objectName():
            db_dialog.setObjectName(u"db_dialog")
        db_dialog.resize(417, 300)
        db_dialog.setModal(True)
        self.buttonBox = QDialogButtonBox(db_dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(40, 210, 341, 31))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.name_edit = QLineEdit(db_dialog)
        self.name_edit.setObjectName(u"name_edit")
        self.name_edit.setGeometry(QRect(150, 10, 241, 21))
        self.db_label = QLabel(db_dialog)
        self.db_label.setObjectName(u"db_label")
        self.db_label.setGeometry(QRect(40, 10, 58, 16))
        self.User_label = QLabel(db_dialog)
        self.User_label.setObjectName(u"User_label")
        self.User_label.setGeometry(QRect(40, 50, 61, 21))
        self.user_edit = QLineEdit(db_dialog)
        self.user_edit.setObjectName(u"user_edit")
        self.user_edit.setGeometry(QRect(150, 50, 241, 21))
        self.system_label = QLabel(db_dialog)
        self.system_label.setObjectName(u"system_label")
        self.system_label.setGeometry(QRect(40, 95, 71, 21))
        self.system_edit = QLineEdit(db_dialog)
        self.system_edit.setObjectName(u"system_edit")
        self.system_edit.setGeometry(QRect(150, 90, 241, 21))
        self.adress_label = QLabel(db_dialog)
        self.adress_label.setObjectName(u"adress_label")
        self.adress_label.setGeometry(QRect(40, 130, 71, 16))
        self.adress_edit = QLineEdit(db_dialog)
        self.adress_edit.setObjectName(u"adress_edit")
        self.adress_edit.setGeometry(QRect(150, 130, 241, 21))
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.adress_edit.setFont(font)
        self.password_label = QLabel(db_dialog)
        self.password_label.setObjectName(u"password_label")
        self.password_label.setGeometry(QRect(40, 170, 101, 16))
        self.password_edit = QLineEdit(db_dialog)
        self.password_edit.setObjectName(u"password_edit")
        self.password_edit.setGeometry(QRect(150, 170, 241, 21))
        self.password_edit.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)

        self.retranslateUi(db_dialog)
        self.buttonBox.accepted.connect(db_dialog.accept)
        self.buttonBox.rejected.connect(db_dialog.reject)

        QMetaObject.connectSlotsByName(db_dialog)
    # setupUi

    def retranslateUi(self, db_dialog):
        db_dialog.setWindowTitle(QCoreApplication.translate("db_dialog", u"Dialog", None))
        self.db_label.setText(QCoreApplication.translate("db_dialog", u"DB_name", None))
        self.User_label.setText(QCoreApplication.translate("db_dialog", u"DB_user", None))
        self.system_label.setText(QCoreApplication.translate("db_dialog", u"DB_system", None))
        self.adress_label.setText(QCoreApplication.translate("db_dialog", u"DB_adress", None))
        self.password_label.setText(QCoreApplication.translate("db_dialog", u"DB_password", None))
    # retranslateUi

