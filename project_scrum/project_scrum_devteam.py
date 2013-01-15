# -*- coding: utf-8 -*-
from osv import fields, osv
from tools.translate import _

class projectScrumDevteam(osv.osv):
    _name = 'project.scrum.devteam'
    
    _columns = {
        'name': fields.char("Name", size=128, required=True),
        'code': fields.char("Code", size=16),
        'active': fields.boolean("Active"),
    }
    
    _defaults = {
        'active': True,
    }

class resUsersInherit(osv.osv):
    _inherit = "res.users"
    
    _columns = {
        'scrum_devteam_id': fields.many2one('project.scrum.devteam', "Scrum Development Team"),
    }

class projectScrumDevTeamInherit(osv.osv):
    _inherit = "project.scrum.devteam"
    
    _columns = {
        'developer_ids': fields.one2many('res.users', 'scrum_devteam_id', "Developers"),
    }
