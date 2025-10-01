# -*- coding: utf-8 -*-
"""
ملف الموظف الشامل
Employee Profile
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                            QFrame, QTabWidget, QPushButton, QScrollArea,
                            QWidget, QFileDialog, QTableWidget, QTableWidgetItem,
                            QGridLayout, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QPixmap, QColor
from datetime import datetime
import os


class EmployeeProfileDialog(QDialog):
    """نافذة حوار ملف الموظف الشامل"""
    
    data_changed = pyqtSignal()
    
    def __init__(self, employee_id, database, engine, parent=None):
        super().__init__(parent)
        self.employee_id = employee_id
        self.db = database
        self.engine = engine
        
        self.setWindowTitle("📂 ملف الموظف")
        self.setMinimumSize(1000, 700)
        
        self.load_data()
        self.init_ui()
    
    def load_data(self):
        """تحميل بيانات الموظف"""
        self.employee = self.db.get_employee(self.employee_id)
        if not self.employee:
            QMessageBox.critical(self, "خطأ", "لم يتم العثور على الموظف!")
            self.reject()
            return
        
        self.entitlement = self.engine.calculate_next_entitlement(self.employee_id)
        self.career_history = self.db.get_career_history(self.employee_id)
        self.professional_events = self.db.get_employee_events(self.employee_id)
    
    def init_ui(self):
        """تهيئة الواجهة"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # منطقة التمرير
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(25)
        
        # رأس الملف
        header = self.create_header()
        content_layout.addWidget(header)
        
        # البطاقات الرئيسية
        main_cards = self.create_main_cards()
        content_layout.addWidget(main_cards)
        
        # التبويبات
        tabs = self.create_tabs()
        content_layout.addWidget(tabs)
        
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        # الأزرار
        buttons = self.create_buttons()
        layout.addWidget(buttons)
    
    def create_header(self):
        """إنشاء رأس الملف"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #667eea,
                    stop: 1 #764ba2
                );
                border-radius: 15px;
                padding: 30px;
            }
        """)
        
        layout = QHBoxLayout(header)
        layout.setSpacing(25)
        
        # الصورة الشخصية
        photo_container = QFrame()
        photo_container.setFixedSize(150, 150)
        photo_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 75px;
                border: 5px solid rgba(255, 255, 255, 0.3);
            }
        """)
        
        photo_layout = QVBoxLayout(photo_container)
        photo_layout.setContentsMargins(0, 0, 0, 0)
        
        self.photo_label = QLabel()
        self.photo_label.setAlignment(Qt.AlignCenter)
        
        if self.employee.get('photo_path') and os.path.exists(self.employee['photo_path']):
            pixmap = QPixmap(self.employee['photo_path'])
            self.photo_label.setPixmap(pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.photo_label.setText("👤")
            self.photo_label.setStyleSheet("font-size: 80px; color: #667eea;")
        
        photo_layout.addWidget(self.photo_label)
        layout.addWidget(photo_container)
        
        # المعلومات الأساسية
        info_layout = QVBoxLayout()
        info_layout.setSpacing(10)
        
        # الاسم
        name_label = QLabel(self.employee['full_name'])
        name_label.setStyleSheet("""
            color: white;
            font-size: 32px;
            font-weight: bold;
        """)
        info_layout.addWidget(name_label)
        
        # العنوان والصنف
        details_layout = QHBoxLayout()
        details_layout.setSpacing(15)
        
        job_title = QLabel(f"💼 {self.employee['job_title']}")
        job_title.setStyleSheet("""
            color: rgba(255, 255, 255, 0.95);
            font-size: 18px;
            font-weight: 600;
        """)
        details_layout.addWidget(job_title)
        
        category = QLabel(f"👔 {self.employee['job_category']}")
        category.setStyleSheet("""
            color: rgba(255, 255, 255, 0.95);
            font-size: 18px;
            font-weight: 600;
        """)
        details_layout.addWidget(category)
        
        education = QLabel(f"🎓 {self.employee['education_degree']}")
        education.setStyleSheet("""
            color: rgba(255, 255, 255, 0.95);
            font-size: 18px;
            font-weight: 600;
        """)
        details_layout.addWidget(education)
        
        details_layout.addStretch()
        
        info_layout.addLayout(details_layout)
        
        # الحالة
        status_label = QLabel(f"✅ {self.employee['status']}")
        status_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9);
            font-size: 16px;
        """)
        info_layout.addWidget(status_label)
        
        info_layout.addStretch()
        
        layout.addLayout(info_layout)
        
        # زر تغيير الصورة
        change_photo_btn = QPushButton("📷 تغيير الصورة")
        change_photo_btn.setFixedSize(140, 40)
        change_photo_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.4);
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        change_photo_btn.clicked.connect(self.change_photo)
        layout.addWidget(change_photo_btn, alignment=Qt.AlignTop | Qt.AlignRight)
        
        return header
    
    def create_main_cards(self):
        """إنشاء البطاقات الرئيسية"""
        container = QFrame()
        layout = QHBoxLayout(container)
        layout.setSpacing(20)
        
        # بطاقة الدرجة والمرحلة الحالية
        current_card = self.create_current_status_card()
        layout.addWidget(current_card)
        
        # بطاقة الاستحقاق القادم
        next_card = self.create_next_entitlement_card()
        layout.addWidget(next_card)
        
        # بطاقة الخدمة الفعلية
        service_card = self.create_service_card()
        layout.addWidget(service_card)
        
        return container
    
    def create_current_status_card(self):
        """بطاقة الوضع الحالي"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border-right: 5px solid #3498db;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(15)
        
        # الأيقونة والعنوان
        title_layout = QHBoxLayout()
        
        icon = QLabel("🏆")
        icon.setStyleSheet("font-size: 36px;")
        title_layout.addWidget(icon)
        
        title = QLabel("الدرجة والمرحلة الحالية")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # المعلومات
        grade_label = QLabel(f"الدرجة: {self.employee['job_grade']}")
        grade_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #3498db;")
        layout.addWidget(grade_label)
        
        stage_label = QLabel(f"المرحلة: {self.employee['job_stage']}")
        stage_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #3498db;")
        layout.addWidget(stage_label)
        
        date_label = QLabel(f"التاريخ: {self.employee['last_entitlement_date']}")
        date_label.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        layout.addWidget(date_label)
        
        # الراتب
        if self.entitlement:
            salary = self.entitlement['current_salary']
            salary_label = QLabel(f"الراتب: {salary:,} دينار")
            salary_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #27ae60;")
            layout.addWidget(salary_label)
        
        layout.addStretch()
        
        return card
    
    def create_next_entitlement_card(self):
        """بطاقة الاستحقاق القادم"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border-right: 5px solid #27ae60;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(15)
        
        # الأيقونة والعنوان
        title_layout = QHBoxLayout()
        
        icon = QLabel("📅")
        icon.setStyleSheet("font-size: 36px;")
        title_layout.addWidget(icon)
        
        title = QLabel("الاستحقاق القادم")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        if self.entitlement and self.entitlement['type'] != 'لا يوجد':
            # النوع
            ent_type = "🎉 علاوة" if self.entitlement['type'] == 'علاوة' else "⬆️ ترفيع"
            type_label = QLabel(ent_type)
            type_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #27ae60;")
            layout.addWidget(type_label)
            
            # الدرجة والمرحلة القادمة
            next_info = QLabel(f"الدرجة {self.entitlement['next_grade']} / المرحلة {self.entitlement['next_stage']}")
            next_info.setStyleSheet("font-size: 18px; font-weight: bold; color: #3498db;")
            layout.addWidget(next_info)
            
            # التاريخ
            date_label = QLabel(f"التاريخ: {self.entitlement['date'].strftime('%Y/%m/%d')}")
            date_label.setStyleSheet("font-size: 14px; color: #e74c3c; font-weight: bold;")
            layout.addWidget(date_label)
            
            # الراتب القادم
            salary = self.entitlement['next_salary']
            salary_label = QLabel(f"الراتب: {salary:,} دينار")
            salary_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #27ae60;")
            layout.addWidget(salary_label)
        else:
            no_ent = QLabel("لا يوجد استحقاق قادم")
            no_ent.setStyleSheet("font-size: 16px; color: #95a5a6;")
            layout.addWidget(no_ent)
        
        layout.addStretch()
        
        return card
    
    def create_service_card(self):
        """بطاقة الخدمة الفعلية"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border-right: 5px solid #e67e22;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(15)
        
        # الأيقونة والعنوان
        title_layout = QHBoxLayout()
        
        icon = QLabel("⏱️")
        icon.setStyleSheet("font-size: 36px;")
        title_layout.addWidget(icon)
        
        title = QLabel("الخدمة الفعلية")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # حساب الخدمة الفعلية
        service = self.engine._calculate_effective_service(self.employee_id)
        
        # السنوات
        years_label = QLabel(f"{service['years']} سنة")
        years_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #e67e22;")
        layout.addWidget(years_label)
        
        # الأشهر والأيام
        details_label = QLabel(f"{service['months']} شهر، {service['days']} يوم")
        details_label.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        layout.addWidget(details_label)
        
        layout.addStretch()
        
        return card
    
    def create_tabs(self):
        """إنشاء التبويبات"""
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e1e8ed;
                border-radius: 10px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                color: #7f8c8d;
                padding: 15px 25px;
                margin-right: 5px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-weight: 600;
                font-size: 15px;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
            }
        """)
        
        # تبويب المسار الوظيفي
        career_tab = self.create_career_tab()
        tabs.addTab(career_tab, "📈 المسار الوظيفي")
        
        # تبويب الأحداث المهنية
        events_tab = self.create_events_tab()
        tabs.addTab(events_tab, "📝 الأحداث المهنية")
        
        return tabs
    
    def create_career_tab(self):
        """تبويب المسار الوظيفي"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # العنوان
        title = QLabel("📊 سجل العلاوات والترفيعات")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        if self.career_history:
            # عرض كل حدث
            for record in self.career_history:
                record_card = self.create_career_record_card(record)
                layout.addWidget(record_card)
        else:
            no_data = QLabel("لا يوجد سجل وظيفي حتى الآن")
            no_data.setStyleSheet("font-size: 16px; color: #95a5a6; padding: 30px;")
            no_data.setAlignment(Qt.AlignCenter)
            layout.addWidget(no_data)
        
        layout.addStretch()
        
        return tab
    
    def create_career_record_card(self, record):
        """إنشاء بطاقة سجل وظيفي"""
        card = QFrame()
        
        if record['event_type'] == 'علاوة':
            border_color = "#27ae60"
        else:
            border_color = "#3498db"
        
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #f8f9fa;
                border-radius: 10px;
                border-right: 4px solid {border_color};
                padding: 15px;
            }}
        """)
        
        layout = QHBoxLayout(card)
        layout.setSpacing(20)
        
        # الأيقونة
        icon = "🎉" if record['event_type'] == 'علاوة' else "⬆️"
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 32px;")
        layout.addWidget(icon_label)
        
        # المعلومات
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        # النوع
        type_label = QLabel(f"✨ {record['event_type']}")
        type_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {border_color};")
        info_layout.addWidget(type_label)
        
        # التفاصيل
        details = f"من الدرجة {record['old_grade']}/المرحلة {record['old_stage']} ({record['old_salary']:,} دينار)"
        details += f" → الدرجة {record['new_grade']}/المرحلة {record['new_stage']} ({record['new_salary']:,} دينار)"
        details_label = QLabel(details)
        details_label.setStyleSheet("font-size: 14px; color: #34495e;")
        details_label.setWordWrap(True)
        info_layout.addWidget(details_label)
        
        # التاريخ
        date_label = QLabel(f"📅 {record['entitlement_date']}")
        date_label.setStyleSheet("font-size: 13px; color: #7f8c8d;")
        info_layout.addWidget(date_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        return card
    
    def create_events_tab(self):
        """تبويب الأحداث المهنية"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # العنوان وزر الإضافة
        header_layout = QHBoxLayout()
        
        title = QLabel("📝 الأحداث المهنية")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        add_event_btn = QPushButton("➕ إضافة حدث مهني")
        add_event_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        add_event_btn.clicked.connect(self.add_professional_event)
        header_layout.addWidget(add_event_btn)
        
        layout.addLayout(header_layout)
        
        if self.professional_events:
            # عرض كل حدث
            for event in self.professional_events:
                event_card = self.create_event_card(event)
                layout.addWidget(event_card)
        else:
            no_data = QLabel("لا توجد أحداث مهنية مسجلة")
            no_data.setStyleSheet("font-size: 16px; color: #95a5a6; padding: 30px;")
            no_data.setAlignment(Qt.AlignCenter)
            layout.addWidget(no_data)
        
        layout.addStretch()
        
        return tab
    
    def create_event_card(self, event):
        """إنشاء بطاقة حدث مهني"""
        card = QFrame()
        
        # تحديد اللون حسب النوع
        if 'شكر' in event['event_type']:
            border_color = "#27ae60"
            icon = "⭐"
        elif 'عقوبة' in event['event_type'] or event['event_type'] in ['لفت نظر', 'إنذار', 'توبيخ']:
            border_color = "#e74c3c"
            icon = "⚠️"
        elif 'إجازة' in event['event_type']:
            border_color = "#f39c12"
            icon = "🏖️"
        else:
            border_color = "#3498db"
            icon = "📄"
        
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #f8f9fa;
                border-radius: 10px;
                border-right: 4px solid {border_color};
                padding: 15px;
            }}
        """)
        
        layout = QHBoxLayout(card)
        layout.setSpacing(15)
        
        # الأيقونة
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 28px;")
        layout.addWidget(icon_label)
        
        # المعلومات
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        # النوع والحالة
        type_text = event['event_type']
        if event['is_cancelled']:
            type_text += " (ملغى)"
        type_label = QLabel(type_text)
        type_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {border_color};")
        info_layout.addWidget(type_label)
        
        # رقم وتاريخ الحدث
        details = f"رقم: {event['event_number']} | تاريخ: {event['event_date']}"
        details_label = QLabel(details)
        details_label.setStyleSheet("font-size: 13px; color: #7f8c8d;")
        info_layout.addWidget(details_label)
        
        # الوصف
        if event['description']:
            desc_label = QLabel(event['description'])
            desc_label.setStyleSheet("font-size: 13px; color: #34495e;")
            desc_label.setWordWrap(True)
            info_layout.addWidget(desc_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # التأثير
        if event['effect_months'] != 0:
            effect_text = f"{abs(event['effect_months'])} شهر"
            if event['effect_months'] > 0:
                effect_text = f"+{effect_text}"
                effect_color = "#e74c3c"
            else:
                effect_text = f"-{effect_text}"
                effect_color = "#27ae60"
            
            effect_label = QLabel(effect_text)
            effect_label.setStyleSheet(f"""
                font-size: 18px;
                font-weight: bold;
                color: {effect_color};
            """)
            layout.addWidget(effect_label)
        
        return card
    
    def create_buttons(self):
        """إنشاء أزرار التحكم"""
        buttons_widget = QFrame()
        buttons_widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border-top: 1px solid #e1e8ed;
                padding: 15px 30px;
            }
        """)
        
        layout = QHBoxLayout(buttons_widget)
        layout.setSpacing(15)
        
        layout.addStretch()
        
        # زر إغلاق
        close_btn = QPushButton("✖️ إغلاق")
        close_btn.setFixedHeight(40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 30px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        return buttons_widget
    
    def change_photo(self):
        """تغيير صورة الموظف"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "اختر صورة",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            # تحديث الصورة في قاعدة البيانات
            self.employee['photo_path'] = file_path
            self.db.update_employee(self.employee_id, self.employee)
            
            # تحديث العرض
            pixmap = QPixmap(file_path)
            self.photo_label.setPixmap(pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            
            self.data_changed.emit()
    
    def add_professional_event(self):
        """إضافة حدث مهني جديد"""
        QMessageBox.information(
            self,
            "قريباً",
            "سيتم إضافة نافذة الأحداث المهنية في التحديث القادم!"
        )

