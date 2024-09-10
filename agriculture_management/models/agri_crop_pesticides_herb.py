from odoo import models, fields, api

class CropPesticide(models.Model):
    _name = 'agri.crop.pesticides.herb'
    _description = 'Crop Pesticide'

    name = fields.Char(string='Nama Pestisida', required=True)
    threat_level = fields.Selection([
        ('danger', 'Danger'),
        ('caution', 'Caution'),
        ('flammable', 'Flammable'),
        ('toxic', 'Toxic'),
        ('corrosive', 'Corrosive')],
        string='Level Ancaman', required=True)
    pkg_qty = fields.Float(string='Pkg Qty', required=True, help='Jumlah pestisida dalam satu kemasan')
    price = fields.Float(string='Price', required=True, help='Harga pestisida per unit')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'IDR')], limit=1))
    uom_id = fields.Many2one('uom.uom', string='Unit', required=True)
    image_1920 = fields.Binary(string='Image')
    image_1920_fname = fields.Char()