"""
ملف الموظف التفصيلي
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import json

class EmployeeProfileDialog(QDialog):
    def __init__(self, db_manager, calculation_engine, employee_id, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.engine = calculation_engine
        self.employee_id = employee_id
        self.employee = self.db.get_employee(employee_id)
        self.setWindowTitle(f"ملف الموظف - {self.employee['full_name']}")
        self.setMinimumSize(1000, 700)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # القسم العلوي
        header = QLabel(f"👤 {self.employee['full_name']}")
        header.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px; background-color: #2196F3; color: white; border-radius: 10px;")
        layout.addWidget(header)
        
        # المعلومات الأساسية
        info_group = QGroupBox("المعلومات الأساسية")
        info_layout = QFormLayout()
        info_group.setLayout(info_layout)
        
        info_layout.addRow("العنوان الوظيفي:", QLabel(self.employee['job_title']))
        info_layout.addRow("الصنف:", QLabel(self.employee['job_category']))
        info_layout.addRow("الشهادة:", QLabel(self.employee['academic_qualification']))
        info_layout.addRow("الدرجة/المرحلة:", QLabel(f"{self.employee['degree']}/{self.employee['stage']}"))
        
        layout.addWidget(info_group)
        
        # التبويبات
        tabs = QTabWidget()
        
        # تبويب المسار الوظيفي
        career_tab = QWidget()
        career_layout = QVBoxLayout()
        career_tab.setLayout(career_layout)
        
        career_label = QLabel("سجل العلاوات والترفيعات")
        career_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        career_layout.addWidget(career_label)
        
        history = self.db.get_employee_entitlement_history(self.employee_id)
        if history:
            table = QTableWidget(len(history), 5)
            table.setHorizontalHeaderLabels(["التاريخ", "النوع", "من", "إلى", "الراتب الجديد"])
            for i, record in enumerate(history):
                table.setItem(i, 0, QTableWidgetItem(record['entitlement_date']))
                table.setItem(i, 1, QTableWidgetItem(record['entitlement_type']))
                table.setItem(i, 2, QTableWidgetItem(f"د{record.get('previous_degree', '-')}/م{record.get('previous_stage', '-')}"))
                table.setItem(i, 3, QTableWidgetItem(f"د{record['new_degree']}/م{record['new_stage']}"))
                table.setItem(i, 4, QTableWidgetItem(f"{record['new_salary']:,.0f}"))
            career_layout.addWidget(table)
        else:
            career_layout.addWidget(QLabel("لا يوجد سجل"))
        
        tabs.addTab(career_tab, "المسار الوظيفي")
        
        # تبويب الأحداث
        events_tab = QWidget()
        events_layout = QVBoxLayout()
        events_tab.setLayout(events_layout)
        
        events_label = QLabel("الأحداث المهنية")
        events_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        events_layout.addWidget(events_label)
        
        events = self.db.get_employee_events(self.employee_id)
        if events:
            events_table = QTableWidget(len(events), 4)
            events_table.setHorizontalHeaderLabels(["التاريخ", "النوع", "التأثير", "الحالة"])
            for i, event in enumerate(events):
                events_table.setItem(i, 0, QTableWidgetItem(event['event_date']))
                events_table.setItem(i, 1, QTableWidgetItem(event['event_type']))
                impact = event.get('impact_months', 0)
                events_table.setItem(i, 2, QTableWidgetItem(f"{impact:+d} شهر" if impact != 0 else "-"))
                events_table.setItem(i, 3, QTableWidgetItem("ملغى" if event['is_cancelled'] else "نشط"))
            events_layout.addWidget(events_table)
        else:
            events_layout.addWidget(QLabel("لا توجد أحداث"))
        
        tabs.addTab(events_tab, "الأحداث المهنية")
        
        layout.addWidget(tabs)
        
        # زر الإغلاق
        close_btn = QPushButton("إغلاق")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
