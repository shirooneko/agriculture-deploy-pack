from odoo import models, fields

class PackagingConfig(models.Model):
    _name = 'packaging.config'
    _description = 'Konfigurasi Kemasan'

    name = fields.Char(string='Nama Kemasan', required=True)
    size = fields.Selection([
        ('5', '5 kg'),
        ('10', '10 kg'),
    ], string='Ukuran Kemasan', required=True)
    uom_id = fields.Many2one('uom.uom', string='Satuan', required=True, default=lambda self: self.env.ref('uom.product_uom_kg'))
    price_per_unit = fields.Float(string='Harga per Kemasan')
    project_id = fields.Many2one('project.project', string='Proyek')  # Tambahkan field project_id

