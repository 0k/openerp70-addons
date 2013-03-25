# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from osv import osv, fields

class sandbox_transfer_to_backlog(osv.osv_memory):
    _name = 'project.scrum.sandbox.to.backlog'
    _description = 'Transfer user story from sandbox to Product Backlogs'
    _columns = {
        'role_id': fields.many2one('project.scrum.role', "As"),
        'name' : fields.char('I want', size=128),
        'for_then' : fields.char('For', size=128),
        'project_id': fields.many2one('project.project', "Project", domain=[('is_scrum', '=', True)]),
        'developer_id': fields.many2one('res.users', 'Developer'),
        'release_id': fields.many2one('project.scrum.release', "Release"),
        'acceptance_testing': fields.text("Acceptance testing", required=True,),
        'priority_id': fields.many2one('project.scrum.priority', "Priority",help="Priority of the request."),
    }

    def do_transfer(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        
        sandbox_spg = self.pool.get('project.scrum.sandbox')
        backlog_spg = self.pool.get('project.scrum.product.backlog')
        sandboxes = sandbox_spg.browse(cr, uid, context['active_ids'], context=context)
        data = self.read(cr, uid, ids, [], context=context)[0]
        for sandbox in sandboxes:
            backlog_id = backlog_spg.create(cr, uid, {
                'role_id': sandbox.role_id.id,
                'name': sandbox.name,
                'acceptance_testing': data.get('acceptance_testing', False) or "---",
                'for_then': data.get('for_then', False),
                'project_id': sandbox.project_id.id,
                'priority_id': data.get('priority_id', False),
                'release_id':data.get('release_id') and data['release_id'][0] or False, 
            })
            if backlog_id:
                sandbox_spg.unlink(cr, uid, [sandbox.id])
        #mod_obj = self.pool.get('ir.model.data')
        #task = self.pool.get('project.task')
        #backlog_id = self.pool.get('project.scrum.product.backlog')
        #document_pool = self.pool.get('ir.attachment')
        #ids_task = []
        #
        #data = self.read(cr, uid, ids, [], context=context)[0]
        #backlogs = backlog_id.browse(cr, uid, context['active_ids'], context=context)
        #result = mod_obj._get_id(cr, uid, 'project', 'view_task_search_form')
        #id = mod_obj.read(cr, uid, result, ['res_id'])
        #
        #for backlog in backlogs:
        #    task_id = task.create(cr, uid, {
        #        'product_backlog_id': backlog.id,
        #        'name': backlog.name,
        #        'description': backlog.description,
        #        'project_id': backlog.project_id.id,
        #        'user_id': data.get('user_id') and data['user_id'][0] or False,
        #        'planned_hours': backlog.expected_hours,
        #        'remaining_hours':backlog.expected_hours,
        #        'sequence':backlog.sequence,
        #    })
        #    document_ids = document_pool.search(cr, uid, [('res_id', '=', backlog.id), ('res_model', '=', backlog_id._name)])
        #    for document_id in document_ids:
        #        document_pool.copy(cr, uid, document_id, default={'res_id':task_id, 'res_model':task._name})
        #    ids_task.append(task_id)
        #return {
        #    'domain': "[('product_backlog_id','in',["+','.join(map(str, context['active_ids']))+"])]",
        #    'name': 'Tasks',
        #    'res_id': ids_task,
        #    'view_type': 'form',
        #    'view_mode': 'tree,form',
        #    'res_model': 'project.task',
        #    'view_id': False,
        #    'type': 'ir.actions.act_window',
        #    'search_view_id': id['res_id'],
        #}
        return True

sandbox_transfer_to_backlog()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
