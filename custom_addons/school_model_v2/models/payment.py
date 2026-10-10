from odoo import models, fields, api
from num2words import num2words
from odoo.exceptions import ValidationError

class Payment(models.Model):
    _name = "payment"
    _description = 'Student Payment'
    student_id = fields.Many2one(
        "student", string="إسم الطالب",required=True
    )
    payment_date = fields.Date("تاريخ الدفع", default=fields.Date.today,required=True)
    amount = fields.Integer("المبلغ", required=True)
    amount_text=fields.Char(
        string="المبلغ نص",
        compute="_compute_amount_text"
    )
    payment_type = fields.Many2one('school.installment' , string="نوع القسط" ,store=True)
    receipt_number = fields.Char(
        string="الرقم المتسلسل",
        required=True,
        readonly=True,
        copy=False,
        default='New'
    )  
    def action_print_receipt(self):
        return self.env.ref(
            'school_model_v2.student_payment_receipt_report'
        ).report_action(self)
    @api.depends('amount')
    def _compute_amount_text(self):
        for rec in self:
            amount = rec.amount
            if amount:
                try:
                    rec.amount_text = num2words(amount, lang='ar')
                except ImportError:
                    rec.amount_text = _('num2words library is not installed.')
            else:
                rec.amount_text = ''
      
    @api.constrains('student_id', 'amount')
    def _check_total_payments(self):
        for rec in self:
            if rec.student_id and rec.student_id.total_fees:
                # اجمع كل الدفعيات الحالية باستثناء الريكورد الجاري
                total_paid = sum(rec.student_id.payment_ids.filtered(lambda p: p.id != rec.id).mapped('amount'))
                # + المبلغ الجديد
                if total_paid + rec.amount > rec.student_id.total_fees:
                    raise ValidationError(f"إجمالي الدفعيات ({total_paid + rec.amount}) تجاوز قيمة الرسوم الكلية ({rec.student_id.total_fees})، لا يمكن تسجيل هذه الدفعة.")
    @api.constrains('payment_type.code', 'student_id')
    def _check_unique_payment(self):
        for rec in self:
            if not rec.student_id or not rec.payment_type.code:
                continue

            # لو دفع كامل
            if rec.payment_type.code == "100":
                existing = self.search([
                    ('student_id', '=', rec.student_id.id),
                    ('payment_type.code', '=', '100'),
                    ('id', '!=', rec.id)
                ])
                if existing:
                    raise ValidationError("هذا الطالب عنده دفع كامل بالفعل، لا يمكن إضافة دفعيات أخرى.")

                # كمان نمنع أي قسط مع الدفع الكامل
                other = self.search([
                    ('student_id', '=', rec.student_id.id),
                    ('payment_type.code', '!=', '100'),
                    ('id', '!=', rec.id)
                ])
                if other:
                    raise ValidationError("لا يمكن إضافة أقساط لطالب عنده دفع كامل.")

            # لو قسط
            else:
                # تأكد مافي دفع كامل للطالب
                full_payment = self.search([
                    ('student_id', '=', rec.student_id.id),
                    ('payment_type.code', '=', '100'),
                    ('id', '!=', rec.id)
                ])
                if full_payment:
                    raise ValidationError("لا يمكن إضافة أقساط لطالب عنده دفع كامل.")

                # تأكد ما في قسط مكرر
                existing_installment = self.search([
                    ('student_id', '=', rec.student_id.id),
                    ('payment_type.code', '=', rec.payment_type.code),
                    ('id', '!=', rec.id)
                ])
                if existing_installment:
                    raise ValidationError(f"هذا الطالب عنده {rec.payment_type.code} بالفعل، لا يمكن إضافته مرة أخرى.")
    @api.model
    def create(self, vals):
        rec = super(Payment, self).create(vals)
        student = rec.student_id

        # تحديث حسب نوع الدفعية
        if rec.payment_type.code == '1':
            student.installment1_paid = rec.amount
        elif rec.payment_type.code == '2':
            student.installment2_paid = rec.amount
        elif rec.payment_type.code == '3':
            student.installment3_paid = rec.amount
        elif rec.payment_type.code == '4':
            student.installment4_paid = rec.amount
        elif rec.payment_type.code == '5':
            student.installment5_paid = rec.amount
        elif rec.payment_type.code == '100':
            student.full_payment = True
            # نخزن المبلغ كله كمدفوع
            student.total_paid = student.total_fees

        # تحديث المجموعات
        total = (student.installment1_paid + student.installment2_paid +
                student.installment3_paid + student.installment4_paid +
                student.installment5_paid)
        if student.full_payment:
            total = student.total_fees
        student.total_paid = total
        student.remaining_fees = student.total_fees - total 

        if rec.receipt_number == 'New':
            rec.receipt_number = self.env['ir.sequence'].next_by_code('payment_sequence') 
          
        return rec