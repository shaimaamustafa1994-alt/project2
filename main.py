# -*- coding: utf-8 -*-
"""
نظام إدارة شؤون الموظفين والعلاوات والترفيعات
Employee Management and Entitlements System
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QStackedWidget,
                            QFrame, QScrollArea, QSplitter)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QColor

# استيراد الوحدات
from database import Database
from calculation_engine import CalculationEngine
from ui.dashboard import DashboardWidget
from ui.employees_list import EmployeesListWidget
from ui.add_employee import AddEmployeeDialog
from ui.statistics import StatisticsWidget
from ui.upcoming_entitlements import UpcomingEntitlementsWidget
from ui.styles import get_stylesheet


class MainWindow(QMainWindow):
    """النافذة الرئيسية للتطبيق"""
    
    def __init__(self):
        super().__init__()
        
        # تهيئة قاعدة البيانات ومحرك الحسابات
        self.db = Database()
        self.engine = CalculationEngine(self.db)
        
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        self.setWindowTitle("نظام إدارة شؤون الموظفين والعلاوات والترفيعات")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 800)
        
        # الويدجت المركزي
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # التخطيط الرئيسي
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # الشريط الجانبي
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # منطقة المحتوى
        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area)
        
        # إضافة الصفحات
        self.add_pages()
        
        # عرض الصفحة الرئيسية
        self.content_area.setCurrentIndex(0)
    
    def create_sidebar(self):
        """إنشاء الشريط الجانبي"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(280)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # الشعار والعنوان
        header = QFrame()
        header.setObjectName("sidebar_header")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 30, 20, 30)
        
        title = QLabel("نظام إدارة\nالموظفين")
        title.setObjectName("sidebar_title")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        layout.addWidget(header)
        
        # قائمة الأزرار
        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(10, 20, 10, 20)
        buttons_layout.setSpacing(10)
        
        # تعريف أزرار القائمة
        menu_items = [
            ("🏠", "الصفحة الرئيسية", 0),
            ("👥", "قائمة الموظفين", 1),
            ("➕", "إضافة موظف جديد", 2),
            ("📊", "الإحصائيات", 3),
            ("📅", "الاستحقاقات القادمة", 4),
            ("⚙️", "الإعدادات", 5),
        ]
        
        self.menu_buttons = []
        
        for icon, text, index in menu_items:
            btn = self.create_menu_button(icon, text, index)
            buttons_layout.addWidget(btn)
            self.menu_buttons.append(btn)
        
        buttons_layout.addStretch()
        
        # زر الخروج
        exit_btn = QPushButton("🚪  خروج")
        exit_btn.setObjectName("exit_button")
        exit_btn.clicked.connect(self.close)
        buttons_layout.addWidget(exit_btn)
        
        layout.addWidget(buttons_widget)
        
        return sidebar
    
    def create_menu_button(self, icon, text, index):
        """إنشاء زر في القائمة الجانبية"""
        btn = QPushButton(f"{icon}  {text}")
        btn.setObjectName("menu_button")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setCheckable(True)
        
        if index == 0:
            btn.setChecked(True)
        
        btn.clicked.connect(lambda: self.switch_page(index))
        
        return btn
    
    def switch_page(self, index):
        """تبديل الصفحة"""
        # إلغاء تحديد جميع الأزرار
        for btn in self.menu_buttons:
            btn.setChecked(False)
        
        # تحديد الزر الحالي
        if index < len(self.menu_buttons):
            self.menu_buttons[index].setChecked(True)
        
        # معالجة خاصة لزر "إضافة موظف"
        if index == 2:
            self.show_add_employee_dialog()
            # العودة للصفحة السابقة
            prev_index = self.content_area.currentIndex()
            if prev_index < len(self.menu_buttons):
                self.menu_buttons[prev_index].setChecked(True)
        else:
            self.content_area.setCurrentIndex(index)
    
    def add_pages(self):
        """إضافة الصفحات إلى منطقة المحتوى"""
        
        # 0: الصفحة الرئيسية
        dashboard = DashboardWidget(self.db, self.engine)
        self.content_area.addWidget(dashboard)
        
        # 1: قائمة الموظفين
        employees_list = EmployeesListWidget(self.db, self.engine)
        employees_list.employee_updated.connect(self.refresh_all)
        self.content_area.addWidget(employees_list)
        
        # 2: إضافة موظف (مخصص - يفتح نافذة حوار)
        placeholder = QWidget()
        self.content_area.addWidget(placeholder)
        
        # 3: الإحصائيات
        statistics = StatisticsWidget(self.db)
        self.content_area.addWidget(statistics)
        
        # 4: الاستحقاقات القادمة
        upcoming = UpcomingEntitlementsWidget(self.db, self.engine)
        self.content_area.addWidget(upcoming)
        
        # 5: الإعدادات
        settings = QLabel("⚙️ صفحة الإعدادات\n\nقيد التطوير...")
        settings.setAlignment(Qt.AlignCenter)
        settings.setStyleSheet("font-size: 24px; color: #666;")
        self.content_area.addWidget(settings)
    
    def show_add_employee_dialog(self):
        """عرض نافذة إضافة موظف جديد"""
        dialog = AddEmployeeDialog(self.db, self)
        if dialog.exec_():
            # تحديث القوائم بعد إضافة الموظف
            self.refresh_all()
    
    def refresh_all(self):
        """تحديث جميع الواجهات"""
        # تحديث لوحة التحكم
        widget = self.content_area.widget(0)
        if hasattr(widget, 'refresh'):
            widget.refresh()
        
        # تحديث قائمة الموظفين
        widget = self.content_area.widget(1)
        if hasattr(widget, 'refresh'):
            widget.refresh()
        
        # تحديث الإحصائيات
        widget = self.content_area.widget(3)
        if hasattr(widget, 'refresh'):
            widget.refresh()
        
        # تحديث الاستحقاقات القادمة
        widget = self.content_area.widget(4)
        if hasattr(widget, 'refresh'):
            widget.refresh()
    
    def apply_styles(self):
        """تطبيق الأنماط"""
        self.setStyleSheet(get_stylesheet())
    
    def closeEvent(self, event):
        """حدث إغلاق التطبيق"""
        self.db.close()
        event.accept()


def main():
    """دالة التشغيل الرئيسية"""
    
    # إنشاء التطبيق
    app = QApplication(sys.argv)
    
    # تعيين خصائص التطبيق
    app.setApplicationName("نظام إدارة شؤون الموظفين")
    app.setOrganizationName("نظام الموارد البشرية")
    
    # تعيين الخط الافتراضي (دعم العربية)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # إنشاء النافذة الرئيسية
    window = MainWindow()
    window.show()
    
    # تشغيل التطبيق
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

