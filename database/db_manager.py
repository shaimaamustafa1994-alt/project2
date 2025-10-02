"""
مدير قاعدة البيانات
Database Manager
"""

import sqlite3
import os
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    """مدير قاعدة البيانات المحلية"""
    
    def __init__(self, db_path: str = "employee_management.db"):
        """تهيئة قاعدة البيانات"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect()
    
    def _connect(self):
        """الاتصال بقاعدة البيانات"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.conn.row_factory = sqlite3.Row
    
    def create_tables(self):
        """إنشاء جداول قاعدة البيانات"""
        
        # جدول الموظفين
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                job_category TEXT NOT NULL,
                job_title TEXT NOT NULL,
                degree INTEGER NOT NULL,
                stage INTEGER NOT NULL,
                academic_qualification TEXT NOT NULL,
                start_date DATE NOT NULL,
                last_entitlement_date DATE NOT NULL,
                tracking_indicator TEXT NOT NULL,
                photo_path TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الأحداث المهنية
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS professional_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                document_number TEXT,
                document_date DATE,
                event_date DATE NOT NULL,
                impact_months INTEGER DEFAULT 0,
                start_date DATE,
                end_date DATE,
                new_qualification TEXT,
                new_job_title TEXT,
                new_job_category TEXT,
                notes TEXT,
                is_cancelled BOOLEAN DEFAULT 0,
                cancelled_by_event_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
                FOREIGN KEY (cancelled_by_event_id) REFERENCES professional_events(id)
            )
        ''')
        
        # جدول تاريخ العلاوات والترفيعات
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS entitlement_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                entitlement_type TEXT NOT NULL,
                previous_degree INTEGER,
                previous_stage INTEGER,
                new_degree INTEGER NOT NULL,
                new_stage INTEGER NOT NULL,
                previous_salary REAL,
                new_salary REAL NOT NULL,
                entitlement_date DATE NOT NULL,
                related_events TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
            )
        ''')
        
        # جدول سلم الرواتب
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS salary_scale (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                degree INTEGER NOT NULL,
                stage INTEGER NOT NULL,
                salary REAL NOT NULL,
                allowance_amount REAL NOT NULL,
                years_for_promotion INTEGER NOT NULL,
                UNIQUE(degree, stage)
            )
        ''')
        
        self.conn.commit()
        
        # إدخال بيانات سلم الرواتب إذا كانت الجدول فارغاً
        self._initialize_salary_scale()
    
    def _initialize_salary_scale(self):
        """تهيئة سلم الرواتب"""
        
        # التحقق من وجود بيانات
        self.cursor.execute("SELECT COUNT(*) FROM salary_scale")
        if self.cursor.fetchone()[0] > 0:
            return
        
        # بيانات سلم الرواتب
        salary_data = [
            # الدرجة الأولى
            (1, 1, 910, 20, 0), (1, 2, 930, 20, 0), (1, 3, 950, 20, 0),
            (1, 4, 970, 20, 0), (1, 5, 990, 20, 0), (1, 6, 1010, 20, 0),
            (1, 7, 1030, 20, 0), (1, 8, 1050, 20, 0), (1, 9, 1070, 20, 0),
            (1, 10, 1090, 20, 0), (1, 11, 1110, 20, 0),
            
            # الدرجة الثانية
            (2, 1, 723, 17, 5), (2, 2, 740, 17, 5), (2, 3, 757, 17, 5),
            (2, 4, 774, 17, 5), (2, 5, 791, 17, 5), (2, 6, 808, 17, 5),
            (2, 7, 825, 17, 5), (2, 8, 842, 17, 5), (2, 9, 859, 17, 5),
            (2, 10, 876, 17, 5), (2, 11, 893, 17, 5),
            
            # الدرجة الثالثة
            (3, 1, 600, 10, 5), (3, 2, 610, 10, 5), (3, 3, 620, 10, 5),
            (3, 4, 630, 10, 5), (3, 5, 640, 10, 5), (3, 6, 650, 10, 5),
            (3, 7, 660, 10, 5), (3, 8, 670, 10, 5), (3, 9, 680, 10, 5),
            (3, 10, 690, 10, 5), (3, 11, 700, 10, 5),
            
            # الدرجة الرابعة
            (4, 1, 509, 8, 5), (4, 2, 517, 8, 5), (4, 3, 525, 8, 5),
            (4, 4, 533, 8, 5), (4, 5, 541, 8, 5), (4, 6, 549, 8, 5),
            (4, 7, 557, 8, 5), (4, 8, 565, 8, 5), (4, 9, 573, 8, 5),
            (4, 10, 581, 8, 5), (4, 11, 589, 8, 5),
            
            # الدرجة الخامسة
            (5, 1, 429, 6, 5), (5, 2, 435, 6, 5), (5, 3, 441, 6, 5),
            (5, 4, 447, 6, 5), (5, 5, 453, 6, 5), (5, 6, 459, 6, 5),
            (5, 7, 465, 6, 5), (5, 8, 471, 6, 5), (5, 9, 477, 6, 5),
            (5, 10, 483, 6, 5), (5, 11, 489, 6, 5),
            
            # الدرجة السادسة
            (6, 1, 362, 6, 4), (6, 2, 368, 6, 4), (6, 3, 374, 6, 4),
            (6, 4, 380, 6, 4), (6, 5, 386, 6, 4), (6, 6, 392, 6, 4),
            (6, 7, 398, 6, 4), (6, 8, 404, 6, 4), (6, 9, 410, 6, 4),
            (6, 10, 416, 6, 4), (6, 11, 422, 6, 4),
            
            # الدرجة السابعة
            (7, 1, 296, 6, 4), (7, 2, 302, 6, 4), (7, 3, 308, 6, 4),
            (7, 4, 314, 6, 4), (7, 5, 320, 6, 4), (7, 6, 326, 6, 4),
            (7, 7, 332, 6, 4), (7, 8, 338, 6, 4), (7, 9, 344, 6, 4),
            (7, 10, 350, 6, 4), (7, 11, 356, 6, 4),
            
            # الدرجة الثامنة
            (8, 1, 260, 3, 4), (8, 2, 263, 3, 4), (8, 3, 266, 3, 4),
            (8, 4, 269, 3, 4), (8, 5, 272, 3, 4), (8, 6, 275, 3, 4),
            (8, 7, 278, 3, 4), (8, 8, 281, 3, 4), (8, 9, 284, 3, 4),
            (8, 10, 287, 3, 4), (8, 11, 290, 3, 4),
            
            # الدرجة التاسعة
            (9, 1, 210, 3, 4), (9, 2, 213, 3, 4), (9, 3, 216, 3, 4),
            (9, 4, 219, 3, 4), (9, 5, 222, 3, 4), (9, 6, 225, 3, 4),
            (9, 7, 228, 3, 4), (9, 8, 231, 3, 4), (9, 9, 234, 3, 4),
            (9, 10, 237, 3, 4), (9, 11, 240, 3, 4),
            
            # الدرجة العاشرة
            (10, 1, 170, 3, 4), (10, 2, 173, 3, 4), (10, 3, 176, 3, 4),
            (10, 4, 179, 3, 4), (10, 5, 182, 3, 4), (10, 6, 185, 3, 4),
            (10, 7, 188, 3, 4), (10, 8, 191, 3, 4), (10, 9, 194, 3, 4),
            (10, 10, 197, 3, 4), (10, 11, 200, 3, 4),
        ]
        
        self.cursor.executemany('''
            INSERT INTO salary_scale (degree, stage, salary, allowance_amount, years_for_promotion)
            VALUES (?, ?, ?, ?, ?)
        ''', salary_data)
        
        self.conn.commit()
    
    def get_salary(self, degree: int, stage: int) -> Optional[float]:
        """الحصول على الراتب حسب الدرجة والمرحلة"""
        self.cursor.execute('''
            SELECT salary FROM salary_scale 
            WHERE degree = ? AND stage = ?
        ''', (degree, stage))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_salary_info(self, degree: int, stage: int) -> Optional[Dict]:
        """الحصول على معلومات الراتب الكاملة"""
        self.cursor.execute('''
            SELECT * FROM salary_scale 
            WHERE degree = ? AND stage = ?
        ''', (degree, stage))
        row = self.cursor.fetchone()
        if row:
            return dict(row)
        return None
    
    def add_employee(self, employee_data: Dict) -> int:
        """إضافة موظف جديد"""
        self.cursor.execute('''
            INSERT INTO employees (
                full_name, job_category, job_title, degree, stage,
                academic_qualification, start_date, last_entitlement_date,
                tracking_indicator, photo_path, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            employee_data['full_name'],
            employee_data['job_category'],
            employee_data['job_title'],
            employee_data['degree'],
            employee_data['stage'],
            employee_data['academic_qualification'],
            employee_data['start_date'],
            employee_data['last_entitlement_date'],
            employee_data['tracking_indicator'],
            employee_data.get('photo_path'),
            employee_data.get('notes')
        ))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_employee(self, employee_id: int) -> Optional[Dict]:
        """الحصول على بيانات موظف"""
        self.cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
        row = self.cursor.fetchone()
        if row:
            return dict(row)
        return None
    
    def get_all_employees(self, job_category: Optional[str] = None) -> List[Dict]:
        """الحصول على قائمة جميع الموظفين"""
        if job_category:
            self.cursor.execute('''
                SELECT * FROM employees 
                WHERE job_category = ?
                ORDER BY full_name
            ''', (job_category,))
        else:
            self.cursor.execute('SELECT * FROM employees ORDER BY full_name')
        
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def update_employee(self, employee_id: int, employee_data: Dict):
        """تحديث بيانات موظف"""
        fields = []
        values = []
        
        for key, value in employee_data.items():
            if key != 'id':
                fields.append(f"{key} = ?")
                values.append(value)
        
        values.append(datetime.now())
        fields.append("updated_at = ?")
        values.append(employee_id)
        
        query = f"UPDATE employees SET {', '.join(fields)} WHERE id = ?"
        self.cursor.execute(query, values)
        self.conn.commit()
    
    def delete_employee(self, employee_id: int):
        """حذف موظف"""
        self.cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
        self.conn.commit()
    
    def add_professional_event(self, event_data: Dict) -> int:
        """إضافة حدث مهني"""
        self.cursor.execute('''
            INSERT INTO professional_events (
                employee_id, event_type, document_number, document_date,
                event_date, impact_months, start_date, end_date,
                new_qualification, new_job_title, new_job_category, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event_data['employee_id'],
            event_data['event_type'],
            event_data.get('document_number'),
            event_data.get('document_date'),
            event_data['event_date'],
            event_data.get('impact_months', 0),
            event_data.get('start_date'),
            event_data.get('end_date'),
            event_data.get('new_qualification'),
            event_data.get('new_job_title'),
            event_data.get('new_job_category'),
            event_data.get('notes')
        ))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_employee_events(self, employee_id: int) -> List[Dict]:
        """الحصول على أحداث موظف"""
        self.cursor.execute('''
            SELECT * FROM professional_events 
            WHERE employee_id = ? 
            ORDER BY event_date DESC
        ''', (employee_id,))
        
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def add_entitlement_record(self, record_data: Dict) -> int:
        """إضافة سجل استحقاق"""
        self.cursor.execute('''
            INSERT INTO entitlement_history (
                employee_id, entitlement_type, previous_degree, previous_stage,
                new_degree, new_stage, previous_salary, new_salary,
                entitlement_date, related_events
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record_data['employee_id'],
            record_data['entitlement_type'],
            record_data.get('previous_degree'),
            record_data.get('previous_stage'),
            record_data['new_degree'],
            record_data['new_stage'],
            record_data.get('previous_salary'),
            record_data['new_salary'],
            record_data['entitlement_date'],
            record_data.get('related_events')
        ))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_employee_entitlement_history(self, employee_id: int) -> List[Dict]:
        """الحصول على سجل استحقاقات الموظف"""
        self.cursor.execute('''
            SELECT * FROM entitlement_history 
            WHERE employee_id = ? 
            ORDER BY entitlement_date DESC
        ''', (employee_id,))
        
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_statistics(self) -> Dict:
        """الحصول على الإحصائيات العامة"""
        stats = {}
        
        # إجمالي عدد الموظفين
        self.cursor.execute("SELECT COUNT(*) FROM employees")
        stats['total_employees'] = self.cursor.fetchone()[0]
        
        # حسب الصنف الوظيفي
        self.cursor.execute('''
            SELECT job_category, COUNT(*) as count 
            FROM employees 
            GROUP BY job_category
        ''')
        stats['by_category'] = {row[0]: row[1] for row in self.cursor.fetchall()}
        
        # حسب المؤهل العلمي
        self.cursor.execute('''
            SELECT academic_qualification, COUNT(*) as count 
            FROM employees 
            GROUP BY academic_qualification
        ''')
        stats['by_qualification'] = {row[0]: row[1] for row in self.cursor.fetchall()}
        
        # حسب الدرجة الوظيفية
        self.cursor.execute('''
            SELECT degree, COUNT(*) as count 
            FROM employees 
            GROUP BY degree 
            ORDER BY degree
        ''')
        stats['by_degree'] = {row[0]: row[1] for row in self.cursor.fetchall()}
        
        return stats
    
    def close(self):
        """إغلاق الاتصال بقاعدة البيانات"""
        if self.conn:
            self.conn.close()

