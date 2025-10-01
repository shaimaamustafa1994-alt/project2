# -*- coding: utf-8 -*-
"""
قائمة الموظفين
Employees List
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                            QTableWidgetItem, QPushButton, QLineEdit, QComboBox,
                            QLabel, QFrame, QHeaderView, QMessageBox, QAbstractItemView)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from datetime import datetime


class EmployeesListWidget(QWidget):
    """واجهة قائمة الموظفين"""
    
    employee_updated = pyqtSignal()
    
    def __init__(self, database, engine, parent=None):
        super().__init__(parent)
        self.db = database
        self.engine = engine
        self.current_filter = None
        self.current_search = ""
        self.init_ui()
        self.load_employees()
    
    def init_ui(self):
        """تهيئة الواجهة"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # العنوان
        title = QLabel("📋 قائمة الموظفين")
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
        """)
        layout.addWidget(title)
        
        # شريط الأدوات
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        
        # الجدول
        self.table = self.create_table()
        layout.addWidget(self.table)
    
    def create_toolbar(self):
        """إنشاء شريط الأدوات"""
        toolbar = QFrame()
        toolbar.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        layout = QHBoxLayout(toolbar)
        layout.setSpacing(15)
        
        # فلتر الصنف الوظيفي
        filter_label = QLabel("الصنف:")
        filter_label.setStyleSheet("font-weight: bold; color: #34495e;")
        layout.addWidget(filter_label)
        
        self.category_filter = QComboBox()
        self.category_filter.addItems(["الكل", "تدريسي", "إداري", "فني"])
        self.category_filter.setFixedWidth(150)
        self.category_filter.currentTextChanged.connect(self.apply_filters)
        layout.addWidget(self.category_filter)
        
        layout.addSpacing(20)
        
        # البحث
        search_label = QLabel("🔍 بحث:")
        search_label.setStyleSheet("font-weight: bold; color: #34495e;")
        layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث بالاسم أو العنوان الوظيفي...")
        self.search_input.setFixedWidth(300)
        self.search_input.textChanged.connect(self.apply_filters)
        layout.addWidget(self.search_input)
        
        layout.addStretch()
        
        # زر تحديث
        refresh_btn = QPushButton("🔄 تحديث")
        refresh_btn.setFixedWidth(120)
        refresh_btn.clicked.connect(self.refresh)
        layout.addWidget(refresh_btn)
        
        return toolbar
    
    def create_table(self):
        """إنشاء جدول الموظفين"""
        table = QTableWidget()
        table.setColumnCount(9)
        table.setHorizontalHeaderLabels([
            "الاسم الكامل",
            "العنوان الوظيفي",
            "الصنف",
            "الدرجة",
            "المرحلة",
            "الحدث القادم",
            "التاريخ",
            "الخدمة الفعلية",
            "الإجراءات"
        ])
        
        # تنسيق الجدول
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e1e8ed;
                border-radius: 10px;
                gridline-color: #ecf0f1;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ecf0f1;
            }
            QTableWidget::item:selected {
                background-color: #e8f4f8;
                color: #2c3e50;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        # خصائص الجدول
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        
        # توزيع الأعمدة
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.Fixed)
        table.setColumnWidth(8, 200)
        
        return table
    
    def load_employees(self):
        """تحميل بيانات الموظفين"""
        self.table.setRowCount(0)
        
        # جلب الموظفين
        category = None if self.category_filter.currentText() == "الكل" else self.category_filter.currentText()
        search = self.search_input.text().strip() if self.search_input.text() else None
        
        employees = self.db.get_all_employees(category=category, search_term=search)
        
        for emp in employees:
            self.add_employee_row(emp)
    
    def add_employee_row(self, employee):
        """إضافة صف موظف للجدول"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # الاسم
        name_item = QTableWidgetItem(employee['full_name'])
        name_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.table.setItem(row, 0, name_item)
        
        # العنوان الوظيفي
        self.table.setItem(row, 1, QTableWidgetItem(employee['job_title']))
        
        # الصنف
        category_item = QTableWidgetItem(employee['job_category'])
        if employee['job_category'] == 'تدريسي':
            category_item.setForeground(QColor("#27ae60"))
        elif employee['job_category'] == 'إداري':
            category_item.setForeground(QColor("#3498db"))
        else:
            category_item.setForeground(QColor("#e67e22"))
        category_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.table.setItem(row, 2, category_item)
        
        # الدرجة
        self.table.setItem(row, 3, QTableWidgetItem(str(employee['job_grade'])))
        
        # المرحلة
        self.table.setItem(row, 4, QTableWidgetItem(str(employee['job_stage'])))
        
        # حساب الاستحقاق القادم
        try:
            entitlement = self.engine.calculate_next_entitlement(employee['id'])
            if entitlement:
                # نوع الحدث
                event_type = "🎉 علاوة" if entitlement['type'] == 'علاوة' else "⬆️ ترفيع"
                event_item = QTableWidgetItem(event_type)
                event_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
                if entitlement['type'] == 'علاوة':
                    event_item.setForeground(QColor("#27ae60"))
                else:
                    event_item.setForeground(QColor("#3498db"))
                self.table.setItem(row, 5, event_item)
                
                # التاريخ
                date_item = QTableWidgetItem(entitlement['date'].strftime("%Y/%m/%d"))
                date_item.setForeground(QColor("#e74c3c"))
                self.table.setItem(row, 6, date_item)
            else:
                self.table.setItem(row, 5, QTableWidgetItem("-"))
                self.table.setItem(row, 6, QTableWidgetItem("-"))
            
            # الخدمة الفعلية
            service = self.engine._calculate_effective_service(employee['id'])
            service_text = f"{service['years']} سنة، {service['months']} شهر"
            self.table.setItem(row, 7, QTableWidgetItem(service_text))
            
        except Exception as e:
            print(f"خطأ في حساب الاستحقاق: {e}")
            self.table.setItem(row, 5, QTableWidgetItem("-"))
            self.table.setItem(row, 6, QTableWidgetItem("-"))
            self.table.setItem(row, 7, QTableWidgetItem("-"))
        
        # أزرار الإجراءات
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(5, 5, 5, 5)
        actions_layout.setSpacing(5)
        
        # زر عرض الملف
        view_btn = QPushButton("📂 ملف")
        view_btn.setFixedSize(70, 30)
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        view_btn.clicked.connect(lambda checked, e=employee: self.view_employee(e))
        actions_layout.addWidget(view_btn)
        
        # زر حذف
        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedSize(40, 30)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        delete_btn.clicked.connect(lambda checked, e=employee: self.delete_employee(e))
        actions_layout.addWidget(delete_btn)
        
        self.table.setCellWidget(row, 8, actions_widget)
    
    def apply_filters(self):
        """تطبيق الفلاتر"""
        self.load_employees()
    
    def view_employee(self, employee):
        """عرض ملف الموظف"""
        from ui.employee_profile import EmployeeProfileDialog
        dialog = EmployeeProfileDialog(employee['id'], self.db, self.engine, self)
        dialog.data_changed.connect(self.employee_updated.emit)
        dialog.exec_()
        self.refresh()
    
    def delete_employee(self, employee):
        """حذف موظف"""
        reply = QMessageBox.question(
            self,
            "تأكيد الحذف",
            f"هل أنت متأكد من حذف الموظف:\n{employee['full_name']}؟\n\nسيتم حذف جميع البيانات المرتبطة به.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.db.delete_employee(employee['id'])
            if success:
                QMessageBox.information(self, "نجح", "تم حذف الموظف بنجاح!")
                self.refresh()
                self.employee_updated.emit()
            else:
                QMessageBox.critical(self, "خطأ", "فشل حذف الموظف!")
    
    def refresh(self):
        """تحديث القائمة"""
        self.load_employees()

