from odoo import models, fields, api

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _description = 'Partner'
    
    is_farmer = fields.Boolean(string='Farmer', compute='_compute_is_farmer', store=True)

    @api.depends('function')
    def _compute_is_farmer(self):
        for partner in self:
            if partner.function and partner.function.lower() == 'petani':
                partner.is_farmer = True
            else:
                partner.is_farmer = False
