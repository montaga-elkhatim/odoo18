from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Student(models.Model):
    _name = 'student' 
    _description = "student"
    course_ids= fields.Many2many("course",string="courses")  
    
    name = fields.Char("اسم الطالب", required=True)
    partner_id=fields.Many2one("res.partner",string="شريك")
    note = fields.Text("ملاحظات", )
    image = fields.Binary(string="Image")
    birth_date = fields.Date("تاريخ الميلاد",default=fields.Date.today)
    registration_date = fields.Date("تاريخ التسجيل",default=fields.Date.today)
    academic_year = fields.Many2one('school.academic.year' , string="السنة الدراسية" ,store=True)  
    state = fields.Many2one('school.state' , string="الولاية" ,store=True) 
    locality = fields.Char("المحلية")
    address = fields.Text("عنوان السكن")
    father_name = fields.Char("اسم ولي الامر")
    father_phone = fields.Char("هاتف ولي الامر",required=True)
    another_father_phone = fields.Char("هاتف ولي الامر اخر", ) 
    grade = fields.Many2one('school.class' , string="الصف الدراسي" ,required=True)  
    class_section = fields.Selection([
        ('a', 'أ'),
        ('b', 'ب'),
        ('c', 'ج')
    ], string="الفصل",default="a",required=True)
    section = fields.Selection([
        ('biology', 'احياء'),
        ('engineer', 'هندسية'),
        ('studies', 'دراسات')
    ], string="القسم")
    level=fields.Selection([
        ('1', 'الثانوي'),
        ('2', 'المتوسط'), 
    ], string="مدرسة",compute="_compute_level",default="1",required=True)
    primary_total = fields.Integer("مجموع الأساس")
    percentage = fields.Integer("النسبة")
    health_status = fields.Selection([
        ('well', 'بصحة جيدة'),
        ('Sick', 'مريض'),
        ('disabled', 'معاق'),
        ('other', 'اخري')
    ], string="الحالة الصحية",default="well", required=True)
    payment_ids = fields.One2many(
        "payment", "student_id", string="الدفعايات"
    )
    total_fees = fields.Integer(string="إجمالي الرسوم ", compute="_compute_total_fees",default=0, store=True)
    total_paid = fields.Integer(string="الرسوم المدفوعة", compute="_compute_total_paid",default=0, store=True)
    remaining_fees = fields.Integer(string="المتبقي سداده", compute="_compute_remaining_fees", store=True)
    discount_type = fields.Selection([
                ('1', 'من غير تخفيض'),
        ('2', 'ابن معلم'),
        ('3', 'لديه اخ طالب'),
        ('4', 'يتيم'),
        ('5', 'مجانا')
    ], string="نوع الخصم", )
    discount_value = fields.Integer(string="قيمة الخصم")
    payment_ids = fields.One2many("payment", "student_id", string="الاقساط المدفوعة")
    installment1_paid = fields.Integer(string="القسط الاول المدفوع", compute="_compute_installments_paid", default=0,store=True)
    installment2_paid = fields.Integer(string="القسط الثاني المدفوع", compute="_compute_installments_paid",  default=0 ,store=True)
    installment3_paid = fields.Integer(string="القسط الثالث المدفوع", compute="_compute_installments_paid",  default=0 ,store=True)
    installment4_paid = fields.Integer(string="القسط الرابع المدفوع", compute="_compute_installments_paid",  default=0 ,store=True)
    installment5_paid = fields.Integer(string="القسط الخامس المدفوع", compute="_compute_installments_paid",  default=0,store=True)
    installment6_paid = fields.Integer(string="القسط السادس المدفوع", compute="_compute_installments_paid",  default=0 ,store=True)
    installment7_paid = fields.Integer(string="القسط السابع المدفوع", compute="_compute_installments_paid",  default=0 ,store=True)
    installment8_paid = fields.Integer(string="القسط الثامن المدفوع", compute="_compute_installments_paid",  default=0 ,store=True)
    installment9_paid = fields.Integer(string="القسط التاسع المدفوع", compute="_compute_installments_paid",  default=0 ,store=True)
    installment10_paid = fields.Integer(string="القسط العاشر المدفوع", compute="_compute_installments_paid",  default=0 ,store=True)
    
    full_payment = fields.Boolean(string="دفع كامل؟", default=False)
    _sql_constraints = [
        ('unique_student_name','unique(name)','عذرا يوجد طالب مسجل بنفس الاسم ')
    ]
    @api.depends("payment_ids")
    def _compute_installments_paid(self):
        for rec in self.payment_ids: 

            if rec.payment_type.code == 1:
                self.installment1_paid = rec.amount
                print(rec.payment_type.name)
                
            if rec.payment_type.code == 2:
                self.installment2_paid = rec.amount
                print(rec.payment_type.name)
                
            if rec.payment_type.code == 3:
                self.installment3_paid = rec.amount
                print(rec.payment_type.name)
                
            if rec.payment_type.code == 4:
                self.installment4_paid = rec.amount
                print(rec.payment_type.name)
            
            if rec.payment_type.code == 5:
                self.installment5_paid = rec.amount
                print(rec.payment_type.name)
                
            if rec.payment_type.code == 6:
                self.installment6_paid = rec.amount
                print(rec.payment_type.name)
                
            if rec.payment_type.code == 7:
                self.installment7_paid = rec.amount
                print(rec.payment_type.name)
                
            if rec.payment_type.code == 8:
                self.installment8_paid = rec.amount
                print(rec.payment_type.name)
                
            if rec.payment_type.code == 9:
                self.installment9_paid = rec.amount
                print(rec.payment_type.name)
                
            if rec.payment_type.code == 10:
                self.installment10_paid = rec.amount
                print(rec.payment_type.name)
                 
    @api.depends("discount_value", "discount_type","level")
    def _compute_total_fees(self):
        for rec in self:
            if rec.level == "1":  
                base_fee = self.env['school.amount'].search([
                    ('active', '=', True)
                ]).secondary_amount
            
            if rec.level == "2":  
                base_fee = self.env['school.amount'].search([
                    ('active', '=', True)
                ]).middle_amount 
            if rec.discount_type == "1":
                rec.total_fees = base_fee
            elif rec.discount_type == "free":
                rec.total_fees = 0
            else:
                rec.total_fees = base_fee - rec.discount_value
 
    @api.depends("payment_ids.amount")
    def _compute_total_paid(self):
        for rec in self:
            rec.total_paid = sum(rec.payment_ids.mapped("amount"))

    @api.depends("grade")
    def _compute_level(self):
        for rec in self:
            if rec.grade.category == "1":
                rec.level = "1"
            else:
                rec.level = "2"

 
    @api.depends("total_fees", "total_paid")
    def _compute_remaining_fees(self):
        for rec in self:
            rec.remaining_fees = rec.total_fees - rec.total_paid

 