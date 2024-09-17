from odoo import http
from odoo.http import request

class ProjectAPIController(http.Controller):
    
    @http.route('/api/projects', auth='public', type='json', methods=['GET'])
    def get_projects(self, **kwargs):
        projects = request.env['project.project'].search_read([], ['name', 'description'])
        return projects
