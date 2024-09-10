from odoo import models, fields, api

class FarmingSeason(models.Model):
    _name = 'agri.farming.seasson'
    _description = 'Farming Season'

    name = fields.Char(string='Season Name', required=True)
    farm_id = fields.Many2one('agri.lands.farm', string='Farm', required=True)
    farmer_id = fields.Many2one('res.partner', string='Farmer', required=True, domain=[('is_farmer', '=', True)])
    crop_id = fields.Many2many('agri.crop', string='Crop', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    user_id = fields.Many2one('res.users', string='Responsible User', required=True)
    state = fields.Selection([
        ('season_start', 'Season Start'),
        ('season_progress', 'Season In Progress'),
        ('season_end', 'Season End'),
    ], string='State', default='season_start')
    image_1920 = fields.Binary(string='Image')
    image_1920_fname = fields.Char()
    project_ids = fields.Many2one('project.project', string='Project')
