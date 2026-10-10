from odoo import models, fields, api

  
class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "teacher"

    name = fields.Char(string="إسم الموظف" ,required=True)
    image = fields.Binary(string="Image")
    subject_name = fields.Many2many('school.subject', string="المواد الدراسية")
    salary = fields.Float(string="الراتب", required=True)
    # lec_number = fields.Integer(string="عدد الحصص", required=True)
    active = fields.Boolean(string="active", default=True)

    # ربط مع المنصرفات
    expense_ids = fields.One2many('school.expense', 'teacher_id', string="expense")
    salafists_ids = fields.One2many('school.salafist', 'salafist_id', string="salafist")


class SchoolExpense(models.Model):
    _inherit = "school.expense"

    teacher_id = fields.Many2one("school.teacher", string="name")
