# my_product_inherit/models/product.py
from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = 'product.template'

    is_agricultural_product = fields.Boolean(string='Is Agricultural Product', default=True)
