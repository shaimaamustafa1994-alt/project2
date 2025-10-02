"""
واجهة إدارة الموظفين
Employee Management Interface
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QComboBox, QSpinBox, QDateEdit, QTextEdit,
                             QPushButton, QLabel, QFrame, QMessageBox, QGroupBox,
                             QScrollArea)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from datetime import datetime, date

class EmployeeManagement(QWidget):
    """واجهة إضافة وتعديل الموظفين"""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.current_employee_id = None
        self.init_ui()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # العنوان
        title = QLabel("إضافة موظف جديد")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1976D2;
                padding: 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E3F2FD, stop:1 #BBDEFB);
                border-radius: 10px;
                margin-bottom: 20px;
            }
        """)
        main_layout.addWidget(title)
        
        # منطقة التمرير
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        # محتوى النموذج
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(25)
        
        # مجموعة البيانات الأساسية
        basic_group = self.create_basic_info_group()
        form_layout.addWidget(basic_group)
        
        # مجموعة البيانات الوظيفية
        job_group = self.create_job_info_group()
        form_layout.addWidget(job_group)
        
        # مجموعة التواريخ
        dates_group = self.create_dates_group()
        form_layout.addWidget(dates_group)
        
        # مجموعة الملاحظات
        notes_group = self.create_notes_group()
        form_layout.addWidget(notes_group)
        
        scroll_area.setWidget(form_widget)
        main_layout.addWidget(scroll_area)
        
        # أزرار العمليات
        buttons_layout = self.create_buttons()
        main_layout.addLayout(buttons_layout)
    
    def create_basic_info_group(self):
        """إنشاء مجموعة البيانات الأساسية"""
        group = QGroupBox("البيانات الأساسية")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #1976D2;
                border: 2px solid #2196F3;
                border-radius: 10px;
                margin-top: 15px;
                padding: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top right;
                padding: 0 15px;
                background-color: white;
            }
        """)
        
        layout = QFormLayout(group)
        layout.setSpacing(15)
        layout.setLabelAlignment(Qt.AlignRight)
        
        # الاسم الرباعي واللقب
        self.full_name_edit = QLineEdit()
        self.full_name_edit.setPlaceholderText("أدخل الاسم الرباعي واللقب")
        layout.addRow("الاسم الرباعي واللقب:", self.full_name_edit)
        
        # الشهادة العلمية
        self.qualification_edit = QLineEdit()
        self.qualification_edit.setPlaceholderText("مثال: بكالوريوس، ماجستير، دكتوراه")
        layout.addRow("الشهادة العلمية:", self.qualification_edit)
        
        return group
    
    def create_job_info_group(self):
        """إنشاء مجموعة البيانات الوظيفية"""
        group = QGroupBox("البيانات الوظيفية")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #1976D2;
                border: 2px solid #2196F3;
                border-radius: 10px;
                margin-top: 15px;
                padding: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top right;
                padding: 0 15px;
                background-color: white;
            }
        """)
        
        layout = QFormLayout(group)
        layout.setSpacing(15)
        layout.setLabelAlignment(Qt.AlignRight)
        
        # صنف الوظيفة
        self.job_category_combo = QComboBox()
        self.job_category_combo.addItems(["تدريسي", "إداري", "فني"])
        self.job_category_combo.setStyleSheet("QComboBox { min-height: 40px; }")
        layout.addRow("صنف الوظيفة:", self.job_category_combo)
        
        # العنوان الوظيفي
        self.job_title_edit = QLineEdit()
        self.job_title_edit.setPlaceholderText("مثال: مدرس، موظف، فني")
        layout.addRow("العنوان الوظيفي:", self.job_title_edit)
        
        # الدرجة الوظيفية
        self.degree_spin = QSpinBox()
        self.degree_spin.setRange(1, 10)
        self.degree_spin.setValue(10)
        self.degree_spin.setStyleSheet("QSpinBox { min-height: 40px; }")
        layout.addRow("الدرجة الوظيفية:", self.degree_spin)
        
        # المرحلة الوظيفية
        self.stage_spin = QSpinBox()
        self.stage_spin.setRange(1, 11)
        self.stage_spin.setValue(1)
        self.stage_spin.setStyleSheet("QSpinBox { min-height: 40px; }")
        layout.addRow("المرحلة الوظيفية:", self.stage_spin)
        
        # مؤشر تتبع العلاوة
        self.tracking_combo = QComboBox()
        self.tracking_combo.addItems([
            "4/1", "4/2", "4/3", "4/4",
            "5/1", "5/2", "5/3", "5/4", "5/5"
        ])
        self.tracking_combo.setStyleSheet("QComboBox { min-height: 40px; }")
        layout.addRow("مؤشر تتبع العلاوة:", self.tracking_combo)
        
        return group
    
    def create_dates_group(self):
        """إنشاء مجموعة التواريخ"""
        group = QGroupBox("التواريخ المهمة")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #1976D2;
                border: 2px solid #2196F3;
                border-radius: 10px;
                margin-top: 15px;
                padding: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top right;
                padding: 0 15px;
                background-color: white;
            }
        """)
        
        layout = QFormLayout(group)
        layout.setSpacing(15)
        layout.setLabelAlignment(Qt.AlignRight)
        
        # تاريخ المباشرة بالوظيفة
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate())
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setStyleSheet("QDateEdit { min-height: 40px; }")
        layout.addRow("تاريخ المباشرة بالوظيفة:", self.start_date_edit)
        
        # تاريخ آخر استحقاق للعلاوة
        self.last_entitlement_edit = QDateEdit()
        self.last_entitlement_edit.setDate(QDate.currentDate())
        self.last_entitlement_edit.setCalendarPopup(True)
        self.last_entitlement_edit.setStyleSheet("QDateEdit { min-height: 40px; }")
        layout.addRow("تاريخ آخر استحقاق للعلاوة:", self.last_entitlement_edit)
        
        return group
    
    def create_notes_group(self):
        """إنشاء مجموعة الملاحظات"""
        group = QGroupBox("ملاحظات إضافية")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #1976D2;
                border: 2px solid #2196F3;
                border-radius: 10px;
                margin-top: 15px;
                padding: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top right;
                padding: 0 15px;
                background-color: white;
            }
        """)
        
        layout = QFormLayout(group)
        layout.setSpacing(15)
        layout.setLabelAlignment(Qt.AlignRight)
        
        # الملاحظات
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(100)
        self.notes_edit.setPlaceholderText("أي ملاحظات إضافية حول الموظف...")
        layout.addRow("الملاحظات:", self.notes_edit)
        
        return group
    
    def create_buttons(self):
        """إنشاء أزرار العمليات"""
        layout = QHBoxLayout()
        layout.setSpacing(15)
        
        # زر الحفظ
        save_btn = QPushButton("💾 حفظ الموظف")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
                border-radius: 8px;
                min-width: 150px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_btn.clicked.connect(self.save_employee)
        
        # زر المسح
        clear_btn = QPushButton("🗑️ مسح الحقول")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
                border-radius: 8px;
                min-width: 150px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        clear_btn.clicked.connect(self.clear_form)
        
        # زر المعاينة
        preview_btn = QPushButton("👁️ معاينة البيانات")
        preview_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
                border-radius: 8px;
                min-width: 150px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        preview_btn.clicked.connect(self.preview_data)
        
        layout.addStretch()
        layout.addWidget(save_btn)
        layout.addWidget(clear_btn)
        layout.addWidget(preview_btn)
        layout.addStretch()
        
        return layout
    
    def save_employee(self):
        """حفظ بيانات الموظف"""
        
        # التحقق من صحة البيانات
        if not self.validate_form():
            return
        
        try:
            # جمع البيانات
            employee_data = {
                'full_name': self.full_name_edit.text().strip(),
                'job_category': self.job_category_combo.currentText(),
                'job_title': self.job_title_edit.text().strip(),
                'degree': self.degree_spin.value(),
                'stage': self.stage_spin.value(),
                'academic_qualification': self.qualification_edit.text().strip(),
                'start_date': self.start_date_edit.date().toString('yyyy-MM-dd'),
                'last_entitlement_date': self.last_entitlement_edit.date().toString('yyyy-MM-dd'),
                'tracking_indicator': self.tracking_combo.currentText(),
                'photo_path': None,
                'notes': self.notes_edit.toPlainText().strip()
            }
            
            # حفظ في قاعدة البيانات
            employee_id = self.db.add_employee(employee_data)
            
            # رسالة نجاح
            QMessageBox.information(self, "نجح الحفظ", 
                                    f"تم حفظ بيانات الموظف بنجاح!\nرقم الموظف: {employee_id}")
            
            # مسح النموذج
            self.clear_form()
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ في الحفظ", 
                                f"حدث خطأ أثناء حفظ البيانات:\n{str(e)}")
    
    def validate_form(self):
        """التحقق من صحة البيانات"""
        
        # التحقق من الحقول المطلوبة
        if not self.full_name_edit.text().strip():
            QMessageBox.warning(self, "بيانات ناقصة", "يرجى إدخال الاسم الرباعي واللقب")
            self.full_name_edit.setFocus()
            return False
        
        if not self.qualification_edit.text().strip():
            QMessageBox.warning(self, "بيانات ناقصة", "يرجى إدخال الشهادة العلمية")
            self.qualification_edit.setFocus()
            return False
        
        if not self.job_title_edit.text().strip():
            QMessageBox.warning(self, "بيانات ناقصة", "يرجى إدخال العنوان الوظيفي")
            self.job_title_edit.setFocus()
            return False
        
        # التحقق من منطقية التواريخ
        start_date = self.start_date_edit.date().toPyDate()
        last_entitlement = self.last_entitlement_edit.date().toPyDate()
        
        if last_entitlement < start_date:
            QMessageBox.warning(self, "خطأ في التواريخ", 
                               "تاريخ آخر استحقاق لا يمكن أن يكون قبل تاريخ المباشرة")
            return False
        
        return True
    
    def clear_form(self):
        """مسح جميع الحقول"""
        self.full_name_edit.clear()
        self.qualification_edit.clear()
        self.job_title_edit.clear()
        self.job_category_combo.setCurrentIndex(0)
        self.degree_spin.setValue(10)
        self.stage_spin.setValue(1)
        self.tracking_combo.setCurrentIndex(0)
        self.start_date_edit.setDate(QDate.currentDate())
        self.last_entitlement_edit.setDate(QDate.currentDate())
        self.notes_edit.clear()
        
        # التركيز على أول حقل
        self.full_name_edit.setFocus()
    
    def preview_data(self):
        """معاينة البيانات المدخلة"""
        
        if not self.validate_form():
            return
        
        # تجميع البيانات للمعاينة
        data = f"""
البيانات الأساسية:
• الاسم: {self.full_name_edit.text()}
• الشهادة: {self.qualification_edit.text()}

البيانات الوظيفية:
• الصنف: {self.job_category_combo.currentText()}
• العنوان: {self.job_title_edit.text()}
• الدرجة: {self.degree_spin.value()}
• المرحلة: {self.stage_spin.value()}
• المؤشر: {self.tracking_combo.currentText()}

التواريخ:
• المباشرة: {self.start_date_edit.date().toString('dd/MM/yyyy')}
• آخر استحقاق: {self.last_entitlement_edit.date().toString('dd/MM/yyyy')}

الملاحظات:
{self.notes_edit.toPlainText() if self.notes_edit.toPlainText() else 'لا توجد ملاحظات'}
        """
        
        QMessageBox.information(self, "معاينة البيانات", data)

