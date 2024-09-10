from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class ProjectProject(models.Model):
    _inherit = 'project.project'

    # Fields definition
    farm_id = fields.Many2one('agri.lands.farm', string='Lahan Pertanian', store=True, required=True)
    is_agriculture = fields.Boolean(string='Apakah Pertanian?', compute='_compute_is_agriculture', store=True)
    crop_id = fields.One2many('agri.crop', 'project_id', string='Tanaman')
    crop_type = fields.Selection(related='crop_id.crop_type', string='Crop Type')
    seed_id = fields.Many2one('agri.crop.seeds', string='Benih', compute='_compute_seed_id', store=True)
    seed_quantity = fields.Float(string='Kuantitas Benih (kg)')
    current_seed_quantity = fields.Float(string='Stok Benih Tersedia (kg)', compute='_compute_current_seed_quantity', store=False)
    current_price = fields.Float(string='Harga Benih Saat Ini', compute='_compute_current_price', store=False)
    total_seed_expense = fields.Float(string='Total Biaya Benih', compute='_compute_total_seed_expense', store=True, help='Total biaya benih yang digunakan dalam proyek')
    total_seed_expense_str = fields.Char(string='Total Biaya Benih', compute='_compute_total_seed_expense_str', store=False)
    crop_ids_display = fields.Char(string="Crop ID Display")
    task_ids = fields.One2many('project.task', 'project_id', string='Tasks', domain=lambda self: [('stage_id', '=', self.curent_stage_id.id)])
    packaging_config_ids = fields.One2many('packaging.config', 'project_id', string='Konfigurasi Kemasan')
    season_crop_diseases_id = fields.One2many('agri.season.crop.disease', 'project_ids', string='Tasks')
    curent_stage_id = fields.Many2one('project.task.type',  string='Stage')
    state = fields.Selection([
        ('season_start', 'Season Start'),
        ('season_progress', 'Season In Progress'),
        ('season_end', 'Season End'),
    ], string='State', default='season_start', help="State of the project", color={'season_start': 'green', 'season_progress': 'yellow', 'season_end': 'red'})
    harvest_ids = fields.One2many('crop.harvest', 'project_id', string='Hasil Panen')
    total_pesticide_price = fields.Float(string='Pesticide Expense')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'IDR')], limit=1))
    total_healty_manure_price = fields.Float(compute='_compute_total_healty_manure_price', string='Healty Manure Expense')
    total_healty_manure_price_str = fields.Char(compute='_compute_total_healty_manure_price', string='Healty Manure Expense')


    total_harvest_quantity = fields.Float(
        string='Total Hasil Panen',
        compute='_compute_total_harvest_quantity',
        store=True
    )

    @api.depends('harvest_ids')
    def _compute_total_harvest_quantity(self):
        for project in self:
            # Menghitung total jumlah hasil panen yang terkait dengan proyek ini
            total_quantity = sum(harvest.quantity for harvest in project.harvest_ids)
            project.total_harvest_quantity = total_quantity

    
    # Compute Methods
    @api.depends('farm_id', 'crop_id')
    def _compute_is_agriculture(self):
        for project in self:
            project.is_agriculture = bool(project.farm_id) or bool(project.crop_id)

    @api.depends('seed_id')
    def _compute_current_seed_quantity(self):
        for project in self:
            if project.seed_id:
                project.current_seed_quantity = project.seed_id.qty_on_hand
            else:
                project.current_seed_quantity = 0

    @api.depends('seed_id.current_price')
    def _compute_current_price(self):
        for project in self:
            if project.seed_id:
                project.current_price = project.seed_id.current_price
            else:
                project.current_price = 0.0

    @api.depends('seed_id.current_price', 'seed_quantity')
    def _compute_total_seed_expense(self):
        for project in self:
            if project.seed_id and project.seed_quantity:
                project.total_seed_expense = project.seed_id.current_price * project.seed_quantity
            else:
                project.total_seed_expense = 0.0

    @api.depends('total_seed_expense')
    def _compute_total_seed_expense_str(self):
        for project in self:
            project.total_seed_expense_str = f"Rp {project.total_seed_expense:,.0f}"

    @api.depends('season_crop_diseases_id.healty_manure_id.price')
    def _compute_total_healty_manure_price(self):
        for record in self:
            total_price = 0.0
            for disease in record.season_crop_diseases_id:
                if disease.healty_manure_id:
                    total_price += disease.healty_manure_id.price
            record.total_healty_manure_price = total_price
            record.total_healty_manure_price_str = "Rp {:,.0f}".format(total_price)

    @api.depends('crop_id.seed_ids')
    def _compute_total_seed_price(self):
        pass
        # for record in self:
        #     total_price = 0.0
        #     for crop in record.crop_id:
        #         for seed in crop.seed_ids:
        #             total_price += seed.price
        #     record.total_seed_price_str = "Rp {:,.0f}".format(total_price)

    @api.depends('crop_id')
    def _compute_seed_id(self):
        for project in self:
            if project.crop_id:
                seed_ids = project.crop_id.mapped('seed_ids')
                if seed_ids:
                    project.seed_id = seed_ids[0]  # Memilih seed pertama yang ditemukan
                else:
                    project.seed_id = False 
            else:
                project.seed_id = False

    # Action Methods
    def action_view_detail_project(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Project',
            'view_mode': 'form',
            'res_model': 'project.project',
            'res_id': self.id,
            'views': [(self.env.ref('agriculture_management.view_agri_farm_form').id, 'form')],
        }
        
    def action_view_seeds(self):
        self.ensure_one()
        crop_ids = self.crop_id.ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Seeds',
            'view_mode': 'tree',
            'res_model': 'agri.crop.seeds', 
            'domain': [('crop_id', 'in', crop_ids)],  
            'views': [(self.env.ref('agriculture_management.view_season_crop_seeds_tree').id, 'tree')],
        }

    def action_view_healty_manure(self):
        self.ensure_one()
        healty_manure_ids = self.season_crop_diseases_id.mapped('healty_manure_id').ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Healty Manure',
            'view_mode': 'tree',
            'res_model': 'agri.crop.healty.manure',
            'domain': [('id', 'in', healty_manure_ids)],
            'views': [(self.env.ref('agriculture_management.view_season_healty_manure_tree').id, 'tree')],
        }
        
    def start_agriculture(self):
        for project in self:
            # Validasi bahwa seed_quantity harus lebih dari 0
            if project.seed_quantity <= 0:
                raise ValidationError("Masukan Kuantitas benih yang dibutuhkan untuk memulai pertanian.")

            # Create update record
            update_vals = {
                'name': f'Start Agriculture - {datetime.now().strftime("%Y-%m-%d")}',
                'status': 'on_track',
                'date': fields.Date.context_today(project),
                'progress': 100,
                'project_id': project.id,
            }
            self.env['project.update'].create(update_vals)

            # Find the first stage/task type
            first_stage_type = self.env['project.task.type'].search([
                ('project_ids', 'in', [project.id])
            ], limit=1, order='id asc')

            # Update the current_stage_id field
            project.write({
                'state': 'season_progress',
                'curent_stage_id': first_stage_type.id if first_stage_type else False
            })
    
    def agricultural_cycle_begins(self):
        for project in self:
            # Validasi bahwa seed_quantity harus lebih dari 0
            if project.seed_quantity <= 0:
                raise ValidationError("Masukan Kuantitas benih yang dibutuhkan untuk memulai pertanian.")
            
            # Buat record pembaruan
            update_vals = {
                'name': f'Cycle Agriculture - {datetime.now().strftime("%Y-%m-%d")}',
                'status': 'on_track',
                'date': fields.Date.context_today(project),
                'progress': 100,
                'project_id': project.id,
            }
            self.env['project.update'].create(update_vals)

            # Temukan stage/task type dengan nama "Pemeliharaan"
            stage_type = self.env['project.task.type'].search([
                ('name', '=', 'Pemeliharaan'),
                ('project_ids', 'in', [project.id])
            ], limit=1)

            if not stage_type:
                raise ValidationError("Tugas pemeliharaan dengan nama 'Pemeliharaan' tidak ditemukan.")
            
            # Update field current_stage_id
            project.write({
                'state': 'season_progress',
                'curent_stage_id': stage_type.id
            })

            # Cari semua tugas yang berada di stage "Pemeliharaan" dan update statusnya
            tasks = self.env['project.task'].search([
                ('stage_id', '=', stage_type.id)
            ])

            if tasks:
                tasks.write({
                    'state': '01_in_progress'
                })
            
            project.write({
                'date_start': False,
                'date': False
            })

    # CRUD Overrides
    @api.model
    def create(self, vals):
        project = super(ProjectProject, self).create(vals)
        project.create_project_task_type()
        project._update_seed_stock()
        return project

    def write(self, vals):
        res = super(ProjectProject, self).write(vals)

        # Cek perubahan pada crop_id, stage_ids, seed_quantity, atau seed_id
        if 'crop_id' in vals or 'stage_ids' in vals or 'seed_quantity' in vals or 'seed_id' in vals:
            for project in self:
                # Update atau hapus task type berdasarkan perubahan crop_id atau stage_ids
                if 'crop_id' in vals and not vals['crop_id']:
                    project.delete_project_task_type()
                elif 'crop_id' in vals or 'stage_ids' in vals:
                    project.update_project_task_type()

                # Update stok benih jika ada perubahan pada seed_quantity atau seed_id
                if 'seed_quantity' in vals or 'seed_id' in vals:
                    if project.seed_id:
                        project._update_seed_stock()

        return res
        
    def _update_seed_stock(self):
        for project in self:
            if project.seed_id:
                seed = project.seed_id
                # Ambil stok saat ini dari current_seed_quantity
                current_stock = project.current_seed_quantity
                new_qty = current_stock - project.seed_quantity
                
                if new_qty < 0:
                    raise ValidationError(
                        f"Stok benih '{seed.name}' tidak mencukupi. "
                        f"Sisa stok: {seed.qty_on_hand}, "
                        f"Kebutuhan: {project.seed_quantity}"
                    )
                seed.qty_on_hand = new_qty

    # Task Type Management
    def create_project_task_type(self):
        for project in self:
            if project.crop_id:
                if not project.crop_id.seed_ids:
                    raise ValidationError('Crop ini tidak memiliki data seeds.')
                if not project.crop_id.stage_ids:
                    raise ValidationError('Crop ini tidak memiliki stage template.')

            stage_templates = project.crop_id.stage_ids
            for stage_template in stage_templates:
                existing_task_type = self.env['project.task.type'].search([
                    ('name', '=', stage_template.name),
                    ('project_ids', 'in', [project.id])
                ], limit=1)
                if not existing_task_type:
                    task_type_vals = {
                        'name': stage_template.name,
                        'project_ids': [(4, project.id)],
                        'crop_id': project.crop_id.id,
                    }
                    new_task_type = self.env['project.task.type'].create(task_type_vals)
                else:
                    new_task_type = existing_task_type
                for task_template in stage_template.task_template_id:
                    existing_task = self.env['project.task'].search([
                        ('name', '=', task_template.name),
                        ('project_id', '=', project.id),
                        ('stage_id', '=', new_task_type.id)
                    ], limit=1)
                    if not existing_task:
                        task_vals = {
                            'name': task_template.name,
                            'project_id': project.id,
                            'stage_id': new_task_type.id,
                        }
                        self.env['project.task'].create(task_vals)

    def update_project_task_type(self):
        for project in self:
            if project.crop_id:
                if not project.crop_id.seed_ids:
                    raise ValidationError('Crop ini tidak memiliki data seeds.')
                if not project.crop_id.stage_ids:
                    raise ValidationError('Crop ini tidak memiliki stage template.')

            crop_id = project.crop_id
            self.delete_project_task_type()
            if crop_id:
                stage_templates = crop_id.stage_ids
                for stage_template in stage_templates:
                    task_type_vals = {
                        'name': stage_template.name,
                        'project_ids': [(4, project.id)],
                        'crop_id': crop_id.id,
                    }
                    new_task_type = self.env['project.task.type'].create(task_type_vals)
                    for task_template in stage_template.task_template_id:
                        task_vals = {
                            'name': task_template.name,
                            'project_id': project.id,
                            'stage_id': new_task_type.id,
                        }
                        self.env['project.task'].create(task_vals)

    def delete_project_task_type(self):
        for project in self:
            task_types = self.env['project.task.type'].search([
                ('project_ids', 'in', [project.id])
            ])
            tasks = self.env['project.task'].search([
                ('project_id', '=', project.id)
            ])
            tasks.unlink()
            task_types.unlink()

    def unlink(self):
        # Hapus semua project update terkait
        self.env['project.update'].search([('project_id', 'in', self.ids)]).unlink()

        # Hapus semua season crop disease terkait
        self.env['agri.season.crop.disease'].search([('project_ids', 'in', self.ids)]).unlink()

        # Hapus semua crop harvest terkait
        self.env['crop.harvest'].search([('project_id', 'in', self.ids)]).unlink()

        return super(ProjectProject, self).unlink()
