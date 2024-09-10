from odoo import models, fields

class FarmType(models.Model):
    _name = 'farm.type'
    _description = 'Farm Type'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    
