{
    'name': 'agriculture_management',
    'version': '1.0',
    'summary': 'Module for managing agricultural activities',
    'description': 'This module allows you to manage various agricultural activities and data in Odoo.',
    'category': 'agriculture, farming',
    'author': 'shirooneko',
    'depends': ['base', 'website_sale','mail','project','board', 'web', 'sale'],
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        # 'views/dashboard_view.xml',
        'views/agri_lands_farm_view.xml',
        'views/agri_farmer_view.xml',
        'views/agri_crops_view.xml',
        'views/agri_crop_diseases_view.xml',
        'views/agri_crop_healty_manure_view.xml',
        'views/agri_task_stage_view.xml',
        'views/agri_farm_season_view.xml',
        'views/agri_season_crop_diseases_wizard.xml',
        'views/agri_season_seeds_view.xml',
        # 'views/crop_fertilisers_view.xml',agri_stage_view.xml
        'views/agri_pesticides_herb_view.xml',
        'views/agri_stage_view.xml',
        'views/agri_task_template_view.xml',
        'views/agri_crop_seeds_view.xml',
        # 'views/product_view.xml',
        # 'views/crop_incidents_view.xml',
        # 'views/incidents_type_view.xml',
        # 'views/incident_view.xml',
        # 'views/agri_task_view.xml',
        'views/agri_farm_types_view.xml',
        'views/agri_equipment_tags_view.xml',
        'views/agriculture_management_menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [
            'agriculture_management/static/src/components/**/*.js',
            'agriculture_management/static/src/components/**/*.xml',
            'agriculture_management/static/src/components/**/*.scss',
        ],
    },
}
