# -*- coding: utf-8 -*-
"""
لوحة الاستحقاقات القادمة
Upcoming Entitlements Dashboard
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QFrame, QTabWidget, QTableWidget, QTableWidgetItem,
                            QPushButton, QScrollArea, QHeaderView, QAbstractItemView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from datetime import datetime


class UpcomingEntitlementsWidget(QWidget):
    """واجهة الاستحقاقات القادمة"""
    
    def __init__(self, database, engine, parent=None):
        super().__init__(parent)
        self.db = database
        self.engine = engine
        self.init_ui()
    
    def init_ui(self):
        """تهيئة الواجهة"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        # العنوان
        title = QLabel("📅 الاستحقاقات القادمة")
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
        """)
        layout.addWidget(title)
        
        # التبويبات
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e1e8ed;
                border-radius: 10px;
                background-color: white;
                top: -1px;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                color: #7f8c8d;
                padding: 15px 30px;
                margin-right: 5px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-weight: 600;
                font-size: 16px;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
            }
            QTabBar::tab:hover {
                background-color: #d5dbdb;
            }
        """)
        
        # تبويب الأسبوع القادم
        week_tab = self.create_entitlements_tab(7)
        tabs.addTab(week_tab, "📅 الأسبوع القادم (7 أيام)")
        
        # تبويب الشهر القادم
        month_tab = self.create_entitlements_tab(30)
        tabs.addTab(month_tab, "📅 الشهر القادم (30 يوم)")
        
        # تبويب الثلاثة أشهر القادمة
        quarter_tab = self.create_entitlements_tab(90)
        tabs.addTab(quarter_tab, "📅 الثلاثة أشهر القادمة")
        
        layout.addWidget(tabs)
    
    def create_entitlements_tab(self, days):
        """إنشاء تبويب الاستحقاقات"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # معلومات إحصائية
        info_bar = self.create_info_bar(days)
        layout.addWidget(info_bar)
        
        # الجدول
        table = self.create_entitlements_table(days)
        layout.addWidget(table)
        
        return tab
    
    def create_info_bar(self, days):
        """إنشاء شريط المعلومات الإحصائية"""
        bar = QFrame()
        bar.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #667eea,
                    stop: 1 #764ba2
                );
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        layout = QHBoxLayout(bar)
        
        # جلب البيانات
        upcoming = self.engine.get_upcoming_entitlements(days)
        
        # إحصائيات
        total_count = len(upcoming)
        allowance_count = len([u for u in upcoming if u['entitlement']['type'] == 'علاوة'])
        promotion_count = len([u for u in upcoming if u['entitlement']['type'] == 'ترفيع'])
        
        # بطاقات المعلومات
        total_info = self.create_info_card("📊", "إجمالي", str(total_count))
        allowance_info = self.create_info_card("🎉", "علاوات", str(allowance_count))
        promotion_info = self.create_info_card("⬆️", "ترفيعات", str(promotion_count))
        
        layout.addWidget(total_info)
        layout.addWidget(allowance_info)
        layout.addWidget(promotion_info)
        layout.addStretch()
        
        return bar
    
    def create_info_card(self, icon, label, value):
        """إنشاء بطاقة معلومات صغيرة"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        layout = QHBoxLayout(card)
        layout.setSpacing(10)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 32px; color: white;")
        layout.addWidget(icon_label)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9);
            font-size: 14px;
            font-weight: 600;
        """)
        text_layout.addWidget(label_widget)
        
        value_widget = QLabel(value)
        value_widget.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        text_layout.addWidget(value_widget)
        
        layout.addLayout(text_layout)
        
        return card
    
    def create_entitlements_table(self, days):
        """إنشاء جدول الاستحقاقات"""
        table = QTableWidget()
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels([
            "الاسم",
            "العنوان الوظيفي",
            "الصنف",
            "الدرجة الحالية",
            "المرحلة الحالية",
            "نوع الاستحقاق",
            "التاريخ",
            "الأيام المتبقية"
        ])
        
        # تنسيق الجدول
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                gridline-color: #ecf0f1;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #ecf0f1;
            }
            QTableWidget::item:selected {
                background-color: #e8f4f8;
                color: #2c3e50;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 15px;
                border: none;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        
        # توزيع الأعمدة
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        
        # جلب البيانات
        upcoming = self.engine.get_upcoming_entitlements(days)
        
        # ملء الجدول
        table.setRowCount(len(upcoming))
        
        for row, item in enumerate(upcoming):
            emp = item['employee']
            ent = item['entitlement']
            
            # الاسم
            name_item = QTableWidgetItem(emp['full_name'])
            name_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            table.setItem(row, 0, name_item)
            
            # العنوان الوظيفي
            table.setItem(row, 1, QTableWidgetItem(emp['job_title']))
            
            # الصنف
            category_item = QTableWidgetItem(emp['job_category'])
            if emp['job_category'] == 'تدريسي':
                category_item.setForeground(QColor("#27ae60"))
            elif emp['job_category'] == 'إداري':
                category_item.setForeground(QColor("#3498db"))
            else:
                category_item.setForeground(QColor("#e67e22"))
            category_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            table.setItem(row, 2, category_item)
            
            # الدرجة الحالية
            table.setItem(row, 3, QTableWidgetItem(str(ent['current_grade'])))
            
            # المرحلة الحالية
            table.setItem(row, 4, QTableWidgetItem(str(ent['current_stage'])))
            
            # نوع الاستحقاق
            ent_type = "🎉 علاوة" if ent['type'] == 'علاوة' else "⬆️ ترفيع"
            ent_item = QTableWidgetItem(ent_type)
            ent_item.setFont(QFont("Segoe UI", 11, QFont.Bold))
            if ent['type'] == 'علاوة':
                ent_item.setForeground(QColor("#27ae60"))
            else:
                ent_item.setForeground(QColor("#3498db"))
            table.setItem(row, 5, ent_item)
            
            # التاريخ
            date_item = QTableWidgetItem(ent['date'].strftime("%Y/%m/%d"))
            date_item.setForeground(QColor("#e74c3c"))
            date_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            table.setItem(row, 6, date_item)
            
            # الأيام المتبقية
            days_left = (ent['date'] - datetime.now().date()).days
            days_item = QTableWidgetItem(f"{days_left} يوم")
            
            # تلوين حسب الأيام المتبقية
            if days_left <= 7:
                days_item.setForeground(QColor("#e74c3c"))
                days_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            elif days_left <= 14:
                days_item.setForeground(QColor("#f39c12"))
            else:
                days_item.setForeground(QColor("#27ae60"))
            
            table.setItem(row, 7, days_item)
        
        # رسالة إذا لم توجد بيانات
        if len(upcoming) == 0:
            table.setRowCount(1)
            no_data = QTableWidgetItem("✅ لا توجد استحقاقات خلال هذه الفترة")
            no_data.setTextAlignment(Qt.AlignCenter)
            no_data.setFont(QFont("Segoe UI", 14))
            no_data.setForeground(QColor("#95a5a6"))
            table.setSpan(0, 0, 1, 8)
            table.setItem(0, 0, no_data)
            table.setRowHeight(0, 100)
        
        return table
    
    def refresh(self):
        """تحديث البيانات"""
        # إعادة بناء الواجهة
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        self.init_ui()

