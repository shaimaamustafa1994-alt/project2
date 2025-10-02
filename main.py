"""
نظام إدارة العلاوات والترفيعات الوظيفية
Employee Allowances and Promotions Management System
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from ui.main_window import MainWindow
from database.db_manager import DatabaseManager

def main():
    """النقطة الرئيسية لتشغيل التطبيق"""
    
    # إنشاء قاعدة البيانات
    db = DatabaseManager()
    db.create_tables()
    
    # إنشاء التطبيق
    app = QApplication(sys.argv)
    
    # تعيين الخط الافتراضي كبير وواضح
    font = QFont("Arial", 12)
    app.setFont(font)
    
    # تعيين اتجاه النص من اليمين لليسار للدعم العربي
    app.setLayoutDirection(Qt.RightToLeft)
    
    # تطبيق ستايل عصري
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QPushButton {
            background-color: #2196F3;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 6px;
            min-height: 40px;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
        QPushButton:pressed {
            background-color: #0D47A1;
        }
        QPushButton:disabled {
            background-color: #BDBDBD;
        }
        QLineEdit, QTextEdit, QComboBox, QSpinBox, QDateEdit {
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            background-color: white;
            font-size: 13px;
            min-height: 35px;
        }
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDateEdit:focus {
            border: 2px solid #2196F3;
        }
        QLabel {
            font-size: 13px;
            color: #333;
        }
        QTableWidget {
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            background-color: white;
            gridline-color: #e0e0e0;
        }
        QTableWidget::item {
            padding: 8px;
        }
        QTableWidget::item:selected {
            background-color: #E3F2FD;
            color: #1976D2;
        }
        QHeaderView::section {
            background-color: #2196F3;
            color: white;
            padding: 10px;
            border: none;
            font-weight: bold;
            font-size: 13px;
        }
        QTabWidget::pane {
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            background-color: white;
        }
        QTabBar::tab {
            background-color: #f5f5f5;
            color: #666;
            padding: 12px 24px;
            margin-right: 4px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            font-size: 13px;
            font-weight: bold;
        }
        QTabBar::tab:selected {
            background-color: white;
            color: #2196F3;
            border-bottom: 3px solid #2196F3;
        }
        QGroupBox {
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            margin-top: 12px;
            padding: 15px;
            font-weight: bold;
            font-size: 14px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top right;
            padding: 0 10px;
            color: #2196F3;
        }
        QScrollBar:vertical {
            border: none;
            background: #f5f5f5;
            width: 12px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: #BDBDBD;
            border-radius: 6px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background: #9E9E9E;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
        QMessageBox {
            background-color: white;
        }
        QMessageBox QPushButton {
            min-width: 100px;
        }
    """)
    
    # إنشاء وعرض النافذة الرئيسية
    window = MainWindow()
    window.showMaximized()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

