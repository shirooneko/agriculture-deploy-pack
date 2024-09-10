from odoo import models, fields, api

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
