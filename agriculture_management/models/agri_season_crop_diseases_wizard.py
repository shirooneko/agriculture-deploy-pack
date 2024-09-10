from odoo import models, fields, api

from odoo.exceptions import ValidationError

class SeasonCropDiseaseWizard(models.TransientModel):
    _name = 'season.crop.disease.wizard'
    _description = 'Wizard untuk Menangani Penyakit Tanaman'

    name = fields.Char(string='Nama Penyakit', required=True)
    healty_manure_id = fields.Many2one('agri.crop.healty.manure', string='Kompos', required=True)
    project_ids = fields.Many2one('project.project', string='Proyek', store=True, required=True, default=lambda self: self.env.context.get('default_project_id', False))
    season_crop_diseases_id = fields.Many2one('agri.season.crop.disease', string='Season crop diseases', store=True, required=True, default=lambda self: self.env.context.get('default_season_crop_disease_id', False))

    
    def action_to_handle(self):
        self.ensure_one()

        season_crop_disease_objs = self.env['agri.season.crop.disease'].search([('id', '=', self.season_crop_diseases_id.id)], limit=1)

        if not season_crop_disease_objs:
            raise ValidationError("Season crop disease tidak ditemukan atau tidak valid.")
        
        season_crop_disease_obj = season_crop_disease_objs[0]

        # Check if the disease has already been handled
        if season_crop_disease_obj.handled:
            raise ValidationError("Penyakit tanaman sudah ditangani sebelumnya.")
        
        # Prepare values to update
        values = {
            'handled': True,
            'healty_manure_id': self.healty_manure_id.id,
        }

        # Write the new values to the season crop disease object
        season_crop_disease_obj.write(values)

        # Optionally, you can add more logic here if needed
        
        # Close the wizard window after handling
        return {'type': 'ir.actions.act_window_close'}