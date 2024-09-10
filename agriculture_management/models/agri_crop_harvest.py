from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class CropHarvest(models.Model):
    _name = 'crop.harvest'
    _description = 'Hasil Panen'

    def _check_registration(self):
        _logger.info("CropHarvest model registered successfully.")


    # --- Fields (Non-Computed) ---
    date = fields.Date(string='Tanggal Panen', required=True, default=fields.Date.today())
    crop_id = fields.Many2one('agri.crop', string='Tanaman', required=True, store=True)
    quantity = fields.Float(string='Jumlah Panen', required=True)
    unit_id = fields.Many2one('uom.uom', string='Satuan', required=True, domain=[('category_id.name', '=', 'Berat')])
    quality = fields.Selection([
        ('good', 'Baik'),
        ('average', 'Sedang'),
        ('poor', 'Buruk'),
    ], string='Kualitas')
    notes = fields.Text(string='Keterangan')
    photo = fields.Binary(string='Foto')
    project_id = fields.Many2one('project.project', string='Proyek', required=True)
    packaging_name = fields.Char(string='Nama Kemasan')
    packaging_size = fields.Selection([(str(i), f'{i} kg') for i in range(1, 31)], string='Ukuran Kemasan')
    packaging_price_per_unit = fields.Float(string='Harga per Kemasan')
    desired_num_packages = fields.Float(string='Jumlah Kemasan yang Diinginkan')
    currency_id = fields.Many2one('res.currency', string='Mata Uang', required=True, default=lambda self: self.env['res.currency'].search([('name', '=', 'IDR')], limit=1))
    periode_pan = fields.Char(string='Periode Panen', compute='_compute_periode_pan', store=True)




    # --- Computed Fields ---
    used_quantity = fields.Float(string='Jumlah Terpakai (kg)', compute='_compute_used_quantity', store=True)
    total_packaging_cost = fields.Float(
        string='Total Biaya Kemasan',
        compute='_compute_total_packaging_cost',
        store=True
    )

    @api.depends('project_id')
    def _compute_periode_pan(self):
        for record in self:
            if record.project_id:
                start_date = record.project_id.date_start
                end_date = record.project_id.date
                if start_date and end_date:
                    record.periode_pan = f'{start_date} - {end_date}'
                else:
                    record.periode_pan = 'Tanggal tidak lengkap'
            else:
                record.periode_pan = 'Proyek tidak ditetapkan'

    # --- Onchange Methods ---
    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id and self.project_id.crop_id:
            self.crop_id = self.project_id.crop_id
  

    # --- Compute Methods ---
    @api.depends('desired_num_packages', 'packaging_size')
    def _compute_used_quantity(self):
        for harvest in self:
            if harvest.desired_num_packages and harvest.packaging_size:
                harvest.used_quantity = harvest.desired_num_packages * int(harvest.packaging_size[0])
                if harvest.used_quantity > harvest.quantity:
                    raise ValidationError("Jumlah Terpakai tidak boleh melebihi Jumlah Panen.")
            else:
                harvest.used_quantity = 0

    @api.depends('desired_num_packages', 'packaging_price_per_unit')
    def _compute_total_packaging_cost(self):
        for harvest in self:
            if harvest.desired_num_packages and harvest.packaging_price_per_unit:
                harvest.total_packaging_cost = harvest.desired_num_packages * harvest.packaging_price_per_unit
            else:
                harvest.total_packaging_cost = 0

    # --- Other Methods (e.g., write) ---
    @api.model
    def create(self, vals):
        # Create the crop harvest record
        harvest = super(CropHarvest, self).create(vals)

        # Update the product quantity
        self._update_product_quantity(harvest)

        return harvest

    def write(self, vals):
        for harvest in self:
            if 'desired_num_packages' in vals or 'packaging_size' in vals:
                # Simulate the new values for validation
                desired_num_packages = vals.get('desired_num_packages', harvest.desired_num_packages)
                packaging_size = vals.get('packaging_size', harvest.packaging_size)
                
                if desired_num_packages and packaging_size:
                    new_used_quantity = desired_num_packages * float(packaging_size)
                    if new_used_quantity > harvest.quantity:
                        raise ValidationError("Jumlah kemasan yang diinginkan melebihi jumlah panen yang tersedia.")

        res = super(CropHarvest, self).write(vals)

        # Update the product quantity after write
        for harvest in self:
            self._update_product_quantity(harvest)

        return res

    def _update_product_quantity(self, harvest):
        # Get the product template related to the crop
        if harvest.crop_id and harvest.crop_id.product_template_id:
            product_template = harvest.crop_id.product_template_id

            # Call the stock.change.product.qty wizard to update the quantity
            if product_template:
                wizard = self.env['stock.change.product.qty'].create({
                    'product_id': product_template.id,
                    'product_tmpl_id': product_template.id,
                    'new_quantity': product_template.product_variant_id.qty_available + harvest.desired_num_packages
                })
                wizard.change_product_qty()
