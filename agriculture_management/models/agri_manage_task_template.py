from odoo import models, fields, api

class TaskTemplate(models.Model):
    _name = 'agri.task.template'
    _description = 'Task Template'
    _order = 'sequence, id'

    is_optional = fields.Boolean(string='Optional Task?')
    name = fields.Char(string='Name', required=True)
    notes = fields.Html(string='Notes')
    sequence = fields.Integer(string='Sequence')
    stage_id = fields.Many2one('agri.stage', string='Stage')
    target_days_completed = fields.Integer(string='Target Days')
    crop_id = fields.Many2one('agri.crop', string='Tanaman', readonly=True, store=True)
    state = fields.Selection([
        ('01_draft', 'Draft'),
        ('02_scheduled', 'Scheduled'),
        ('03_in_progress', 'In Progress'),
        ('04_on_hold', 'On Hold'),
        ('05_completed', 'Completed'),
        ('06_cancelled', 'Cancelled'),
    ], string='State', default='01_draft', required=True, tracking=True)

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        if self.stage_id and self.stage_id.crop_id:
            self.crop_id = self.stage_id.crop_id.id

    @api.model
    def default_get(self, fields_list):
        res = super(TaskTemplate, self).default_get(fields_list)
        if self._context.get('default_crop_id'):
            res['crop_id'] = self._context.get('default_crop_id')
        return res


    
