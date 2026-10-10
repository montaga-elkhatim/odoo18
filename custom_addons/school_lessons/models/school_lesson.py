# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError, ValidationError


class SchoolLesson(models.Model):
    _name = 'school.lesson'
    _description = 'Lesson | حصة دراسية'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _order = 'sequence, date_published desc, id desc'
    _rec_name = 'name'

    name = fields.Char(string='عنوان الحصة', required=True, tracking=True)
    sequence = fields.Integer(default=10)

    teacher_id = fields.Many2one(
        'res.users', string='الأستاذ',
        default=lambda self: self.env.user, required=True, tracking=True,
        domain=lambda self: [('groups_id', 'in', self.env.ref('school_lessons.group_school_teacher').id)]
    )

    # ------------------------------------------------------------------
    # عدّل comodel_name هنا لو أسماء الموديلات عندك مختلفة
    # (مثلاً لو موديول التسجيل بتاعك بيسمّيها school.batch أو op.batch)
    # ------------------------------------------------------------------
    class_id = fields.Many2one(
        'school.class', string='الفصل', required=True, tracking=True,
        help='الفصل اللي هتظهر له الحصة'
    )
    subject_id = fields.Many2one('school.subject', string='المادة')

    lesson_type = fields.Selection([
        ('video_upload', 'فيديو مرفوع'),
        ('video_link', 'رابط فيديو (يوتيوب/فيميو)'),
        ('pdf', 'ملف PDF'),
        ('mixed', 'محتوى متعدد (فيديو + ملفات)'),
    ], string='نوع المحتوى', default='pdf', required=True, tracking=True)

    video_url = fields.Char(
        string='رابط الفيديو',
        help='رابط يوتيوب أو فيميو (Unlisted/Private يفضل للخصوصية)'
    )
    video_embed_url = fields.Char(compute='_compute_video_embed_url', string='رابط العرض')

    attachment_ids = fields.Many2many(
        'ir.attachment', 'school_lesson_attachment_rel',
        'lesson_id', 'attachment_id',
        string='الملفات المرفقة (PDF / فيديو)',
    )

    description = fields.Html(string='وصف الحصة')
    date_published = fields.Date(default=fields.Date.context_today, string='تاريخ النشر')

    state = fields.Selection([
        ('draft', 'مسودة'),
        ('published', 'منشورة'),
        ('archived', 'مؤرشفة'),
    ], string='الحالة', default='draft', tracking=True, required=True)

    active = fields.Boolean(default=True)

    view_log_ids = fields.One2many('school.lesson.view.log', 'lesson_id', string='سجل المشاهدات')
    view_count = fields.Integer( string='عدد المشاهدات')
    students_total = fields.Integer( string='إجمالي الطلاب')
    students_viewed = fields.Integer( string='الطلاب اللي شافوا')

    # ---------------------------------------------------------------
    # Compute
    # ---------------------------------------------------------------
    @api.depends('video_url')
    def _compute_video_embed_url(self):
        for rec in self:
            url = (rec.video_url or '').strip()
            embed = False
            if url:
                if 'youtube.com/watch' in url:
                    video_id = url.split('v=')[-1].split('&')[0]
                    embed = f'https://www.youtube.com/embed/{video_id}'
                elif 'youtu.be/' in url:
                    video_id = url.split('youtu.be/')[-1].split('?')[0]
                    embed = f'https://www.youtube.com/embed/{video_id}'
                elif 'youtube.com/embed' in url:
                    embed = url
                elif 'vimeo.com/' in url:
                    video_id = url.rstrip('/').split('/')[-1]
                    embed = f'https://player.vimeo.com/video/{video_id}'
                else:
                    embed = url
            rec.video_embed_url = embed

    # def _compute_view_count(self):
    #     Student = self.env['student'].sudo()
    #     for rec in self:
            rec.view_count = len(rec.view_log_ids)
            # students = Student.search([('grade', '=', rec.class_id)]) if rec.class_id else Student.browse()
            # rec.students_total = len(students)
            # rec.students_viewed = len(rec.view_log_ids.mapped('student_id'))

    # ---------------------------------------------------------------
    # Constraints
    # ---------------------------------------------------------------
    @api.constrains('lesson_type', 'video_url', 'attachment_ids')
    def _check_content_present(self):
        for rec in self:
            if rec.lesson_type == 'video_link' and not rec.video_url:
                raise ValidationError(_('من فضلك أدخل رابط الفيديو.'))
            if rec.lesson_type in ('pdf', 'video_upload') and not rec.attachment_ids:
                raise ValidationError(_('من فضلك ارفع ملف واحد على الأقل.'))

    # ---------------------------------------------------------------
    # Actions
    # ---------------------------------------------------------------
    def action_publish(self):
        for rec in self:
            rec.state = 'published'
            rec.date_published = fields.Date.context_today(rec)
            rec._notify_students()
        return True

    def action_set_draft(self):
        self.write({'state': 'draft'})

    def action_archive_lesson(self):
        self.write({'state': 'archived', 'active': False})

    def _notify_students(self):
        """يبعت إشعار/رسالة للطلاب المسجلين في الفصل لما الحصة تتنشر"""
        self.ensure_one()
        Student = self.env['student'].sudo()
        students = Student.search([('grade', '=', self.class_id.id)])
        partners = students.mapped('partner_id').filtered(lambda p: p.id)
        if partners:
            self.message_notify(
                partner_ids=partners.ids,
                subject=_('حصة جديدة: %s') % self.name,
                body=_('تم نشر حصة جديدة "%s" في مادة %s. يمكنك مشاهدتها من بوابة الطالب.') % (
                    self.name, self.subject_id.name or ''
                ),
            )

    def action_view_students_progress(self):
        self.ensure_one()
        return {
            'name': _('من شاف الحصة'),
            'type': 'ir.actions.act_window',
            'res_model': 'school.lesson.view.log',
            'view_mode': 'list,form',
            'domain': [('lesson_id', '=', self.id)],
        }

    # ---------------------------------------------------------------
    # Portal helpers
    # ---------------------------------------------------------------
    def _portal_student_has_access(self, partner):
        """يتأكد إن الـ partner ده طالب مسجل في نفس فصل الحصة"""
        self.ensure_one()
        if self.state != 'published':
            return False
        student = self.env['student'].sudo().search(
            [('partner_id', '=', partner.id), ('grade', '=', self.class_id.id)], limit=1
        )
        return bool(student)

    def _log_student_view(self, partner):
        """يسجل إن الطالب فتح الحصة (مرة واحدة يوميًا يكفي، هنا بسيط: أول مرة بس)"""
        self.ensure_one()
        student = self.env['student'].sudo().search(
            [('partner_id', '=', partner.id)], limit=1
        )
        if not student:
            return
        existing = self.env['school.lesson.view.log'].sudo().search([
            ('lesson_id', '=', self.id), ('student_id', '=', student.id)
        ], limit=1)
        if not existing:
            self.env['school.lesson.view.log'].sudo().create({
                'lesson_id': self.id,
                'student_id': student.id,
            })
