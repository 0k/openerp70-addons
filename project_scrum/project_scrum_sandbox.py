# -*- coding: utf-8 -*-
from osv import fields, osv
from tools.translate import _



class projectScrumSandbox(osv.osv):
    _name = 'project.scrum.sandbox'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'role_id': fields.many2one('project.scrum.role', "As", required=True,),
        'name' : fields.char('I want', size=128, required=True),
        'for' : fields.char('For', size=128, required=True),
        'project_id': fields.many2one('project.project', "Project", required=True, domain=[('is_scrum', '=', True)]),
        'developer_id': fields.many2one('res.users', 'Developer'),
        'note':fields.text('Note', translate=False, ),
        'priority_id': fields.many2one('project.scrum.priority', "Priority",help="Priority of the request."),
    }
    
    _defaults = {
        'developer_id': lambda self, cr, uid, context: uid,
    }