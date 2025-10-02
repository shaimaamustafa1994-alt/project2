"""
إدارة الأحداث المهنية
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate

class EventsManagementWidget(QWidget):
    def __init__(self, db_manager, calculation_engine):
        super().__init__()
        self.db = db_manager
        self.engine = calculation_engine
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(layout)
        
        title = QLabel("📝 إدارة الأحداث المهنية")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1976D2; padding: 15px; background-color: white; border-radius: 8px;")
        layout.addWidget(title)
        
        # نموذج إضافة حدث
        form_group = QGroupBox("إضافة حدث جديد")
        form_layout = QFormLayout()
        form_group.setLayout(form_layout)
        
        # اختيار الموظف
        self.employee_combo = QComboBox()
        employees = self.db.get_all_employees()
        for emp in employees:
            self.employee_combo.addItem(emp['full_name'], emp['id'])
        form_layout.addRow("الموظف:", self.employee_combo)
        
        # نوع الحدث
        self.event_type_combo = QComboBox()
        self.event_type_combo.addItems([
            "كتاب شكر",
            "شهادة علمية",
            "لفت نظر",
            "إنذار",
            "توبيخ",
            "إجازة أمومة",
            "إجازة بدون راتب"
        ])
        form_layout.addRow("نوع الحدث:", self.event_type_combo)
        
        # رقم الكتاب
        self.doc_number_input = QLineEdit()
        form_layout.addRow("رقم الكتاب:", self.doc_number_input)
        
        # تاريخ الحدث
        self.event_date = QDateEdit()
        self.event_date.setCalendarPopup(True)
        self.event_date.setDate(QDate.currentDate())
        self.event_date.setDisplayFormat("dd/MM/yyyy")
        form_layout.addRow("تاريخ الحدث:", self.event_date)
        
        # التأثير (بالأشهر)
        self.impact_spin = QSpinBox()
        self.impact_spin.setRange(-12, 12)
        self.impact_spin.setValue(0)
        form_layout.addRow("التأثير (أشهر):", self.impact_spin)
        
        # زر الحفظ
        save_btn = QPushButton("💾 حفظ الحدث")
        save_btn.setFixedHeight(50)
        save_btn.clicked.connect(self.save_event)
        form_layout.addRow("", save_btn)
        
        layout.addWidget(form_group)
        layout.addStretch()
    
    def save_event(self):
        employee_id = self.employee_combo.currentData()
        
        event_type_map = {
            "كتاب شكر": "commendation",
            "شهادة علمية": "academic_degree",
            "لفت نظر": "notice_penalty",
            "إنذار": "warning_penalty",
            "توبيخ": "reprimand_penalty",
            "إجازة أمومة": "maternity_leave",
            "إجازة بدون راتب": "unpaid_leave"
        }
        
        event_data = {
            'employee_id': employee_id,
            'event_type': event_type_map[self.event_type_combo.currentText()],
            'document_number': self.doc_number_input.text(),
            'event_date': self.event_date.date().toString("yyyy-MM-dd"),
            'impact_months': self.impact_spin.value()
        }
        
        try:
            self.db.add_professional_event(event_data)
            QMessageBox.information(self, "نجح", "تم إضافة الحدث بنجاح!")
            self.doc_number_input.clear()
            self.impact_spin.setValue(0)
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ: {str(e)}")
