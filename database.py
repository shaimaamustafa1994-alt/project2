# -*- coding: utf-8 -*-
"""
نظام إدارة شؤون الموظفين - قاعدة البيانات
Employee Management System - Database Module
"""

import sqlite3
import os
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
import json


class Database:
    """فئة إدارة قاعدة البيانات"""
    
    def __init__(self, db_name: str = "employees.db"):
        """تهيئة الاتصال بقاعدة البيانات"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """إنشاء اتصال بقاعدة البيانات"""
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        # تفعيل المفاتيح الخارجية
        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.conn.commit()
    
    def create_tables(self):
        """إنشاء جداول قاعدة البيانات"""
        
        # جدول الموظفين
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            start_date DATE NOT NULL,
            last_entitlement_date DATE NOT NULL,
            education_degree TEXT NOT NULL,
            job_category TEXT NOT NULL CHECK(job_category IN ('تدريسي', 'إداري', 'فني')),
            job_title TEXT NOT NULL,
            job_grade INTEGER NOT NULL CHECK(job_grade BETWEEN 1 AND 10),
            job_stage INTEGER NOT NULL CHECK(job_stage BETWEEN 1 AND 11),
            entitlement_indicator TEXT NOT NULL,
            photo_path TEXT,
            status TEXT DEFAULT 'في الخدمة',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # جدول الأحداث المهنية
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS professional_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            event_number TEXT NOT NULL,
            event_date DATE NOT NULL,
            effect_months INTEGER DEFAULT 0,
            is_freeze BOOLEAN DEFAULT 0,
            start_date DATE,
            end_date DATE,
            description TEXT,
            notes TEXT,
            is_cancelled BOOLEAN DEFAULT 0,
            cancelled_by_event_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
            FOREIGN KEY (cancelled_by_event_id) REFERENCES professional_events(id)
        )
        """)
        
        # جدول السجل الوظيفي (العلاوات والترفيعات)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS career_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            event_type TEXT NOT NULL CHECK(event_type IN ('علاوة', 'ترفيع')),
            old_grade INTEGER NOT NULL,
            old_stage INTEGER NOT NULL,
            old_salary REAL NOT NULL,
            new_grade INTEGER NOT NULL,
            new_stage INTEGER NOT NULL,
            new_salary REAL NOT NULL,
            entitlement_date DATE NOT NULL,
            related_events TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
        )
        """)
        
        # جدول سلم الرواتب
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS salary_scale (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grade INTEGER NOT NULL,
            stage INTEGER NOT NULL,
            salary REAL NOT NULL,
            allowance_amount REAL NOT NULL,
            years_for_promotion INTEGER,
            UNIQUE(grade, stage)
        )
        """)
        
        # جدول الإحصائيات المخزنة مؤقتاً (للأداء)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS statistics_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stat_type TEXT NOT NULL UNIQUE,
            stat_value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        self.conn.commit()
        
        # ملء جدول سلم الرواتب إذا كان فارغاً
        self._populate_salary_scale()
    
    def _populate_salary_scale(self):
        """ملء جدول سلم الرواتب بالبيانات الافتراضية"""
        
        # التحقق إذا كان الجدول فارغاً
        self.cursor.execute("SELECT COUNT(*) FROM salary_scale")
        if self.cursor.fetchone()[0] > 0:
            return
        
        # بيانات سلم الرواتب (الدرجة، السنوات للترفيع، مقدار العلاوة، المراحل)
        salary_data = {
            1: (None, 20000, [910, 930, 950, 970, 990, 1010, 1030, 1050, 1070, 1090, 1110]),
            2: (5, 17000, [723, 740, 757, 774, 791, 808, 825, 842, 859, 876, 893]),
            3: (5, 10000, [600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700]),
            4: (5, 8000, [509, 517, 525, 533, 541, 549, 557, 565, 573, 581, 589]),
            5: (5, 6000, [429, 435, 441, 447, 453, 459, 465, 471, 477, 483, 489]),
            6: (4, 6000, [362, 368, 374, 380, 386, 392, 398, 404, 410, 416, 422]),
            7: (4, 6000, [296, 302, 308, 314, 320, 326, 332, 338, 344, 350, 356]),
            8: (4, 3000, [260, 263, 266, 269, 272, 275, 278, 281, 284, 287, 290]),
            9: (4, 3000, [210, 213, 216, 219, 222, 225, 228, 231, 234, 237, 240]),
            10: (4, 3000, [170, 173, 176, 179, 182, 185, 188, 191, 194, 197, 200])
        }
        
        for grade, (years_for_promotion, allowance, stages) in salary_data.items():
            for stage_num, salary in enumerate(stages, start=1):
                self.cursor.execute("""
                INSERT INTO salary_scale (grade, stage, salary, allowance_amount, years_for_promotion)
                VALUES (?, ?, ?, ?, ?)
                """, (grade, stage_num, salary, allowance, years_for_promotion))
        
        self.conn.commit()
    
    # ========== عمليات الموظفين ==========
    
    def add_employee(self, employee_data: Dict) -> int:
        """إضافة موظف جديد"""
        self.cursor.execute("""
        INSERT INTO employees (
            full_name, start_date, last_entitlement_date, education_degree,
            job_category, job_title, job_grade, job_stage, entitlement_indicator,
            photo_path, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            employee_data['full_name'],
            employee_data['start_date'],
            employee_data['last_entitlement_date'],
            employee_data['education_degree'],
            employee_data['job_category'],
            employee_data['job_title'],
            employee_data['job_grade'],
            employee_data['job_stage'],
            employee_data['entitlement_indicator'],
            employee_data.get('photo_path'),
            employee_data.get('notes')
        ))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_employee(self, employee_id: int, employee_data: Dict) -> bool:
        """تحديث بيانات موظف"""
        try:
            self.cursor.execute("""
            UPDATE employees SET
                full_name = ?,
                education_degree = ?,
                job_category = ?,
                job_title = ?,
                job_grade = ?,
                job_stage = ?,
                entitlement_indicator = ?,
                last_entitlement_date = ?,
                photo_path = ?,
                notes = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """, (
                employee_data['full_name'],
                employee_data['education_degree'],
                employee_data['job_category'],
                employee_data['job_title'],
                employee_data['job_grade'],
                employee_data['job_stage'],
                employee_data['entitlement_indicator'],
                employee_data['last_entitlement_date'],
                employee_data.get('photo_path'),
                employee_data.get('notes'),
                employee_id
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"خطأ في تحديث الموظف: {e}")
            return False
    
    def delete_employee(self, employee_id: int) -> bool:
        """حذف موظف"""
        try:
            self.cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"خطأ في حذف الموظف: {e}")
            return False
    
    def get_employee(self, employee_id: int) -> Optional[Dict]:
        """جلب بيانات موظف محدد"""
        self.cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
        row = self.cursor.fetchone()
        if row:
            return dict(row)
        return None
    
    def get_all_employees(self, category: Optional[str] = None, 
                         search_term: Optional[str] = None) -> List[Dict]:
        """جلب قائمة بجميع الموظفين مع خيار الفلترة"""
        query = "SELECT * FROM employees WHERE 1=1"
        params = []
        
        if category:
            query += " AND job_category = ?"
            params.append(category)
        
        if search_term:
            query += " AND (full_name LIKE ? OR job_title LIKE ?)"
            params.extend([f"%{search_term}%", f"%{search_term}%"])
        
        query += " ORDER BY full_name"
        
        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ========== عمليات الأحداث المهنية ==========
    
    def add_professional_event(self, event_data: Dict) -> int:
        """إضافة حدث مهني"""
        self.cursor.execute("""
        INSERT INTO professional_events (
            employee_id, event_type, event_number, event_date,
            effect_months, is_freeze, start_date, end_date,
            description, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event_data['employee_id'],
            event_data['event_type'],
            event_data['event_number'],
            event_data['event_date'],
            event_data.get('effect_months', 0),
            event_data.get('is_freeze', 0),
            event_data.get('start_date'),
            event_data.get('end_date'),
            event_data.get('description'),
            event_data.get('notes')
        ))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_employee_events(self, employee_id: int, 
                           event_type: Optional[str] = None) -> List[Dict]:
        """جلب الأحداث المهنية لموظف محدد"""
        query = "SELECT * FROM professional_events WHERE employee_id = ?"
        params = [employee_id]
        
        if event_type:
            query += " AND event_type = ?"
            params.append(event_type)
        
        query += " ORDER BY event_date DESC"
        
        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def cancel_event(self, event_id: int, cancelled_by_event_id: int) -> bool:
        """إلغاء حدث مهني"""
        try:
            self.cursor.execute("""
            UPDATE professional_events 
            SET is_cancelled = 1, cancelled_by_event_id = ?
            WHERE id = ?
            """, (cancelled_by_event_id, event_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"خطأ في إلغاء الحدث: {e}")
            return False
    
    # ========== عمليات السجل الوظيفي ==========
    
    def add_career_record(self, record_data: Dict) -> int:
        """إضافة سجل في المسار الوظيفي"""
        self.cursor.execute("""
        INSERT INTO career_history (
            employee_id, event_type, old_grade, old_stage, old_salary,
            new_grade, new_stage, new_salary, entitlement_date, related_events
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record_data['employee_id'],
            record_data['event_type'],
            record_data['old_grade'],
            record_data['old_stage'],
            record_data['old_salary'],
            record_data['new_grade'],
            record_data['new_stage'],
            record_data['new_salary'],
            record_data['entitlement_date'],
            record_data.get('related_events', '')
        ))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_career_history(self, employee_id: int) -> List[Dict]:
        """جلب السجل الوظيفي لموظف"""
        self.cursor.execute("""
        SELECT * FROM career_history 
        WHERE employee_id = ?
        ORDER BY entitlement_date DESC
        """, (employee_id,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ========== عمليات سلم الرواتب ==========
    
    def get_salary_info(self, grade: int, stage: int) -> Optional[Dict]:
        """جلب معلومات الراتب لدرجة ومرحلة محددة"""
        self.cursor.execute("""
        SELECT * FROM salary_scale 
        WHERE grade = ? AND stage = ?
        """, (grade, stage))
        row = self.cursor.fetchone()
        if row:
            return dict(row)
        return None
    
    def get_grade_info(self, grade: int) -> Dict:
        """جلب معلومات كاملة عن درجة وظيفية"""
        self.cursor.execute("""
        SELECT * FROM salary_scale 
        WHERE grade = ?
        ORDER BY stage
        """, (grade,))
        stages = [dict(row) for row in self.cursor.fetchall()]
        
        if stages:
            return {
                'grade': grade,
                'stages': stages,
                'years_for_promotion': stages[0]['years_for_promotion'],
                'allowance_amount': stages[0]['allowance_amount']
            }
        return {}
    
    # ========== الإحصائيات ==========
    
    def get_statistics(self) -> Dict:
        """جلب إحصائيات شاملة"""
        stats = {}
        
        # إجمالي الموظفين
        self.cursor.execute("SELECT COUNT(*) as total FROM employees")
        stats['total_employees'] = self.cursor.fetchone()['total']
        
        # حسب الصنف الوظيفي
        self.cursor.execute("""
        SELECT job_category, COUNT(*) as count 
        FROM employees 
        GROUP BY job_category
        """)
        stats['by_category'] = {row['job_category']: row['count'] 
                               for row in self.cursor.fetchall()}
        
        # حسب المؤهل العلمي
        self.cursor.execute("""
        SELECT education_degree, COUNT(*) as count 
        FROM employees 
        GROUP BY education_degree
        """)
        stats['by_education'] = {row['education_degree']: row['count'] 
                                for row in self.cursor.fetchall()}
        
        # حسب الحالة
        self.cursor.execute("""
        SELECT status, COUNT(*) as count 
        FROM employees 
        GROUP BY status
        """)
        stats['by_status'] = {row['status']: row['count'] 
                             for row in self.cursor.fetchall()}
        
        # حسب الدرجة الوظيفية
        self.cursor.execute("""
        SELECT job_grade, COUNT(*) as count 
        FROM employees 
        GROUP BY job_grade
        ORDER BY job_grade
        """)
        stats['by_grade'] = {row['job_grade']: row['count'] 
                            for row in self.cursor.fetchall()}
        
        return stats
    
    # ========== دوال مساعدة ==========
    
    def close(self):
        """إغلاق الاتصال بقاعدة البيانات"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """دعم استخدام with statement"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """إغلاق تلقائي عند استخدام with statement"""
        self.close()


if __name__ == "__main__":
    # اختبار قاعدة البيانات
    db = Database()
    print("✅ تم إنشاء قاعدة البيانات بنجاح!")
    
    # اختبار إضافة موظف
    test_employee = {
        'full_name': 'أحمد محمد علي حسن',
        'start_date': '2020-01-15',
        'last_entitlement_date': '2020-01-15',
        'education_degree': 'بكالوريوس',
        'job_category': 'إداري',
        'job_title': 'مدير إداري',
        'job_grade': 7,
        'job_stage': 1,
        'entitlement_indicator': '1/4'
    }
    
    emp_id = db.add_employee(test_employee)
    print(f"✅ تم إضافة موظف تجريبي برقم: {emp_id}")
    
    # عرض الإحصائيات
    stats = db.get_statistics()
    print(f"\n📊 الإحصائيات:")
    print(f"إجمالي الموظفين: {stats['total_employees']}")
    
    db.close()

