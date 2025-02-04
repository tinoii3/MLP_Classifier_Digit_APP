import sys
import numpy as np
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class GuidePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.load_styles()
    
    def init_ui(self):
        # ใช้ QVBoxLayout หลัก
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)  # กำหนดระยะห่างระหว่างส่วนต่างๆ

        # Header Section
        self.header = QLabel("MLP Classifier Guide")
        self.header.setObjectName("guideTitle")
        self.header.setAlignment(Qt.AlignCenter)

        # กล่องข้อความ
        self.text_box = QTextEdit()
        self.text_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text_box.setFixedHeight(350)
        self.text_box.setFixedWidth(480)
        self.text_box.setReadOnly(True)
        self.text_box.setObjectName("guideText")

        # Control Button (อยู่นอกกรอบกราฟ)
        self.btn_back = QPushButton("Back to Menu")
        self.btn_back.setObjectName("guideBtn")
        self.btn_back.clicked.connect(lambda: self.parent.stacked_widget.setCurrentIndex(0))
        
        # Add Widgets to Main Layout
        # ใช้ QGridLayout เพื่อควบคุมตำแหน่งให้จัดกึ่งกลาง
        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))  # เพิ่มระยะห่างด้านบน
        self.layout.addWidget(self.header, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.text_box, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.btn_back, alignment=Qt.AlignCenter)
        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))  # เพิ่มระยะห่างด้านล่าง
        
        self.setLayout(self.layout)
        self.load_guide_content()

    def load_styles(self):
        # ตั้งค่า Style Sheet
        self.setStyleSheet("""
            QLabel#guideTitle {
                font-size: 42px;
                font-weight: 300;
                margin-top: 20px;
                font-weight: bold;
            }
            QPushButton#guideBtn {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 2px solid #4C566A;
                border-radius: 10px;
                padding: 15px 30px;
                min-width: 250px;
                font-size: 18px;
            }
            QPushButton#guideBtn:hover {
                background-color: #434C5E;
                border-color: #5E81AC;
            }
            QTextEdit#guideText {
                background-color: #3B4252;
                color: white;
                border: 2px solid #4C566A;
                border-radius: 10px;
                padding: 15px;
                font-size: 14px;
            }
        """)
        
    def load_guide_content(self):
        guide_text = """
        <div>
            <!-- ส่วนข้อความ -->
            <div style="margin-bottom: 10px;">
                <h2 style="font-weight: bold;">ขั้นตอนการใช้งาน:</h2>
                <div style="font-size: 18px;">
                    <ol>
                        <li style="margin-bottom: 5px;">ใช้เมาส์วาดตัวเลข (0-9) ในพื้นที่วาดสีดำ</li>
                        <li style="margin-bottom: 5px;" >ระบบจะประมวลผลและแสดงผลลัพธ์เป็นข้อความ สีเขียวเหนือตัวเลขทันที</li>
                        <li style="margin-bottom: 5px;">กดปุ่ม "Clear Canvas" เพื่อล้างพื้นที่วาดและเริ่มใหม่</li>
                        <li style="margin-bottom: 5px;">กดปุ่ม "Back to Menu" เพื่อกลับไปหน้าเมนูหลัก</li>
                    </ol>
                    <h2 style="margin-bottom: 5px;">ข้อควรทราบ:</h2>
                    <ol>
                        <li style="margin-bottom: 5px;">เขียนตัวเลขให้ชัดเจนในกรอบสีดำ</li>
                        <li style="margin-bottom: 5px;">ผลลัพธ์อาจคลาดเคลื่อนหากตัวเลขเบี้ยวหรือเล็กเกิน ไป</li>
                    </ol>
                </div>
            </div>
        </div>
        """
        self.text_box.setHtml(guide_text)
        self.text_box.setAlignment(Qt.AlignCenter)