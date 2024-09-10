from odoo import models, fields

class AgriStage(models.Model):
    _name = 'agri.stage'
    _description = 'Agricultural Stage'

    name = fields.Char(string='Stage Name', required=True)
    project_id = fields.Many2one('project.project', string='Project')
    crop_id = fields.Many2one('agri.crop', string='Tanaman', required=True)
    task_template_id = fields.One2many('agri.task.template', 'stage_id', string='Task')
