from odoo import models, fields

class ProjectTaskTypeInherit(models.Model):
    _inherit = 'project.task.type'
    
    task_ids = fields.One2many('project.task', 'stage_id', string='Tasks')
    crop_id = fields.Many2one('agri.crop', string='Tanaman', readonly=True)