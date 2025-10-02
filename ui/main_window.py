"""
النافذة الرئيسية للتطبيق
Main Application Window
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame, QScrollArea, QGridLayout,
                             QMessageBox, QStackedWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QIcon
import os

from database.db_manager import DatabaseManager
from core.calculation_engine import CalculationEngine

class MainWindow(QMainWindow):
    """النافذة الرئيسية للتطبيق"""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.calc_engine = CalculationEngine(self.db)
        self.init_ui()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        self.setWindowTitle("نظام إدارة العلاوات والترفيعات الوظيفية")
        self.setMinimumSize(1200, 800)
        
        # الويدجت المركزي
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # التخطيط الرئيسي
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # الشريط الجانبي
        self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # المنطقة الرئيسية
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget, 1)
        
        # إنشاء الصفحات
        self.create_pages()
        
        # عرض الصفحة الرئيسية
        self.show_home_page()
    
    def create_sidebar(self):
        """إنشاء الشريط الجانبي"""
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(300)
        self.sidebar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1976D2, stop:1 #2196F3);
                border-right: 3px solid #0D47A1;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: none;
                padding: 15px 20px;
                font-size: 16px;
                font-weight: bold;
                text-align: right;
                border-radius: 8px;
                margin: 5px 10px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                transform: translateX(-5px);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QPushButton:checked {
                background-color: rgba(255, 255, 255, 0.25);
                border-left: 4px solid white;
            }
        """)
        
        layout = QVBoxLayout(self.sidebar)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 20, 15, 20)
        
        # العنوان
        title = QLabel("نظام إدارة العلاوات\nوالترفيعات الوظيفية")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 20px;
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(title)
        
        # أزرار القائمة
        menu_buttons = [
            ("🏠", "الصفحة الرئيسية", self.show_home_page),
            ("➕", "إضافة موظف جديد", self.show_add_employee),
            ("📋", "قائمة الموظفين", self.show_employees_list),
            ("📝", "إدارة الأحداث المهنية", self.show_events_management),
            ("📅", "لوحة الاستحقاقات", self.show_entitlements_dashboard),
            ("📊", "الإحصائيات", self.show_statistics),
        ]
        
        self.menu_buttons = []
        for icon, text, callback in menu_buttons:
            btn = QPushButton(f"{icon}  {text}")
            btn.clicked.connect(callback)
            btn.setCheckable(True)
            layout.addWidget(btn)
            self.menu_buttons.append(btn)
        
        layout.addStretch()
        
        # معلومات النسخة
        version_label = QLabel("الإصدار 1.0\n© 2024")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 12px;
                padding: 10px;
            }
        """)
        layout.addWidget(version_label)
    
    def create_pages(self):
        """إنشاء صفحات التطبيق"""
        # الصفحة الرئيسية
        self.home_page = self.create_home_page()
        self.stacked_widget.addWidget(self.home_page)
        
        # صفحات أخرى (ستُنشأ عند الحاجة)
        self.add_employee_page = None
        self.employees_list_page = None
        self.events_management_page = None
        self.entitlements_dashboard_page = None
        self.statistics_page = None
    
    def create_home_page(self):
        """إنشاء الصفحة الرئيسية"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(30)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # العنوان الرئيسي
        title = QLabel("مرحباً بك في نظام إدارة العلاوات والترفيعات الوظيفية")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #1976D2;
                padding: 30px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E3F2FD, stop:1 #BBDEFB);
                border-radius: 15px;
                border: 2px solid #2196F3;
            }
        """)
        layout.addWidget(title)
        
        # بطاقات الوصول السريع
        cards_layout = QGridLayout()
        cards_layout.setSpacing(20)
        
        cards_data = [
            ("➕", "إضافة موظف جديد", "إضافة موظف جديد إلى النظام", "#4CAF50", self.show_add_employee),
            ("📋", "قائمة الموظفين", "عرض وإدارة جميع الموظفين", "#FF9800", self.show_employees_list),
            ("📝", "الأحداث المهنية", "إدارة كتب الشكر والعقوبات", "#9C27B0", self.show_events_management),
            ("📅", "الاستحقاقات", "متابعة العلاوات والترفيعات", "#F44336", self.show_entitlements_dashboard),
            ("📊", "الإحصائيات", "تقارير وإحصائيات شاملة", "#607D8B", self.show_statistics),
            ("⚙️", "الإعدادات", "إعدادات النظام والتخصيص", "#795548", self.show_settings),
        ]
        
        for i, (icon, title, desc, color, callback) in enumerate(cards_data):
            card = self.create_card(icon, title, desc, color, callback)
            row = i // 3
            col = i % 3
            cards_layout.addWidget(card, row, col)
        
        layout.addLayout(cards_layout)
        
        # إحصائيات سريعة
        stats_frame = QFrame()
        stats_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
                padding: 20px;
            }
        """)
        stats_layout = QHBoxLayout(stats_frame)
        
        # الحصول على الإحصائيات
        stats = self.db.get_statistics()
        
        stats_items = [
            ("👥", "إجمالي الموظفين", str(stats.get('total_employees', 0))),
            ("🎓", "التدريسي", str(stats.get('by_category', {}).get('تدريسي', 0))),
            ("💼", "الإداري", str(stats.get('by_category', {}).get('إداري', 0))),
            ("🔧", "الفني", str(stats.get('by_category', {}).get('فني', 0))),
        ]
        
        for icon, label, value in stats_items:
            stat_widget = QWidget()
            stat_layout = QVBoxLayout(stat_widget)
            stat_layout.setAlignment(Qt.AlignCenter)
            
            icon_label = QLabel(icon)
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setStyleSheet("font-size: 32px; margin-bottom: 10px;")
            
            value_label = QLabel(value)
            value_label.setAlignment(Qt.AlignCenter)
            value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2196F3;")
            
            desc_label = QLabel(label)
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setStyleSheet("font-size: 14px; color: #666;")
            
            stat_layout.addWidget(icon_label)
            stat_layout.addWidget(value_label)
            stat_layout.addWidget(desc_label)
            
            stats_layout.addWidget(stat_widget)
        
        layout.addWidget(stats_frame)
        layout.addStretch()
        
        return page
    
    def create_card(self, icon, title, description, color, callback):
        """إنشاء بطاقة وصول سريع"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 12px;
                border: 2px solid {color};
                padding: 20px;
                min-height: 150px;
            }}
            QFrame:hover {{
                background-color: #f8f9fa;
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        
        # الأيقونة
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(f"""
            font-size: 48px;
            color: {color};
            margin-bottom: 10px;
        """)
        layout.addWidget(icon_label)
        
        # العنوان
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {color};
            margin-bottom: 5px;
        """)
        layout.addWidget(title_label)
        
        # الوصف
        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("""
            font-size: 13px;
            color: #666;
            line-height: 1.4;
        """)
        layout.addWidget(desc_label)
        
        # زر الوصول
        access_btn = QPushButton("الوصول")
        access_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                margin-top: 10px;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
        """)
        access_btn.clicked.connect(callback)
        layout.addWidget(access_btn)
        
        return card
    
    def set_active_button(self, active_button):
        """تعيين الزر النشط"""
        for btn in self.menu_buttons:
            btn.setChecked(False)
        active_button.setChecked(True)
    
    def show_home_page(self):
        """عرض الصفحة الرئيسية"""
        self.stacked_widget.setCurrentWidget(self.home_page)
        if self.menu_buttons:
            self.set_active_button(self.menu_buttons[0])
    
    def show_add_employee(self):
        """عرض صفحة إضافة موظف"""
        if not self.add_employee_page:
            from ui.employee_management import EmployeeManagement
            self.add_employee_page = EmployeeManagement(self.db)
            self.stacked_widget.addWidget(self.add_employee_page)
        
        self.stacked_widget.setCurrentWidget(self.add_employee_page)
        if len(self.menu_buttons) > 1:
            self.set_active_button(self.menu_buttons[1])
    
    def show_employees_list(self):
        """عرض قائمة الموظفين"""
        if not self.employees_list_page:
            from ui.employees_list import EmployeesList
            self.employees_list_page = EmployeesList(self.db, self.calc_engine)
            self.stacked_widget.addWidget(self.employees_list_page)
        
        self.stacked_widget.setCurrentWidget(self.employees_list_page)
        if len(self.menu_buttons) > 2:
            self.set_active_button(self.menu_buttons[2])
    
    def show_events_management(self):
        """عرض إدارة الأحداث"""
        if not self.events_management_page:
            from ui.events_management import EventsManagement
            self.events_management_page = EventsManagement(self.db, self.calc_engine)
            self.stacked_widget.addWidget(self.events_management_page)
        
        self.stacked_widget.setCurrentWidget(self.events_management_page)
        if len(self.menu_buttons) > 3:
            self.set_active_button(self.menu_buttons[3])
    
    def show_entitlements_dashboard(self):
        """عرض لوحة الاستحقاقات"""
        if not self.entitlements_dashboard_page:
            from ui.entitlements_dashboard import EntitlementsDashboard
            self.entitlements_dashboard_page = EntitlementsDashboard(self.db, self.calc_engine)
            self.stacked_widget.addWidget(self.entitlements_dashboard_page)
        
        self.stacked_widget.setCurrentWidget(self.entitlements_dashboard_page)
        if len(self.menu_buttons) > 4:
            self.set_active_button(self.menu_buttons[4])
    
    def show_statistics(self):
        """عرض الإحصائيات"""
        if not self.statistics_page:
            from ui.statistics_dashboard import StatisticsDashboard
            self.statistics_page = StatisticsDashboard(self.db)
            self.stacked_widget.addWidget(self.statistics_page)
        
        self.stacked_widget.setCurrentWidget(self.statistics_page)
        if len(self.menu_buttons) > 5:
            self.set_active_button(self.menu_buttons[5])
    
    def show_settings(self):
        """عرض الإعدادات"""
        QMessageBox.information(self, "الإعدادات", "صفحة الإعدادات قيد التطوير...")
    
    def closeEvent(self, event):
        """عند إغلاق التطبيق"""
        self.db.close()
        event.accept()

