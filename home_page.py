import sys
import numpy as np
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt

class HomePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.load_styles()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)  # เพิ่มระยะห่างระหว่างปุ่ม

        # สร้าง Header Widget และตั้งชื่อ object
        self.header = QWidget(self)
        self.header.setObjectName("header")  # กำหนด object name
        self.header.setFixedHeight(300)
        
        header_layout = QVBoxLayout(self.header)
        
        # โลโก้ (ใช้ QIcon แทนการโหลดจากไฟล์)
        logo_btn = QPushButton()
        logo_btn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        logo_btn.setIconSize(QSize(240, 240))
        logo_btn.setFlat(True)
        logo_btn.setStyleSheet("background-color: transparent;")
        
        # ชื่อแอป
        title_label = QLabel("MLP Classifier Digit Recognizer")
        title_label.setObjectName("title")
        
        header_layout.addStretch()
        header_layout.addWidget(logo_btn, alignment=Qt.AlignCenter)
        header_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        header_layout.addStretch()

        # เมนูปุ่ม
        self.btn_writing = QPushButton("HandWriting", self)
        self.btn_writing.setObjectName("menuBtn")
        self.btn_writing.clicked.connect(lambda: self.parent.stacked_widget.setCurrentIndex(1))

        self.btn_guide = QPushButton("Guide", self)
        self.btn_guide.setObjectName("menuBtn")
        self.btn_guide.clicked.connect(lambda: self.parent.stacked_widget.setCurrentIndex(2))

        # เพิ่ม SpacerItem ก่อนและหลังปุ่มเพื่อจัดตำแหน่งกลาง
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # จัด Layout หลัก
        self.layout.addWidget(self.header, alignment=Qt.AlignCenter)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.btn_writing, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.btn_guide, alignment=Qt.AlignCenter)
        
        # เพิ่ม SpacerItem ด้านล่างเพื่อจัดตำแหน่ง
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(self.layout)

    def load_styles(self):
        # ตั้งค่า Style Sheet
        self.setStyleSheet("""
            QLabel#title {
                font-size: 42px;
                font-weight: 300;
                margin-top: 20px;
            }
            QPushButton#menuBtn {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 2px solid #4C566A;
                border-radius: 10px;
                padding: 15px 30px;
                min-width: 250px;
                font-size: 18px;
            }
            QPushButton#menuBtn:hover {
                background-color: #434C5E;
                border-color: #5E81AC;
            }
        """)