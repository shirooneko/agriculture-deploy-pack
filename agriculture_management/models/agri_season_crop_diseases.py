from odoo import models, fields, api

class SeasonCropDisease(models.Model):
    _name = 'agri.season.crop.disease'
    _description = 'Penyakit Tanaman Musim'

    name = fields.Char(string='Nama Penyakit', compute='_compute_name_from_disease_id', store=True)
    project_ids = fields.Many2one('project.project', string='Proyek', store=True, required=True, default=lambda self: self._context.get('default_project_id', False))
    crop_id = fields.Many2one('agri.crop', string='Tanaman', store=True)
    evidence_photo = fields.Binary(string='Foto Bukti')
    damage_total = fields.Float(string='Total Kerusakan', required=True)
    disease_id = fields.Many2one('agri.crop.disease', string='Penyakit', required=True, domain=lambda self: [
        ('id', 'not in', self.search([
            ('id', '!=', self.id),
            ('project_ids', '=', self.project_ids.id)  # Filter berdasarkan project
        ]).mapped('disease_id').ids)
    ])
    handled = fields.Boolean(string='Ditangani?', store=True)

    healty_manure_id = fields.Many2one('agri.crop.healty.manure', string='Kompos', compute='_compute_healty_manure_id', store=True, required=False)


    @api.depends('disease_id')
    def _compute_name_from_disease_id(self):
        for record in self:
            if record.disease_id:
                record.name = record.disease_id.name

    @api.onchange('project_ids')
    def _onchange_project_ids(self):
        if self.project_ids:
            self.crop_id = self.project_ids.crop_id.id


    def action_open_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Handle Disease',
            'res_model': 'season.crop.disease.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_season_crop_disease_id': self.id,
                'default_crop_id': self.crop_id.id,
                'default_name': self.name,
                'default_project_id': self.project_ids.id
            },
        }
    
    @api.depends('project_ids')
    def _compute_healty_manure_id(self):
        for record in self:
            if record.project_ids:
                wizard = self.env['season.crop.disease.wizard'].search([('season_crop_diseases_id', '=', record.id)], limit=1)
                if wizard:
                    record.healty_manure_id = wizard.healty_manure_id.id