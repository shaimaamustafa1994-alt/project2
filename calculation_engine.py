# -*- coding: utf-8 -*-
"""
محرك الحسابات الذكي
Intelligent Calculation Engine
"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Dict, List, Tuple, Optional
import calendar


class CalculationEngine:
    """محرك حسابات العلاوات والترفيعات الذكي"""
    
    def __init__(self, database):
        """
        تهيئة محرك الحسابات
        
        Args:
            database: كائن قاعدة البيانات
        """
        self.db = database
    
    def calculate_next_entitlement(self, employee_id: int) -> Dict:
        """
        حساب الاستحقاق القادم للموظف
        
        Returns:
            Dict: معلومات الاستحقاق القادم
            {
                'type': 'علاوة' أو 'ترفيع',
                'date': تاريخ الاستحقاق,
                'current_grade': الدرجة الحالية,
                'current_stage': المرحلة الحالية,
                'current_salary': الراتب الحالي,
                'next_grade': الدرجة القادمة,
                'next_stage': المرحلة القادمة,
                'next_salary': الراتب القادم,
                'effective_service': الخدمة الفعلية
            }
        """
        # جلب بيانات الموظف
        employee = self.db.get_employee(employee_id)
        if not employee:
            return None
        
        # الخطوة 1: تحديد نقطة الانطلاق
        last_entitlement_date = datetime.strptime(
            employee['last_entitlement_date'], '%Y-%m-%d'
        ).date()
        
        # الخطوة 2: حساب المدة المعدلة بناءً على الأحداث المهنية
        base_months = 12  # المدة الأساسية
        adjusted_months = self._calculate_adjusted_period(
            employee_id, last_entitlement_date, base_months
        )
        
        # الخطوة 3: حساب تاريخ الاستحقاق القادم
        next_entitlement_date = self._add_months_precise(
            last_entitlement_date, adjusted_months
        )
        
        # الخطوة 4: تحديد نوع الاستحقاق والتغييرات
        entitlement_info = self._determine_entitlement_type(employee)
        
        # جلب معلومات الرواتب
        current_salary_info = self.db.get_salary_info(
            employee['job_grade'], employee['job_stage']
        )
        next_salary_info = self.db.get_salary_info(
            entitlement_info['new_grade'], entitlement_info['new_stage']
        )
        
        # حساب الخدمة الفعلية
        effective_service = self._calculate_effective_service(employee_id)
        
        return {
            'type': entitlement_info['type'],
            'date': next_entitlement_date,
            'current_grade': employee['job_grade'],
            'current_stage': employee['job_stage'],
            'current_salary': current_salary_info['salary'] if current_salary_info else 0,
            'next_grade': entitlement_info['new_grade'],
            'next_stage': entitlement_info['new_stage'],
            'next_salary': next_salary_info['salary'] if next_salary_info else 0,
            'effective_service': effective_service,
            'new_indicator': entitlement_info['new_indicator']
        }
    
    def _calculate_adjusted_period(self, employee_id: int, 
                                   last_entitlement_date, 
                                   base_months: int) -> float:
        """
        حساب المدة المعدلة بناءً على الأحداث المهنية
        
        Args:
            employee_id: معرف الموظف
            last_entitlement_date: تاريخ آخر استحقاق
            base_months: المدة الأساسية (12 شهر)
        
        Returns:
            float: المدة المعدلة بالأشهر
        """
        # جلب جميع الأحداث المهنية بعد آخر استحقاق
        events = self.db.get_employee_events(employee_id)
        
        total_adjustment = 0  # التعديل الإجمالي
        freeze_days = 0  # أيام التجميد
        
        for event in events:
            event_date = datetime.strptime(event['event_date'], '%Y-%m-%d').date()
            
            # تجاهل الأحداث قبل آخر استحقاق
            if event_date < last_entitlement_date:
                continue
            
            # تجاهل الأحداث الملغاة
            if event['is_cancelled']:
                continue
            
            # معالجة أحداث التجميد
            if event['is_freeze'] and event['start_date'] and event['end_date']:
                start = datetime.strptime(event['start_date'], '%Y-%m-%d').date()
                end = datetime.strptime(event['end_date'], '%Y-%m-%d').date()
                freeze_days += (end - start).days
            else:
                # إضافة/طرح الشهور
                total_adjustment += event['effect_months']
        
        # تحويل أيام التجميد إلى أشهر
        freeze_months = freeze_days / 30.0
        
        # المدة النهائية
        adjusted_months = base_months + total_adjustment + freeze_months
        
        # التأكد من أن المدة لا تقل عن صفر
        return max(0, adjusted_months)
    
    def _add_months_precise(self, start_date, months: float) -> datetime.date:
        """
        إضافة أشهر بدقة مع مراعاة أطوال الأشهر المختلفة
        
        Args:
            start_date: تاريخ البداية
            months: عدد الأشهر (يمكن أن يكون كسرياً)
        
        Returns:
            datetime.date: التاريخ الجديد
        """
        # فصل الأشهر الصحيحة عن الأيام
        whole_months = int(months)
        remaining_days = (months - whole_months) * 30
        
        # إضافة الأشهر الصحيحة
        new_date = start_date + relativedelta(months=whole_months)
        
        # إضافة الأيام المتبقية
        new_date = new_date + timedelta(days=int(remaining_days))
        
        return new_date
    
    def _determine_entitlement_type(self, employee: Dict) -> Dict:
        """
        تحديد نوع الاستحقاق القادم (علاوة أو ترفيع)
        
        Args:
            employee: بيانات الموظف
        
        Returns:
            Dict: معلومات الاستحقاق
        """
        current_grade = employee['job_grade']
        current_stage = employee['job_stage']
        indicator = employee['entitlement_indicator']
        
        # تحليل المؤشر (مثال: "3/4" -> current=3, total=4)
        if '/' in indicator:
            current_pos, total_pos = map(int, indicator.split('/'))
        else:
            current_pos = total_pos = 1
        
        # حالة خاصة: الدرجة الأولى (لا يوجد ترفيع)
        if current_grade == 1:
            if current_stage < 11:
                return {
                    'type': 'علاوة',
                    'new_grade': 1,
                    'new_stage': current_stage + 1,
                    'new_indicator': f"{current_pos + 1}/11"
                }
            else:
                # وصل إلى سقف الدرجة
                return {
                    'type': 'لا يوجد',
                    'new_grade': 1,
                    'new_stage': 11,
                    'new_indicator': "11/11"
                }
        
        # حالة خاصة: الدبلوم في الدرجة الثامنة المرحلة الخامسة
        if (employee['education_degree'] == 'دبلوم' and 
            current_grade == 8 and current_stage == 5 and 
            indicator == "1/1"):
            return {
                'type': 'ترفيع',
                'new_grade': 7,
                'new_stage': 1,
                'new_indicator': "1/4"
            }
        
        # تحديد إذا كان الاستحقاق القادم ترفيع
        is_promotion_due = (current_pos == total_pos)
        
        if is_promotion_due:
            # ترفيع للدرجة الأعلى
            new_grade = current_grade - 1
            new_stage = 1
            
            # تحديد المؤشر الجديد بناءً على الدرجة الجديدة
            grade_info = self.db.get_grade_info(new_grade)
            years_for_promotion = grade_info.get('years_for_promotion', 4)
            
            if new_grade == 1:
                new_indicator = "1/11"
            elif years_for_promotion == 5:
                new_indicator = "1/5"
            else:
                new_indicator = "1/4"
            
            return {
                'type': 'ترفيع',
                'new_grade': new_grade,
                'new_stage': new_stage,
                'new_indicator': new_indicator
            }
        else:
            # علاوة (الانتقال للمرحلة التالية)
            return {
                'type': 'علاوة',
                'new_grade': current_grade,
                'new_stage': current_stage + 1,
                'new_indicator': f"{current_pos + 1}/{total_pos}"
            }
    
    def _calculate_effective_service(self, employee_id: int) -> Dict:
        """
        حساب الخدمة الفعلية للموظف
        
        Returns:
            Dict: {'years': سنوات, 'months': أشهر, 'days': أيام}
        """
        employee = self.db.get_employee(employee_id)
        if not employee:
            return {'years': 0, 'months': 0, 'days': 0}
        
        start_date = datetime.strptime(employee['start_date'], '%Y-%m-%d').date()
        current_date = datetime.now().date()
        
        # حساب الفترة الأساسية
        delta = relativedelta(current_date, start_date)
        
        # طرح فترات التجميد (الإجازات الطويلة)
        events = self.db.get_employee_events(employee_id)
        total_freeze_days = 0
        
        for event in events:
            if event['is_freeze'] and event['start_date'] and event['end_date']:
                start = datetime.strptime(event['start_date'], '%Y-%m-%d').date()
                end = datetime.strptime(event['end_date'], '%Y-%m-%d').date()
                total_freeze_days += (end - start).days
        
        # تحويل أيام التجميد وطرحها
        freeze_delta = relativedelta(days=total_freeze_days)
        adjusted_date = current_date - freeze_delta
        final_delta = relativedelta(adjusted_date, start_date)
        
        return {
            'years': final_delta.years,
            'months': final_delta.months,
            'days': final_delta.days
        }
    
    def process_entitlement(self, employee_id: int) -> bool:
        """
        معالجة استحقاق (تسجيله في السجل الوظيفي وتحديث بيانات الموظف)
        
        Args:
            employee_id: معرف الموظف
        
        Returns:
            bool: نجاح العملية
        """
        try:
            # حساب الاستحقاق
            entitlement = self.calculate_next_entitlement(employee_id)
            if not entitlement or entitlement['type'] == 'لا يوجد':
                return False
            
            employee = self.db.get_employee(employee_id)
            
            # جمع الأحداث المهنية ذات الصلة
            events = self.db.get_employee_events(employee_id)
            related_events = []
            
            last_entitlement = datetime.strptime(
                employee['last_entitlement_date'], '%Y-%m-%d'
            ).date()
            
            for event in events:
                event_date = datetime.strptime(event['event_date'], '%Y-%m-%d').date()
                if event_date >= last_entitlement and not event['is_cancelled']:
                    related_events.append({
                        'number': event['event_number'],
                        'date': event['event_date'],
                        'type': event['event_type']
                    })
            
            # تسجيل في السجل الوظيفي
            career_record = {
                'employee_id': employee_id,
                'event_type': entitlement['type'],
                'old_grade': entitlement['current_grade'],
                'old_stage': entitlement['current_stage'],
                'old_salary': entitlement['current_salary'],
                'new_grade': entitlement['next_grade'],
                'new_stage': entitlement['next_stage'],
                'new_salary': entitlement['next_salary'],
                'entitlement_date': entitlement['date'].strftime('%Y-%m-%d'),
                'related_events': str(related_events)
            }
            
            self.db.add_career_record(career_record)
            
            # تحديث بيانات الموظف
            updated_employee = {
                'full_name': employee['full_name'],
                'education_degree': employee['education_degree'],
                'job_category': employee['job_category'],
                'job_title': employee['job_title'],
                'job_grade': entitlement['next_grade'],
                'job_stage': entitlement['next_stage'],
                'entitlement_indicator': entitlement['new_indicator'],
                'last_entitlement_date': entitlement['date'].strftime('%Y-%m-%d'),
                'photo_path': employee.get('photo_path'),
                'notes': employee.get('notes')
            }
            
            self.db.update_employee(employee_id, updated_employee)
            
            return True
            
        except Exception as e:
            print(f"خطأ في معالجة الاستحقاق: {e}")
            return False
    
    def check_penalty_cancellation(self, employee_id: int, 
                                  new_commendation_event_id: int) -> bool:
        """
        التحقق من إمكانية إلغاء عقوبة باستخدام كتب شكر
        
        Args:
            employee_id: معرف الموظف
            new_commendation_event_id: معرف كتاب الشكر الجديد
        
        Returns:
            bool: تم الإلغاء أم لا
        """
        # جلب الحدث الجديد
        new_event = None
        events = self.db.get_employee_events(employee_id)
        
        for event in events:
            if event['id'] == new_commendation_event_id:
                new_event = event
                break
        
        if not new_event or new_event['event_type'] != 'كتاب شكر':
            return False
        
        new_event_date = datetime.strptime(new_event['event_date'], '%Y-%m-%d').date()
        new_event_year = new_event_date.year
        
        # البحث عن عقوبات نشطة في نفس السنة
        penalties = [e for e in events if 
                    e['event_type'] in ['لفت نظر', 'إنذار', 'توبيخ'] and
                    not e['is_cancelled']]
        
        for penalty in penalties:
            penalty_date = datetime.strptime(penalty['event_date'], '%Y-%m-%d').date()
            
            # التحقق من نفس السنة والأسبقية الزمنية
            if penalty_date.year != new_event_year or penalty_date >= new_event_date:
                continue
            
            # حساب عدد كتب الشكر بعد العقوبة
            commendations_after = [e for e in events if
                                  e['event_type'] == 'كتاب شكر' and
                                  not e['is_cancelled'] and
                                  datetime.strptime(e['event_date'], '%Y-%m-%d').date() > penalty_date and
                                  datetime.strptime(e['event_date'], '%Y-%m-%d').date().year == new_event_year]
            
            required_count = {'لفت نظر': 1, 'إنذار': 2, 'توبيخ': 3}
            needed = required_count.get(penalty['event_type'], 0)
            
            if len(commendations_after) >= needed:
                # إلغاء العقوبة
                self.db.cancel_event(penalty['id'], new_commendation_event_id)
                return True
        
        return False
    
    def get_upcoming_entitlements(self, days: int = 30) -> List[Dict]:
        """
        جلب قائمة بالاستحقاقات القادمة خلال فترة محددة
        
        Args:
            days: عدد الأيام (7 للأسبوع، 30 للشهر)
        
        Returns:
            List[Dict]: قائمة الموظفين المستحقين
        """
        all_employees = self.db.get_all_employees()
        upcoming = []
        
        target_date = datetime.now().date() + timedelta(days=days)
        
        for employee in all_employees:
            entitlement = self.calculate_next_entitlement(employee['id'])
            
            if entitlement and entitlement['type'] != 'لا يوجد':
                if entitlement['date'] <= target_date:
                    upcoming.append({
                        'employee': employee,
                        'entitlement': entitlement
                    })
        
        # ترتيب حسب التاريخ
        upcoming.sort(key=lambda x: x['entitlement']['date'])
        
        return upcoming


if __name__ == "__main__":
    # اختبار المحرك
    from database import Database
    
    db = Database()
    engine = CalculationEngine(db)
    
    print("✅ محرك الحسابات جاهز للعمل!")
    
    # اختبار حساب الاستحقاق
    employees = db.get_all_employees()
    if employees:
        emp_id = employees[0]['id']
        result = engine.calculate_next_entitlement(emp_id)
        
        if result:
            print(f"\n📊 الاستحقاق القادم:")
            print(f"النوع: {result['type']}")
            print(f"التاريخ: {result['date']}")
            print(f"من الدرجة {result['current_grade']}/المرحلة {result['current_stage']}")
            print(f"إلى الدرجة {result['next_grade']}/المرحلة {result['next_stage']}")
    
    db.close()

