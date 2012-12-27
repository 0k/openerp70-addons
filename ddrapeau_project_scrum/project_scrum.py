# -*- coding: utf-8 -*-
from osv import fields, osv
from tools.translate import _
import re
import time
import tools
from datetime import datetime
from dateutil.relativedelta import relativedelta

SPRINT_STATES = [('draft','Draft'),
    ('open','Open'),
    ('pending','Pending'),
    ('cancel','Cancelled'),
    ('done','Done')]

BACKLOG_STATES = [('draft','Draft'),
    ('open','Open'),
    ('pending','Pending'),
    ('done','Done'),
    ('cancel','Cancelled')]

class projectScrumSprint(osv.osv):
    _name = 'project.scrum.sprint'
    _description = 'Project Scrum Sprint'
    
    def _compute(self, cr, uid, ids, fields, arg, context=None):
        res = {}.fromkeys(ids, 0.0)
        progress = {}
        if not ids:
            return res
        if context is None:
            context = {}
        for sprint in self.browse(cr, uid, ids, context=context):
            tot = 0.0
            prog = 0.0
            effective = 0.0
            progress = 0.0
            for bl in sprint.backlog_ids:
                tot += bl.expected_hours
                effective += bl.effective_hours
                prog += bl.expected_hours * bl.progress / 100.0
            if tot>0:
                progress = round(prog/tot*100)
            res[sprint.id] = {
                'progress' : progress,
                'expected_hours' : tot,
                'effective_hours': effective,
            }
        return res

    def button_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'cancel'}, context=context)
        return True

    def button_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'draft'}, context=context)
        return True

    def button_open(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'open'}, context=context)
        for (id, name) in self.name_get(cr, uid, ids):
            message = _("The sprint '%s' has been opened.") % (name,)
            self.log(cr, uid, id, message)
        return True

    def button_close(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'done'}, context=context)
        for (id, name) in self.name_get(cr, uid, ids):
            message = _("The sprint '%s' has been closed.") % (name,)
            self.log(cr, uid, id, message)
        return True

    def button_pending(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'pending'}, context=context)
        return True

    _columns = {
        'name': fields.char('Sprint Name', required=True, size=64),
        'date_start': fields.date('Starting Date', required=True),
        'date_stop': fields.date('Ending Date', required=True),
        'release_id': fields.many2one('project.scrum.release', 'Release', required=True),
        'project_id': fields.related('release_id', 'project_id', type='many2one', relation='project.project', string="Project", readonly=True),
        
        #FIX product_owner_id and scrum_master_id are defined in project.project (delete from here)
        'product_owner_id': fields.many2one('res.users', 'Product Owner', required=True,help="The person who is responsible for the product"),
        'scrum_master_id': fields.many2one('res.users', 'Scrum Master', required=True,help="The person who is maintains the processes for the product"),
        
        'meeting_ids': fields.one2many('project.scrum.meeting', 'sprint_id', 'Daily Scrum'),
        'review': fields.text('Sprint Review'),
        'retrospective': fields.text('Sprint Retrospective'),
        'backlog_ids': fields.one2many('project.scrum.product.backlog', 'sprint_id', 'Sprint Backlog'),
        'progress': fields.function(_compute, group_operator="avg", type='float', multi="progress", method=True, string='Progress (0-100)', help="Computed as: Time Spent / Total Time."),
        'effective_hours': fields.function(_compute, multi="effective_hours", method=True, string='Effective hours', help="Computed using the sum of the task work done."),
        'expected_hours': fields.function(_compute, multi="expected_hours", method=True, string='Planned Hours', help='Estimated time to do the task.'),
        'state': fields.selection(SPRINT_STATES, 'State', required=True),
        'goal': fields.char("Goal", size=128),
    }
    
    
    _defaults = {
        'state': 'draft',
        'date_start' : lambda *a: time.strftime('%Y-%m-%d'),
    }
    _order = 'date_start desc'
    
    def _check_dates(self, cr, uid, ids, context=None):
        for leave in self.read(cr, uid, ids, ['date_start', 'date_stop'], context=context):
            if leave['date_start'] and leave['date_stop']:
                if leave['date_start'] > leave['date_stop']:
                    return False
        return True

    _constraints = [
        (_check_dates, 'Error! sprint start-date must be lower than project end-date.', ['date_start', 'date_stop'])
    ]


class projectScrumProductBacklog(osv.osv):
    _name = 'project.scrum.product.backlog'
    
    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args=[]
        if name:
            match = re.match('^S\(([0-9]+)\)$', name)
            if match:
                ids = self.search(cr, uid, [('sprint_id','=', int(match.group(1)))], limit=limit, context=context)
                return self.name_get(cr, uid, ids, context=context)
        return super(projectScrumProductBacklog, self).name_search(cr, uid, name, args, operator,context, limit=limit)

    def _compute(self, cr, uid, ids, fields, arg, context=None):
        res = {}.fromkeys(ids, 0.0)
        progress = {}
        if not ids:
            return res
        for backlog in self.browse(cr, uid, ids, context=context):
            tot = 0.0
            prog = 0.0
            effective = 0.0
            task_hours = 0.0
            progress = 0.0
            
            for task in backlog.tasks_id:
                task_hours += task.total_hours
                effective += task.effective_hours
                tot += task.planned_hours
                prog += task.planned_hours * task.progress / 100.0
            if tot>0:
                progress = round(prog/tot*100)
            #TODO display an error message if tot==0 (division by 0 is impossible)
            res[backlog.id] = {
                'progress' : progress,
                'effective_hours': effective,
                'task_hours' : task_hours
            }
        return res

    def button_cancel(self, cr, uid, ids, context=None):
        obj_project_task = self.pool.get('project.task')
        self.write(cr, uid, ids, {'state':'cancel'}, context=context)
        for backlog in self.browse(cr, uid, ids, context=context):
            obj_project_task.write(cr, uid, [i.id for i in backlog.tasks_id], {'state': 'cancelled'})
        return True
    
    def button_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'draft'}, context=context)
        return True
    
    def button_open(self, cr, uid, ids, context=None):
        lines = self.read(cr, uid, ids, ['sprint_id'])
        for line in lines:
            if line['sprint_id'] == False:
                raise osv.except_osv(_("Warning !"), _("You must affect this user story in a sprint before open it."))
            else:
                self.write(cr, uid, ids, {'state':'open', 'date_open':time.strftime('%Y-%m-%d')}, context=context)
                return True
    
    def button_close(self, cr, uid, ids, context=None):
        obj_project_task = self.pool.get('project.task')
        self.write(cr, uid, ids, {'state':'done', 'date_done':time.strftime('%Y-%m-%d')}, context=context)
        for backlog in self.browse(cr, uid, ids, context=context):
            obj_project_task.write(cr, uid, [i.id for i in backlog.tasks_id], {'state': 'done'})
        return True
    
    def button_pending(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'pending'}, context=context)
        return True
    
    _columns = {
        'role_id': fields.many2one('project.scrum.role', "As", required=True),
        'name' : fields.char('I want', size=128, required=True),
        'for' : fields.char('For', size=128, required=True),
        
        'description': fields.text("Description"),
        'sequence' : fields.integer('Sequence', help="Gives the sequence order when displaying a list of product backlog."),
        'expected_hours': fields.float('Planned Hours', help='Estimated total time to do the Backlog'),
        'complexity': fields.integer('Complexity', help='Complexity of the User Story'),
        'active' : fields.boolean('Active', help="If Active field is set to true, it will allow you to hide the product backlog without removing it."),
        
        'state': fields.selection(BACKLOG_STATES, 'State', required=True),
        'date_open': fields.date("Date open"),
        'date_done': fields.date("Date done"),
        
        'project_id': fields.many2one('project.project', "Project", required=True, domain=[('is_scrum', '=', True)]),
        'release_id': fields.many2one('project.scrum.release', "Release", required=True),
        'sprint_id': fields.many2one('project.scrum.sprint', 'Sprint'),
        
        'user_id': fields.many2one('res.users', 'Author'),
        'task_id': fields.many2one('project.task', required=False,
            string="Related Task", ondelete='restrict',
            help='Task-related data of the user story'),
        'tasks_id': fields.one2many('project.task', 'product_backlog_id', 'Tasks Details'),
        
        'progress': fields.function(_compute, multi="progress", group_operator="avg", type='float', method=True, string='Progress', help="Computed as: Time Spent / Total Time."),
        'effective_hours': fields.function(_compute, multi="effective_hours", method=True, string='Spent Hours', help="Computed using the sum of the time spent on every related tasks", store=True),
        'task_hours': fields.function(_compute, multi="task_hours", method=True, string='Task Hours', help='Estimated time of the total hours of the tasks'),
        
        'color': fields.integer('Color Index'),
    }
    
    _defaults = {
        'state': 'draft',
        'user_id': lambda self, cr, uid, context: uid,
        'active':  1,
        'sequence': 1000, #TODO create function to compute sequence by uniq value for all product backlog
    }
    
    _order = "sequence"


class projectTaskInherit(osv.osv):
    _inherit = 'project.task'

    def _get_task(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('project.scrum.product.backlog').browse(cr, uid, ids, context=context):
            for task in line.tasks_id:
                result[task.id] = True
        return result.keys()
    
    _columns = {
        'product_backlog_id': fields.many2one('project.scrum.product.backlog', 'Product Backlog',
                help="Related product backlog that contains this task. Used in SCRUM methodology"),
        'sprint_id': fields.related('product_backlog_id','sprint_id', type='many2one', relation='project.scrum.sprint', string='Sprint',
            store={
                'project.task': (lambda self, cr, uid, ids, c={}: ids, ['product_backlog_id'], 10),
                'project.scrum.product.backlog': (_get_task, ['sprint_id'], 10)
            }),
        #'work_ids': fields.one2many('project.task.work', 'task_id', 'Work'),
        #'pb_role': fields.related('product_id', 'role_id', type='many2one', string="Role", relation="project.scrum.role", readonly=True),
        #'pb_description': fields.related('product_id', 'description', type='text', string="Description", relation="project.scrum.role", readonly=True),
    }
    
    def _check_dates(self, cr, uid, ids, context=None):
        for leave in self.read(cr, uid, ids, ['date_deadline'], context=context):
            if leave['date_deadline']:
                if leave['date_deadline'] < time.strftime('%Y-%m-%d'):
                    return False
        return True

    _constraints = [
        (_check_dates, 'Error! Date of creation must be lower than task date deadline.', ['date_deadline'])
    ]

    def onchange_backlog_id(self, cr, uid, ids, backlog_id=False):
        if not backlog_id:
            return {}
        project_id = self.pool.get('project.scrum.product.backlog').browse(cr, uid, backlog_id).project_id.id
        return {'value': {'project_id': project_id}}

#class projectScrumTaskWorkInherit(osv.osv):
#    _inherit = 'project.task.work'
#    
#    _columns = {
#        'task_id': fields.many2one('project.task', "Task"),
#    }
#

class projectScrumMeeting(osv.osv):
    _name = 'project.scrum.meeting'
    _description = 'Scrum Meeting'
    _order = 'date desc'
    _columns = {
        'name' : fields.char('Meeting Name', size=64),
        'date': fields.date('Meeting Date', required=True),
        'sprint_id': fields.many2one('project.scrum.sprint', 'Sprint', domain=['&', ('date_start', '<=', time.strftime("%Y-%m-%d")), ('date_stop', '>=', time.strftime("%Y-%m-%d"))]),
        'project_id': fields.many2one('project.project', 'Project'),
        'question_yesterday': fields.text('Tasks since yesterday'),
        'question_today': fields.text('Tasks for today'),
        'question_blocks': fields.text('Blocks encountered'),
        'question_backlog': fields.text('Backlog Accurate'),
        'task_ids': fields.many2many('project.task', 'meeting_task_rel', 'metting_id', 'task_id', 'Tasks'),
        'user_id': fields.related('sprint_id', 'scrum_master_id', type='many2one', relation='res.users', string='Scrum Master', readonly=True),
    }
    #
    # TODO: Find the right sprint thanks to users and date (ok for date, rest for user --> think conception before)
    #
    def _find_sprints(self, cr, uid, today):
        sprint_ids = self.pool.get('project.scrum.sprint').search(cr, uid, ['&', ('date_start', '<=', today), ('date_stop', '>=', today)])
        return sprint_ids
    
    def _get_right_sprint(self, cr, uid, context=None):
        today = time.strftime("%Y-%m-%d")
        sprint_ids = self._find_sprints(cr, uid, today)
        for sprint_id in sprint_ids:
            return sprint_id
    
    _defaults = {
        'sprint_id': _get_right_sprint,
        'date' : lambda *a: time.strftime('%Y-%m-%d'),
    }

    def button_send_to_master(self, cr, uid, ids, context=None):
        meeting_id = self.browse(cr, uid, ids, context=context)[0]
        if meeting_id and meeting_id.sprint_id.scrum_master_id.user_email:
            res = self.email_send(cr, uid, ids, meeting_id.sprint_id.scrum_master_id.user_email)
            if not res:
                raise osv.except_osv(_('Error !'), _('Email notification could not be sent to the scrum master %s') % meeting_id.sprint_id.scrum_master_id.name)
        else:
            raise osv.except_osv(_('Error !'), _('Please provide email address for scrum master defined on sprint.'))
        return True

    def button_send_product_owner(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        context.update({'button_send_product_owner': True})
        meeting_id = self.browse(cr, uid, ids, context=context)[0]
        if meeting_id.sprint_id.product_owner_id.user_email:
            res = self.email_send(cr,uid,ids,meeting_id.sprint_id.product_owner_id.user_email)
            if not res:
                raise osv.except_osv(_('Error !'), _('Email notification could not be sent to the product owner %s') % meeting_id.sprint_id.product_owner_id.name)
        else:
            raise osv.except_osv(_('Error !'), _('Please provide email address for product owner defined on sprint.'))
        return True

    def email_send(self, cr, uid, ids, email, context=None):
        email_from = tools.config.get('email_from', False)
        meeting_id = self.browse(cr, uid, ids, context=context)[0]
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        user_email = email_from or user.address_id.email  or email_from
        body = _('Hello ') + meeting_id.sprint_id.scrum_master_id.name + ",\n" + " \n" +_('I am sending you Daily Meeting Details of date')+ ' %s ' % (meeting_id.date)+ _('for the Sprint')+ ' %s\n' % (meeting_id.sprint_id.name)
        body += "\n"+ _('*Tasks since yesterday:')+ '\n_______________________%s' % (meeting_id.question_yesterday) + '\n' +_("*Task for Today:")+ '\n_______________________ %s\n' % (meeting_id.question_today )+ '\n' +_('*Blocks encountered:') +'\n_______________________ %s' % (meeting_id.question_blocks or _('No Blocks'))
        body += "\n\n"+_('Thank you')+",\n"+ user.name
        sub_name = meeting_id.name or _('Scrum Meeting of %s') % meeting_id.date
        flag = tools.email_send(user_email , [email], sub_name, body, reply_to=None, openobject_id=str(meeting_id.id))
        if not flag:
            return False
        return True
