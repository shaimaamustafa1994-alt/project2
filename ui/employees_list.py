"""
واجهة قائمة الموظفين
Employees List Interface
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLabel, QComboBox,
                             QLineEdit, QMessageBox, QHeaderView, QFrame,
                             QAbstractItemView)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from datetime import datetime

class EmployeesList(QWidget):
    """واجهة عرض قائمة الموظفين"""
    
    employee_selected = pyqtSignal(int)  # إشارة عند اختيار موظف
    
    def __init__(self, db_manager, calc_engine):
        super().__init__()
        self.db = db_manager
        self.calc_engine = calc_engine
        self.current_employees = []
        self.init_ui()
        self.load_employees()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # العنوان
        title = QLabel("قائمة الموظفين")
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
        
        # شريط الأدوات والفلاتر
        toolbar = self.create_toolbar()
        main_layout.addWidget(toolbar)
        
        # جدول الموظفين
        self.create_employees_table()
        main_layout.addWidget(self.employees_table)
        
        # شريط الحالة
        status_bar = self.create_status_bar()
        main_layout.addWidget(status_bar)
    
    def create_toolbar(self):
        """إنشاء شريط الأدوات والفلاتر"""
        toolbar = QFrame()
        toolbar.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        layout = QHBoxLayout(toolbar)
        layout.setSpacing(15)
        
        # فلتر الصنف الوظيفي
        category_label = QLabel("الصنف الوظيفي:")
        category_label.setStyleSheet("font-weight: bold; color: #333;")
        
        self.category_filter = QComboBox()
        self.category_filter.addItems(["الكل", "تدريسي", "إداري", "فني"])
        self.category_filter.setStyleSheet("QComboBox { min-width: 120px; }")
        self.category_filter.currentTextChanged.connect(self.filter_employees)
        
        # البحث بالاسم
        search_label = QLabel("البحث:")
        search_label.setStyleSheet("font-weight: bold; color: #333;")
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("ابحث بالاسم...")
        self.search_edit.setStyleSheet("QLineEdit { min-width: 200px; }")
        self.search_edit.textChanged.connect(self.filter_employees)
        
        # زر التحديث
        refresh_btn = QPushButton("🔄 تحديث")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 6px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        refresh_btn.clicked.connect(self.load_employees)
        
        # زر إضافة موظف جديد
        add_btn = QPushButton("➕ إضافة موظف")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 6px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        add_btn.clicked.connect(self.add_new_employee)
        
        # ترتيب العناصر
        layout.addWidget(category_label)
        layout.addWidget(self.category_filter)
        layout.addWidget(search_label)
        layout.addWidget(self.search_edit)
        layout.addStretch()
        layout.addWidget(refresh_btn)
        layout.addWidget(add_btn)
        
        return toolbar
    
    def create_employees_table(self):
        """إنشاء جدول الموظفين"""
        self.employees_table = QTableWidget()
        
        # تعيين الأعمدة
        headers = [
            "الرقم", "الاسم الكامل", "الصنف الوظيفي", "العنوان الوظيفي",
            "الدرجة", "المرحلة", "الحدث القادم", "تاريخ الاستحقاق",
            "الخدمة الفعلية", "عرض الملف", "حذف"
        ]
        
        self.employees_table.setColumnCount(len(headers))
        self.employees_table.setHorizontalHeaderLabels(headers)
        
        # تنسيق الجدول
        self.employees_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                gridline-color: #f0f0f0;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
            QHeaderView::section {
                background-color: #2196F3;
                color: white;
                padding: 12px 8px;
                border: none;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        # إعدادات الجدول
        self.employees_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.employees_table.setAlternatingRowColors(True)
        self.employees_table.setSortingEnabled(True)
        
        # تعديل عرض الأعمدة
        header = self.employees_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # عمود الاسم
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # عمود العنوان
        
        # تعيين عرض ثابت لبعض الأعمدة
        self.employees_table.setColumnWidth(0, 60)   # الرقم
        self.employees_table.setColumnWidth(4, 80)   # الدرجة
        self.employees_table.setColumnWidth(5, 80)   # المرحلة
        self.employees_table.setColumnWidth(9, 100)  # عرض الملف
        self.employees_table.setColumnWidth(10, 80)  # حذف
    
    def create_status_bar(self):
        """إنشاء شريط الحالة"""
        status_bar = QFrame()
        status_bar.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        
        layout = QHBoxLayout(status_bar)
        
        self.status_label = QLabel("جاري التحميل...")
        self.status_label.setStyleSheet("color: #666; font-weight: bold;")
        
        layout.addWidget(self.status_label)
        layout.addStretch()
        
        return status_bar
    
    def load_employees(self):
        """تحميل قائمة الموظفين"""
        try:
            # الحصول على جميع الموظفين
            self.current_employees = self.db.get_all_employees()
            
            # تحديث الجدول
            self.update_table()
            
            # تحديث شريط الحالة
            count = len(self.current_employees)
            self.status_label.setText(f"إجمالي الموظفين: {count}")
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تحميل البيانات:\n{str(e)}")
            self.status_label.setText("خطأ في التحميل")
    
    def update_table(self):
        """تحديث جدول الموظفين"""
        
        # تعيين عدد الصفوف
        self.employees_table.setRowCount(len(self.current_employees))
        
        for row, employee in enumerate(self.current_employees):
            try:
                # حساب الاستحقاق القادم
                next_entitlement = self.calc_engine.calculate_next_entitlement(employee['id'])
                
                # حساب الخدمة الفعلية
                service = self.calc_engine.calculate_actual_service(employee['id'])
                
                # ملء البيانات
                self.employees_table.setItem(row, 0, QTableWidgetItem(str(employee['id'])))
                self.employees_table.setItem(row, 1, QTableWidgetItem(employee['full_name']))
                self.employees_table.setItem(row, 2, QTableWidgetItem(employee['job_category']))
                self.employees_table.setItem(row, 3, QTableWidgetItem(employee['job_title']))
                self.employees_table.setItem(row, 4, QTableWidgetItem(str(employee['degree'])))
                self.employees_table.setItem(row, 5, QTableWidgetItem(str(employee['stage'])))
                
                # الحدث القادم
                if next_entitlement:
                    event_text = next_entitlement['entitlement_type']
                    self.employees_table.setItem(row, 6, QTableWidgetItem(event_text))
                    
                    # تاريخ الاستحقاق
                    date_text = next_entitlement['next_entitlement_date'].strftime('%Y/%m/%d')
                    self.employees_table.setItem(row, 7, QTableWidgetItem(date_text))
                else:
                    self.employees_table.setItem(row, 6, QTableWidgetItem("غير محدد"))
                    self.employees_table.setItem(row, 7, QTableWidgetItem("غير محدد"))
                
                # الخدمة الفعلية
                if service:
                    service_text = f"{service['years']} سنة، {service['months']} شهر"
                    self.employees_table.setItem(row, 8, QTableWidgetItem(service_text))
                else:
                    self.employees_table.setItem(row, 8, QTableWidgetItem("غير محسوبة"))
                
                # زر عرض الملف
                view_btn = QPushButton("👁️ ملف")
                view_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2196F3;
                        color: white;
                        border: none;
                        padding: 8px 12px;
                        border-radius: 4px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #1976D2;
                    }
                """)
                view_btn.clicked.connect(lambda checked, emp_id=employee['id']: self.view_employee_profile(emp_id))
                self.employees_table.setCellWidget(row, 9, view_btn)
                
                # زر الحذف
                delete_btn = QPushButton("🗑️")
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #F44336;
                        color: white;
                        border: none;
                        padding: 8px 12px;
                        border-radius: 4px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #D32F2F;
                    }
                """)
                delete_btn.clicked.connect(lambda checked, emp_id=employee['id']: self.delete_employee(emp_id))
                self.employees_table.setCellWidget(row, 10, delete_btn)
                
            except Exception as e:
                print(f"خطأ في معالجة الموظف {employee['id']}: {str(e)}")
                # ملء البيانات الأساسية فقط
                self.employees_table.setItem(row, 0, QTableWidgetItem(str(employee['id'])))
                self.employees_table.setItem(row, 1, QTableWidgetItem(employee['full_name']))
                self.employees_table.setItem(row, 2, QTableWidgetItem(employee['job_category']))
                self.employees_table.setItem(row, 3, QTableWidgetItem(employee['job_title']))
                self.employees_table.setItem(row, 4, QTableWidgetItem(str(employee['degree'])))
                self.employees_table.setItem(row, 5, QTableWidgetItem(str(employee['stage'])))
                self.employees_table.setItem(row, 6, QTableWidgetItem("خطأ"))
                self.employees_table.setItem(row, 7, QTableWidgetItem("خطأ"))
                self.employees_table.setItem(row, 8, QTableWidgetItem("خطأ"))
    
    def filter_employees(self):
        """فلترة الموظفين حسب الصنف والبحث"""
        category_filter = self.category_filter.currentText()
        search_text = self.search_edit.text().lower()
        
        # إخفاء/إظهار الصفوف
        for row in range(self.employees_table.rowCount()):
            show_row = True
            
            # فلتر الصنف
            if category_filter != "الكل":
                category_item = self.employees_table.item(row, 2)
                if category_item and category_item.text() != category_filter:
                    show_row = False
            
            # فلتر البحث
            if search_text and show_row:
                name_item = self.employees_table.item(row, 1)
                if name_item and search_text not in name_item.text().lower():
                    show_row = False
            
            self.employees_table.setRowHidden(row, not show_row)
        
        # تحديث عداد النتائج
        visible_count = sum(1 for row in range(self.employees_table.rowCount()) 
                           if not self.employees_table.isRowHidden(row))
        total_count = len(self.current_employees)
        self.status_label.setText(f"عرض {visible_count} من أصل {total_count} موظف")
    
    def view_employee_profile(self, employee_id):
        """عرض ملف الموظف"""
        try:
            from ui.employee_profile import EmployeeProfile
            
            # إنشاء نافذة ملف الموظف
            profile_window = EmployeeProfile(self.db, self.calc_engine, employee_id)
            profile_window.show()
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء فتح ملف الموظف:\n{str(e)}")
    
    def delete_employee(self, employee_id):
        """حذف موظف"""
        # الحصول على اسم الموظف
        employee = self.db.get_employee(employee_id)
        if not employee:
            return
        
        # تأكيد الحذف
        reply = QMessageBox.question(
            self, "تأكيد الحذف",
            f"هل أنت متأكد من حذف الموظف:\n{employee['full_name']}؟\n\n"
            "سيتم حذف جميع البيانات والأحداث المرتبطة بهذا الموظف.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_employee(employee_id)
                QMessageBox.information(self, "تم الحذف", "تم حذف الموظف بنجاح")
                self.load_employees()  # إعادة تحميل القائمة
                
            except Exception as e:
                QMessageBox.critical(self, "خطأ في الحذف", f"حدث خطأ أثناء حذف الموظف:\n{str(e)}")
    
    def add_new_employee(self):
        """إضافة موظف جديد"""
        # إرسال إشارة للانتقال لصفحة إضافة موظف
        # يمكن تنفيذ هذا من خلال النافذة الرئيسية
        QMessageBox.information(self, "إضافة موظف", "استخدم القائمة الجانبية للانتقال إلى صفحة إضافة موظف جديد")

