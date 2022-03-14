# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 20:04:06 2022

@author: kdrcn
"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from datetime import datetime
import sys
from PyQt5 import QtWidgets

from PyQt5.QtGui import QIntValidator
import requests

class Arayuz(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.miktar1=QtWidgets.QLineEdit()
        self.miktar2=QtWidgets.QLineEdit()
        self.doviz1=QtWidgets.QComboBox()
        self.doviz2=QtWidgets.QComboBox()
        self.adres=QtWidgets.QLineEdit()
        self.gonder=QtWidgets.QPushButton("E-Posta Olarak Gönder")
        self.zaman=QtWidgets.QLabel()
        self.zaman.setText("--/--/--")
        self.guncelle=QtWidgets.QPushButton("Veri Al")
        self.hesapla=QtWidgets.QPushButton("Hesapla")
        self.epostaIcerik=QtWidgets.QPlainTextEdit()
        self.ekle=QtWidgets.QPushButton("Ekle")
        self.dovizDurum=False    
    
        hBox1=QtWidgets.QHBoxLayout()
        hBox1.addWidget(self.miktar1)
        hBox1.addWidget(self.doviz1)
        
        hBox2=QtWidgets.QHBoxLayout()
        hBox2.addWidget(self.miktar2)
        hBox2.addWidget(self.doviz2)
        
        hBox3=QtWidgets.QHBoxLayout()
        hBox3.addStretch()
        hBox3.addWidget(self.gonder)
        
        hBox4=QtWidgets.QHBoxLayout()
        hBox4.addWidget(self.ekle)
        hBox4.addWidget(self.hesapla)
        
        vBox=QtWidgets.QVBoxLayout()
        vBox.addLayout(hBox1)
        vBox.addLayout(hBox2)
        vBox.addWidget(self.zaman)
        vBox.addLayout(hBox4)
        vBox.addWidget(self.guncelle)
        vBox.addWidget(self.epostaIcerik)
        vBox.addStretch()
        vBox.addWidget(self.adres)
        vBox.addLayout(hBox3)
        vBox.addStretch()
        
        self.guncelle.clicked.connect(self.veriAl)
        self.hesapla.clicked.connect(self.dovizHesapla)
        self.gonder.clicked.connect(self.epostaGonder)
        self.ekle.clicked.connect(self.icerikEkle)
        
        self.onlyInt = QIntValidator()
        self.miktar1.setValidator(self.onlyInt)
        self.miktar2.setReadOnly(True)
        self.setLayout(vBox)
        self.setWindowTitle("Döviz Çevirici")
        self.setGeometry(600,300,350,400)
        self.show()
        
    def veriAl(self):
        # url="http://data.fixer.io/api/latest?access_key=eaa83080789013171157063c91eb4565&format=1"
        url = " { JSON DATAS }
        r=requests.get(url)
        j=r.json()
        zaman=j["timestamp"]
        zaman=datetime.fromtimestamp(zaman)
        self.zaman.setText(datetime.ctime(zaman))
        self.dovizList=j["rates"]
        for i,k in self.dovizList.items():
            self.doviz1.addItem(str(i))
            self.doviz2.addItem(str(i))
        self.epostaIcerik.textCursor().insertText(datetime.ctime(zaman)+"\n\n")
            
    def dovizHesapla(self):
        if self.miktar1.text():
            self.miktar2.setText(str(self.dovizList[self.doviz2.currentText()]/self.dovizList[self.doviz1.currentText()]))
            self.dovizDurum=True
        else:
            self.miktar1.setText("Buraya miktar giriniz!")
            self.miktar2.setText("Uygunsuz hesaplama!")
            
    def epostaGonder(self):
        if self.dovizDurum:
            mesaj=MIMEMultipart()
            mesaj["From"]=" {E-MAIL} "
            mesaj["To"]=self.adres.text()
            
            mesaj["Subject"]=" {E-MAIL SUBJECT} "
            icerik=self.epostaIcerik.toPlainText()
            mesaj_govdesi=MIMEText(icerik,"plain")
            mesaj.attach(mesaj_govdesi)
            try:
                mail=smtplib.SMTP("smtp.gmail.com",587)
                mail.ehlo()
                mail.starttls()
                mail.login(" {E-MAIL} ", " {PASSWORD} ")
                mail.sendmail(mesaj["From"],mesaj["To"],mesaj.as_string())
                mail.close()
            except:
                sys.stderr.write("BAŞARAMADIK")
                sys.stderr.flush()
        else:
            self.miktar1.setText("Uygunsuz hesaplama!")
            self.miktar2.setText("Uygunsuz hesaplama!")
            
    def icerikEkle(self):
        if self.dovizDurum:
            self.epostaIcerik.textCursor().insertText("{} {}={} {}\n\n".format(self.miktar1.text(),self.doviz1.currentText(),self.miktar2.text(),self.doviz2.currentText()))
        else:
            self.miktar1.setText("Uygunsuz hesaplama!")
            self.miktar2.setText("Uygunsuz hesaplama!")
        
app = QtWidgets.QApplication(sys.argv)
uygulama=Arayuz()
sys.exit(app.exec_())





















