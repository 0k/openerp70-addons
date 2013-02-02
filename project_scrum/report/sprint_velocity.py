# -*- coding: utf-8 -*-
import StringIO
import pooler

from report.render import render
from report.interface import report_int

from pychart import *
import pychart.legend

import pooler

class external_pdf(render):
    def __init__(self, pdf):
        render.__init__(self)
        self.pdf = pdf
        self.output_type='pdf'
    
    def _render(self):
        return self.pdf

class report_tasks(report_int):
    def create(self, cr, uid, ids, datas, context=None):
        # ids = list of ids of projects
        # datas =  {'report_type': u'pdf'}
        
        if context is None:
            context = {}
        io = StringIO.StringIO()
        
        canv = canvas.init(fname=io, format='pdf')
        canv.set_author("David DRAPEAU")
        canv.set_title("Sprints Velocities")
        
        pool = pooler.get_pool(cr.dbname)
        sprint_pool = pool.get('project.scrum.sprint')
        project_pool = pool.get('project.project')
        
        # For add the report header on the top of the report.
        tb = text_box.T(loc=(320, 500), text="/hL/15/bSprints velocities (of project)", line_style=None)
        tb.draw()
        
        sprint_ids = sprint_pool.search(cr, uid, [('project_id', '=', ids[0])])
        sprint_ids.sort()
        #print "sprint_ids = ", sprint_ids
        planned_velocity = [(0, 0)]
        effective_velocity = [(0,0)]
        for sprint_obj in sprint_pool.browse(cr, uid, sprint_ids, context=context):
            planned_velocity.append((sprint_obj.id, sprint_obj.planned_velocity))
            print "planned_velocity = ", planned_velocity
            if sprint_obj.state == 'done':
                effective_velocity.append((sprint_obj.id, sprint_obj.effective_velocity_sprint_done))
                print "effective_velocity = ", effective_velocity
            #planned_velocity = [(1, 15), (2, 18), (3, 20), (4, 20), (5, 20)]
            #effective_velocity = [(1, 12), (2, 17)]
        planned_velocity.sort()
        effective_velocity.sort()
        ar = area.T(x_grid_style=line_style.gray50_dash1,
                    x_axis=axis.X(label="Velocity"),
                    y_axis=axis.Y(label="Sprint"),
                    x_grid_interval=1,
                    y_grid_interval=1,
                    x_range = (0, None),
                    y_range = (0, None),
                    legend = None,
                    size = (680,450))
        
        ar.add_plot(line_plot.T(label="plot1", data=planned_velocity, line_style=line_style.red))
        ar.add_plot(line_plot.T(label="plot2", data=effective_velocity, line_style=line_style.green))
        
        entr1 = pychart.legend.Entry(label="Planned Velocity", line_style=line_style.red)
        entr2 = pychart.legend.Entry(label="Effective Velocity",line_style=line_style.green)
        legend = pychart.legend.T(nr_rows=2, inter_row_sep=5)
        legend.draw(ar,[entr1,entr2],canv)
        
        ar.draw(canv)
        
        canv.close()
        
        self.obj = external_pdf(io.getvalue())
        self.obj.render()
        return (self.obj.pdf, 'pdf')
    
report_tasks('report.scrum.sprint.velocity')
