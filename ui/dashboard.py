# -*- coding: utf-8 -*-
"""
لوحة التحكم الرئيسية
Main Dashboard
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QGridLayout, QScrollArea, QPushButton)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QIcon
from datetime import datetime, timedelta


class DashboardWidget(QWidget):
    """واجهة لوحة التحكم الرئيسية"""
    
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
        
        # العنوان الرئيسي
        header = self.create_header()
        layout.addWidget(header)
        
        # منطقة التمرير
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(25)
        
        # بطاقات المؤشرات الرئيسية
        stats_grid = self.create_statistics_cards()
        content_layout.addWidget(stats_grid)
        
        # قسم الاستحقاقات القريبة
        upcoming_section = self.create_upcoming_section()
        content_layout.addWidget(upcoming_section)
        
        # قسم النشاط الأخير
        activity_section = self.create_activity_section()
        content_layout.addWidget(activity_section)
        
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
    
    def create_header(self):
        """إنشاء رأس الصفحة"""
        header = QFrame()
        layout = QVBoxLayout(header)
        
        # العنوان
        title = QLabel("مرحباً بك في نظام إدارة الموظفين 👋")
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
        """)
        layout.addWidget(title)
        
        # التاريخ والوقت
        now = datetime.now()
        date_label = QLabel(now.strftime("📅 %Y/%m/%d  🕐 %I:%M %p"))
        date_label.setStyleSheet("""
            font-size: 16px;
            color: #7f8c8d;
            margin-top: 5px;
        """)
        layout.addWidget(date_label)
        
        return header
    
    def create_statistics_cards(self):
        """إنشاء بطاقات الإحصائيات"""
        container = QFrame()
        container.setStyleSheet("background: transparent;")
        
        grid = QGridLayout(container)
        grid.setSpacing(20)
        
        # جلب الإحصائيات
        stats = self.db.get_statistics()
        
        # بطاقة إجمالي الموظفين
        total_card = self.create_stat_card(
            "👥",
            "إجمالي الموظفين",
            str(stats.get('total_employees', 0)),
            "#3498db"
        )
        grid.addWidget(total_card, 0, 0)
        
        # بطاقة التدريسيين
        teaching_count = stats.get('by_category', {}).get('تدريسي', 0)
        teaching_card = self.create_stat_card(
            "🎓",
            "الكادر التدريسي",
            str(teaching_count),
            "#27ae60"
        )
        grid.addWidget(teaching_card, 0, 1)
        
        # بطاقة الإداريين
        admin_count = stats.get('by_category', {}).get('إداري', 0)
        admin_card = self.create_stat_card(
            "💼",
            "الكادر الإداري",
            str(admin_count),
            "#9b59b6"
        )
        grid.addWidget(admin_card, 0, 2)
        
        # بطاقة الفنيين
        tech_count = stats.get('by_category', {}).get('فني', 0)
        tech_card = self.create_stat_card(
            "🔧",
            "الكادر الفني",
            str(tech_count),
            "#e67e22"
        )
        grid.addWidget(tech_card, 0, 3)
        
        # بطاقة الاستحقاقات القادمة
        upcoming = self.engine.get_upcoming_entitlements(30)
        upcoming_card = self.create_stat_card(
            "📅",
            "استحقاقات الشهر القادم",
            str(len(upcoming)),
            "#e74c3c"
        )
        grid.addWidget(upcoming_card, 1, 0)
        
        # بطاقة الدكتوراه
        phd_count = stats.get('by_education', {}).get('دكتوراه', 0)
        phd_card = self.create_stat_card(
            "🎓",
            "حملة الدكتوراه",
            str(phd_count),
            "#16a085"
        )
        grid.addWidget(phd_card, 1, 1)
        
        # بطاقة الماجستير
        master_count = stats.get('by_education', {}).get('ماجستير', 0)
        master_card = self.create_stat_card(
            "📚",
            "حملة الماجستير",
            str(master_count),
            "#2980b9"
        )
        grid.addWidget(master_card, 1, 2)
        
        # بطاقة البكالوريوس
        bachelor_count = stats.get('by_education', {}).get('بكالوريوس', 0)
        bachelor_card = self.create_stat_card(
            "📖",
            "حملة البكالوريوس",
            str(bachelor_count),
            "#8e44ad"
        )
        grid.addWidget(bachelor_card, 1, 3)
        
        return container
    
    def create_stat_card(self, icon, title, value, color):
        """إنشاء بطاقة إحصائية"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 15px;
                border-right: 5px solid {color};
                padding: 20px;
            }}
            QFrame:hover {{
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            }}
        """)
        
        layout = QHBoxLayout(card)
        layout.setSpacing(15)
        
        # الأيقونة
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 48px;
            color: {color};
        """)
        icon_label.setFixedSize(70, 70)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # النص
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 14px;
            color: #7f8c8d;
            font-weight: 600;
        """)
        text_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            font-size: 32px;
            color: {color};
            font-weight: bold;
        """)
        text_layout.addWidget(value_label)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        
        return card
    
    def create_upcoming_section(self):
        """إنشاء قسم الاستحقاقات القريبة"""
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 25px;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setSpacing(15)
        
        # العنوان
        title = QLabel("📅 الاستحقاقات القادمة (الأسبوع القادم)")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2c3e50;
        """)
        layout.addWidget(title)
        
        # جلب الاستحقاقات
        upcoming = self.engine.get_upcoming_entitlements(7)
        
        if upcoming:
            for item in upcoming[:5]:  # عرض أول 5 فقط
                emp = item['employee']
                ent = item['entitlement']
                
                card = self.create_upcoming_card(emp, ent)
                layout.addWidget(card)
        else:
            no_data = QLabel("لا توجد استحقاقات خلال الأسبوع القادم ✅")
            no_data.setStyleSheet("""
                font-size: 16px;
                color: #95a5a6;
                padding: 20px;
            """)
            no_data.setAlignment(Qt.AlignCenter)
            layout.addWidget(no_data)
        
        return section
    
    def create_upcoming_card(self, employee, entitlement):
        """إنشاء بطاقة استحقاق قادم"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 15px;
                border-right: 4px solid #3498db;
            }
        """)
        
        layout = QHBoxLayout(card)
        
        # معلومات الموظف
        info_layout = QVBoxLayout()
        
        name = QLabel(f"👤 {employee['full_name']}")
        name.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        info_layout.addWidget(name)
        
        details = QLabel(
            f"{employee['job_title']} - الدرجة {employee['job_grade']}/المرحلة {employee['job_stage']}"
        )
        details.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        info_layout.addWidget(details)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # معلومات الاستحقاق
        ent_layout = QVBoxLayout()
        ent_layout.setAlignment(Qt.AlignRight)
        
        ent_type = "🎉 علاوة" if entitlement['type'] == 'علاوة' else "⬆️ ترفيع"
        type_label = QLabel(ent_type)
        type_label.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            color: #27ae60;
        """)
        ent_layout.addWidget(type_label)
        
        date_label = QLabel(entitlement['date'].strftime("%Y/%m/%d"))
        date_label.setStyleSheet("font-size: 14px; color: #e74c3c;")
        ent_layout.addWidget(date_label)
        
        layout.addLayout(ent_layout)
        
        return card
    
    def create_activity_section(self):
        """إنشاء قسم النشاط الأخير"""
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 25px;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setSpacing(15)
        
        # العنوان
        title = QLabel("📊 ملخص سريع")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2c3e50;
        """)
        layout.addWidget(title)
        
        # معلومات إضافية
        info_text = """
        <p style='font-size: 16px; color: #34495e; line-height: 1.8;'>
        ✅ النظام يعمل بكفاءة عالية<br>
        📈 جميع الحسابات محدثة تلقائياً<br>
        🔄 يتم تحديث الاستحقاقات بشكل فوري<br>
        💡 استخدم القائمة الجانبية للتنقل بين الأقسام
        </p>
        """
        
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        return section
    
    def refresh(self):
        """تحديث البيانات"""
        # إعادة بناء الواجهة
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        self.init_ui()

