# -*- coding: utf-8 -*-
"""
لوحة الإحصائيات
Statistics Dashboard
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QFrame, QGridLayout, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter, QColor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class StatisticsWidget(QWidget):
    """واجهة الإحصائيات"""
    
    def __init__(self, database, parent=None):
        super().__init__(parent)
        self.db = database
        self.init_ui()
    
    def init_ui(self):
        """تهيئة الواجهة"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        # العنوان
        title = QLabel("📊 الإحصائيات الشاملة")
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
        """)
        layout.addWidget(title)
        
        # منطقة التمرير
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(25)
        
        # البطاقات الإحصائية
        stats_cards = self.create_stat_cards()
        content_layout.addWidget(stats_cards)
        
        # الرسوم البيانية
        charts_section = self.create_charts_section()
        content_layout.addWidget(charts_section)
        
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
    
    def create_stat_cards(self):
        """إنشاء بطاقات الإحصائيات"""
        container = QFrame()
        container.setStyleSheet("background: transparent;")
        
        grid = QGridLayout(container)
        grid.setSpacing(20)
        
        # جلب الإحصائيات
        stats = self.db.get_statistics()
        
        # بطاقة إجمالي الموظفين
        total_card = self.create_card(
            "👥", "إجمالي الموظفين",
            str(stats.get('total_employees', 0)),
            "#3498db"
        )
        grid.addWidget(total_card, 0, 0)
        
        # حسب الصنف
        teaching = stats.get('by_category', {}).get('تدريسي', 0)
        admin = stats.get('by_category', {}).get('إداري', 0)
        tech = stats.get('by_category', {}).get('فني', 0)
        
        teaching_card = self.create_card("🎓", "تدريسي", str(teaching), "#27ae60")
        admin_card = self.create_card("💼", "إداري", str(admin), "#9b59b6")
        tech_card = self.create_card("🔧", "فني", str(tech), "#e67e22")
        
        grid.addWidget(teaching_card, 0, 1)
        grid.addWidget(admin_card, 0, 2)
        grid.addWidget(tech_card, 0, 3)
        
        # حسب المؤهل
        phd = stats.get('by_education', {}).get('دكتوراه', 0)
        master = stats.get('by_education', {}).get('ماجستير', 0)
        bachelor = stats.get('by_education', {}).get('بكالوريوس', 0)
        
        phd_card = self.create_card("🎓", "دكتوراه", str(phd), "#16a085")
        master_card = self.create_card("📚", "ماجستير", str(master), "#2980b9")
        bachelor_card = self.create_card("📖", "بكالوريوس", str(bachelor), "#8e44ad")
        
        grid.addWidget(phd_card, 1, 0)
        grid.addWidget(master_card, 1, 1)
        grid.addWidget(bachelor_card, 1, 2)
        
        # بطاقة في الخدمة
        in_service = stats.get('by_status', {}).get('في الخدمة', 0)
        service_card = self.create_card("✅", "في الخدمة", str(in_service), "#27ae60")
        grid.addWidget(service_card, 1, 3)
        
        return container
    
    def create_card(self, icon, title, value, color):
        """إنشاء بطاقة إحصائية"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 15px;
                border-top: 5px solid {color};
                padding: 20px;
            }}
            QFrame:hover {{
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)
        
        # الأيقونة
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 48px; color: {color};")
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # القيمة
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            font-size: 36px;
            font-weight: bold;
            color: {color};
        """)
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)
        
        # العنوان
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 16px;
            color: #7f8c8d;
            font-weight: 600;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        return card
    
    def create_charts_section(self):
        """إنشاء قسم الرسوم البيانية"""
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 25px;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setSpacing(20)
        
        # العنوان
        title = QLabel("📈 التوزيعات البيانية")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2c3e50;
        """)
        layout.addWidget(title)
        
        # الرسوم البيانية
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)
        
        try:
            # رسم التوزيع حسب الصنف
            category_chart = self.create_category_chart()
            charts_layout.addWidget(category_chart)
            
            # رسم التوزيع حسب المؤهل
            education_chart = self.create_education_chart()
            charts_layout.addWidget(education_chart)
            
            # رسم التوزيع حسب الدرجة
            grade_chart = self.create_grade_chart()
            charts_layout.addWidget(grade_chart)
            
        except Exception as e:
            error_label = QLabel(f"❌ خطأ في عرض الرسوم البيانية:\n{str(e)}")
            error_label.setStyleSheet("color: #e74c3c; padding: 20px;")
            error_label.setAlignment(Qt.AlignCenter)
            charts_layout.addWidget(error_label)
        
        layout.addLayout(charts_layout)
        
        return section
    
    def create_category_chart(self):
        """إنشاء رسم بياني للتوزيع حسب الصنف"""
        stats = self.db.get_statistics()
        categories = stats.get('by_category', {})
        
        if not categories:
            return QLabel("لا توجد بيانات")
        
        fig = Figure(figsize=(4, 4))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        
        labels = list(categories.keys())
        sizes = list(categories.values())
        colors = ['#27ae60', '#3498db', '#e67e22']
        
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
              startangle=90, textprops={'fontsize': 10, 'weight': 'bold'})
        ax.set_title('التوزيع حسب الصنف', fontsize=12, weight='bold')
        
        fig.tight_layout()
        
        return canvas
    
    def create_education_chart(self):
        """إنشاء رسم بياني للتوزيع حسب المؤهل"""
        stats = self.db.get_statistics()
        education = stats.get('by_education', {})
        
        if not education:
            return QLabel("لا توجد بيانات")
        
        fig = Figure(figsize=(4, 4))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        
        labels = list(education.keys())
        values = list(education.values())
        colors = ['#16a085', '#2980b9', '#8e44ad', '#f39c12', '#e74c3c']
        
        ax.bar(range(len(labels)), values, color=colors[:len(labels)])
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
        ax.set_ylabel('العدد', fontsize=10, weight='bold')
        ax.set_title('التوزيع حسب المؤهل', fontsize=12, weight='bold')
        
        fig.tight_layout()
        
        return canvas
    
    def create_grade_chart(self):
        """إنشاء رسم بياني للتوزيع حسب الدرجة"""
        stats = self.db.get_statistics()
        grades = stats.get('by_grade', {})
        
        if not grades:
            return QLabel("لا توجد بيانات")
        
        fig = Figure(figsize=(4, 4))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        
        # ترتيب الدرجات من 1 إلى 10
        sorted_grades = sorted(grades.items())
        labels = [f"الدرجة {g}" for g, _ in sorted_grades]
        values = [v for _, v in sorted_grades]
        
        ax.plot(labels, values, marker='o', linewidth=2, markersize=8, color='#3498db')
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
        ax.set_ylabel('العدد', fontsize=10, weight='bold')
        ax.set_title('التوزيع حسب الدرجة', fontsize=12, weight='bold')
        ax.grid(True, alpha=0.3)
        
        fig.tight_layout()
        
        return canvas
    
    def refresh(self):
        """تحديث البيانات"""
        # إعادة بناء الواجهة
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        self.init_ui()

