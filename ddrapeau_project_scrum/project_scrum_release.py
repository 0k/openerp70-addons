# -*- coding: utf-8 -*-
from osv import fields, osv
from tools.translate import _

class projectScrumRelease(osv.osv):
    _name = 'project.scrum.release'
    
    _columns = {
        'name': fields.char("Name", size=128, required=True),
        'project_id': fields.many2one('project.project', "Project", domain=[('is_scrum', '=', True)], required=True),
        'delivery_date_estimated': fields.date("Estimated date of delivery"),
        'delivery_date_effective': fields.date("Effective date of delivery"),
    }
