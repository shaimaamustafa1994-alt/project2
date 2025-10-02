"""
لوحة الاستحقاقات
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from datetime import date, timedelta

class EntitlementsDashboardWidget(QWidget):
    def __init__(self, db_manager, calculation_engine):
        super().__init__()
        self.db = db_manager
        self.engine = calculation_engine
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(layout)
        
        title = QLabel("📅 لوحة الاستحقاقات القادمة")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1976D2; padding: 15px; background-color: white; border-radius: 8px;")
        layout.addWidget(title)
        
        # الاستحقاقات الأسبوع القادم
        week_group = QGroupBox("الاستحقاقات خلال الأسبوع القادم")
        week_layout = QVBoxLayout()
        week_group.setLayout(week_layout)
        
        self.week_table = QTableWidget()
        self.week_table.setColumnCount(5)
        self.week_table.setHorizontalHeaderLabels(["الاسم", "العنوان", "الحدث", "التاريخ", "الراتب الجديد"])
        week_layout.addWidget(self.week_table)
        
        layout.addWidget(week_group)
        
        # الاستحقاقات الشهر القادم
        month_group = QGroupBox("الاستحقاقات خلال الشهر القادم")
        month_layout = QVBoxLayout()
        month_group.setLayout(month_layout)
        
        self.month_table = QTableWidget()
        self.month_table.setColumnCount(5)
        self.month_table.setHorizontalHeaderLabels(["الاسم", "العنوان", "الحدث", "التاريخ", "الراتب الجديد"])
        month_layout.addWidget(self.month_table)
        
        layout.addWidget(month_group)
        
        # زر تحديث
        refresh_btn = QPushButton("🔄 تحديث")
        refresh_btn.setFixedHeight(45)
        refresh_btn.clicked.connect(self.load_data)
        layout.addWidget(refresh_btn)
    
    def load_data(self):
        # الأسبوع القادم
        week_entitlements = self.engine.get_upcoming_entitlements(7)
        self.week_table.setRowCount(len(week_entitlements))
        
        for i, item in enumerate(week_entitlements):
            emp = item['employee']
            ent = item['entitlement']
            
            self.week_table.setItem(i, 0, QTableWidgetItem(emp['full_name']))
            self.week_table.setItem(i, 1, QTableWidgetItem(emp['job_title']))
            self.week_table.setItem(i, 2, QTableWidgetItem(ent['entitlement_type']))
            self.week_table.setItem(i, 3, QTableWidgetItem(ent['next_entitlement_date'].strftime('%Y/%m/%d')))
            self.week_table.setItem(i, 4, QTableWidgetItem(f"{ent['new_salary']:,.0f}"))
        
        # الشهر القادم
        month_entitlements = self.engine.get_upcoming_entitlements(30)
        self.month_table.setRowCount(len(month_entitlements))
        
        for i, item in enumerate(month_entitlements):
            emp = item['employee']
            ent = item['entitlement']
            
            self.month_table.setItem(i, 0, QTableWidgetItem(emp['full_name']))
            self.month_table.setItem(i, 1, QTableWidgetItem(emp['job_title']))
            self.month_table.setItem(i, 2, QTableWidgetItem(ent['entitlement_type']))
            self.month_table.setItem(i, 3, QTableWidgetItem(ent['next_entitlement_date'].strftime('%Y/%m/%d')))
            self.month_table.setItem(i, 4, QTableWidgetItem(f"{ent['new_salary']:,.0f}"))
