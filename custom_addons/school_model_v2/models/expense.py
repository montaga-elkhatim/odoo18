from odoo import models, fields
 
class SchoolExpense(models.Model):
    _name = "school.expense"
    _description = "School Expenses"

    # category = fields.Many2one('school.category.expense' , string="نوع المنصرف",required=True)
    category_expense = fields.Selection([
        ('1', 'مصروفات موظفين'),
        ('2', 'مصروفات امتحانات'),
        ('3', 'مصروفات يومية'), 
        ('4', 'ايجار'), 
        ('5', 'كهرباء'), 
    ], string="نوع المنصرف",required=True)
    exam_type = fields.Many2one('school.exam' , string="نوع الإمتحان")
    exam_expense_type = fields.Many2one('school.exam.type' , string="نوع صرف الإمتحان" ,store=True)
 
    subject_id = fields.Many2one('school.subject', string="أسم المادة")
    lec_number = fields.Integer(string="عدد الحصص", required=True)
 
    papers_number = fields.Integer(string="عدد الأوراق", store=True)
    control_number = fields.Integer(string="عدد المراقبين", store=True)
    owner = fields.Char(string="owner", store=True)
    purpose = fields.Text(string="الغرض", store=True)
    amount = fields.Integer(string="المبلغ", store=True, required=True)
    date = fields.Date(string="التاريخ", default=fields.Date.today)
 
    notes = fields.Text(string="ملاحظات") 
