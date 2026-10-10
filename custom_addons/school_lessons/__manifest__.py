# -*- coding: utf-8 -*-
{
    'name': 'School Lessons Portal | بوابة الحصص الدراسية',
    'version': '18.0.1.0.0',
    'summary': 'الأساتذة يرفعوا حصص (فيديو/PDF) والطلاب يشوفوها من بوابة البورتال',
    'description': """
School Lessons Portal
======================
- الأساتذة يقدروا يرفعوا حصص (فيديو مرفوع، رابط يوتيوب/فيميو، أو ملفات PDF)
- كل حصة مربوطة بفصل ومادة معينة
- الطلاب يشوفوا حصص فصلهم بس من خلال بوابة البورتال (Portal)
- تتبع مين من الطلاب فتح/شاف الحصة
- إشعار تلقائي للطلاب لما حصة جديدة تتنشر
- الحصص ليها حالة (مسودة / منشورة) عشان الأستاذ يراجع قبل النشر
""",
    'category': 'Education',
    'author': 'Your Company',
    'depends': [
        'base',
        'mail',
        'portal',
        'website',
        # عدّل ده لاسم موديول تسجيل الطلاب بتاعك لو مختلف
        'school_model_v2',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/lesson_views.xml',
        'views/portal_templates.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
