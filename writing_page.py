from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import cv2
from tensorflow.keras.models import load_model
import sys
import os

def resource_path(relative_path):
    """ ฟังก์ชันสำหรับหา path ที่ถูกต้องทั้งในโหมดพัฒนาและโหมด Executable """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DrawingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1200, 550)
        self.points = []
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.black)

        try:
            model_path = resource_path("MNIT_model.h5")
            self.model = load_model(model_path)
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
        
        self.LABEL = {
            0: "Zero", 1: "One", 2: "Two", 3: "Three",
            4: "Four", 5: "Five", 6: "Six", 7: "Seven",
            8: "Eight", 9: "Nine"
        }

        self.predictions = []
        self.last_point = QPoint()

        # ภาพหลักสำหรับเก็บทุกสิ่งที่วาด (ARGB32 เพื่อรองรับการผสมภาพ)
        self.drawing_image = QImage(self.size(), QImage.Format_ARGB32)
        self.drawing_image.fill(Qt.black)

        # ภาพชั่วคราวขณะวาด (ARGB32 เพื่อความโปร่งใส)
        self.temporary_image = QImage(self.size(), QImage.Format_ARGB32)
        self.temporary_image.fill(Qt.transparent)

        # ภาพสำหรับแสดงผลรวม
        self.display_image = QImage(self.size(), QImage.Format_ARGB32)
        self.display_image.fill(Qt.black)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()

            # เตรียมภาพชั่วคราว (โปร่งใส)
            self.temporary_image.fill(Qt.transparent)
            painter = QPainter(self.temporary_image)
            painter.setPen(QPen(Qt.white, 4, Qt.SolidLine))
            painter.drawPoint(self.last_point)
            painter.end()
            self.updateTemporaryDisplay()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            painter = QPainter(self.temporary_image)  # วาดลงใน drawing_image
            painter.setPen(QPen(Qt.white, 4, Qt.SolidLine))
            painter.drawLine(self.last_point, event.pos())
            painter.end()

            self.last_point = event.pos()

            self.updateTemporaryDisplay()  # อัปเดต display_image

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            try:
                # ประมวลผลภาพชั่วคราว (เฉพาะเส้นที่เพิ่งวาด)
                self.process_drawing()
                # ผนวกภาพชั่วคราวเข้ากับภาพหลัก (ไม่ทับของเก่า)
                painter = QPainter(self.drawing_image)
                painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
                painter.drawImage(0, 0, self.temporary_image)
                painter.end()
            except Exception as e:
                print(f"Error processing drawing: {e}")
            finally:
                self.updateDisplay()

    def paintEvent(self, event):
        # แสดง QImage เท่านั้น (ไม่ต้องวาดเส้นเพิ่ม)
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.display_image, self.display_image.rect())

    def updateTemporaryDisplay(self):
        """อัปเดตภาพแสดงผลชั่วคราว (ภาพหลัก + ภาพที่กำลังวาด)"""
        self.display_image = self.drawing_image.copy()
        painter = QPainter(self.display_image)
        painter.drawImage(0, 0, self.temporary_image)
        painter.end()
        self.update()

    def process_drawing(self):
        """ประมวลผลภาพชั่วคราวเพื่อทำนายตัวเลข"""
        # แปลง QImage เป็น numpy array
        h, w = self.temporary_image.height(), self.temporary_image.width()
        ptr = self.temporary_image.constBits()
        ptr.setsize(h * w * 4)
        arr = np.frombuffer(ptr, dtype=np.uint8).reshape((h, w, 4))
        
        # แปลงเป็น grayscale (เส้นขาวบนพื้นดำ)
        gray = cv2.cvtColor(arr, cv2.COLOR_RGBA2GRAY)
        if np.all(gray == 0):
            return
        
        # Threshold และหา Contour
        _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # เลือก Contour ที่ใหญ่ที่สุด
            contour = max(contours, key=cv2.contourArea)
            x, y, w_box, h_box = cv2.boundingRect(contour)
            cropped = gray[y:y+h_box, x:x+w_box]
            
            # ปรับขนาดและเพิ่ม Padding
            aspect_ratio = w_box / h_box
            new_size = 20
            if aspect_ratio > 1:
                new_w, new_h = new_size, int(new_size / aspect_ratio)
            else:
                new_h, new_w = new_size, int(new_size * aspect_ratio)
            
            resized = cv2.resize(cropped, (new_w, new_h))
            delta_w, delta_h = 28 - new_w, 28 - new_h
            top = delta_h // 2
            bottom = delta_h - top
            left = delta_w // 2
            right = delta_w - left
            
            padded = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=0)
            
            if padded.shape != (28, 28):
                padded = cv2.resize(padded, (28, 28))
            
            # ทำนายผล
            final_img = padded.astype(np.float32) / 255.0
            prediction = self.model.predict(final_img.reshape(1, 784))
            label = self.LABEL[np.argmax(prediction)]
            
            # คำนวณตำแหน่งข้อความ
            text_x = x + 20  # เยื้องจากตัวเลข
            text_y = y - 30 if y - 30 > 0 else y + 50
            self.predictions.append((label, text_x, text_y))

    def updateDisplay(self):
        """อัปเดตภาพแสดงผลรวม (ภาพหลัก + ข้อความทำนายทั้งหมด)"""
        self.display_image = self.drawing_image.copy()
        painter = QPainter(self.display_image)
        painter.setPen(QColor(0, 255, 0))
        painter.setFont(QFont("Arial", 24, QFont.Bold))
        
        # วาดข้อความทำนายทั้งหมด
        for text, x, y in self.predictions:
            text_width = painter.fontMetrics().width(text)
            if x + text_width > self.width():
                x = self.width() - text_width - 10
            painter.drawText(x, y, text)
        
        painter.end()
        self.update()

    def clear_canvas(self):
        """ล้างทุกอย่าง"""
        self.drawing_image.fill(Qt.black)
        self.display_image.fill(Qt.black)
        self.predictions = []
        self.update()

class WritingPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.load_styles()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # Drawing Area
        self.drawing_widget = DrawingWidget()
        
        # Control Buttons
        self.btn_clear = QPushButton("Clear Canvas")
        self.btn_clear.clicked.connect(self.drawing_widget.clear_canvas)
        
        self.btn_back = QPushButton("Back to Menu")
        self.btn_back.clicked.connect(lambda: self.parent.stacked_widget.setCurrentIndex(0))

        # Button Container
        btn_container = QHBoxLayout()
        btn_container.addWidget(self.btn_clear)
        btn_container.addWidget(self.btn_back)

        self.layout.addWidget(self.drawing_widget)
        self.layout.addLayout(btn_container)
        self.setLayout(self.layout)

    def load_styles(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #3B4252;
                color: #ECEFF4;
                border: 2px solid #4C566A;
                border-radius: 10px;
                padding: 15px 30px;
                min-width: 200px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #434C5E;
                border-color: #5E81AC;
            }
            DrawingWidget {
                background-color: #2E3440;
                border: 2px solid #4C566A;
                border-radius: 10px;
            }
        """)