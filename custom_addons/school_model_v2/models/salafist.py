from odoo import models, fields

class SchoolSalafist(models.Model):
    _name = "school.salafist"
    _description = "School salafists"

    date = fields.Date(string="التاريخ", default=fields.Date.today)
    salafist_id = fields.Many2one( "school.employee" , string="أسم صاحب السلفية")   
    amount = fields.Integer(string="المبلغ", store=True, required=True)
    notes = fields.Text(string="ملاحظات", required=True) 

 