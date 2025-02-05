# Digit Writing Recognizer
โปรแกรม **Digit Writing Recognizer** เป็นแอปพลิเคชันสำหรับวาดตัวเลขด้วยเมาส์บนหน้าจอและทำนายตัวเลขที่วาดโดยใช้โมเดลที่ผ่านการฝึกฝนไว้ล่วงหน้า (`MINIT_model.h5`)
โปรแกรมนี้ใช้ **PyQt5** สำหรับ GUI, **OpenCV** สำหรับประมวลผลภาพ และ **TensorFlow/Keras** สำหรับการทำนายตัวเลข

---

## ฟีเจอร์ของโปรแกรม

- **วาดตัวเลข**  
  วาดตัวเลขด้วยเมาส์บนหน้าจอ (canvas) พร้อมแสดงผลแบบเรียลไทม์

- **ประมวลผลภาพ**  
  คัดแยกส่วนที่มีการวาดด้วยการหาขอบเขต (bounding box) และปรับขนาดภาพให้เป็น 28x28 ตามรูปแบบของ MNIST

- **ทำนายตัวเลข**  
  ใช้โมเดล `MINIT_model.h5` ที่ผ่านการฝึกฝนมาแล้วเพื่อทำนายตัวเลขที่วาด

- **แสดงผลการทำนาย**  
  แสดงผลลัพธ์ (label) ที่ได้จากการทำนายลงบนภาพในตำแหน่งที่ใกล้กับบริเวณที่วาด

- **ล้างหน้าจอ (Clear Canvas)**  
  มีฟังก์ชันสำหรับล้างหน้าจอเพื่อเริ่มวาดใหม่

---

## **Project Structure**
```
digit-drawing-recognizer/
├── main.py               # จุดเริ่มต้นของโปรแกรม
├── home_page.py          # หน้าจอหลัก
├── writing_page.py       # หน้าวาดรูป และทำนายผล
├── guide_page.py         # รายละเอียดการใช้งานเบื้องต้น
├── main.spec             # สำคัญมาก!! ไฟล์เก็บการตั้งค่าต่างๆสำหรับการ build ไฟล์ .exe
├── MINIT_model.h5        # โมเดลที่ผ่านการฝึกฝนสำหรับทำนายตัวเลข
├── requirements.txt      # รายการ dependencies ที่จำเป็น
├── README.md             # เอกสารนี้
├── TRAIN_MLP_MNIT        # ไฟล์ที่ใช้ Train model MLP นามสกุล jupyer
└── /dist/
    ├── main.exe          # ไฟล์ EXE
```

---

## **การติดตั้ง Dependencies และการรันโปรเจกต์**

### **:one: ติดตั้ง Dependencies**
ใช้คำสั่งนี้เพื่อติดตั้งแพ็กเกจที่จำเป็น:
```bash
pip install PyQt5 numpy opencv-python tensorflow
```
หรือหากมีไฟล์ `requirements.txt` ให้ใช้:
```bash
pip install -r requirements.txt
```

### **:two: รันโปรเจกต์**
```bash
python main.py
```

---

## **วิธีการ Build เป็นไฟล์ EXE (Windows)**

### **:one: ติดตั้ง PyInstaller**
```bash
pip install pyinstaller
```

### **:two: Build เป็นไฟล์ Executable**
```bash
pyinstaller --onefile --add-data "MNIT_model.h5;." main.py
```

---

### **ตำแหน่งไฟล์ EXE**

หลังจาก build เสร็จ ไฟล์ executable จะอยู่ในโฟลเดอร์ dist ภายในโฟลเดอร์โปรเจกต์

**:hourglass_flowing_sand: หมายเหตุ:**  
ไฟล์ `.exe` อาจใช้เวลา **ประมาณ 10 วินาที** ในการรัน
