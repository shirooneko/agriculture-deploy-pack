from odoo import models, fields, api
from datetime import date

class CropSeedPurchase(models.Model):
    _name = 'agri.crop.seed.purchase'
    _description = 'Riwayat Pembelian Benih'
    _order = 'purchase_date desc'

    seed_id = fields.Many2one('agri.crop.seeds', string='Benih', required=True, ondelete='cascade')
    purchase_date = fields.Date(string='Tanggal Pembelian', required=True, default=fields.Date.today())
    quantity = fields.Float(string='Kuantitas', required=True, digits=(16, 0)  )
    price_per_unit = fields.Float(string='Harga per Kg', required=True, digits=(16, 0))
    uom_id = fields.Many2one('uom.uom', string='Satuan', required=True, domain=[('category_id.name', '=', 'Berat')])
    total_price = fields.Monetary(string='Total Harga', compute='_compute_total_price', store=True, digits=(16, 0))
    currency_id = fields.Many2one('res.currency', string='Mata Uang', required=True, default=lambda self: self.env['res.currency'].search([('name', '=', 'IDR')], limit=1))

    @api.depends('quantity', 'price_per_unit')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.quantity * record.price_per_unit

    @api.model_create_multi
    def create(self, vals_list):
        res = super(CropSeedPurchase, self).create(vals_list)
        for rec in res:
            if rec.seed_id:
                rec.seed_id.qty_on_hand += rec.quantity
        return res

    def write(self, vals):
        old_quantities = {rec.id: rec.quantity for rec in self}  # Store old quantities
        res = super(CropSeedPurchase, self).write(vals)
        for rec in self:
            if rec.seed_id:
                diff = rec.quantity - old_quantities.get(rec.id, 0)
                rec.seed_id.qty_on_hand += diff
        return res

    def unlink(self):
        for rec in self:
            if rec.seed_id:
                rec.seed_id.qty_on_hand = max(0, rec.seed_id.qty_on_hand - rec.quantity)  # Ensure qty_on_hand >= 0
        return super(CropSeedPurchase, self).unlink()
