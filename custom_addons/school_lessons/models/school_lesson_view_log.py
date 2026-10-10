# -*- coding: utf-8 -*-
from odoo import models, fields


class SchoolLessonViewLog(models.Model):
    _name = 'school.lesson.view.log'
    _description = 'Lesson View Log | سجل مشاهدة الحصص'
    _order = 'view_date desc'

    lesson_id = fields.Many2one('school.lesson', string='الحصة', required=True, ondelete='cascade')
    student_id = fields.Many2one('student', string='الطالب', required=True, ondelete='cascade')
    view_date = fields.Datetime(string='تاريخ أول مشاهدة', default=fields.Datetime.now)

    _sql_constraints = [
        ('lesson_student_uniq', 'unique(lesson_id, student_id)',
         'الطالب مسجل مشاهدة الحصة دي بالفعل.'),
    ]
