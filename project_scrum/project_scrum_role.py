# -*- coding: utf-8 -*-
from osv import fields, osv

class projectScrumRole(osv.osv):
    _name = 'project.scrum.role'
    
    _columns = {
        'name' : fields.char('Name', size=128, required=True),
        'code' : fields.char('Code', size=16),
        'project_id': fields.many2one('project.project', "Project", required=True),
        
        'persona_name' : fields.char('Persona Name', size=128),
        'persona_description' : fields.text('Persona Description'),
    }
