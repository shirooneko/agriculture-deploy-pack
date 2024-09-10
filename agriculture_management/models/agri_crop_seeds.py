from odoo import models, fields, api

class CropSeed(models.Model):
    _name = 'agri.crop.seeds'
    _description = 'Benih Tanaman'

    name = fields.Char(string='Nama Benih', required=True)
    image_1920 = fields.Binary(string='Gambar')
    image_1920_fname = fields.Char()
    crop_id = fields.Many2one('agri.crop', string='Tanaman', required=True)
    qty_on_hand = fields.Float(string='Stok Benih', store=True, digits=(16, 0))
    purchase_history_ids = fields.One2many('agri.crop.seed.purchase', 'seed_id', string='Riwayat Pembelian')
    current_price = fields.Float(string='Harga Saat Ini', compute='_compute_current_price',digits=(16, 0), store=True, help='Harga terbaru dari riwayat pembelian benih')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'IDR')], limit=1))

    @api.depends('purchase_history_ids.price_per_unit')
    def _compute_current_price(self):
        for seed in self:
            latest_purchase = seed.purchase_history_ids.sorted(key='purchase_date', reverse=True)
            if latest_purchase:
                seed.current_price = latest_purchase[0].price_per_unit
            else:
                seed.current_price = 0.0  # Atau nilai default lainnya jika belum ada pembelian


    def action_history_stok(self):
        pass