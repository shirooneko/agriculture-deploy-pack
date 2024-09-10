from odoo import models, fields, api
from datetime import datetime


class AgricultureTask(models.Model):
    _description = 'Agriculture Task'
    _inherit = 'project.task'
    _order = "stage_id ASC"

        
    project_ids_display = fields.Char(string="Project IDs", compute="_compute_project_ids_display")
    crop_id = fields.Many2one('agri.crop', string='Tanaman', readonly=True)

    @api.depends('stage_id.project_ids')
    def _compute_project_ids_display(self):
        for task in self:
            # Join the IDs of project_ids related to the stage_id into a string
            task.project_ids_display = ', '.join(map(str, task.stage_id.project_ids.ids))
    
    crop_id = fields.Many2one('agri.crop', string='Tanaman')

    def action_done(self):
        self.write({'state': '1_done'})  # Update state task ke '1_done'

        stage_ids_ordered = self.env['project.task.type'].search([], order='id')
        stage_id_mapping = {stage.id: stage for stage in stage_ids_ordered}

        for task in self:
            project_ids = task.stage_id.project_ids.ids
            for project_id in project_ids:
                project = self.env['project.project'].browse(project_id)

                # Cari task yang belum selesai pada stage saat ini
                unfinished_tasks = self.env['project.task'].search([
                    ('project_id', '=', project_id),
                    ('stage_id', '=', task.stage_id.id),
                    ('state', '!=', '1_done')  # Tidak termasuk task yang sudah selesai
                ])

                if not unfinished_tasks:
                    # Jika tidak ada task yang belum selesai, cari index stage saat ini
                    current_stage_index = stage_ids_ordered.ids.index(task.stage_id.id)
                    
                    # Cek apakah ada stage selanjutnya
                    if current_stage_index < len(stage_ids_ordered) - 1:
                        next_stage_id = stage_ids_ordered[current_stage_index + 1].id
                        project.write({'curent_stage_id': next_stage_id})

                # Cek apakah semua task dalam project sudah selesai (logic untuk season_end)
                all_tasks_done = True
                for project_task in project.task_ids:
                    if project_task.state != '1_done':
                        all_tasks_done = False
                        break

                if all_tasks_done:
                    project.write({'state': 'season_end'})

                    update_vals = {
                        'name': f'End Agriculture - {datetime.now().strftime("%Y-%m-%d")}',
                        'status': 'done',
                        'date': fields.Date.context_today(project),
                        'progress': 100,
                        'project_id': project.id,
                    }
                    self.env['project.update'].create(update_vals)

    def action_cancel(self):
        self.write({'state': '1_canceled'})

