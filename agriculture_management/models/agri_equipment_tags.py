from odoo import models, fields
import random

class EquipmentTag(models.Model):
    _name = 'equipment.tag'
    _description = 'Equipment Tag'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    farm_id = fields.Many2one('agri.lands.farm', string='Farm')
    color = fields.Integer('Color Index', default=lambda self: random.randint(1, 10))
    
