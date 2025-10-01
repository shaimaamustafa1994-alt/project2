# -*- coding: utf-8 -*-
"""
أنماط التطبيق
Application Styles
"""

def get_stylesheet():
    """إرجاع ملف الأنماط CSS للتطبيق"""
    
    return """
    /* الأنماط العامة */
    * {
        font-family: 'Segoe UI', 'Tahoma', 'Arial', sans-serif;
    }
    
    QMainWindow {
        background-color: #f5f7fa;
    }
    
    /* الشريط الجانبي */
    #sidebar {
        background: qlineargradient(
            x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 #667eea,
            stop: 1 #764ba2
        );
        border-right: 1px solid #5568d3;
    }
    
    #sidebar_header {
        background-color: rgba(255, 255, 255, 0.1);
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    #sidebar_title {
        color: white;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        line-height: 1.3;
    }
    
    /* أزرار القائمة */
    #menu_button {
        background-color: transparent;
        color: white;
        border: none;
        text-align: right;
        padding: 15px 20px;
        font-size: 16px;
        font-weight: 500;
        border-radius: 10px;
        margin: 2px 0;
    }
    
    #menu_button:hover {
        background-color: rgba(255, 255, 255, 0.15);
    }
    
    #menu_button:checked {
        background-color: rgba(255, 255, 255, 0.25);
        font-weight: bold;
    }
    
    #exit_button {
        background-color: rgba(231, 76, 60, 0.8);
        color: white;
        border: none;
        padding: 12px;
        font-size: 15px;
        font-weight: bold;
        border-radius: 8px;
    }
    
    #exit_button:hover {
        background-color: rgba(192, 57, 43, 0.9);
    }
    
    /* البطاقات */
    .card {
        background-color: white;
        border-radius: 15px;
        padding: 25px;
        border: 1px solid #e1e8ed;
    }
    
    .card:hover {
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }
    
    /* العناوين */
    .page_title {
        font-size: 32px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    
    .card_title {
        font-size: 20px;
        font-weight: bold;
        color: #34495e;
        margin-bottom: 15px;
    }
    
    .section_title {
        font-size: 18px;
        font-weight: 600;
        color: #7f8c8d;
        margin: 20px 0 10px 0;
    }
    
    /* الأزرار */
    QPushButton {
        background-color: #3498db;
        color: white;
        border: none;
        padding: 12px 24px;
        font-size: 14px;
        font-weight: 600;
        border-radius: 8px;
    }
    
    QPushButton:hover {
        background-color: #2980b9;
    }
    
    QPushButton:pressed {
        background-color: #21618c;
    }
    
    QPushButton:disabled {
        background-color: #bdc3c7;
        color: #7f8c8d;
    }
    
    .primary_button {
        background-color: #27ae60;
    }
    
    .primary_button:hover {
        background-color: #229954;
    }
    
    .danger_button {
        background-color: #e74c3c;
    }
    
    .danger_button:hover {
        background-color: #c0392b;
    }
    
    .warning_button {
        background-color: #f39c12;
    }
    
    .warning_button:hover {
        background-color: #d68910;
    }
    
    /* حقول الإدخال */
    QLineEdit, QTextEdit, QComboBox, QSpinBox, QDateEdit {
        background-color: white;
        border: 2px solid #e1e8ed;
        border-radius: 8px;
        padding: 10px;
        font-size: 14px;
        color: #2c3e50;
    }
    
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus, 
    QSpinBox:focus, QDateEdit:focus {
        border: 2px solid #3498db;
    }
    
    QComboBox::drop-down {
        border: none;
        width: 30px;
    }
    
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid #7f8c8d;
        width: 0;
        height: 0;
    }
    
    /* التسميات */
    QLabel {
        color: #2c3e50;
        font-size: 14px;
    }
    
    .label_bold {
        font-weight: bold;
        color: #34495e;
    }
    
    .label_large {
        font-size: 18px;
    }
    
    /* الجداول */
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
    
    /* شريط التمرير */
    QScrollBar:vertical {
        border: none;
        background-color: #f5f7fa;
        width: 12px;
        margin: 0;
    }
    
    QScrollBar::handle:vertical {
        background-color: #bdc3c7;
        border-radius: 6px;
        min-height: 30px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #95a5a6;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0;
    }
    
    QScrollBar:horizontal {
        border: none;
        background-color: #f5f7fa;
        height: 12px;
        margin: 0;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #bdc3c7;
        border-radius: 6px;
        min-width: 30px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #95a5a6;
    }
    
    /* التبويبات */
    QTabWidget::pane {
        border: 1px solid #e1e8ed;
        border-radius: 8px;
        background-color: white;
        top: -1px;
    }
    
    QTabBar::tab {
        background-color: #ecf0f1;
        color: #7f8c8d;
        padding: 12px 24px;
        margin-right: 5px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        font-weight: 600;
    }
    
    QTabBar::tab:selected {
        background-color: white;
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
    }
    
    QTabBar::tab:hover {
        background-color: #d5dbdb;
    }
    
    /* مربعات الاختيار */
    QCheckBox {
        spacing: 8px;
        color: #2c3e50;
    }
    
    QCheckBox::indicator {
        width: 20px;
        height: 20px;
        border-radius: 4px;
        border: 2px solid #bdc3c7;
        background-color: white;
    }
    
    QCheckBox::indicator:checked {
        background-color: #27ae60;
        border-color: #27ae60;
    }
    
    /* أزرار الراديو */
    QRadioButton {
        spacing: 8px;
        color: #2c3e50;
    }
    
    QRadioButton::indicator {
        width: 18px;
        height: 18px;
        border-radius: 9px;
        border: 2px solid #bdc3c7;
        background-color: white;
    }
    
    QRadioButton::indicator:checked {
        background-color: #3498db;
        border-color: #3498db;
    }
    
    /* نوافذ الحوار */
    QDialog {
        background-color: #f5f7fa;
    }
    
    /* شريط التقدم */
    QProgressBar {
        border: 2px solid #e1e8ed;
        border-radius: 8px;
        text-align: center;
        background-color: white;
        height: 25px;
    }
    
    QProgressBar::chunk {
        background-color: #27ae60;
        border-radius: 6px;
    }
    
    /* الإطارات */
    QFrame {
        border: none;
    }
    
    /* القوائم */
    QListWidget {
        background-color: white;
        border: 1px solid #e1e8ed;
        border-radius: 8px;
        padding: 5px;
    }
    
    QListWidget::item {
        padding: 10px;
        border-radius: 5px;
    }
    
    QListWidget::item:selected {
        background-color: #e8f4f8;
        color: #2c3e50;
    }
    
    QListWidget::item:hover {
        background-color: #f8f9fa;
    }
    
    /* التلميحات */
    QToolTip {
        background-color: #34495e;
        color: white;
        border: none;
        padding: 8px;
        border-radius: 5px;
        font-size: 12px;
    }
    
    /* رسائل التنبيه */
    QMessageBox {
        background-color: white;
    }
    
    QMessageBox QPushButton {
        min-width: 80px;
    }
    """

