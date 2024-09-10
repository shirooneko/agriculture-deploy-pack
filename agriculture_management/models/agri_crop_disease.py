from odoo import models, fields

class CropDisease(models.Model):
    _name = 'agri.crop.disease'
    _description = 'Penyakit Tanaman'

    name = fields.Char(string='Nama Penyakit', required=True)
    description = fields.Text(string='Deskripsi')
    prevention = fields.Text(string='Pencegahan')
    cure = fields.Text(string='Pengobatan')
    crop_ids = fields.Many2many('agri.crop', string='Tanaman Terdampak')
    image_1920 = fields.Binary(string='Image')
    image_1920_fname = fields.Char()