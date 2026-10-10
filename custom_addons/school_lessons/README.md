# School Lessons Portal — دليل التركيب

## ⚠️ لازم تظبط دول الأول قبل التثبيت

الموديول مبني على افتراض إن عندك الموديلات دي في موديول تسجيل الطلاب بتاعك:

| الموديل      | الحقول المفترضة                          |
|--------------|-------------------------------------------|
| `school.class`   | `name`, و One2many اسمه `student_ids` بيربط بـ `school.student` |
| `school.student` | `partner_id` (Many2one لـ res.partner), `class_id` (Many2one لـ school.class) |
| `school.subject` | `name` (اختياري - لو مش موجود عندك امسح الحقل `subject_id` من كل الملفات) |

**لو أسماء الموديلات أو الحقول عندك مختلفة**، دور على النقط دي وعدّلها:

1. `models/school_lesson.py` → `class_id`, `_notify_students()`, `_portal_student_has_access()`, `_log_student_view()`
2. `security/security.xml` → قاعدة `rule_lesson_portal_own_class` (فيها `class_id.student_ids.partner_id`)
3. `models/school_lesson.py` → `_compute_view_count()`

كمان في `__manifest__.py`، فعّل سطر الـ `depends` بتاع موديول تسجيل الطلاب بتاعك عشان الترتيب يتضمن إنه يتحمّل الأول:
```python
'depends': ['base', 'mail', 'portal', 'website', 'اسم_موديولك_هنا'],
```

## التركيب

```bash
cp -r school_lessons /path/to/your/odoo/addons/
```
بعدين من الواجهة: Apps → Update Apps List → دور على "School Lessons Portal" → Install.

## إعطاء صلاحية "أستاذ" لمستخدم

Settings → Users → افتح المستخدم → تبويب "Other" → حط جروب **أستاذ (رفع الحصص)**
(الجروب موجود تحت فئة Education).

## إزاي يستخدمها الأستاذ

1. من القائمة الجديدة "الحصص الدراسية" → إنشاء حصة جديدة
2. يختار الفصل والمادة ونوع المحتوى
3. يرفع الملفات (PDF أو فيديو) من تبويب "الملفات"، أو يحط رابط يوتيوب/فيميو
4. يضغط "نشر الحصة" → الطلاب المسجلين في الفصل يوصلهم إشعار فورًا

## إزاي يشوفها الطالب

من بوابة البورتال (`/my`) → "حصصي الدراسية"، أو مباشرة `/my/lessons`

## نقاط أمان مهمة (اتعملت بالفعل)

- الملفات مش عامة أبدًا — أي تحميل بيعدّي على `_portal_student_has_access()` اللي بيتأكد
  إن الطالب فعلاً في نفس فصل الحصة وإن الحصة منشورة، قبل ما يدي أي بايت من الملف.
- استخدمنا `ir.attachment` عن طريق Many2many (widget `many2many_binary`) بدل تخزين
  الملفات كـ Binary في الموديل نفسه — ده بيخلي الأداء أحسن وبيستخدم الـ filestore
  بدل ما يضخم الداتابيز.
- فيه Record Rules على مستوى الموديل كطبقة حماية إضافية غير الكنترولر.

## تحسينات ممكن تضيفها بعدين (لو حبيت)

- حد أقصى لحجم الملف المرفوع (validation على `attachment_ids` بالـ `file_size`)
- تحويل الفيديوهات الكبيرة تلقائيًا لصيغة مضغوطة (يحتاج سيرفر خارجي/queue job)
- واجب/تسليم مرتبط بكل حصة (نموذج `school.assignment` جديد)
- تقييم الطلاب للحصة (نجوم / تعليقات)
