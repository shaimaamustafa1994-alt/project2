"""
محرك الحسابات الذكي
Intelligent Calculation Engine
"""

from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from typing import Dict, List, Optional, Tuple
import json

class CalculationEngine:
    """محرك حساب العلاوات والترفيعات الذكي"""
    
    def __init__(self, db_manager):
        """تهيئة المحرك"""
        self.db = db_manager
    
    def calculate_next_entitlement(self, employee_id: int) -> Dict:
        """
        حساب الاستحقاق القادم للموظف
        
        Returns:
            Dict containing:
            - next_entitlement_date: تاريخ الاستحقاق القادم
            - entitlement_type: نوع الاستحقاق (علاوة/ترفيع)
            - new_degree: الدرجة الجديدة
            - new_stage: المرحلة الجديدة
            - new_salary: الراتب الجديد
            - new_indicator: المؤشر الجديد
        """
        
        # الحصول على بيانات الموظف
        employee = self.db.get_employee(employee_id)
        if not employee:
            return None
        
        # نقطة الارتكاز الزمنية
        last_entitlement_date = datetime.strptime(employee['last_entitlement_date'], '%Y-%m-%d').date()
        
        # المدة الأساسية (12 شهر)
        base_period_months = 12
        
        # حساب التأثير الصافي للأحداث المهنية
        events_impact = self._calculate_events_impact(employee_id, last_entitlement_date)
        
        # المدة النهائية
        total_months = base_period_months + events_impact
        
        # حساب تاريخ الاستحقاق القادم
        next_date = last_entitlement_date + relativedelta(months=total_months)
        
        # تحديد نوع الاستحقاق بناءً على المؤشر
        tracking_indicator = employee['tracking_indicator']
        current_degree = employee['degree']
        current_stage = employee['stage']
        
        entitlement_info = self._determine_entitlement_type(
            tracking_indicator, current_degree, current_stage
        )
        
        # الحصول على معلومات الراتب الجديد
        new_salary = self.db.get_salary(
            entitlement_info['new_degree'], 
            entitlement_info['new_stage']
        )
        
        return {
            'next_entitlement_date': next_date,
            'entitlement_type': entitlement_info['type'],
            'new_degree': entitlement_info['new_degree'],
            'new_stage': entitlement_info['new_stage'],
            'new_salary': new_salary,
            'new_indicator': entitlement_info['new_indicator'],
            'current_salary': self.db.get_salary(current_degree, current_stage)
        }
    
    def _calculate_events_impact(self, employee_id: int, since_date: date) -> int:
        """
        حساب التأثير الصافي للأحداث المهنية على المدة
        
        Returns:
            عدد الأشهر (موجب للتمديد، سالب للتقليص)
        """
        
        events = self.db.get_employee_events(employee_id)
        total_impact = 0
        
        for event in events:
            event_date = datetime.strptime(event['event_date'], '%Y-%m-%d').date()
            
            # نعتبر فقط الأحداث بعد آخر استحقاق
            if event_date <= since_date:
                continue
            
            # تجاهل الأحداث الملغاة
            if event['is_cancelled']:
                continue
            
            event_type = event['event_type']
            
            # كتب الشكر والشهادات (تقليص)
            if event_type in ['commendation', 'academic_degree']:
                total_impact -= event.get('impact_months', 0)
            
            # العقوبات (تمديد)
            elif event_type in ['notice_penalty', 'warning_penalty', 'reprimand_penalty']:
                total_impact += event.get('impact_months', 0)
            
            # الإجازات
            elif event_type in ['maternity_leave']:
                total_impact += event.get('impact_months', 0)
            
            # إجازات التجميد
            elif event_type in ['unpaid_leave', 'disability_care_leave', 'five_year_leave']:
                if event['start_date'] and event['end_date']:
                    start = datetime.strptime(event['start_date'], '%Y-%m-%d').date()
                    end = datetime.strptime(event['end_date'], '%Y-%m-%d').date()
                    freeze_days = (end - start).days
                    # تحويل الأيام إلى أشهر (تقريبي)
                    total_impact += int(freeze_days / 30)
            
            # حدث مخصص
            elif event_type == 'custom_event':
                total_impact += event.get('impact_months', 0)
        
        return total_impact
    
    def _determine_entitlement_type(self, tracking_indicator: str, 
                                    current_degree: int, 
                                    current_stage: int) -> Dict:
        """
        تحديد نوع الاستحقاق القادم بناءً على المؤشر
        
        Returns:
            Dict containing type, new_degree, new_stage, new_indicator
        """
        
        # تحليل المؤشر (مثال: "3/4" أو "4/5")
        parts = tracking_indicator.split('/')
        current_position = int(parts[0])
        total_steps = int(parts[1])
        
        # حالة خاصة: الدرجة الأولى (لا ترفيع بعدها)
        if current_degree == 1:
            if current_stage < 11:
                return {
                    'type': 'علاوة',
                    'new_degree': 1,
                    'new_stage': current_stage + 1,
                    'new_indicator': f"{current_position + 1}/11"
                }
            else:
                # وصل إلى السقف
                return {
                    'type': 'لا يوجد',
                    'new_degree': 1,
                    'new_stage': 11,
                    'new_indicator': "11/11"
                }
        
        # حالة الترفيع (وصل إلى نهاية المؤشر)
        if current_position >= total_steps:
            # الترفيع يعني الانتقال إلى درجة أعلى (رقم أقل)
            new_degree = current_degree - 1
            
            # تحديد المؤشر الجديد بناءً على الدرجة الجديدة
            if new_degree >= 6:  # درجات 10-6
                new_indicator = "1/4"
            elif new_degree >= 2:  # درجات 5-2
                new_indicator = "1/5"
            else:  # درجة 1
                new_indicator = "1/11"
            
            return {
                'type': 'ترفيع',
                'new_degree': new_degree,
                'new_stage': 1,
                'new_indicator': new_indicator
            }
        
        # حالة العلاوة (لم يصل لنهاية المؤشر)
        else:
            return {
                'type': 'علاوة',
                'new_degree': current_degree,
                'new_stage': current_stage + 1,
                'new_indicator': f"{current_position + 1}/{total_steps}"
            }
    
    def get_upcoming_entitlements(self, days_ahead: int = 30) -> List[Dict]:
        """
        الحصول على قائمة الاستحقاقات القادمة خلال فترة محددة
        
        Args:
            days_ahead: عدد الأيام للبحث عن الاستحقاقات القادمة
        
        Returns:
            قائمة الموظفين والاستحقاقات القادمة
        """
        
        employees = self.db.get_all_employees()
        upcoming = []
        
        target_date = date.today() + timedelta(days=days_ahead)
        
        for employee in employees:
            next_entitlement = self.calculate_next_entitlement(employee['id'])
            
            if next_entitlement and next_entitlement['next_entitlement_date'] <= target_date:
                upcoming.append({
                    'employee': employee,
                    'entitlement': next_entitlement
                })
        
        # الترتيب حسب التاريخ
        upcoming.sort(key=lambda x: x['entitlement']['next_entitlement_date'])
        
        return upcoming
    
    def calculate_actual_service(self, employee_id: int) -> Dict:
        """
        حساب الخدمة الفعلية للموظف
        
        (يعتمد على تاريخ المباشرة ويطرح فترات الإجازات الطويلة)
        """
        
        employee = self.db.get_employee(employee_id)
        if not employee:
            return None
        
        start_date = datetime.strptime(employee['start_date'], '%Y-%m-%d').date()
        today = date.today()
        
        # الفترة الإجمالية
        total_days = (today - start_date).days
        
        # طرح فترات الإجازات
        freeze_days = 0
        events = self.db.get_employee_events(employee_id)
        
        for event in events:
            if event['event_type'] in ['unpaid_leave', 'disability_care_leave', 'five_year_leave']:
                if event['start_date'] and event['end_date']:
                    start = datetime.strptime(event['start_date'], '%Y-%m-%d').date()
                    end = datetime.strptime(event['end_date'], '%Y-%m-%d').date()
                    freeze_days += (end - start).days
        
        # الخدمة الفعلية
        actual_days = total_days - freeze_days
        
        # تحويل إلى سنوات وشهور وأيام
        years = actual_days // 365
        remaining = actual_days % 365
        months = remaining // 30
        days = remaining % 30
        
        return {
            'years': years,
            'months': months,
            'days': days,
            'total_days': actual_days
        }

