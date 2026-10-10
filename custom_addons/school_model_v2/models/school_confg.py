from odoo import models, fields, api



class SchoolcState(models.Model):   
    _name = "school.state"
    _description = "school.state"

    name = fields.Char(string="إسم الولاية" ,required=True)
    code = fields.Integer(string="الكود" ,required=True)

class SchoolcAdemicYear(models.Model):   
    _name = "school.academic.year"
    _description = "school.academic.year"

    name = fields.Char(string="إسم السنة الدراسية" ,required=True)
    code = fields.Integer(string="الكود" ,required=True)
class SchoolInstallment(models.Model):  
    _name = "school.installment"
    _description = "school.installment"

    name = fields.Char(string="إسم القسط" ,required=True)
    code = fields.Integer(string="الكود" ,required=True)
class SchoolExamType(models.Model):   
    _name = "school.exam.type"
    _description = "school.exam.type"

    name = fields.Char(string="نوع صرف الإمتحان" ,required=True)
    code = fields.Integer(string="الكود" ,required=True)
class SchoolExam(models.Model):  
    _name = "school.exam"
    _description = "school.exam"

    name = fields.Char(string="إسم الإمتحان" ,required=True)
    code = fields.Integer(string="الكود" ,required=True)
class SchoolCategoryExpense(models.Model): 
    _name = "school.category.expense"
    _description = "school.category.expense"

    name = fields.Char(string="إسم الصرف" ,required=True)
    code = fields.Integer(string="الكود" ,required=True)
class SchoolClass(models.Model):
    _name = "school.class"
    _description = "school.class"

    name = fields.Char(string="إسم الصف" ,required=True)
    category = fields.Selection([
            ('1', 'ثانوي'),
            ('2', 'متوسط'),  
        ], string="التصنيف")
    code = fields.Integer(string="الكود" ,required=True)
    

class SchoolSubject(models.Model):
    _name = "school.subject"
    _description = "school.subject"

    name = fields.Char(string="إسم المادة" ,required=True)
    code = fields.Integer(string="الكود" ,required=True)
    class_ids = fields.Many2many('school.class' , string="الصف الدراسي" )
    

class AmountClass(models.Model):
    _name = "school.amount"
    _description = "school.amount"

    active = fields.Boolean(string="نشط" ,default=False, required=True)
    secondary_amount = fields.Integer(string="رسوم الثانوي" ,required=True)
    middle_amount = fields.Integer(string="رسوم المتوسط" ,required=True) 
    


 

class SchoolEmployee(models.Model):
    _name = "school.employee"
    _description = "employee" 

    name = fields.Char(string="اسم الموظف" ,required=True)
    image = fields.Binary(string="Image")

    category = fields.Selection([
            ('1', 'موظف'),
            ('2', 'أستاذ'),  
        ], string="المسمى الوظيفي")
    subject_ids = fields.Many2many('school.subject', string="المواد الدراسية")
    salary = fields.Float(string="الراتب", required=True)
    lec_number = fields.Integer(string="عدد الحصص", required=True)
    active = fields.Boolean(string="active", default=True)

    # ربط مع المنصرفات
    expense_ids = fields.One2many('school.expense', 'employee_id', string="صرف راتب")
    salafists_ids = fields.One2many('school.salafist', 'salafist_id', string="صرف سلفية")

    _sql_constraints = [
        ('unique_employee_name','unique(name)','عذرا يوجد موظف بنفس الاسم ')
    ]
    def action_add_salary(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'إضافة مرتب',
            'res_model': 'school.expense',
            'view_mode': 'form',
            'target': 'new',

            'context': {
                'default_employee_id': self.id,
                'default_category_expense':'1'
            }
        }

class SchoolExpense(models.Model):
    _inherit = "school.expense"

    employee_id = fields.Many2one("school.employee", string="إسم الموظف")
