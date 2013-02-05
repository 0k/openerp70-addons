# -*- coding: utf-8 -*-
from osv import fields, osv
from tools.translate import _

class projectProjectInehrit(osv.osv):
    _inherit = 'project.project'
    _columns = {
        'is_scrum': fields.boolean("Is it a Scrum Project ?"),
        'scrum_master_id': fields.many2one('res.users', 'Scrum Master', help="The person who is maintains the processes for the product"),
        'product_owner_id': fields.many2one('res.users', "Product Owner"),
        'goal' : fields.text("Goal", help="The document that includes the project, jointly between the team and the customer"),
    }
    _defaults = {
        'is_scrum': True,
    }

