# -*- coding: utf-8 -*-
from osv import fields, osv
from tools.translate import _

class projectProjectInehrit(osv.osv):
    _inherit = 'project.project'
    _columns = {
        #'sprint_size': fields.integer('Sprint Days', help="Number of days allocated for sprint"),
        'is_scrum': fields.boolean("Is it a Scrum Project ?"),
        'product_owner_id': fields.many2one('res.users', "Product Owner"),
        'goal' : fields.text("Goal", help="The document that includes the project, jointly between the team and the customer"),
        #'done' : fields.char("What is the \"Done\"?", size=128),
    }
    _defaults = {
        #'sprint_size': 10,
        'is_scrum': True,
    }

