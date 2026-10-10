# -*- coding: utf-8 -*-
import base64

from odoo import http, _
from odoo.http import request, content_disposition
from odoo.exceptions import AccessError
from odoo.addons.portal.controllers.portal import CustomerPortal


class SchoolLessonsPortal(CustomerPortal):

    def _get_current_student(self):
        partner = request.env.user.partner_id
        return request.env['student'].sudo().search(
            [('partner_id', '=', partner.id)], limit=1
        )

    @http.route(['/my/lessons', '/my/lessons/subject/<int:subject_id>'],
                type='http', auth='user', website=True)
    def portal_lessons_list(self, subject_id=None, **kw):
        student = self._get_current_student()
        if not student:
            return request.render('school_lessons.portal_no_student_template', {})

        domain = [('class_id', '=', student.grade.id), ('state', '=', 'published')]
        if subject_id:
            domain.append(('subject_id', '=', subject_id))

        Lesson = request.env['school.lesson'].sudo()
        lessons = Lesson.search(domain, order='sequence, date_published desc')
        subjects = Lesson.search([
            ('class_id', '=', student.grade.id), ('state', '=', 'published')
        ]).mapped('subject_id')

        viewed_lesson_ids = set(
            request.env['school.lesson.view.log'].sudo().search(
                [('student_id', '=', student.id)]
            ).mapped('lesson_id').ids
        )

        return request.render('school_lessons.portal_lessons_list_template', {
            'lessons': lessons,
            'subjects': subjects,
            'current_subject_id': subject_id,
            'viewed_lesson_ids': viewed_lesson_ids,
            'student': student,
            'page_name': 'lessons',
        })

    @http.route(['/my/lessons/<int:lesson_id>'], type='http', auth='user', website=True)
    def portal_lesson_detail(self, lesson_id, **kw):
        student = self._get_current_student()
        if not student:
            return request.render('school_lessons.portal_no_student_template', {})

        lesson = request.env['school.lesson'].sudo().browse(lesson_id)
        if not lesson.exists() or not lesson._portal_student_has_access(request.env.user.partner_id):
            return request.not_found()

        lesson._log_student_view(request.env.user.partner_id)

        return request.render('school_lessons.portal_lesson_detail_template', {
            'lesson': lesson,
            'page_name': 'lesson_detail',
        })

    @http.route(['/my/lessons/<int:lesson_id>/file/<int:attachment_id>'],
                type='http', auth='user')
    def portal_lesson_attachment(self, lesson_id, attachment_id, **kw):
        """تنزيل/تشغيل الملف بعد التأكد إن الطالب مصرح له فعلاً"""
        lesson = request.env['school.lesson'].sudo().browse(lesson_id)
        if not lesson.exists() or not lesson._portal_student_has_access(request.env.user.partner_id):
            raise AccessError(_('غير مصرح لك بالوصول لهذا الملف.'))

        attachment = lesson.attachment_ids.filtered(lambda a: a.id == attachment_id)
        if not attachment:
            return request.not_found()
        attachment = attachment[0].sudo()

        content = base64.b64decode(attachment.datas or b'')
        headers = [
            ('Content-Type', attachment.mimetype or 'application/octet-stream'),
            ('Content-Length', len(content)),
        ]
        # الفيديوهات تتعرض جوه المتصفح، الـ PDF كمان ممكن يتعرض inline
        if not (attachment.mimetype or '').startswith(('video/', 'application/pdf')):
            headers.append(('Content-Disposition', content_disposition(attachment.name)))

        return request.make_response(content, headers=headers)
