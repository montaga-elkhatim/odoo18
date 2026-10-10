from odoo import models, fields


class SchoolFinancialReportWizard(models.TransientModel):
    _name = 'school.financial.report.wizard'
    _description = 'School Financial Report Wizard'

    date_from = fields.Date(string="من تاريخ ", required=True)
    date_to = fields.Date(string="الي تاريخ ", required=True)

    def action_print_report(self):
        return self.env.ref(
            'school_model_v2.school_financial_report_action'
        ).report_action(self)

    def get_report_data(self):

        student_payments = self.env['payment'].search([
            ('payment_date', '>=', self.date_from),
            ('payment_date', '<=', self.date_to)
        ])

        teacher_expenses = self.env['school.expense'].search([
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
            ('category_expense', '=', 1),
        ])

        school_expenses = self.env['school.expense'].search([
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
            ('category_expense', '!=', 1),

        ])

        total_income = sum(student_payments.mapped('amount'))
        total_teacher_expense = sum(teacher_expenses.mapped('amount'))
        total_school_expense = sum(school_expenses.mapped('amount'))

        net = total_income - (
            total_teacher_expense + total_school_expense
        )

        return {
            'student_payments': student_payments,
            'teacher_expenses': teacher_expenses,
            'school_expenses': school_expenses,
            'total_income': total_income,
            'total_teacher_expense': total_teacher_expense,
            'total_school_expense': total_school_expense,
            'net': net,
        }
 