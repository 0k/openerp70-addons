# -*- coding: utf-8 -*-
import StringIO
import pooler

from report.render import render
from report.interface import report_int

from datetime import datetime, date, timedelta
import time

from pychart import *
import pychart.legend

import _burndown_story_point

class report_tasks(report_int):
    def _get_total_points(self, cr, uid, sprint_id, pb_pool):
        userStory_ids = pb_pool.search(cr, uid, [('sprint_id', '=', sprint_id)])
        total = 0
        for story in pb_pool.browse(cr, uid, userStory_ids):
            total += story.complexity
        return total
    
    def _get_date_start(self, cr, uid, sprint_id, sprint_pool):
        sprint = sprint_pool.browse(cr, uid, sprint_id)
        date_start = sprint.date_start
        return date(int(date_start.split('-')[0]), int(date_start.split('-')[1]), int(date_start.split('-')[2]))
    
    def _get_date_stop(self, cr, uid, sprint_id, sprint_pool):
        sprint = sprint_pool.browse(cr, uid, sprint_id)
        date_stop = sprint.date_stop
        return date(int(date_stop.split('-')[0]), int(date_stop.split('-')[1]), int(date_stop.split('-')[2]))
    
    def _get_days_number(self, cr, uid, sprint_id, sprint_pool):
        sprint = sprint_pool.browse(cr, uid, sprint_id)
        date_start = sprint.date_start
        date_start_tuple = date(int(date_start.split('-')[0]), int(date_start.split('-')[1]), int(date_start.split('-')[2]))
        date_stop = sprint.date_stop
        date_stop_tuple = date(int(date_stop.split('-')[0]), int(date_stop.split('-')[1]), int(date_stop.split('-')[2]))
        return (date_stop_tuple - date_start_tuple).days
    
    def _get_guideline_data(self, cr, uid, sprint_id, sprint_pool, total_points, nb_days):
        data = []
        unit_per_day = float(total_points) / float(nb_days)
        date_start = self._get_date_start(cr, uid, sprint_id, sprint_pool)
        n = 0
        while n <= nb_days:
            this_date = date_start + timedelta(days=n)
            data.append((n+1, unit_per_day * (nb_days - n)))
            n += 1
        return data
    
    def _get_day_velocity(self, cr, uid, sprint_id, userStory_pool, this_date):
        total = 0
        story_ids = userStory_pool.search(cr, uid, ['&', ('sprint_id', '=', sprint_id),('date_done', '=', this_date)])
        for story in userStory_pool.browse(cr, uid, story_ids):
            total += story.complexity
        return total
    
    def _get_effective_data(self, cr, uid, sprint_id, sprint_pool, userStory_pool, total_points, nb_days):
        data = []
        sprint_dates = []
        date_start = self._get_date_start(cr, uid, sprint_id, sprint_pool)
        date_stop = self._get_date_stop(cr, uid, sprint_id, sprint_pool)
        n = 0
        
        while n <= nb_days:
            this_date = date_start + timedelta(days=n)
            total_day_velocity = self._get_day_velocity(cr, uid, sprint_id, userStory_pool, this_date)
            total_points -= total_day_velocity
            data.append((n+1, total_points))
            n += 1
        return data
    
    def create(self, cr, uid, ids, datas, context=None):
        if context is None:
            context = {}
        
        pool = pooler.get_pool(cr.dbname)
        sprint_pool = pool.get('project.scrum.sprint')
        userStory_pool = pool.get('project.scrum.product.backlog')
        
        for sprint in sprint_pool.browse(cr, uid, ids, context=context):
            io = StringIO.StringIO() # <StringIO.StringIO instance at 0xba6c0ec>
            canv = canvas.init(fname=io, format='pdf') # <pychart.pdfcanvas.T object at 0xba6c1ac>
            canv.set_author("David DRAPEAU")
            canv.set_title("Burndown Chart")
            
            total_points = self._get_total_points(cr, uid, sprint.id, userStory_pool)
            nb_days = self._get_days_number(cr, uid, sprint.id, sprint_pool)
            guideline_data = self._get_guideline_data(cr, uid, sprint.id, sprint_pool, total_points, nb_days)
            effective_data = self._get_effective_data(cr, uid, sprint.id, sprint_pool, userStory_pool, total_points, nb_days)
            
            ar = area.T(x_grid_style=line_style.gray50_dash1,
                        x_axis=axis.X(label="Dates"),
                        y_axis= axis.Y(label="Points"),
                        x_range = (1, nb_days+1),
                        y_range = (0, total_points+2),
                        legend = None,
                        size = (680, 450))
            
            draw_guideline = line_plot.T(label="Guideline", data=guideline_data, ycol=1, line_style=line_style.red)
            draw_effective_line = line_plot.T(label="Effective", data=effective_data, ycol=1, line_style=line_style.green)
            ar.add_plot(draw_guideline, draw_effective_line)
            
            entr1 = pychart.legend.Entry(label="guideline", line_style=line_style.red)
            entr2 = pychart.legend.Entry(label="burndownchart",line_style=line_style.green)
            legend = pychart.legend.T(nr_rows=2, inter_row_sep=5)
            legend.draw(ar,[entr1,entr2],canv)
    
            ar.draw()
        canv.close()
        
        self.obj = _burndown_story_point.external_pdf(io.getvalue())
        self.obj.render()
        return (self.obj.pdf, 'pdf')
    
report_tasks('report.scrum.sprint.burndown.storyPoint')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

