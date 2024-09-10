from odoo import models, fields


class CropHealtyManure(models.Model):
    _name = 'agri.crop.healty.manure'
    _description = 'Crop Manure'

    name = fields.Char(string='Nama Kompos', required=True)
    crop_id = fields.Many2one('agri.crop', string='Tanaman', required=True)
    quantity = fields.Float(string='Kuantitas', required=True, help='Jumlah pupuk yang tersedia')
    dosage = fields.Char(string='Dosis per Hektar', required=True, help='Dosis pupuk yang direkomendasikan per hektar')
    price = fields.Monetary(string='Harga', required=True, help='Harga pupuk per unit')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'IDR')], limit=1))
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
    image_1920 = fields.Binary(string='Image')
    image_1920_fname = fields.Char()