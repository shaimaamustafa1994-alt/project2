# -*- coding: utf-8 -*-
"""
نافذة إضافة موظف جديد
Add Employee Dialog
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                            QComboBox, QDateEdit, QSpinBox, QPushButton, QTextEdit,
                            QFormLayout, QFrame, QMessageBox, QScrollArea, QWidget)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from datetime import datetime


class AddEmployeeDialog(QDialog):
    """نافذة حوار لإضافة موظف جديد"""
    
    def __init__(self, database, parent=None):
        super().__init__(parent)
        self.db = database
        self.setWindowTitle("➕ إضافة موظف جديد")
        self.setMinimumSize(700, 800)
        self.init_ui()
    
    def init_ui(self):
        """تهيئة الواجهة"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        
        # العنوان
        title = QLabel("📝 بيانات الموظف الجديد")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            padding: 15px;
            background-color: white;
            border-radius: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # منطقة التمرير
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # النموذج
        form = self.create_form()
        content_layout.addWidget(form)
        
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        # الأزرار
        buttons = self.create_buttons()
        main_layout.addWidget(buttons)
    
    def create_form(self):
        """إنشاء نموذج الإدخال"""
        form_widget = QFrame()
        form_widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 25px;
            }
        """)
        
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        # الاسم الرباعي واللقب
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("مثال: أحمد محمد علي حسن")
        form_layout.addRow("📝 الاسم الرباعي واللقب: *", self.name_input)
        
        # تاريخ المباشرة
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        self.start_date.setDisplayFormat("yyyy/MM/dd")
        form_layout.addRow("📅 تاريخ المباشرة: *", self.start_date)
        
        # تاريخ آخر استحقاق
        self.last_ent_date = QDateEdit()
        self.last_ent_date.setCalendarPopup(True)
        self.last_ent_date.setDate(QDate.currentDate())
        self.last_ent_date.setDisplayFormat("yyyy/MM/dd")
        form_layout.addRow("📅 تاريخ آخر استحقاق: *", self.last_ent_date)
        
        # الشهادة العلمية
        self.education_input = QComboBox()
        self.education_input.addItems([
            "دكتوراه",
            "ماجستير",
            "دبلوم عالي",
            "بكالوريوس",
            "دبلوم",
            "إعدادية"
        ])
        self.education_input.setEditable(True)
        form_layout.addRow("🎓 الشهادة العلمية: *", self.education_input)
        
        # صنف الوظيفة
        self.category_input = QComboBox()
        self.category_input.addItems(["تدريسي", "إداري", "فني"])
        form_layout.addRow("👔 صنف الوظيفة: *", self.category_input)
        
        # العنوان الوظيفي
        self.job_title_input = QLineEdit()
        self.job_title_input.setPlaceholderText("مثال: مدير قسم")
        form_layout.addRow("💼 العنوان الوظيفي: *", self.job_title_input)
        
        # الدرجة الوظيفية
        self.grade_input = QSpinBox()
        self.grade_input.setRange(1, 10)
        self.grade_input.setValue(10)
        self.grade_input.valueChanged.connect(self.update_indicator_options)
        form_layout.addRow("🔢 الدرجة الوظيفية: *", self.grade_input)
        
        # المرحلة الوظيفية
        self.stage_input = QSpinBox()
        self.stage_input.setRange(1, 11)
        self.stage_input.setValue(1)
        form_layout.addRow("📊 المرحلة الوظيفية: *", self.stage_input)
        
        # مؤشر تتبع العلاوة
        self.indicator_input = QComboBox()
        self.update_indicator_options()
        form_layout.addRow("📈 مؤشر تتبع العلاوة: *", self.indicator_input)
        
        # ملاحظات
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("أي ملاحظات إضافية...")
        self.notes_input.setMaximumHeight(100)
        form_layout.addRow("📝 ملاحظات:", self.notes_input)
        
        # ملاحظة الحقول المطلوبة
        required_note = QLabel("* الحقول المطلوبة")
        required_note.setStyleSheet("color: #e74c3c; font-size: 12px; font-style: italic;")
        form_layout.addRow("", required_note)
        
        return form_widget
    
    def update_indicator_options(self):
        """تحديث خيارات مؤشر التتبع حسب الدرجة"""
        self.indicator_input.clear()
        grade = self.grade_input.value()
        
        if grade == 1:
            # الدرجة الأولى: 11 مرحلة
            for i in range(1, 12):
                self.indicator_input.addItem(f"{i}/11")
        elif grade in [2, 3, 4, 5]:
            # الدرجات 2-5: 5 سنوات للترفيع
            for i in range(1, 6):
                self.indicator_input.addItem(f"{i}/5")
        else:
            # الدرجات 6-10: 4 سنوات للترفيع
            for i in range(1, 5):
                self.indicator_input.addItem(f"{i}/4")
    
    def create_buttons(self):
        """إنشاء أزرار التحكم"""
        buttons_widget = QFrame()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setSpacing(15)
        
        # زر الإلغاء
        cancel_btn = QPushButton("❌ إلغاء")
        cancel_btn.setFixedHeight(45)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        # زر الحفظ
        save_btn = QPushButton("✅ حفظ الموظف")
        save_btn.setFixedHeight(45)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        save_btn.clicked.connect(self.save_employee)
        buttons_layout.addWidget(save_btn)
        
        return buttons_widget
    
    def save_employee(self):
        """حفظ بيانات الموظف"""
        # التحقق من الحقول المطلوبة
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "تنبيه", "يرجى إدخال اسم الموظف!")
            self.name_input.setFocus()
            return
        
        if not self.job_title_input.text().strip():
            QMessageBox.warning(self, "تنبيه", "يرجى إدخال العنوان الوظيفي!")
            self.job_title_input.setFocus()
            return
        
        # جمع البيانات
        employee_data = {
            'full_name': self.name_input.text().strip(),
            'start_date': self.start_date.date().toString("yyyy-MM-dd"),
            'last_entitlement_date': self.last_ent_date.date().toString("yyyy-MM-dd"),
            'education_degree': self.education_input.currentText(),
            'job_category': self.category_input.currentText(),
            'job_title': self.job_title_input.text().strip(),
            'job_grade': self.grade_input.value(),
            'job_stage': self.stage_input.value(),
            'entitlement_indicator': self.indicator_input.currentText(),
            'photo_path': None,
            'notes': self.notes_input.toPlainText().strip()
        }
        
        # حفظ في قاعدة البيانات
        try:
            emp_id = self.db.add_employee(employee_data)
            QMessageBox.information(
                self,
                "نجح",
                f"تم إضافة الموظف بنجاح!\n\nالرقم: {emp_id}\nالاسم: {employee_data['full_name']}"
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(
                self,
                "خطأ",
                f"فشل في إضافة الموظف!\n\nالخطأ: {str(e)}"
            )

