from odoo import models, fields, api

class Farm(models.Model):
    _name = 'agri.lands.farm'
    _description = 'Farm'

    name = fields.Char(string='Farm Name', required=True)
    street = fields.Char()
    street2 = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one('res.country.state')
    zip = fields.Char()
    country_id = fields.Many2one('res.country')
    coordinate = fields.Char(string='Coordinate', required=True, help='Google Maps coordinates in format: latitude,longitude')
    farmer_id = fields.Many2one('res.partner', string='Farmer', domain=[('is_farmer', '=', True)])
    image_1920 = fields.Binary(string='Image')
    image_1920_fname = fields.Char()
    farm_type = fields.Many2one('farm.type', string='Farm Type')
    equipment_id = fields.Many2many('equipment.tag', string='Equipment Tags')
    
    # Menambahkan fields untuk panjang dan lebar dalam meter
    length_m = fields.Float(string='Length (m)', help='Length of the farm in meters')
    width_m = fields.Float(string='Width (m)', help='Width of the farm in meters')

    # Field computed untuk menghitung luas dalam hektar
    area_ha = fields.Float(string='Area (ha)', compute='_compute_area_ha', store=True)

    @api.depends('length_m', 'width_m')
    def _compute_area_ha(self):
        for farm in self:
            if farm.length_m and farm.width_m:
                # Menghitung luas dalam meter persegi
                area_sq_m = farm.length_m * farm.width_m
                # Mengkonversi meter persegi ke hektar
                farm.area_ha = area_sq_m / 10_000
            else:
                farm.area_ha = 0