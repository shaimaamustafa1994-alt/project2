"""
لوحة الإحصائيات
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class StatisticsDashboardWidget(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()
        self.load_statistics()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(layout)
        
        title = QLabel("📊 لوحة الإحصائيات")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1976D2; padding: 15px; background-color: white; border-radius: 8px;")
        layout.addWidget(title)
        
        # بطاقات الإحصائيات
        cards_layout = QHBoxLayout()
        
        self.total_card = self.create_stat_card("👥", "إجمالي الموظفين", "0", "#4CAF50")
        cards_layout.addWidget(self.total_card)
        
        self.teaching_card = self.create_stat_card("👨‍🏫", "الكادر التدريسي", "0", "#2196F3")
        cards_layout.addWidget(self.teaching_card)
        
        self.admin_card = self.create_stat_card("💼", "الكادر الإداري", "0", "#FF9800")
        cards_layout.addWidget(self.admin_card)
        
        self.tech_card = self.create_stat_card("🔧", "الكادر الفني", "0", "#9C27B0")
        cards_layout.addWidget(self.tech_card)
        
        layout.addLayout(cards_layout)
        
        # إحصائيات تفصيلية
        details_group = QGroupBox("إحصائيات تفصيلية")
        details_layout = QVBoxLayout()
        details_group.setLayout(details_layout)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setMaximumHeight(300)
        details_layout.addWidget(self.details_text)
        
        layout.addWidget(details_group)
        
        # زر تحديث
        refresh_btn = QPushButton("🔄 تحديث الإحصائيات")
        refresh_btn.setFixedHeight(45)
        refresh_btn.clicked.connect(self.load_statistics)
        layout.addWidget(refresh_btn)
        
        layout.addStretch()
    
    def create_stat_card(self, icon, title, value, color):
        card = QFrame()
        card.setStyleSheet(f"QFrame {{ background-color: {color}; border-radius: 10px; padding: 20px; }}")
        
        layout = QVBoxLayout()
        card.setLayout(layout)
        
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 48px; color: white;")
        layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("font-size: 32px; font-weight: bold; color: white;")
        value_label.setObjectName("value_label")
        layout.addWidget(value_label)
        
        return card
    
    def load_statistics(self):
        stats = self.db.get_statistics()
        
        # تحديث البطاقات
        self.total_card.findChild(QLabel, "value_label").setText(str(stats['total_employees']))
        
        by_category = stats.get('by_category', {})
        self.teaching_card.findChild(QLabel, "value_label").setText(str(by_category.get('تدريسي', 0)))
        self.admin_card.findChild(QLabel, "value_label").setText(str(by_category.get('إداري', 0)))
        self.tech_card.findChild(QLabel, "value_label").setText(str(by_category.get('فني', 0)))
        
        # تحديث التفاصيل
        details_html = "<h3>إحصائيات حسب المؤهل العلمي:</h3><ul>"
        for qual, count in stats.get('by_qualification', {}).items():
            details_html += f"<li><b>{qual}:</b> {count} موظف</li>"
        details_html += "</ul>"
        
        details_html += "<h3>إحصائيات حسب الدرجة الوظيفية:</h3><ul>"
        for degree, count in stats.get('by_degree', {}).items():
            details_html += f"<li><b>الدرجة {degree}:</b> {count} موظف</li>"
        details_html += "</ul>"
        
        self.details_text.setHtml(details_html)
