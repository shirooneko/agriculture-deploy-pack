from odoo import models, fields, api
import random

class Crop(models.Model):
    _name = 'agri.crop'
    _description = 'Crop'

    name = fields.Char(string='Name', required=True)
    crop_type = fields.Selection([
        ('seasonal_plants', 'tanaman musiman'),
        ('one_harvest_plant', 'Tanaman Sekali Panen')],
        string='Crop Type', required=True)
    disease_ids = fields.Many2many('agri.crop.disease', string='Diseases')
    image_1920 = fields.Binary(string='Image')
    image_1920_fname = fields.Char()
    color = fields.Integer('Color Index', default=lambda self: random.randint(1, 10))
    project_id = fields.Many2one('project.project', string='Project')
    seed_ids = fields.One2many('agri.crop.seeds', 'crop_id', string='Seeds')
    
    stage_ids = fields.One2many('agri.stage', 'crop_id', string='Stages')
    task_template_ids = fields.One2many('agri.task.template', 'crop_id', string='Task Templates')
    
    stage_count = fields.Integer(string='Stage Count', compute='_compute_stage_count')
    task_template_count = fields.Integer(string='Task Template Count', compute='_compute_task_template_count')
    
    stage_id = fields.One2many('project.task.type', 'crop_id', string='Stages')
    task_ids = fields.One2many('project.task', 'crop_id', string="Task")

    product_template_id = fields.Many2one('product.template', string='Product Template', ondelete='cascade' ,readonly=True)



    @api.depends('stage_ids')
    def _compute_stage_count(self):
        for crop in self:
            crop.stage_count = len(crop.stage_ids)

    @api.depends('task_template_ids')
    def _compute_task_template_count(self):
        for crop in self:
            crop.task_template_count = len(crop.task_template_ids)

    
    def action_open_stages(self):
        name = 'Stages of {}'.format(self.name)
        return {
            'type': 'ir.actions.act_window',
            'name': name,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'agri.stage',
            'target': 'current',
            'domain': [('crop_id', '=', self.id)],
            'context': {'default_crop_id': self.id},
        }

    def action_open_tasks(self):
        name = 'Tasks of {}'.format(self.name)
        return {
            'type': 'ir.actions.act_window',
            'name': name,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'agri.task.template',
            'target': 'current',
            'domain': [('crop_id', '=', self.id)],
            'context': {
                'default_crop_id': self.id,
                'search_default_group_by_stage': True,
            }
        }
    
    @api.model
    def create(self, vals):
        # Create the crop record
        crop = super(Crop, self).create(vals)

        # Create corresponding product.template record
        product_template = self.env['product.template'].create({
            'name': crop.name,
            'purchase_ok': False,  # Setting purchase_ok to False as per requirement
            'detailed_type': 'product',     # Setting type to 'product'
            'image_1920': crop.image_1920,  # Copy the image
        })

        # Link the product_template to the crop
        crop.product_template_id = product_template.id

        return crop